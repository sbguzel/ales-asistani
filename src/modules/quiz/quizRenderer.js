import katex from 'katex';
import 'katex/dist/katex.min.css';

export class QuizRenderer {
  /**
   * Metin içindeki LaTeX formüllerini ($...$ ve $$...$$) KaTeX HTML'ine dönüştürür
   */
  static renderLatex(text) {
    if (text === null || text === undefined) return '';
    if (typeof text === 'object') {
      text = text.content || text.text || text.value || '';
    }
    if (typeof text !== 'string') {
      text = String(text);
    }
    if (!text.trim()) return '';

    // 1. Blok formüller: $$...$$ (çok satırlı destek)
    let parsed = text.replace(/\$\$([\s\S]+?)\$\$/g, (match, formula) => {
      try {
        // KaTeX'in desteklemediği @{...} sütun hizalama belirteçlerini temizle
        const sanitized = formula.trim().replace(/@\{[^}]*\}/g, '');
        return katex.renderToString(sanitized, {
          displayMode: true,
          throwOnError: false
        });
      } catch (e) {
        return match;
      }
    });

    // 2. Satır içi formüller: $...$ (tek satırda çalışan, diğer $ karakterlerini ve paragrafları yutmayan)
    parsed = parsed.replace(/\$([^\$\n]+?)\$/g, (match, formula) => {
      try {
        const sanitized = formula.trim().replace(/@\{[^}]*\}/g, '');
        return katex.renderToString(sanitized, {
          displayMode: false,
          throwOnError: false
        });
      } catch (e) {
        return match;
      }
    });

    // 3. Kalın metin (Markdown Bold): **metin**
    parsed = parsed.replace(/\*\*([\s\S]+?)\*\*/g, '<strong>$1</strong>');

    // 4. Liste maddeleri: Satır başındaki "* " veya "- " işaretlerini zarif "• " maddelerine çevir
    parsed = parsed.replace(/^[ \t]*[*-][ \t]+/gm, '• ');

    // 5. İtalik metin (Markdown Italic): *metin*
    parsed = parsed.replace(/(^|[^*])\*([^* \n][^*]*?[^* \n])\*/g, '$1<em>$2</em>');

    // 6. Satır sonlarını HTML <br>'e çevir
    return parsed.replace(/\n/g, '<br>');
  }

  /**
   * Soru ve şıkları DOM'a basar
   */
  static renderQuestion(question, container, onOptionSelect) {
    if (!question || !container) return;

    const diffDots = [1, 2, 3, 4, 5].map(level => 
      `<span class="diff-dot ${level <= question.difficulty ? 'active' : ''}"></span>`
    ).join('');

    const sharedText = typeof question.sharedContext === 'object' && question.sharedContext !== null
      ? (question.sharedContext.content || question.sharedContext.text || '')
      : (question.sharedContext || '');

    const groupHeader = question.groupHeader || 
      (typeof question.sharedContext === 'object' && question.sharedContext ? question.sharedContext.title : null) || 
      'Ortak Bilgilendirme';

    const groupHtml = question.isGroupQuestion ? `
      <div class="group-context-card">
        <div class="group-header-banner">
          <div class="group-badge">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
            <span>Bağlantılı Soru Metni (${question.groupIndex || 1} / ${question.groupTotal || 1})</span>
          </div>
          <span class="group-title">${groupHeader}</span>
        </div>
        <div class="group-context-body">
          ${this.renderLatex(sharedText)}
        </div>
      </div>
    ` : '';

    let imageHtml = '';
    if (question.hasImage) {
      if (question.svgContent) {
        imageHtml = `<div class="question-image-container">${question.svgContent}</div>`;
      } else if (question.imageUrl) {
        imageHtml = `<div class="question-image-container">
          <img src="${question.imageUrl}" alt="Soru ${question.number || ''}" class="question-image" />
        </div>`;
      }
    }

    const textHtml = question.questionText && question.questionText.trim()
      ? `<div class="question-text">${this.renderLatex(question.questionText)}</div>`
      : '';

    const optionsList = Array.isArray(question.options) ? question.options : [];
    const optionsHtml = optionsList.map(opt => `
      <button class="option-btn" data-key="${opt.key}">
        <div class="option-key">${opt.key}</div>
        <div class="option-text">${this.renderLatex(opt.text)}</div>
      </button>
    `).join('');

    container.innerHTML = `
      <div class="question-content-active">
        ${groupHtml}

        <div class="question-header-meta">
          <span class="question-tag">${question.topicTitle || question.subject}</span>
          <div class="question-difficulty" title="Zorluk Derecesi: ${question.difficulty}/5">
            ${diffDots}
          </div>
        </div>

        ${imageHtml}
        ${textHtml}

        <div class="options-list">
          ${optionsHtml}
        </div>

        <div class="solution-card" id="solution-card">
          <div class="solution-header">
            <span>✓ Doğru Çözüm & ALES Analizi</span>
          </div>
          <div class="quick-tip-banner">
            ${this.renderLatex(question.quickTip || '💡 ALES Taktiği: Sorularda önce şıkların büyüklük dağılımını gözlemleyin.')}
          </div>
          <div class="solution-body">
            ${this.renderLatex(question.suggestedSolution || 'Detaylı çözüm hazırlanıyor.')}
          </div>
          <button class="next-question-btn" id="next-question-btn">
            Sonraki Soruya Geç ➔
          </button>
        </div>
      </div>
    `;

    // Şık butonlarına tıklama event'ini bağla
    const optionBtns = container.querySelectorAll('.option-btn');
    optionBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const key = btn.getAttribute('data-key');
        onOptionSelect(key, btn);
      });
    });
  }

  /**
   * Soru öncesi "Başla" kartını DOM'a basar.
   * Kullanıcı butona basana kadar soru metni ve şıklar gizlidir, süre başlamaz.
   */
  static renderStartCard(question, container, onStart, meta = {}) {
    if (!question || !container) return;

    const diffDots = [1, 2, 3, 4, 5].map(level => 
      `<span class="diff-dot ${level <= (question.difficulty || 3) ? 'active' : ''}"></span>`
    ).join('');

    const targetSec = question.targetTimeSec || 75;
    const mins = Math.floor(targetSec / 60);
    const secs = targetSec % 60;
    const targetTimeFormatted = mins > 0 
      ? (secs > 0 ? `${mins} dk ${secs} sn` : `${mins} dk`) 
      : `${secs} sn`;

    const topicName = question.topicTitle || (
      question.subject === 'matematik' ? 'Matematik' :
      question.subject === 'turkce' ? 'Türkçe' :
      question.subject === 'mantik' ? 'Mantık' : 'ALES'
    );

    const questionNum = (meta.currentIndex !== undefined && meta.totalCount !== undefined)
      ? `Soru ${meta.currentIndex + 1} / ${meta.totalCount}`
      : `Soru ${question.number || ''}`;

    const groupBadge = question.isGroupQuestion
      ? `<span class="start-badge group">Bağlantılı Soru (${question.groupIndex || 1} / ${question.groupTotal || 1})</span>`
      : '';

    container.innerHTML = `
      <div class="question-start-screen">
        <div class="start-header-meta">
          <span class="question-tag">${topicName}</span>
          <span class="start-counter-badge">${questionNum}</span>
          ${groupBadge}
        </div>

        <div class="start-card">
          <div class="start-icon-pulse">
            <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
          </div>

          <h2 class="start-title">Soru Çözümüne Hazır mısınız?</h2>

          <p class="start-subtitle">
            Rahat bir mola verebilir veya karalama alanınızı hazırlayabilirsiniz.<br>
            <strong>Başla</strong> butonuna bastığınızda soru açılacak ve süreniz saymaya başlayacaktır.
          </p>

          <div class="start-info-grid">
            <div class="start-info-box">
              <span class="start-info-label">Hedef Çözüm Süresi</span>
              <span class="start-info-value">⏱️ ${targetTimeFormatted}</span>
            </div>
            <div class="start-info-box">
              <span class="start-info-label">Zorluk Seviyesi</span>
              <div class="question-difficulty" title="Zorluk Derecesi: ${question.difficulty || 3}/5">
                ${diffDots}
              </div>
            </div>
          </div>

          <button type="button" class="btn-start-question" id="btn-start-question">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <polygon points="6 4 20 12 6 20 6 4"></polygon>
            </svg>
            <span>Başla</span>
          </button>

          <div class="start-hint-text">
            <span>Klavyeden <strong>Boşluk (Space)</strong> veya <strong>Enter</strong> tuşuna basarak da başlatabilirsiniz</span>
          </div>
        </div>
      </div>
    `;

    const startBtn = container.querySelector('#btn-start-question');
    if (startBtn) {
      startBtn.addEventListener('click', (e) => {
        e.preventDefault();
        onStart();
      });
    }
  }
}
