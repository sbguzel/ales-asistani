import { collection, query, where, documentId, getDocs, doc, getDoc } from 'firebase/firestore';
import { db } from '../../core/config.js';
import { eventBus } from '../../core/eventBus.js';

/**
 * QuestionBufferService:
 * Veritabanından optimum 10'ar soruluk akıllı paketler halinde veri çeker (Sliding Window Buffer).
 * Kullanıcı soruları çözerken arka planda (prefetch) sıradaki soruları indirir ve çevrimdışı 
 * kullanım için arabellekte (localStorage / in-memory) saklar.
 * İnternet kesilse dahi kullanıcının 5-10 soruyu kesintisiz çözebilmesini garanti eder.
 */
export class QuestionBufferService {
  static BUFFER_SIZE = 10;        // Optimum soru tampon boyutu (10 soru = ~15-20 dk çalışma, ~35KB)
  static LOW_WATERMARK = 4;       // Tamponda kalan soru 4 veya altına indiğinde yeni parti çek
  static CACHE_KEY = 'ales_offline_buffer_v2';
  static MANIFEST_KEY = 'ales_manifest_cache_v2';

  constructor() {
    this.memoryCache = new Map();   // id -> question object
    this.seedMap = null;            // id -> canonical repaired question object from /data/seed_questions.json
    this.manifest = [];             // [{ id, subject, number, orderIndex, category, isGroupQuestion, groupId }]
    this.isFetching = false;
    this.isOnline = typeof navigator !== 'undefined' ? navigator.onLine : true;
    this.lastPrefetchIndex = -1;

    this.clearLegacyCaches();
    this.initNetworkListeners();
    this.restoreLocalBuffer();
  }

  clearLegacyCaches() {
    if (typeof localStorage === 'undefined') return;
    try {
      localStorage.removeItem('ales_offline_buffer');
      localStorage.removeItem('ales_manifest_cache');
      localStorage.removeItem('ales_cached_questions');
    } catch (e) {}
  }

  async ensureSeedMap() {
    if (this.seedMap) return this.seedMap;
    try {
      const resp = await fetch('/data/seed_questions.json');
      if (resp.ok) {
        const seeds = await resp.json();
        this.seedMap = new Map(seeds.map(q => [q.id, q]));
      }
    } catch (e) {}
    return this.seedMap;
  }

  // 1. Ağ durumu dinleyicileri (Online/Offline)
  initNetworkListeners() {
    if (typeof window === 'undefined') return;

    window.addEventListener('online', () => {
      this.isOnline = true;
      console.log('🌐 [QuestionBufferService] İnternet bağlantısı sağlandı.');
      eventBus.emit('network:status', { isOnline: true });
    });

    window.addEventListener('offline', () => {
      this.isOnline = false;
      console.log('⚠️ [QuestionBufferService] İnternet bağlantısı kesildi. Çevrimdışı tampon devrede.');
      eventBus.emit('network:status', { isOnline: false, bufferedCount: this.getBufferedCount() });
    });
  }

  // 2. Yerel arabellekten (localStorage) önceden indirilmiş tamponu geri yükle
  restoreLocalBuffer() {
    try {
      const saved = localStorage.getItem(QuestionBufferService.CACHE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed)) {
          parsed.forEach(q => {
            if (q && q.id) this.memoryCache.set(q.id, q);
          });
          console.log(`📦 [QuestionBufferService] Yerel tampondan ${this.memoryCache.size} soru belleğe alındı.`);
        }
      }
    } catch (e) {
      console.warn('Tampon geri yükleme uyarısı:', e);
    }
  }

  // Bellekteki ve yerel hafızadaki tamponu güncelle
  persistBuffer() {
    try {
      const items = Array.from(this.memoryCache.values());
      // Tamponun aşırı büyümesini engellemek için en fazla son 30 soruyu yerel sakla
      const toStore = items.slice(-30);
      localStorage.setItem(QuestionBufferService.CACHE_KEY, JSON.stringify(toStore));
    } catch (e) {
      console.warn('Tampon saklama hatası:', e);
    }
  }

  getBufferedCount() {
    return this.memoryCache.size;
  }

  // 3. Hafif Soru Manifestosu (Soru kimlikleri ve filtre meta verileri ~50KB)
  async loadManifest() {
    let localManifestMap = null;
    try {
      const resp = await fetch('/data/questions_manifest.json');
      if (resp.ok) {
        const localItems = await resp.json();
        localManifestMap = new Map(localItems.map(item => [item.id, item]));
      }
    } catch (e) {}

    // 1. Firestore meta dokümanı dene
    if (this.isOnline) {
      try {
        const manifestRef = doc(db, 'system', 'manifest');
        const snap = await getDoc(manifestRef);
        if (snap.exists() && snap.data().items) {
          this.manifest = snap.data().items.map(item => {
            const canonical = localManifestMap ? localManifestMap.get(item.id) : null;
            return canonical ? { ...item, ...canonical } : item;
          });
          localStorage.setItem(QuestionBufferService.MANIFEST_KEY, JSON.stringify(this.manifest));
          return { manifest: this.manifest, source: 'firestore' };
        }
      } catch (err) {
        console.warn('[QuestionBufferService] Firestore manifestosu alınamadı, yedeğe geçiliyor:', err);
      }
    }

    // 2. LocalStorage manifestosu dene
    try {
      const cached = localStorage.getItem(QuestionBufferService.MANIFEST_KEY);
      if (cached) {
        const parsed = JSON.parse(cached);
        if (Array.isArray(parsed) && parsed.length > 0) {
          this.manifest = parsed.map(item => {
            const canonical = localManifestMap ? localManifestMap.get(item.id) : null;
            return canonical ? { ...item, ...canonical } : item;
          });
          return { manifest: this.manifest, source: 'cache' };
        }
      }
    } catch (e) {}

    // 3. Statik JSON dosya yedeği (/data/questions_manifest.json veya seed_questions.json)
    if (localManifestMap && localManifestMap.size > 0) {
      this.manifest = Array.from(localManifestMap.values());
      return { manifest: this.manifest, source: 'manifest_json' };
    }

    // 4. Son çare: seed_questions.json dosyasından derle
    const resp = await fetch('/data/seed_questions.json');
    const fullQuestions = await resp.json();
    fullQuestions.forEach(q => this.memoryCache.set(q.id, q));
    this.manifest = fullQuestions.map((q, idx) => ({
      id: q.id,
      number: q.number,
      subject: q.subject,
      category: q.category,
      orderIndex: q.orderIndex || idx + 1,
      isGroupQuestion: !!q.isGroupQuestion,
      groupId: q.groupId || null
    }));
    return { manifest: this.manifest, source: 'seed_json' };
  }

  // 4. Belirli soru ID'lerini Firestore'dan 10'luk parti halinde çek
  async fetchBatch(questionIds) {
    if (!questionIds || questionIds.length === 0) return [];

    const missingIds = questionIds.filter(id => !this.memoryCache.has(id));
    if (missingIds.length === 0) {
      return questionIds.map(id => this.memoryCache.get(id)).filter(Boolean);
    }

    const seedMap = await this.ensureSeedMap();

    // Eksik soruları Firestore'dan 'in' sorgusu ile tek seferde çek (Maksimum 10-30 eleman)
    if (this.isOnline) {
      try {
        const questionsCol = collection(db, 'questions');
        // Firestore 'in' sorgusu en fazla 30 eleman kabul eder; biz 10'luk paketler kullanıyoruz
        const chunks = [];
        for (let i = 0; i < missingIds.length; i += 10) {
          chunks.push(missingIds.slice(i, i + 10));
        }

        for (const chunk of chunks) {
          const qQuery = query(questionsCol, where(documentId(), 'in', chunk));
          const snap = await getDocs(qQuery);
          snap.forEach(docSnap => {
            const data = docSnap.data();
            const canonical = seedMap ? seedMap.get(data.id) : null;
            this.memoryCache.set(data.id, canonical ? { ...data, ...canonical } : data);
          });
        }

        this.persistBuffer();
      } catch (err) {
        console.warn('[QuestionBufferService] Firestore batch çekme hatası (Fallback devrede):', err);
      }
    }

    // Eğer çevrimdışıysa ve bazı sorular hâlâ eksikse, yerel seed dosyasından tamamla
    const stillMissing = questionIds.filter(id => !this.memoryCache.has(id));
    if (stillMissing.length > 0 && seedMap) {
      stillMissing.forEach(id => {
        const q = seedMap.get(id);
        if (q) this.memoryCache.set(id, q);
      });
      this.persistBuffer();
    }

    return questionIds.map(id => this.memoryCache.get(id)).filter(Boolean);
  }

  // 5. Belirtilen indeks ve sonrasındaki 10 sorunun tamponda hazır olmasını sağla
  async ensureBufferAhead(orderedManifest, currentIndex) {
    if (!orderedManifest || orderedManifest.length === 0) return [];

    const targetIds = [];
    const endIndex = Math.min(currentIndex + QuestionBufferService.BUFFER_SIZE, orderedManifest.length);

    for (let i = currentIndex; i < endIndex; i++) {
      targetIds.push(orderedManifest[i].id);
    }

    // Hedef partiyi çek
    const loadedQuestions = await this.fetchBatch(targetIds);

    // Eğer tampon eşiğinin altına indiysek, arka planda bir sonraki partiyi önden çek (Prefetch)
    this.checkAndPrefetch(orderedManifest, currentIndex);

    return loadedQuestions;
  }

  // 6. Akıllı Arka Plan Ön Yüklemesi (Prefetch Next 10 Questions)
  checkAndPrefetch(orderedManifest, currentIndex) {
    if (this.isFetching || !this.isOnline) return;
    if (this.lastPrefetchIndex === currentIndex) return;

    // Tamponda kullanıcının önünde kaç hazır soru var hesapla
    let readyAhead = 0;
    for (let i = currentIndex + 1; i < orderedManifest.length; i++) {
      if (this.memoryCache.has(orderedManifest[i].id)) {
        readyAhead++;
      } else {
        break; // İlk eksikte dur
      }
    }

    // Eğer hazır soru sayısı eşik değerin (LOW_WATERMARK = 4) altındaysa, bir sonraki 10 soruyu arka planda indir
    if (readyAhead <= QuestionBufferService.LOW_WATERMARK) {
      const prefetchStart = currentIndex + readyAhead;
      const prefetchEnd = Math.min(prefetchStart + QuestionBufferService.BUFFER_SIZE, orderedManifest.length);
      const prefetchIds = [];

      for (let i = prefetchStart; i < prefetchEnd; i++) {
        if (!this.memoryCache.has(orderedManifest[i].id)) {
          prefetchIds.push(orderedManifest[i].id);
        }
      }

      if (prefetchIds.length > 0) {
        this.isFetching = true;
        this.lastPrefetchIndex = currentIndex;
        eventBus.emit('buffer:status', { status: 'buffering', count: prefetchIds.length });

        this.fetchBatch(prefetchIds).then(() => {
          this.isFetching = false;
          eventBus.emit('buffer:status', { 
            status: 'ready', 
            bufferedAhead: this.countReadyAhead(orderedManifest, currentIndex) 
          });
        }).catch(() => {
          this.isFetching = false;
        });
      }
    }
  }

  countReadyAhead(orderedManifest, currentIndex) {
    let count = 0;
    for (let i = currentIndex; i < Math.min(currentIndex + QuestionBufferService.BUFFER_SIZE, orderedManifest.length); i++) {
      if (this.memoryCache.has(orderedManifest[i].id)) count++;
    }
    return count;
  }

  // Soruyu tampondan hızlıca döndür
  getQuestion(id) {
    return this.memoryCache.get(id) || null;
  }
}

export const questionBufferService = new QuestionBufferService();
