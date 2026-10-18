import { state } from './core/state.js';
import { eventBus } from './core/eventBus.js';
import { AuthService } from './modules/auth/authService.js';
import { CanvasManager } from './modules/canvas/canvasManager.js';
import { QuizRenderer } from './modules/quiz/quizRenderer.js';
import { ZenTimer } from './modules/quiz/timer.js';
import { FirestoreService } from './modules/storage/firestoreService.js';
import { AuthModal } from './ui/components/authModal.js';
import { AnalyticsManager } from './modules/analytics/analyticsManager.js';

class App {
  constructor() {
    this.allQuestions = [];
    this.filteredQuestions = [];
    this.currentIndex = 0;
    this.canvasManager = null;
    this.timer = null;
    this.authModal = null;
    this.analyticsManager = new AnalyticsManager(this);
    this.isEvaluating = false;

    this.init();
  }

  async init() {
    this.initTouchGestures();
    this.initTheme();
    this.initAuth();
    this.initCanvas();
    this.initTimer();
    this.initModeSelector();
    this.initNavigation();
    this.initMobileToggle();
    await this.loadQuestions();
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
    eventBus.on('auth:stateChanged', (user) => {
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
    });

    AuthService.initAuthListener();
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
    this.applyFilter();
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

    // Klavye yön tuşları ile hızlı geçiş (Sol/Sağ ok)
    window.addEventListener('keydown', (e) => {
      // Eğer kullanıcı input/textarea içinde yazıyorsa yön tuşlarını engelleme
      const activeTag = document.activeElement ? document.activeElement.tagName.toLowerCase() : '';
      if (activeTag === 'input' || activeTag === 'textarea') return;

      if (e.key === 'ArrowLeft') {
        this.prevQuestion();
      } else if (e.key === 'ArrowRight') {
        this.nextQuestion();
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

  // Soru Verilerini Yükleme (Firestore Veritabanı + Akıllı Fallback)
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
      const { questions, source } = await FirestoreService.getQuestions();
      this.allQuestions = questions;
      this.dataSource = source;
      this.updateDbStatusBadge(source);
      this.applyFilter();
    } catch (err) {
      console.error('Soru verisi yüklenirken hata oluştu:', err);
      this.updateDbStatusBadge('error');
      if (container) {
        container.innerHTML = `<p style="color: var(--zen-error); padding: 20px;">Sorular yüklenemedi. Lütfen sayfayı yenileyin.</p>`;
      }
    }
  }

  updateDbStatusBadge(source) {
    const badge = document.getElementById('db-status-badge');
    if (!badge) return;

    badge.className = 'db-status-badge';
    const textEl = badge.querySelector('.db-status-text');

    if (source === 'firestore') {
      badge.classList.remove('loading', 'offline');
      badge.title = 'Sorular canlı Firebase Firestore veritabanından başarıyla yüklendi.';
      if (textEl) textEl.textContent = 'Firestore';
    } else if (source === 'cache') {
      badge.classList.add('offline');
      badge.title = 'Sorular yerel önbellekten (çevrimdışı) yüklendi.';
      if (textEl) textEl.textContent = 'Önbellek';
    } else if (source === 'seed_json') {
      badge.classList.add('offline');
      badge.title = 'Sorular statik veri kaynağından yüklendi.';
      if (textEl) textEl.textContent = 'Statik';
    } else {
      badge.classList.add('offline');
      badge.title = 'Veritabanı bağlantısı kurulamadı.';
      if (textEl) textEl.textContent = 'Çevrimdışı';
    }
  }

  applyFilter() {
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

    this.filteredQuestions = result;
    this.currentIndex = 0;
    this.renderCurrentQuestion();
  }

  renderCurrentQuestion() {
    if (this.filteredQuestions.length === 0) return;

    this.isEvaluating = false;
    const question = this.filteredQuestions[this.currentIndex];
    const container = document.getElementById('question-container');

    // Soru sayacını ve ok butonlarını güncelle
    const counterEl = document.getElementById('question-counter');
    if (counterEl) {
      counterEl.textContent = `Soru ${this.currentIndex + 1} / ${this.filteredQuestions.length}`;
    }
    const prevBtn = document.getElementById('prev-question-btn');
    if (prevBtn) {
      prevBtn.disabled = this.currentIndex === 0;
    }
    const nextNavBtn = document.getElementById('next-nav-btn');
    if (nextNavBtn) {
      nextNavBtn.disabled = this.currentIndex === this.filteredQuestions.length - 1;
    }

    // KaTeX ile soruyu ve şıkları render et
    QuizRenderer.renderQuestion(question, container, (selectedKey, buttonEl) => {
      this.handleOptionSelection(selectedKey, buttonEl, question);
    });

    // Sonraki soru butonunu bağla
    const nextBtn = document.getElementById('next-question-btn');
    if (nextBtn) {
      nextBtn.addEventListener('click', () => this.nextQuestion());
    }

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

    // Kronometreyi başlat (hedef süreye göre)
    const targetSeconds = question.targetTimeSec || 75;
    this.timer.start(targetSeconds);
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
    if (solutionCard) {
      solutionCard.classList.add('active');
      solutionCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // Sonucu yerel önbellek ve Firestore'a kaydet
    await FirestoreService.saveAttempt({
      questionId: question.id,
      category: question.category,
      selectedOption: selectedKey,
      isCorrect,
      timeSpentSeconds: elapsedSeconds,
      targetTimeSec: question.targetTimeSec || 75,
      usedCanvas: this.canvasManager.history.undoStack.length > 0
    });
  }

  prevQuestion() {
    if (this.currentIndex > 0) {
      this.currentIndex--;
      this.renderCurrentQuestion();
      const panel = document.getElementById('question-panel');
      if (panel) panel.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  nextQuestion() {
    if (this.currentIndex + 1 < this.filteredQuestions.length) {
      this.currentIndex++;
    } else {
      this.currentIndex = 0; // Başa dön
    }
    this.renderCurrentQuestion();
    const panel = document.getElementById('question-panel');
    if (panel) panel.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

// Uygulamayı başlat
document.addEventListener('DOMContentLoaded', () => {
  new App();
});
