import { FirestoreService } from '../../modules/storage/firestoreService.js';
import { state } from '../../core/state.js';
import { eventBus } from '../../core/eventBus.js';

export class SettingsModal {
  constructor(app) {
    this.app = app;
    this.createDom();
    this.bindEvents();
  }

  createDom() {
    const backdrop = document.createElement('div');
    backdrop.className = 'modal-backdrop';
    backdrop.id = 'settings-modal-backdrop';

    backdrop.innerHTML = `
      <div class="settings-modal" role="dialog" aria-modal="true">
        <button class="modal-close-btn" id="settings-close-btn" aria-label="Kapat">&times;</button>
        
        <div class="settings-header">
          <div class="settings-logo">⚙️</div>
          <h2 class="settings-title">Ayarlar & Soru Akışı</h2>
          <p class="settings-subtitle">Soru sıralaması, gizleme filtreleri ve hesap ilerlemeniz</p>
        </div>

        <div class="settings-account-card" id="settings-account-card">
          <!-- Dinamik doldurulur -->
        </div>

        <div class="settings-section">
          <div class="settings-section-title">Soru Akışı Tercihleri</div>
          
          <!-- Soru Sıralaması -->
          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-label">Soru Sıralaması</span>
              <span class="setting-desc">Soruları rastgele karıştırarak veya sınav sırasına göre çözün.</span>
            </div>
            <div class="segmented-control" id="order-mode-selector">
              <button type="button" class="segment-btn active" data-order="random">
                <span>🔀 Rastgele</span>
              </button>
              <button type="button" class="segment-btn" data-order="sequential">
                <span>🔢 Sıralı</span>
              </button>
            </div>
          </div>

          <!-- Çözülen Soruları Gizle -->
          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-label">Çözülen Soruları Bir Daha Getirme</span>
              <span class="setting-desc">Cevapladığınız sorular havuzdan çıkarılır, sadece kalan sorular gelir.</span>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" id="toggle-hide-solved" checked />
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>

        <div class="settings-section">
          <div class="settings-section-title">İlerleme & Hafıza</div>
          
          <div class="progress-box">
            <div class="progress-box-header">
              <span class="progress-box-label">Soru Havuzu Durumu</span>
              <span class="progress-box-numbers" id="settings-progress-text">0 / 300 (%0)</span>
            </div>
            <div class="progress-bar-track">
              <div class="progress-bar-fill" id="settings-progress-fill" style="width: 0%;"></div>
            </div>
            <div class="progress-box-sub">
              <span id="settings-solved-count">Çözülen: 0</span>
              <span id="settings-remaining-count">Kalan: 300</span>
            </div>
          </div>

          <div class="reset-box">
            <div class="reset-desc">
              Çözülen soru geçmişinizi sıfırlayarak tüm soruları yeniden havuzunuza dahil edebilirsiniz.
            </div>
            
            <div id="reset-initial-view">
              <button type="button" class="reset-solved-btn" id="reset-solved-btn">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
                  <path d="M3 3v5h5"/>
                </svg>
                <span>Çözülen Soruları Sıfırla</span>
              </button>
            </div>

            <div id="reset-confirm-view" style="display: none; flex-direction: column; gap: 8px;">
              <div style="font-size: 12px; font-weight: 600; color: #ef4444; text-align: center;">
                Tüm çözülen sorular sıfırlanacak. Emin misiniz?
              </div>
              <div style="display: flex; gap: 8px; justify-content: center;">
                <button type="button" class="btn-confirm-yes" id="btn-confirm-reset-yes">
                  Evet, Sıfırla
                </button>
                <button type="button" class="btn-confirm-cancel" id="btn-confirm-reset-cancel">
                  Vazgeç
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="settings-footer-info" id="settings-footer-info">
          🔒 Tercihleriniz ve çözülen sorularınız hesabınıza özel olarak bulutta güvenle saklanır.
        </div>
      </div>
    `;

    document.body.appendChild(backdrop);
    this.backdrop = backdrop;
    this.closeBtn = backdrop.querySelector('#settings-close-btn');
    this.accountCard = backdrop.querySelector('#settings-account-card');
    this.orderSelector = backdrop.querySelector('#order-mode-selector');
    this.hideSolvedToggle = backdrop.querySelector('#toggle-hide-solved');
    this.progressText = backdrop.querySelector('#settings-progress-text');
    this.progressFill = backdrop.querySelector('#settings-progress-fill');
    this.solvedCountEl = backdrop.querySelector('#settings-solved-count');
    this.remainingCountEl = backdrop.querySelector('#settings-remaining-count');
    this.resetInitialView = backdrop.querySelector('#reset-initial-view');
    this.resetConfirmView = backdrop.querySelector('#reset-confirm-view');
    this.resetBtn = backdrop.querySelector('#reset-solved-btn');
    this.confirmResetYesBtn = backdrop.querySelector('#btn-confirm-reset-yes');
    this.confirmResetCancelBtn = backdrop.querySelector('#btn-confirm-reset-cancel');
  }

  bindEvents() {
    this.closeBtn.addEventListener('click', () => this.close());
    this.backdrop.addEventListener('click', (e) => {
      if (e.target === this.backdrop) this.close();
    });

    // Soru Sıralaması Segmentleri
    const segmentBtns = this.orderSelector.querySelectorAll('.segment-btn');
    segmentBtns.forEach(btn => {
      btn.addEventListener('click', async () => {
        const order = btn.getAttribute('data-order');
        segmentBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const isRandom = order === 'random';
        await this.app.updateSettings({ randomOrder: isRandom });
      });
    });

    // Çözülen Soruları Gizle Toggle
    this.hideSolvedToggle.addEventListener('change', async (e) => {
      const hideSolved = e.target.checked;
      await this.app.updateSettings({ hideSolved });
    });

    // Çözülen Soruları Sıfırla - Onay Arayüzünü Aç
    this.resetBtn.addEventListener('click', () => {
      this.resetInitialView.style.display = 'none';
      this.resetConfirmView.style.display = 'flex';
    });

    // Vazgeç
    this.confirmResetCancelBtn.addEventListener('click', () => {
      this.resetConfirmView.style.display = 'none';
      this.resetInitialView.style.display = 'block';
    });

    // Onayla ve Sıfırla
    this.confirmResetYesBtn.addEventListener('click', async () => {
      this.confirmResetYesBtn.disabled = true;
      this.confirmResetYesBtn.textContent = 'Sıfırlanıyor...';

      try {
        await this.app.resetSolvedQuestions();
        this.refreshUI();
        this.resetConfirmView.innerHTML = `
          <div style="font-size: 12px; font-weight: 600; color: #10b981; text-align: center; padding: 4px 0;">
            ✅ Çözülen sorular sıfırlandı!
          </div>
        `;
        setTimeout(() => {
          this.resetConfirmView.style.display = 'none';
          this.resetConfirmView.innerHTML = `
            <div style="font-size: 12px; font-weight: 600; color: #ef4444; text-align: center;">
              Tüm çözülen sorular sıfırlanacak. Emin misiniz?
            </div>
            <div style="display: flex; gap: 8px; justify-content: center;">
              <button type="button" class="btn-confirm-yes" id="btn-confirm-reset-yes">Evet, Sıfırla</button>
              <button type="button" class="btn-confirm-cancel" id="btn-confirm-reset-cancel">Vazgeç</button>
            </div>
          `;
          this.resetInitialView.style.display = 'block';
          // Re-bind confirm buttons
          this.bindResetConfirmEvents();
        }, 1500);
      } catch (err) {
        console.error('Reset error:', err);
        this.resetConfirmView.style.display = 'none';
        this.resetInitialView.style.display = 'block';
      }
    });
  }

  bindResetConfirmEvents() {
    const yesBtn = this.backdrop.querySelector('#btn-confirm-reset-yes');
    const cancelBtn = this.backdrop.querySelector('#btn-confirm-reset-cancel');
    if (cancelBtn) {
      cancelBtn.addEventListener('click', () => {
        this.resetConfirmView.style.display = 'none';
        this.resetInitialView.style.display = 'block';
      });
    }
    if (yesBtn) {
      yesBtn.addEventListener('click', async () => {
        yesBtn.disabled = true;
        yesBtn.textContent = 'Sıfırlanıyor...';
        await this.app.resetSolvedQuestions();
        this.refreshUI();
        this.resetConfirmView.style.display = 'none';
        this.resetInitialView.style.display = 'block';
      });
    }
  }

  refreshUI() {
    const user = state.get().user;
    const settings = this.app.settings || { randomOrder: true, hideSolved: true };
    const solvedIds = this.app.solvedQuestionIds || new Set();
    const totalCount = this.app.allQuestions ? this.app.allQuestions.length : 300;
    const solvedCount = solvedIds.size;
    const remainingCount = Math.max(0, totalCount - solvedCount);
    const percent = totalCount > 0 ? Math.round((solvedCount / totalCount) * 100) : 0;

    // 1. Hesap Bilgisi
    if (user) {
      this.accountCard.innerHTML = `
        <div class="account-card-left">
          <div class="account-avatar">${user.username.charAt(0).toUpperCase()}</div>
          <div class="account-details">
            <span class="account-name">@${user.username}</span>
            <span class="account-sync-badge cloud">
              <span class="sync-dot"></span> Bulut Senkronizasyonu Aktif
            </span>
          </div>
        </div>
      `;
    } else {
      this.accountCard.innerHTML = `
        <div class="account-card-left">
          <div class="account-avatar guest">?</div>
          <div class="account-details">
            <span class="account-name">Misafir Kullanıcı</span>
            <span class="account-sync-badge local">
              <span class="sync-dot local"></span> Yalnızca Bu Cihazda
            </span>
          </div>
        </div>
        <button type="button" class="account-login-link" id="settings-login-btn">Giriş Yap</button>
      `;

      const loginBtn = this.accountCard.querySelector('#settings-login-btn');
      if (loginBtn) {
        loginBtn.addEventListener('click', () => {
          this.close();
          if (this.app.authModal) {
            this.app.authModal.open('login');
          }
        });
      }
    }

    // 2. Segment Kontrolü (Random / Sequential)
    const segmentBtns = this.orderSelector.querySelectorAll('.segment-btn');
    segmentBtns.forEach(btn => {
      const mode = btn.getAttribute('data-order');
      if ((mode === 'random' && settings.randomOrder) || (mode === 'sequential' && !settings.randomOrder)) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    // 3. Toggle
    this.hideSolvedToggle.checked = !!settings.hideSolved;

    // 4. İlerleme Çubuğu ve Sayılar
    this.progressText.textContent = `${solvedCount} / ${totalCount} (%${percent})`;
    this.progressFill.style.width = `${percent}%`;
    this.solvedCountEl.textContent = `Çözülen: ${solvedCount}`;
    this.remainingCountEl.textContent = `Kalan: ${remainingCount}`;
  }

  open() {
    this.refreshUI();
    this.backdrop.classList.add('active');
  }

  close() {
    this.backdrop.classList.remove('active');
  }
}
