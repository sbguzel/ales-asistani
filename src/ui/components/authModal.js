import { AuthService } from '../../modules/auth/authService.js';
import { eventBus } from '../../core/eventBus.js';

export class AuthModal {
  constructor() {
    this.mode = 'login'; // 'login' | 'register'
    this.createDom();
    this.bindEvents();
  }

  createDom() {
    const backdrop = document.createElement('div');
    backdrop.className = 'modal-backdrop';
    backdrop.id = 'auth-modal-backdrop';

    backdrop.innerHTML = `
      <div class="auth-modal" role="dialog" aria-modal="true">
        <button class="modal-close-btn" id="modal-close-btn" aria-label="Kapat">&times;</button>
        
        <div class="auth-header">
          <div class="auth-logo">A</div>
          <h2 class="auth-title" id="auth-modal-title">Giriş Yap</h2>
          <p class="auth-subtitle" id="auth-modal-subtitle">E-posta ve onay gerekmez. Yalnızca kullanıcı adı ve şifre.</p>
        </div>

        <div class="auth-error-msg" id="auth-error-msg"></div>

        <form class="auth-form" id="auth-form">
          <div class="form-group">
            <label class="form-label" for="auth-username">Kullanıcı Adı</label>
            <input 
              type="text" 
              id="auth-username" 
              class="form-input" 
              placeholder="örn: ahmet99" 
              autocomplete="username" 
              required 
              maxlength="20"
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="auth-password">Şifre</label>
            <input 
              type="password" 
              id="auth-password" 
              class="form-input" 
              placeholder="En az 6 karakter" 
              autocomplete="current-password" 
              required 
              minlength="6"
            />
          </div>

          <div class="auth-options">
            <label class="remember-label">
              <input type="checkbox" id="auth-remember" checked />
              <span>Beni Hatırla</span>
            </label>
          </div>

          <button type="submit" class="auth-submit-btn" id="auth-submit-btn">
            <span id="auth-btn-text">Giriş Yap</span>
          </button>
        </form>

        <div class="auth-toggle-mode">
          <span id="auth-toggle-prompt">Hesabın yok mu?</span>
          <button type="button" class="auth-toggle-link" id="auth-toggle-link">Hemen Kaydol</button>
        </div>
      </div>
    `;

    document.body.appendChild(backdrop);
    this.backdrop = backdrop;
    this.form = backdrop.querySelector('#auth-form');
    this.usernameInput = backdrop.querySelector('#auth-username');
    this.passwordInput = backdrop.querySelector('#auth-password');
    this.rememberInput = backdrop.querySelector('#auth-remember');
    this.errorMsg = backdrop.querySelector('#auth-error-msg');
    this.titleEl = backdrop.querySelector('#auth-modal-title');
    this.submitBtnText = backdrop.querySelector('#auth-btn-text');
    this.togglePrompt = backdrop.querySelector('#auth-toggle-prompt');
    this.toggleLink = backdrop.querySelector('#auth-toggle-link');
    this.closeBtn = backdrop.querySelector('#modal-close-btn');
  }

  bindEvents() {
    this.closeBtn.addEventListener('click', () => this.close());
    this.backdrop.addEventListener('click', (e) => {
      if (e.target === this.backdrop) this.close();
    });

    this.toggleLink.addEventListener('click', () => {
      this.mode = this.mode === 'login' ? 'register' : 'login';
      this.updateModeUI();
    });

    this.form.addEventListener('submit', async (e) => {
      e.preventDefault();
      await this.handleSubmit();
    });
  }

  updateModeUI() {
    this.hideError();
    if (this.mode === 'login') {
      this.titleEl.textContent = 'Giriş Yap';
      this.submitBtnText.textContent = 'Giriş Yap';
      this.togglePrompt.textContent = 'Hesabın yok mu?';
      this.toggleLink.textContent = 'Hemen Kaydol';
      this.passwordInput.autocomplete = 'current-password';
    } else {
      this.titleEl.textContent = 'Hesap Oluştur';
      this.submitBtnText.textContent = 'Kaydol ve Başla';
      this.togglePrompt.textContent = 'Zaten hesabın var mı?';
      this.toggleLink.textContent = 'Giriş Yap';
      this.passwordInput.autocomplete = 'new-password';
    }
  }

  showError(message) {
    this.errorMsg.textContent = message;
    this.errorMsg.classList.add('active');
  }

  hideError() {
    this.errorMsg.textContent = '';
    this.errorMsg.classList.remove('active');
  }

  async handleSubmit() {
    const username = this.usernameInput.value.trim();
    const password = this.passwordInput.value;
    const rememberMe = this.rememberInput.checked;

    if (!username) {
      this.showError('Lütfen bir kullanıcı adı girin.');
      return;
    }

    if (password.length < 6) {
      this.showError('Şifre en az 6 karakter olmalıdır.');
      return;
    }

    this.hideError();
    this.submitBtnText.textContent = 'Lütfen bekleyin...';

    try {
      if (this.mode === 'login') {
        await AuthService.login(username, password, rememberMe);
      } else {
        await AuthService.register(username, password, rememberMe);
      }
      this.close();
    } catch (err) {
      this.showError(err.message);
    } finally {
      this.submitBtnText.textContent = this.mode === 'login' ? 'Giriş Yap' : 'Kaydol ve Başla';
    }
  }

  open(mode = 'login') {
    this.mode = mode;
    this.updateModeUI();
    this.usernameInput.value = '';
    this.passwordInput.value = '';
    this.hideError();
    this.backdrop.classList.add('active');
    setTimeout(() => this.usernameInput.focus(), 150);
  }

  close() {
    this.backdrop.classList.remove('active');
  }
}
