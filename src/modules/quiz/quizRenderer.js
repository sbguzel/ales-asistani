import katex from 'katex';
import 'katex/dist/katex.min.css';

export class QuizRenderer {
  /**
   * Metin içindeki LaTeX formüllerini ($...$ ve $$...$$) KaTeX HTML'ine dönüştürür
   */
  static renderLatex(text) {
    if (!text) return '';

    // 1. Blok formüller: $$...$$ (çok satırlı destek)
    let parsed = text.replace(/\$\$(.+?)\$\$/gs, (match, formula) => {
      try {
        return katex.renderToString(formula.trim(), {
          displayMode: true,
          throwOnError: false
        });
      } catch (e) {
        return match;
      }
    });

    // 2. Satır içi formüller: $...$ (çok satırlı destek)
    parsed = parsed.replace(/\$(.+?)\$/gs, (match, formula) => {
      try {
        return katex.renderToString(formula.trim(), {
          displayMode: false,
          throwOnError: false
        });
      } catch (e) {
        return match;
      }
    });

    // Satır sonlarını HTML <br>'e çevir
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

    const optionsHtml = question.options.map(opt => `
      <button class="option-btn" data-key="${opt.key}">
        <div class="option-key">${opt.key}</div>
        <div class="option-text">${this.renderLatex(opt.text)}</div>
      </button>
    `).join('');

    container.innerHTML = `
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
}
