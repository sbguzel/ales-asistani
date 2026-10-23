import { 
  collection, 
  addDoc, 
  serverTimestamp, 
  query, 
  where, 
  getDocs, 
  orderBy, 
  limit, 
  doc, 
  getDoc, 
  setDoc, 
  arrayUnion 
} from 'firebase/firestore';
import { db } from '../../core/config.js';
import { state } from '../../core/state.js';

export class FirestoreService {
  /**
   * Soru çözüm denemesini (attempt) Firestore'a veya yerel depoya kaydeder
   */
  static async saveAttempt({ questionId, category, selectedOption, isCorrect, timeSpentSeconds, targetTimeSec, usedCanvas }) {
    const user = state.get().user;
    const attemptData = {
      userId: user ? user.uid : 'anonymous',
      questionId,
      category,
      selectedOption,
      isCorrect,
      timeSpentSeconds,
      targetTimeSec,
      usedCanvas: !!usedCanvas,
      timestamp: new Date().toISOString()
    };

    // 1. Önce daima yerel hafızaya (Cache-First) yazarak çevrimdışı çalışmayı garantiye al
    try {
      const localAttempts = JSON.parse(localStorage.getItem('ales_attempts') || '[]');
      localAttempts.push(attemptData);
      localStorage.setItem('ales_attempts', JSON.stringify(localAttempts));
    } catch (e) {
      console.warn('LocalStorage save error:', e);
    }

    // 2. Kullanıcı oturum açmışsa Firestore'a asenkron gönder
    if (user && user.uid) {
      if (typeof navigator !== 'undefined' && navigator.onLine) {
        try {
          const attemptsCol = collection(db, 'user_attempts');
          await addDoc(attemptsCol, {
            ...attemptData,
            createdAt: serverTimestamp()
          });
        } catch (err) {
          console.warn('[FirestoreService] Firestore senkronizasyon gecikmesi, kuyruğa alınıyor:', err);
          this.queuePendingAttempt(attemptData);
        }
      } else {
        // Çevrimdışıyken kuyruğa al
        this.queuePendingAttempt(attemptData);
      }
    }

    // 3. Soruyu kullanıcının çözülen sorular listesine ekle
    await this.markQuestionSolved(user ? user.uid : 'anonymous', questionId);

    return attemptData;
  }

  static queuePendingAttempt(attemptData) {
    try {
      const pending = JSON.parse(localStorage.getItem('ales_pending_sync_attempts') || '[]');
      pending.push(attemptData);
      localStorage.setItem('ales_pending_sync_attempts', JSON.stringify(pending));
    } catch (e) {
      console.warn('Pending attempt queue error:', e);
    }
  }

  static async syncPendingAttempts() {
    if (typeof navigator !== 'undefined' && !navigator.onLine) return;
    try {
      const pending = JSON.parse(localStorage.getItem('ales_pending_sync_attempts') || '[]');
      if (!pending || pending.length === 0) return;

      const user = state.get().user;
      if (!user || !user.uid) return;

      console.log(`📤 [FirestoreService] Çevrimdışı kaydedilen ${pending.length} deneme Firestore'a senkronize ediliyor...`);
      const attemptsCol = collection(db, 'user_attempts');

      for (const att of pending) {
        await addDoc(attemptsCol, {
          ...att,
          userId: user.uid,
          createdAt: serverTimestamp()
        });
      }

      localStorage.removeItem('ales_pending_sync_attempts');
      console.log('✅ [FirestoreService] Tüm çevrimdışı denemeler Firestore ile senkronize edildi.');
    } catch (e) {
      console.warn('[FirestoreService] Senkronizasyon hatası:', e);
    }
  }

  /**
   * Kullanıcının geçmiş yanlış yaptığı soruları (Hata Defteri) getirir
   */
  static getMistakeQuestionIds() {
    try {
      const localAttempts = JSON.parse(localStorage.getItem('ales_attempts') || '[]');
      const mistakes = new Set();
      localAttempts.forEach(att => {
        if (!att.isCorrect) mistakes.add(att.questionId);
        else mistakes.delete(att.questionId); // Sonradan doğru çözdüyse hata defterinden düşür
      });
      return Array.from(mistakes);
    } catch (e) {
      return [];
    }
  }

  /**
   * İstatistikleri hesaplar (Toplam çözülen, Doğru, Yanlış, Başarı % ve Ort. Süre)
   */
  static getLocalStats() {
    try {
      const attempts = JSON.parse(localStorage.getItem('ales_attempts') || '[]');
      const total = attempts.length;
      if (total === 0) {
        return { total: 0, correct: 0, wrong: 0, accuracy: 0, avgTime: 0 };
      }
      const correct = attempts.filter(a => a.isCorrect).length;
      const wrong = total - correct;
      const accuracy = Math.round((correct / total) * 100);
      const totalTime = attempts.reduce((acc, curr) => acc + (curr.timeSpentSeconds || 0), 0);
      const avgTime = Math.round(totalTime / total);

      return { total, correct, wrong, accuracy, avgTime };
    } catch (e) {
      return { total: 0, correct: 0, wrong: 0, accuracy: 0, avgTime: 0 };
    }
  }

  /**
   * Firestore'daki 'questions' koleksiyonundan soruları çeker.
   * orderIndex sırasına göre dizer.
   * Çevrimdışı veya hata durumunda yerel önbellek ve statik seed yedeğini kullanır.
   */
  static async getQuestions() {
    try {
      console.log('[FirestoreService] Sorular Firestore veritabanından alınıyor...');
      const questionsCol = collection(db, 'questions');
      const qQuery = query(questionsCol, orderBy('orderIndex', 'asc'));
      const snapshot = await getDocs(qQuery);

      if (!snapshot.empty) {
        const questions = [];
        snapshot.forEach(docSnap => {
          questions.push(docSnap.data());
        });
        console.log(`[FirestoreService] Firestore'dan ${questions.length} soru başarıyla çekildi.`);

        // Çevrimdışı dayanıklılık için localStorage önbelleğini güncelle
        try {
          localStorage.setItem('ales_cached_questions', JSON.stringify(questions));
        } catch (e) {}

        return { questions, source: 'firestore' };
      }
    } catch (err) {
      console.warn('[FirestoreService] Firestore bağlantı uyarısı (Fallback devrede):', err);
    }

    // Fallback 1: LocalStorage önbelleği
    try {
      const cached = localStorage.getItem('ales_cached_questions');
      if (cached) {
        const parsed = JSON.parse(cached);
        if (Array.isArray(parsed) && parsed.length > 0) {
          console.log(`[FirestoreService] Yerel hafızadaki önbellekten ${parsed.length} soru yüklendi.`);
          return { questions: parsed, source: 'cache' };
        }
      }
    } catch (e) {}

    // Fallback 2: /data/seed_questions.json statik dosya
    console.log('[FirestoreService] /data/seed_questions.json yedeğinden yükleniyor...');
    const response = await fetch('/data/seed_questions.json');
    const questions = await response.json();
    return { questions, source: 'seed_json' };
  }

  /**
   * Tüm yerel soru denemelerini getirir
   */
  static getAttempts() {
    try {
      return JSON.parse(localStorage.getItem('ales_attempts') || '[]');
    } catch (e) {
      return [];
    }
  }

  /**
   * Çözüm geçmişini temizler
   */
  static clearAttempts() {
    try {
      localStorage.removeItem('ales_attempts');
      return true;
    } catch (e) {
      return false;
    }
  }

  /**
   * Kullanıcının analiz sayfasını zengin biçimde deneyimleyebilmesi için
   * gerçekçi simülasyon verileri üretir.
   */
  static seedSampleAttempts(questions = []) {
    if (!questions || questions.length === 0) return [];

    const sampleAttempts = [];
    // 14 farklı soru için gerçekçi ALES deneme verisi
    const targetQuestions = questions.slice(0, 16);

    targetQuestions.forEach((q, idx) => {
      // 12 doğru, 4 yanlış dağılımı
      const isWrong = idx === 4 || idx === 8 || idx === 12 || idx === 15;
      const targetSec = q.targetTimeSec || 75;
      
      // Hız varyasyonları
      let timeSpent;
      if (idx % 3 === 0) {
        timeSpent = Math.round(targetSec * 0.65); // Çok hızlı
      } else if (idx % 3 === 1) {
        timeSpent = Math.round(targetSec * 0.9);  // Normal
      } else {
        timeSpent = Math.round(targetSec * 1.25); // Süre aşımı
      }

      sampleAttempts.push({
        userId: 'anonymous',
        questionId: q.id,
        category: q.category || 'genel',
        selectedOption: isWrong ? 'C' : q.correctAnswer,
        isCorrect: !isWrong,
        timeSpentSeconds: timeSpent,
        targetTimeSec: targetSec,
        usedCanvas: idx % 2 === 0,
        timestamp: new Date(Date.now() - (16 - idx) * 3600000).toISOString()
      });
    });

    localStorage.setItem('ales_attempts', JSON.stringify(sampleAttempts));
    return sampleAttempts;
  }

  /**
   * Kullanıcının (hesaba özel veya misafir) çözdüğü soru ID'lerini döndürür.
   */
  static async getUserSolvedQuestionIds(userId) {
    const isAuth = !!(userId && userId !== 'anonymous');
    const localKey = isAuth ? `ales_solved_${userId}` : 'ales_solved_guest';
    
    // 1. Önce anında yerel önbellekten oku (sıfır gecikme)
    let solvedIds = [];
    try {
      const cached = localStorage.getItem(localKey);
      if (cached) {
        solvedIds = JSON.parse(cached);
      }
    } catch (e) {}

    // Eğer yerelde hiç yoksa ve geçmiş denemeler (attempts) varsa oradan toparla
    if (!solvedIds || solvedIds.length === 0) {
      try {
        const attempts = JSON.parse(localStorage.getItem('ales_attempts') || '[]');
        const fromAttempts = attempts
          .filter(a => isAuth ? a.userId === userId : true)
          .map(a => a.questionId);
        solvedIds = Array.from(new Set(fromAttempts));
        if (solvedIds.length > 0) {
          localStorage.setItem(localKey, JSON.stringify(solvedIds));
        }
      } catch (e) {}
    }

    // 2. Kullanıcı oturum açmışsa Firestore'dan hesaba ait veriyi getir ve senkronize et
    if (isAuth) {
      try {
        const userRef = doc(db, 'users', userId);
        const userSnap = await getDoc(userRef);
        if (userSnap.exists()) {
          const data = userSnap.data();
          const cloudIds = Array.isArray(data.solvedQuestionIds) ? data.solvedQuestionIds : [];
          
          // Yerel ile buluttakileri birleştir
          const merged = Array.from(new Set([...solvedIds, ...cloudIds]));
          if (merged.length !== cloudIds.length) {
            // Yerelde fazladan çözülmüş varsa buluta da gönder
            await setDoc(userRef, { solvedQuestionIds: merged }, { merge: true });
          }
          solvedIds = merged;
          localStorage.setItem(localKey, JSON.stringify(solvedIds));
        }
      } catch (err) {
        console.warn('[FirestoreService] Bulut çözülen sorular senkronizasyon uyarısı:', err);
      }
    }

    return Array.from(new Set(solvedIds));
  }

  /**
   * Soruyu hesaba özel olarak çözüldü olarak işaretler.
   */
  static async markQuestionSolved(userId, questionId) {
    const isAuth = !!(userId && userId !== 'anonymous');
    const localKey = isAuth ? `ales_solved_${userId}` : 'ales_solved_guest';

    // 1. Yerel hafızaya hemen ekle
    try {
      const current = JSON.parse(localStorage.getItem(localKey) || '[]');
      if (!current.includes(questionId)) {
        current.push(questionId);
        localStorage.setItem(localKey, JSON.stringify(current));
      }
    } catch (e) {}

    // 2. Oturum açmışsa Firestore'da hesaba kaydet
    if (isAuth) {
      try {
        const userRef = doc(db, 'users', userId);
        await setDoc(userRef, {
          solvedQuestionIds: arrayUnion(questionId),
          lastActiveAt: serverTimestamp()
        }, { merge: true });
      } catch (err) {
        console.warn('[FirestoreService] Firestore markQuestionSolved uyarısı:', err);
      }
    }
  }

  /**
   * Çözülen soruları (hesaba özel) sıfırlar.
   */
  static async resetSolvedQuestions(userId) {
    const isAuth = !!(userId && userId !== 'anonymous');
    const localKey = isAuth ? `ales_solved_${userId}` : 'ales_solved_guest';

    // 1. Yerel hafızadan temizle
    try {
      localStorage.removeItem(localKey);
    } catch (e) {}

    // 2. Firestore'daki hesaptan temizle
    if (isAuth) {
      try {
        const userRef = doc(db, 'users', userId);
        await setDoc(userRef, {
          solvedQuestionIds: [],
          lastResetAt: serverTimestamp()
        }, { merge: true });
      } catch (err) {
        console.warn('[FirestoreService] Firestore resetSolvedQuestions uyarısı:', err);
      }
    }
    return true;
  }

  /**
   * Kullanıcının ayarlarını getirir (Rastgele mod, çözülenleri gizle vb.)
   */
  static async getUserSettings(userId) {
    const isAuth = !!(userId && userId !== 'anonymous');
    const localKey = isAuth ? `ales_settings_${userId}` : 'ales_settings_guest';
    const defaultSettings = {
      randomOrder: true,
      hideSolved: true
    };

    let settings = { ...defaultSettings };
    try {
      const cached = localStorage.getItem(localKey);
      if (cached) {
        settings = { ...settings, ...JSON.parse(cached) };
      }
    } catch (e) {}

    if (isAuth) {
      try {
        const userRef = doc(db, 'users', userId);
        const userSnap = await getDoc(userRef);
        if (userSnap.exists()) {
          const data = userSnap.data();
          if (data.settings) {
            settings = { ...settings, ...data.settings };
            localStorage.setItem(localKey, JSON.stringify(settings));
          }
        }
      } catch (err) {
        console.warn('[FirestoreService] Bulut ayarlar getirme uyarısı:', err);
      }
    }

    return settings;
  }

  /**
   * Kullanıcının ayarlarını kaydeder
   */
  static async saveUserSettings(userId, newSettings) {
    const isAuth = !!(userId && userId !== 'anonymous');
    const localKey = isAuth ? `ales_settings_${userId}` : 'ales_settings_guest';

    let current = await this.getUserSettings(userId);
    const updated = { ...current, ...newSettings };

    try {
      localStorage.setItem(localKey, JSON.stringify(updated));
    } catch (e) {}

    if (isAuth) {
      try {
        const userRef = doc(db, 'users', userId);
        await setDoc(userRef, {
          settings: updated,
          updatedAt: serverTimestamp()
        }, { merge: true });
      } catch (err) {
        console.warn('[FirestoreService] Bulut ayarlar kaydetme uyarısı:', err);
      }
    }

    return updated;
  }
}
