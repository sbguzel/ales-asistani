import { state } from './core/state.js';
import { eventBus } from './core/eventBus.js';
import { AuthService } from './modules/auth/authService.js';
import { CanvasManager } from './modules/canvas/canvasManager.js';
import { QuizRenderer } from './modules/quiz/quizRenderer.js';
import { ZenTimer } from './modules/quiz/timer.js';
import { FirestoreService } from './modules/storage/firestoreService.js';
import { AuthModal } from './ui/components/authModal.js';

class App {
  constructor() {
    this.allQuestions = [];
    this.filteredQuestions = [];
    this.currentIndex = 0;
    this.canvasManager = null;
    this.timer = null;
    this.authModal = null;
    this.isEvaluating = false;

    this.init();
  }

  async init() {
    this.initTheme();
    this.initAuth();
    this.initCanvas();
    this.initTimer();
    this.initModeSelector();
    this.initMobileToggle();
    await this.loadQuestions();
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
    this.selectedExam = 'all';
    this.selectedMode = 'all';

    const examSelect = document.getElementById('exam-selector');
    if (examSelect) {
      examSelect.addEventListener('change', (e) => {
        this.selectedExam = e.target.value;
        this.applyFilter();
      });
    }

    const modeBtns = document.querySelectorAll('.mode-btn');
    modeBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        modeBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.selectedMode = btn.getAttribute('data-mode');
        this.applyFilter();
      });
    });
  }

  // 6. Mobil Karalama Butonu
  initMobileToggle() {
    const toggleBtn = document.getElementById('mobile-view-toggle');
    const canvasPanel = document.getElementById('canvas-panel');
    let isShowingCanvas = false;

    toggleBtn.addEventListener('click', () => {
      isShowingCanvas = !isShowingCanvas;
      canvasPanel.classList.toggle('active-mobile', isShowingCanvas);
      toggleBtn.innerHTML = isShowingCanvas 
        ? '<span>📄 Soruyu Gör</span>' 
        : '<span>✏️ Karalama Tahtası</span>';
      
      if (isShowingCanvas) {
        this.canvasManager.resize();
      }
    });
  }

  // Soru Verilerini Yükleme
  async loadQuestions() {
    try {
      const response = await fetch('/data/seed_questions.json');
      this.allQuestions = await response.json();
      this.applyFilter();
    } catch (err) {
      console.error('Soru verisi yüklenirken hata oluştu:', err);
      const container = document.getElementById('question-container');
      container.innerHTML = `<p style="color: var(--zen-error); padding: 20px;">Sorular yüklenemedi. Lütfen sayfayı yenileyin.</p>`;
    }
  }

  applyFilter() {
    let result = [...this.allQuestions];

    // Sınav filtresi
    if (this.selectedExam && this.selectedExam !== 'all') {
      result = result.filter(q => q.examId === this.selectedExam);
    }

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

    // Soru sayacını güncelle
    const counterEl = document.getElementById('question-counter');
    counterEl.textContent = `Soru ${this.currentIndex + 1} / ${this.filteredQuestions.length}`;

    // KaTeX ile soruyu ve şıkları render et
    QuizRenderer.renderQuestion(question, container, (selectedKey, buttonEl) => {
      this.handleOptionSelection(selectedKey, buttonEl, question);
    });

    // Sonraki soru butonunu bağla
    const nextBtn = document.getElementById('next-question-btn');
    if (nextBtn) {
      nextBtn.addEventListener('click', () => this.nextQuestion());
    }

    // Karalama alanını yeni soru için temizle
    if (this.canvasManager) {
      this.canvasManager.clear();
    }

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

  nextQuestion() {
    if (this.currentIndex + 1 < this.filteredQuestions.length) {
      this.currentIndex++;
    } else {
      this.currentIndex = 0; // Başa dön
    }
    this.renderCurrentQuestion();
    document.getElementById('question-panel').scrollTo({ top: 0, behavior: 'smooth' });
  }
}

// Uygulamayı başlat
document.addEventListener('DOMContentLoaded', () => {
  new App();
});
