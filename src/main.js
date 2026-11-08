import { state } from './core/state.js';
import { eventBus } from './core/eventBus.js';
import { AuthService } from './modules/auth/authService.js';
import { CanvasManager } from './modules/canvas/canvasManager.js';
import { QuizRenderer } from './modules/quiz/quizRenderer.js';
import { ZenTimer } from './modules/quiz/timer.js';
import { FirestoreService } from './modules/storage/firestoreService.js';
import { questionBufferService } from './modules/storage/questionBufferService.js';
import { AuthModal } from './ui/components/authModal.js';
import { SettingsModal } from './ui/components/settingsModal.js';
import { AnalyticsManager } from './modules/analytics/analyticsManager.js';

class App {
  constructor() {
    this.allQuestions = [];
    this.filteredQuestions = [];
    this.currentIndex = 0;
    this.canvasManager = null;
    this.timer = null;
    this.authModal = null;
    this.settingsModal = null;
    this.settings = { randomOrder: true, hideSolved: true };
    this.solvedQuestionIds = new Set();
    this.analyticsManager = new AnalyticsManager(this);
    this.isEvaluating = false;
    this.isQuestionStarted = false;

    this.init();
  }

  async init() {
    this.initTouchGestures();
    this.initTheme();
    this.initAuth();
    this.initSettings();
    this.initCanvas();
    this.initTimer();
    this.initModeSelector();
    this.initNavigation();
    this.initMobileToggle();
    this.initNetworkAndBufferListeners();
    await this.loadUserSettingsAndProgress();
    await this.loadQuestions();
  }

  // Çevrimdışı ve akıllı tampon dinleyicileri
  initNetworkAndBufferListeners() {
    eventBus.on('network:status', async ({ isOnline }) => {
      this.updateBufferStatusBadge();
      if (isOnline) {
        await FirestoreService.syncPendingAttempts();
      }
    });

    eventBus.on('buffer:status', () => {
      this.updateBufferStatusBadge();
    });
  }

  // Dokunmatik cihazlarda ve iOS Safari'de istenmeyen zoom'ları engelleme
  initTouchGestures() {
    let lastTouchEnd = 0;
    document.addEventListener('touchend', (e) => {
      const now = Date.now();
      if (now - lastTouchEnd <= 300) {
        const tag = e.target && e.target.tagName ? e.target.tagName.toLowerCase() : '';
        if (tag !== 'input' && tag !== 'textarea') {
          e.preventDefault();
        }
      }
      lastTouchEnd = now;
    }, { passive: false });

    // iOS Safari gesturestart/change/end (pinch zoom) engelleme
    document.addEventListener('gesturestart', (e) => e.preventDefault());
    document.addEventListener('gesturechange', (e) => e.preventDefault());
    document.addEventListener('gestureend', (e) => e.preventDefault());

    // Mobil tarayıcılarda viewport kaymasını ve header'ın ekrandan çıkmasını engelle
    window.addEventListener('scroll', () => {
      if (window.scrollY !== 0 || window.scrollX !== 0) {
        window.scrollTo(0, 0);
      }
    }, { passive: true });
  }

  // 1. Tema Yönetimi
  initTheme() {
    const savedTheme = localStorage.getItem('ales_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);

    const themeBtn = document.getElementById('theme-toggle-btn');
    themeBtn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('ales_theme', next);
      state.set({ theme: next });
    });
  }

  // 2. Apple Sadeliğinde Auth & Profil
  initAuth() {
    this.authModal = new AuthModal();
    const authContainer = document.getElementById('auth-header-container');

    // Giriş butonunu dinle
    authContainer.addEventListener('click', (e) => {
      const target = e.target.closest('#open-auth-btn');
      if (target) {
        const user = state.get().user;
        if (user) {
          // Zaten giriş yapmışsa çıkış onay/menüsü
          if (confirm(`@${user.username} olarak oturum açık. Çıkış yapmak istiyor musunuz?`)) {
            AuthService.logout();
          }
        } else {
          this.authModal.open('login');
        }
      }
    });

    // Oturum durumundaki değişimleri dinle
    eventBus.on('auth:stateChanged', async (user) => {
      if (user) {
        authContainer.innerHTML = `
          <button class="user-profile-badge" id="open-auth-btn" title="Çıkış yapmak için tıklayın">
            <span class="user-avatar-circle">${user.username.charAt(0).toUpperCase()}</span>
            <span>@${user.username}</span>
          </button>
        `;
      } else {
        authContainer.innerHTML = `
          <button class="user-profile-badge" id="open-auth-btn">
            <span class="user-avatar-circle">?</span>
            <span>Giriş Yap</span>
          </button>
        `;
      }

      // Kullanıcı değiştiğinde o kullanıcıya ait soru ilerlemesini ve ayarları yükle
      await this.loadUserSettingsAndProgress();
      if (this.allQuestions && this.allQuestions.length > 0) {
        this.applyFilter();
      }
      if (this.settingsModal) {
        this.settingsModal.refreshUI();
      }
    });

    AuthService.initAuthListener();
  }

  // 2.1. Ayarlar Modalı ve Sıralama Yönetimi
  initSettings() {
    this.settingsModal = new SettingsModal(this);

    // Ayarlar butonu
    const settingsBtn = document.getElementById('settings-toggle-btn');
    if (settingsBtn) {
      settingsBtn.addEventListener('click', () => {
        this.settingsModal.open();
      });
    }

    // Header hızlı sıra değiştirme butonu
    const orderToggleBtn = document.getElementById('order-mode-toggle');
    if (orderToggleBtn) {
      orderToggleBtn.addEventListener('click', async () => {
        const nextOrder = !this.settings.randomOrder;
        await this.updateSettings({ randomOrder: nextOrder });
      });
    }
  }

  async loadUserSettingsAndProgress() {
    const user = state.get().user;
    const uid = user ? user.uid : 'anonymous';
    this.settings = await FirestoreService.getUserSettings(uid);
    const solvedIds = await FirestoreService.getUserSolvedQuestionIds(uid);
    this.solvedQuestionIds = new Set(solvedIds);
    this.updateOrderModeBadge();
  }

  updateOrderModeBadge() {
    const badge = document.getElementById('order-mode-toggle');
    if (!badge) return;
    const isRandom = !!this.settings.randomOrder;
    badge.className = `order-mode-badge ${isRandom ? 'random' : 'sequential'}`;
    const iconEl = badge.querySelector('.order-icon');
    const textEl = badge.querySelector('.order-text');
    if (iconEl) iconEl.textContent = isRandom ? '🔀' : '🔢';
    if (textEl) textEl.textContent = isRandom ? 'Karışık' : 'Sıralı';
    badge.title = isRandom 
      ? 'Soru Sıralaması: Karışık (Rastgele) - Tıklayarak Sıralı yap'
      : 'Soru Sıralaması: Sınav Sırasına Göre - Tıklayarak Karışık yap';
  }

  async updateSettings(partial) {
    const user = state.get().user;
    const uid = user ? user.uid : 'anonymous';
    this.settings = await FirestoreService.saveUserSettings(uid, partial);
    this.updateOrderModeBadge();
    if (this.settingsModal) {
      this.settingsModal.refreshUI();
    }
    this.applyFilter();
  }

  async resetSolvedQuestions() {
    const user = state.get().user;
    const uid = user ? user.uid : 'anonymous';
    await FirestoreService.resetSolvedQuestions(uid);
    this.solvedQuestionIds.clear();
    this.applyFilter();
    if (this.settingsModal) {
      this.settingsModal.refreshUI();
    }
  }

  async markQuestionAsSolved(questionId) {
    this.solvedQuestionIds.add(questionId);
    const user = state.get().user;
    const uid = user ? user.uid : 'anonymous';
    await FirestoreService.markQuestionSolved(uid, questionId);
    if (this.settingsModal) {
      this.settingsModal.refreshUI();
    }
  }

  // 3. Karalama & Çizim Alanı
  initCanvas() {
    const canvasEl = document.getElementById('drawing-canvas');
    const containerEl = document.getElementById('canvas-panel');
    this.canvasManager = new CanvasManager(canvasEl, containerEl);

    // Toolbar Kontrolleri
    const toolPen = document.getElementById('tool-pen');
    const toolEraser = document.getElementById('tool-eraser');
    const toolGrid = document.getElementById('tool-grid');
    const toolUndo = document.getElementById('tool-undo');
    const toolRedo = document.getElementById('tool-redo');
    const toolClear = document.getElementById('tool-clear');
    const colorDots = document.querySelectorAll('.color-dot');

    toolPen.addEventListener('click', () => {
      state.set({ canvas: { ...state.get().canvas, isEraser: false } });
      toolPen.classList.add('active');
      toolEraser.classList.remove('active');
    });

    toolEraser.addEventListener('click', () => {
      state.set({ canvas: { ...state.get().canvas, isEraser: true } });
      toolEraser.classList.add('active');
      toolPen.classList.remove('active');
    });

    toolGrid.addEventListener('click', () => {
      const isGridActive = this.canvasManager.toggleGrid();
      toolGrid.classList.toggle('active', isGridActive);
    });

    toolUndo.addEventListener('click', () => this.canvasManager.undo());
    toolRedo.addEventListener('click', () => this.canvasManager.redo());
    toolClear.addEventListener('click', () => {
      if (confirm('Karalama alanını temizlemek istiyor musunuz?')) {
        this.canvasManager.clear();
      }
    });

    colorDots.forEach(dot => {
      dot.addEventListener('click', () => {
        colorDots.forEach(d => d.classList.remove('active'));
        dot.classList.add('active');
        const color = dot.getAttribute('data-color');
        state.set({ canvas: { ...state.get().canvas, penColor: color, isEraser: false } });
        toolPen.classList.add('active');
        toolEraser.classList.remove('active');
      });
    });
  }

  // 4. Sessiz Zen Kronometre
  initTimer() {
    const timerEl = document.getElementById('zen-timer');
    this.timer = new ZenTimer(timerEl, 75);
  }

  // 5. Mod ve Kategori Seçici
  initModeSelector() {
    this.selectedMode = 'all';

    const modeBtns = document.querySelectorAll('.mode-btn');
    modeBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const mode = btn.getAttribute('data-mode');
        this.switchMode(mode);
      });
    });

    const brandHome = document.getElementById('brand-home');
    if (brandHome) {
      brandHome.addEventListener('click', () => {
        this.switchMode('all');
      });
    }
  }

  switchMode(mode) {
    this.selectedMode = mode;
    const modeBtns = document.querySelectorAll('.mode-btn');
    modeBtns.forEach(b => {
      if (b.getAttribute('data-mode') === mode) {
        b.classList.add('active');
      } else {
        b.classList.remove('active');
      }
    });
    this.applyFilter(null, true);
  }

  // 6. Soru Gezinme ve Klavye Kısayolları
  initNavigation() {
    const prevBtn = document.getElementById('prev-question-btn');
    const nextBtn = document.getElementById('next-nav-btn');

    if (prevBtn) {
      prevBtn.addEventListener('click', () => this.prevQuestion());
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => this.nextQuestion());
    }

    // Klavye yön tuşları ve başlatma kısayolları (Sol/Sağ ok, Boşluk, Enter)
    window.addEventListener('keydown', (e) => {
      // Eğer kullanıcı input/textarea içinde yazıyorsa yön tuşlarını engelleme
      const activeTag = document.activeElement ? document.activeElement.tagName.toLowerCase() : '';
      if (activeTag === 'input' || activeTag === 'textarea') return;

      const isModalOpen = document.querySelector('.modal-backdrop.active');
      if (isModalOpen) return;

      // Başla ekranındayken Space veya Enter ile soruyu başlat
      if (!this.isQuestionStarted && (e.key === ' ' || e.key === 'Spacebar' || e.key === 'Enter')) {
        e.preventDefault();
        this.startCurrentQuestion();
        return;
      }

      // Soru çözüldükten sonra çözüm kartı açıksa Enter ile sonraki soruya geç
      if (this.isQuestionStarted) {
        const solutionCard = document.getElementById('solution-card');
        if (solutionCard && solutionCard.classList.contains('active') && e.key === 'Enter') {
          e.preventDefault();
          this.nextQuestion();
          return;
        }
      }

      if (e.key === 'ArrowLeft') {
        this.prevQuestion();
      } else if (e.key === 'ArrowRight') {
        this.nextQuestion();
      }
    });

    // URL Hash değiştiğinde ilgili soruya atla
    window.addEventListener('hashchange', async () => {
      const hash = window.location.hash.substring(1);
      if (hash && this.filteredQuestions && this.filteredQuestions.length > 0) {
        let idx = this.filteredQuestions.findIndex(q => q.id === hash);
        if (idx !== -1 && idx !== this.currentIndex) {
          this.currentIndex = idx;
          await this.renderCurrentQuestion();
        }
      }
    });
  }

  // 6. Mobil Karalama Butonu ve Ekran Yönetimi
  initMobileToggle() {
    const toggleBtn = document.getElementById('mobile-view-toggle');
    const closeCanvasBtn = document.getElementById('close-canvas-mobile-btn');
    const canvasPanel = document.getElementById('canvas-panel');
    let isShowingCanvas = false;

    const setCanvasState = (show) => {
      isShowingCanvas = show;
      if (canvasPanel) {
        canvasPanel.classList.toggle('active-mobile', isShowingCanvas);
      }
      if (toggleBtn) {
        toggleBtn.classList.toggle('active-canvas', isShowingCanvas);
        toggleBtn.innerHTML = isShowingCanvas 
          ? '<span>📄 Soruyu Gör</span>' 
          : '<span>✏️ Karalama Tahtası</span>';
      }
      if (isShowingCanvas && this.canvasManager) {
        setTimeout(() => this.canvasManager.resize(), 60);
      }
    };

    if (toggleBtn) {
      toggleBtn.addEventListener('click', (e) => {
        e.preventDefault();
        setCanvasState(!isShowingCanvas);
      });
    }

    if (closeCanvasBtn) {
      closeCanvasBtn.addEventListener('click', (e) => {
        e.preventDefault();
        setCanvasState(false);
      });
    }
  }

  // Soru Verilerini Yükleme (Hafif Manifesto + Optimum 10'luk Akıllı Tampon)
  async loadQuestions() {
    const container = document.getElementById('question-container');
    if (container) {
      container.innerHTML = `
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 320px; gap: 16px; color: var(--text-secondary);">
          <div class="db-spinner"></div>
          <p style="font-size: 14px; font-weight: 500;">Sorular veritabanından getiriliyor...</p>
        </div>
      `;
    }

    try {
      const { manifest, source } = await questionBufferService.loadManifest();
      this.allQuestions = manifest;
      this.dataSource = source;
      await this.applyFilter();
      this.updateBufferStatusBadge();
    } catch (err) {
      console.error('Soru verisi yüklenirken hata oluştu:', err);
      this.updateBufferStatusBadge();
      if (container) {
        container.innerHTML = `<p style="color: var(--zen-error); padding: 20px;">Sorular yüklenemedi. Lütfen sayfayı yenileyin.</p>`;
      }
    }
  }

  updateBufferStatusBadge() {
    const badge = document.getElementById('db-status-badge');
    if (!badge) return;

    badge.className = 'db-status-badge';
    const textEl = badge.querySelector('.db-status-text');

    const isOnline = questionBufferService.isOnline;
    const readyCount = questionBufferService.countReadyAhead(this.filteredQuestions || [], this.currentIndex || 0);

    if (questionBufferService.isFetching) {
      badge.classList.add('loading');
      badge.title = 'Sıradaki sorular arka planda tamponlanıyor...';
      if (textEl) textEl.textContent = 'Tamponlanıyor...';
    } else if (isOnline) {
      badge.classList.remove('loading', 'offline');
      badge.title = `Firestore bağlantısı aktif. Tamponda sıradaki ${readyCount} soru hazır. İnternet kopsa dahi kesintisiz çözebilirsiniz.`;
      if (textEl) textEl.textContent = `Firestore (${readyCount} Hazır)`;
    } else {
      badge.classList.add('offline');
      badge.title = `İnternet bağlantısı kesildi. Tampondaki ${readyCount} soruyu çevrimdışı çözmeye devam edebilirsiniz.`;
      if (textEl) textEl.textContent = `Çevrimdışı (${readyCount} Hazır)`;
    }
  }

  // 5.1. Bağlantılı Soru Gruplarını Koruyan Rastgele Karıştırma Algoritması
  shuffleQuestionsPreservingGroups(questions) {
    if (!questions || questions.length <= 1) return [...questions];

    // Soruları bağımsız sorular veya bağlantılı soru grupları halinde kümele
    const groupsMap = new Map();
    const groupOrder = [];

    questions.forEach((q, idx) => {
      const groupKey = (q.isGroupQuestion && q.groupId) ? `grp_${q.groupId}` : `single_${q.id || idx}`;
      if (!groupsMap.has(groupKey)) {
        groupsMap.set(groupKey, []);
        groupOrder.push(groupKey);
      }
      groupsMap.get(groupKey).push(q);
    });

    // Her küme içindeki soruları kendi orijinal sıra numaralarına göre tut
    const groupArrays = groupOrder.map(key => {
      const items = groupsMap.get(key);
      items.sort((a, b) => (a.number || 0) - (b.number || 0));
      return items;
    });

    // Kümeleri Fisher-Yates algoritması ile rastgele karıştır
    for (let i = groupArrays.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [groupArrays[i], groupArrays[j]] = [groupArrays[j], groupArrays[i]];
    }

    // Düzleştirilmiş listeyi döndür
    return groupArrays.flat();
  }

  async applyFilter(targetQuestionId = null, ignoreHash = false) {
    const questionPanel = document.getElementById('question-panel');
    const canvasPanel = document.getElementById('canvas-panel');
    const analyticsPanel = document.getElementById('analytics-panel');
    const timerEl = document.getElementById('zen-timer');
    const navGroupEl = document.querySelector('.question-nav-group');
    const mobileToggle = document.getElementById('mobile-view-toggle');

    if (this.selectedMode === 'analytics') {
      // 1. Analiz Dashboard Görünümü
      if (questionPanel) questionPanel.style.display = 'none';
      if (canvasPanel) canvasPanel.style.display = 'none';
      if (mobileToggle) mobileToggle.style.display = 'none';
      if (timerEl) timerEl.style.opacity = '0.25';
      if (navGroupEl) navGroupEl.style.opacity = '0.25';

      if (analyticsPanel) {
        analyticsPanel.style.display = 'block';
        this.analyticsManager.render(analyticsPanel);
      }
      return;
    }

    // 2. Soru Çözüm Moduna Dönüş
    if (analyticsPanel) analyticsPanel.style.display = 'none';
    if (questionPanel) questionPanel.style.display = '';
    if (canvasPanel) {
      canvasPanel.style.display = '';
      if (this.canvasManager) this.canvasManager.resize();
    }
    if (mobileToggle) mobileToggle.style.display = '';
    if (timerEl) timerEl.style.opacity = '1';
    if (navGroupEl) navGroupEl.style.opacity = '1';

    let result = [...this.allQuestions];

    // Ders/Mod filtresi
    if (this.selectedMode === 'mistakes') {
      const mistakeIds = FirestoreService.getMistakeQuestionIds();
      result = result.filter(q => mistakeIds.includes(q.id));
      if (result.length === 0) {
        alert('Tebrikler! Seçili filtrede henüz yanlış çözülmüş soru bulunmuyor.');
        result = [...this.allQuestions];
      }
    } else if (this.selectedMode && this.selectedMode !== 'all') {
      result = result.filter(q => q.subject === this.selectedMode);
    }

    // Çözülen soruları gizleme filtresi (Hata Defteri hariç)
    if (this.settings.hideSolved && this.selectedMode !== 'mistakes') {
      result = result.filter(q => !this.solvedQuestionIds.has(q.id));
    }

    // Sıralama (Rastgele Karışık veya Orijinal Sınav Sırasına Göre)
    if (this.settings.randomOrder) {
      result = this.shuffleQuestionsPreservingGroups(result);
    } else {
      result.sort((a, b) => (a.orderIndex || a.number || 0) - (b.orderIndex || b.number || 0));
    }

    this.filteredQuestions = result;
    
    // Belirli bir soru hedefi var mı (parametre, URL query veya URL hash)
    let target = targetQuestionId || new URLSearchParams(window.location.search).get('q');
    
    // Yalnızca sıralı moddaysak ve hash yok sayılmadıysa URL hash'i hedef olarak kullan
    // Karışık (rastgele) moddayken sayfa yenilendiğinde her zaman taze rastgele soru seçilir
    if (!target && !ignoreHash && !this.settings.randomOrder && window.location.hash) {
      target = window.location.hash.substring(1);
    }

    if (target && result.some(q => q.id === target)) {
      this.currentIndex = result.findIndex(q => q.id === target);
    } else {
      this.currentIndex = 0;
      if (result.length > 0 && result[0]?.id && !this.settings.randomOrder) {
        history.replaceState(null, '', '#' + result[0].id);
      } else if (this.settings.randomOrder && window.location.hash) {
        history.replaceState(null, '', window.location.pathname + window.location.search);
      }
    }

    // İlk 10 soruluk akıllı tamponu önden yükle
    await questionBufferService.ensureBufferAhead(this.filteredQuestions, this.currentIndex);
    await this.renderCurrentQuestion();
  }

  async renderCurrentQuestion() {
    this.isEvaluating = false;
    this.isQuestionStarted = false;
    this.resetScrollPositions();
    const container = document.getElementById('question-container');
    const counterEl = document.getElementById('question-counter');
    const prevBtn = document.getElementById('prev-question-btn');
    const nextNavBtn = document.getElementById('next-nav-btn');

    // Eğer çözülenler gizlendiğinde veya filtrelendiğinde havuzda soru kalmadıysa
    if (!this.filteredQuestions || this.filteredQuestions.length === 0) {
      if (counterEl) counterEl.textContent = '0 / 0 (Tamamlandı)';
      if (prevBtn) prevBtn.disabled = true;
      if (nextNavBtn) nextNavBtn.disabled = true;
      if (this.timer) this.timer.reset();

      this.renderAllCompletedState(container);
      return;
    }

    if (this.currentIndex >= this.filteredQuestions.length) {
      this.currentIndex = 0;
    }

    let question = this.filteredQuestions[this.currentIndex];

    // Eğer soru tam içeriği henüz tampona gelmemişse hızlıca indir ve birleştir
    if (!question || !question.questionText) {
      await questionBufferService.ensureBufferAhead(this.filteredQuestions, this.currentIndex);
      const fullQ = questionBufferService.getQuestion(question.id);
      if (fullQ) {
        Object.assign(question, fullQ);
      }
    }

    // Yalnızca sıralı modda URL hash'ini güncelle (Rastgele modda sayfa yenilenince yeni soru gelsin diye hash tutulmaz)
    if (question && question.id && !this.settings.randomOrder) {
      history.replaceState(null, '', '#' + question.id);
    } else if (this.settings.randomOrder && window.location.hash) {
      history.replaceState(null, '', window.location.pathname + window.location.search);
    }

    // Soru sayacını ve ok butonlarını güncelle
    if (counterEl) {
      counterEl.textContent = `Soru ${this.currentIndex + 1} / ${this.filteredQuestions.length}`;
    }
    if (prevBtn) {
      prevBtn.disabled = this.currentIndex === 0;
    }
    if (nextNavBtn) {
      nextNavBtn.disabled = this.currentIndex >= this.filteredQuestions.length - 1;
    }

    // Arka planda sıradaki 10 soruyu tamponla ve durum rozetini tazele
    questionBufferService.checkAndPrefetch(this.filteredQuestions, this.currentIndex);
    this.updateBufferStatusBadge();

    // Karalama alanını akıllı yönet:
    // Eğer aynı soru grubundaysak adayın çizdiği mantık tablosunu/notlarını KORU!
    const prevQuestion = this.currentActiveQuestion;
    const isSameGroup = prevQuestion && 
                        prevQuestion.isGroupQuestion && 
                        question.isGroupQuestion && 
                        prevQuestion.groupId === question.groupId;

    if (!isSameGroup && this.canvasManager) {
      this.canvasManager.clear();
    }
    this.currentActiveQuestion = question;

    // Kronometreyi sıfırla ve hazır durumda beklet (Kullanıcı Başla butonuna basana kadar süre işlemez)
    if (this.timer) {
      this.timer.reset();
    }

    // Soru öncesi "Başla" ekranını render et (Kullanıcı mola verebilir, hazır olduğunda başlar)
    QuizRenderer.renderStartCard(question, container, () => {
      this.startCurrentQuestion();
    }, {
      currentIndex: this.currentIndex,
      totalCount: this.filteredQuestions.length
    });
  }

  async startCurrentQuestion() {
    if (this.isQuestionStarted) return;

    try {
      let question = this.filteredQuestions[this.currentIndex];
      if (!question) return;

      // Eğer soru tam içeriği henüz yüklenmediyse yükle
      if (!question.questionText || !question.options) {
        await questionBufferService.ensureBufferAhead(this.filteredQuestions, this.currentIndex);
        const fullQ = questionBufferService.getQuestion(question.id);
        if (fullQ) {
          Object.assign(question, fullQ);
        }
      }

      this.isQuestionStarted = true;

      const container = document.getElementById('question-container');

      // KaTeX ile soruyu ve şıkları render et
      QuizRenderer.renderQuestion(question, container, (selectedKey, buttonEl) => {
        this.handleOptionSelection(selectedKey, buttonEl, question);
      });

      // Sonraki soru butonunu bağla
      const nextBtn = document.getElementById('next-question-btn');
      if (nextBtn) {
        nextBtn.addEventListener('click', () => this.nextQuestion());
      }

      // Kronometreyi başlat (hedef süreye göre)
      const targetSeconds = question.targetTimeSec || 75;
      if (this.timer) {
        this.timer.start(targetSeconds);
      }
    } catch (err) {
      console.error('[startCurrentQuestion] Hata oluştu:', err);
      this.isQuestionStarted = false;
    }
  }

  renderAllCompletedState(container) {
    if (!container) return;

    const modeLabels = {
      all: 'Tüm Sınav Havuzundaki',
      matematik: 'Matematik & Geometri Dersindeki',
      turkce: 'Türkçe Dersindeki',
      mantik: 'Sözel Mantık Dersindeki',
      mistakes: 'Hata Defterindeki'
    };

    const label = modeLabels[this.selectedMode] || 'Seçili Kategorideki';
    const totalSolved = this.solvedQuestionIds ? this.solvedQuestionIds.size : 0;
    const totalQuestions = this.allQuestions ? this.allQuestions.length : 300;

    container.innerHTML = `
      <div class="all-completed-card">
        <div class="completed-icon-wrapper">🏆</div>
        <h2 class="completed-title">Tebrikler! Sorular Tamamlandı</h2>
        <p class="completed-subtitle">
          ${label} mevcut tüm soruları başarıyla çözdünüz. İlerlemenizi sıfırlayarak tüm soruları yeniden çözebilir veya ayarları değiştirebilirsiniz.
        </p>

        <div style="margin-bottom: 24px; padding: 12px 18px; background: var(--bg-tertiary); border-radius: var(--radius-md); font-size: 13.5px; color: var(--text-secondary);">
          📊 Toplam Çözülen Soru Sayısı: <strong style="color: var(--accent-primary);">${totalSolved}</strong> / ${totalQuestions}
        </div>

        <div class="completed-actions">
          <button type="button" class="completed-primary-btn" id="empty-state-reset-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
              <path d="M3 3v5h5"/>
            </svg>
            <span>Çözülen Soruları Sıfırla</span>
          </button>
          
          <button type="button" class="completed-secondary-btn" id="empty-state-show-all-btn">
            <span>👁️ Tüm Soruları Göster (Çözülenler Dahil)</span>
          </button>
        </div>
      </div>
    `;

    const resetBtn = container.querySelector('#empty-state-reset-btn');
    if (resetBtn) {
      resetBtn.addEventListener('click', async () => {
        if (confirm('Çözülen soruları sıfırlayarak soruları tekrar havuzunuza eklemek istiyor musunuz?')) {
          await this.resetSolvedQuestions();
        }
      });
    }

    const showAllBtn = container.querySelector('#empty-state-show-all-btn');
    if (showAllBtn) {
      showAllBtn.addEventListener('click', async () => {
        await this.updateSettings({ hideSolved: false });
      });
    }
  }

  async handleOptionSelection(selectedKey, buttonEl, question) {
    if (this.isEvaluating) return;
    this.isEvaluating = true;

    // Kronometreyi durdur ve süreyi kaydet
    const elapsedSeconds = this.timer.stop();
    const isCorrect = selectedKey === question.correctAnswer;

    // Şıkların durumlarını güncelle
    const allOptionBtns = document.querySelectorAll('.option-btn');
    allOptionBtns.forEach(btn => {
      btn.disabled = true;
      const key = btn.getAttribute('data-key');
      if (key === question.correctAnswer) {
        btn.classList.add('correct');
      } else if (key === selectedKey && !isCorrect) {
        btn.classList.add('wrong');
      }
    });

    // Çözüm ve ipucu kartını göster
    const solutionCard = document.getElementById('solution-card');
    const questionPanel = document.getElementById('question-panel');
    if (solutionCard && questionPanel) {
      solutionCard.classList.add('active');
      setTimeout(() => {
        const targetScroll = solutionCard.offsetTop - 20;
        questionPanel.scrollTo({ top: targetScroll, behavior: 'smooth' });
      }, 50);
    }

    // Sonucu yerel önbellek ve Firestore'a kaydet (hesaba özel)
    await FirestoreService.saveAttempt({
      questionId: question.id,
      category: question.category,
      selectedOption: selectedKey,
      isCorrect,
      timeSpentSeconds: elapsedSeconds,
      targetTimeSec: question.targetTimeSec || 75,
      usedCanvas: this.canvasManager ? this.canvasManager.history.undoStack.length > 0 : false
    });

    // Soruyu çözüldü olarak işaretle
    await this.markQuestionAsSolved(question.id);
  }

  resetScrollPositions() {
    window.scrollTo(0, 0);
    document.documentElement.scrollTop = 0;
    document.body.scrollTop = 0;
    const appEl = document.getElementById('app');
    if (appEl) appEl.scrollTop = 0;
    const panel = document.getElementById('question-panel');
    if (panel) {
      panel.scrollTop = 0;
      panel.scrollTo({ top: 0, behavior: 'instant' });
    }
  }

  async prevQuestion() {
    if (this.currentIndex > 0) {
      this.currentIndex--;
      await this.renderCurrentQuestion();
      this.resetScrollPositions();
    }
  }

  async nextQuestion() {
    const currentQ = this.filteredQuestions[this.currentIndex];

    // Eğer 'Çözülenleri Gizle' aktifse ve mevcut soru az önce çözülmüşse:
    // Bu soru artık havuzdan çıkarılır ve bir sonraki soruya geçilir.
    if (this.settings.hideSolved && this.selectedMode !== 'mistakes' && currentQ && this.solvedQuestionIds.has(currentQ.id)) {
      this.filteredQuestions.splice(this.currentIndex, 1);
      
      // Eğer listenin sonundaysak ve soru kaldıysa başa al
      if (this.currentIndex >= this.filteredQuestions.length) {
        this.currentIndex = 0;
      }
    } else {
      // Normal ilerleme
      if (this.currentIndex + 1 < this.filteredQuestions.length) {
        this.currentIndex++;
      } else {
        this.currentIndex = 0;
      }
    }

    await this.renderCurrentQuestion();
    this.resetScrollPositions();
  }
}

// Uygulamayı başlat
document.addEventListener('DOMContentLoaded', () => {
  window.app = new App();
});
