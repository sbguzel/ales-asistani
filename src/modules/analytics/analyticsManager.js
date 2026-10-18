import { FirestoreService } from '../storage/firestoreService.js';

export class AnalyticsManager {
  constructor(app) {
    this.app = app;
  }

  /**
   * Çözüm denemelerini ve soru meta verilerini analiz eder
   */
  computeMetrics(attempts, allQuestions = []) {
    const qMap = new Map();
    allQuestions.forEach(q => qMap.set(q.id, q));

    const total = attempts.length;
    if (total === 0) {
      return {
        total: 0,
        correct: 0,
        wrong: 0,
        accuracy: 0,
        netScore: 0,
        totalTimeSec: 0,
        avgTimeSec: 0,
        avgTargetSec: 75,
        timeDiffSec: 0,
        canvasRate: 0,
        matrix: { fastCorrect: [], slowCorrect: [], fastWrong: [], slowWrong: [] },
        subjectStats: {},
        recommendations: [],
        enrichedAttempts: []
      };
    }

    let correctCount = 0;
    let wrongCount = 0;
    let totalTimeSec = 0;
    let totalTargetSec = 0;
    let canvasCount = 0;

    const matrix = {
      fastCorrect: [],
      slowCorrect: [],
      fastWrong: [],
      slowWrong: []
    };

    const subjectStats = {
      matematik: { total: 0, correct: 0, timeSec: 0, targetSec: 0, title: 'Matematik' },
      geometri: { total: 0, correct: 0, timeSec: 0, targetSec: 0, title: 'Geometri' },
      mantik: { total: 0, correct: 0, timeSec: 0, targetSec: 0, title: 'Sözel Mantık' },
      turkce: { total: 0, correct: 0, timeSec: 0, targetSec: 0, title: 'Türkçe' }
    };

    const enrichedAttempts = attempts.map(att => {
      const q = qMap.get(att.questionId) || {};
      const targetSec = att.targetTimeSec || q.targetTimeSec || 75;
      const timeSpent = Math.round(att.timeSpentSeconds || 0);
      const isFast = timeSpent <= targetSec;
      const isCorrect = !!att.isCorrect;

      if (isCorrect) correctCount++;
      else wrongCount++;

      totalTimeSec += timeSpent;
      totalTargetSec += targetSec;
      if (att.usedCanvas) canvasCount++;

      // Hız - Doğruluk Matrisi
      if (isCorrect && isFast) matrix.fastCorrect.push(att);
      else if (isCorrect && !isFast) matrix.slowCorrect.push(att);
      else if (!isCorrect && isFast) matrix.fastWrong.push(att);
      else matrix.slowWrong.push(att);

      // Branş ayrıştırması (Geometri ayrımı dahil)
      let subjKey = q.subject || 'matematik';
      if (q.category && q.category.startsWith('geometri_')) {
        subjKey = 'geometri';
      }
      if (!subjectStats[subjKey]) {
        subjectStats[subjKey] = { total: 0, correct: 0, timeSec: 0, targetSec: 0, title: subjKey };
      }
      subjectStats[subjKey].total++;
      if (isCorrect) subjectStats[subjKey].correct++;
      subjectStats[subjKey].timeSec += timeSpent;
      subjectStats[subjKey].targetSec += targetSec;

      return {
        ...att,
        questionTitle: q.topicTitle || att.questionId,
        subject: subjKey,
        targetSec,
        timeSpent,
        timeDiff: targetSec - timeSpent // pozitif ise süreden kazanç
      };
    });

    const accuracy = Math.round((correctCount / total) * 100);
    const netScore = Math.max(0, parseFloat((correctCount - (wrongCount / 4)).toFixed(2)));
    const avgTimeSec = Math.round(totalTimeSec / total);
    const avgTargetSec = Math.round(totalTargetSec / total) || 75;
    const timeDiffSec = avgTargetSec - avgTimeSec;
    const canvasRate = Math.round((canvasCount / total) * 100);

    // Branş yüzdelerini ve süre ortalamalarını hesapla
    Object.keys(subjectStats).forEach(key => {
      const s = subjectStats[key];
      s.accuracy = s.total > 0 ? Math.round((s.correct / s.total) * 100) : 0;
      s.avgTime = s.total > 0 ? Math.round(s.timeSec / s.total) : 0;
      s.avgTarget = s.total > 0 ? Math.round(s.targetSec / s.total) : 75;
    });

    // Dinamik ALES Taktiksel Tavsiyeleri
    const recommendations = [];
    if (timeDiffSec >= 15 && accuracy >= 75) {
      recommendations.push({
        type: 'success',
        icon: '⚡️',
        title: 'Harika Tempo ve İsabet',
        desc: `Soruları hedef sürenin ortalama ${timeDiffSec} saniye altında ve %${accuracy} doğrulukla çözüyorsunuz. Bu hız sınavda size yaklaşık 15-20 dakika ekstra turlama süresi kazandırır.`
      });
    } else if (timeDiffSec < 0) {
      recommendations.push({
        type: 'warning',
        icon: '⏱️',
        title: 'Süre Aşımı Uyarısı',
        desc: `Ortalama çözüm süreniz (${avgTimeSec} sn) ALES standart hedefinin (${avgTargetSec} sn) üzerinde. Çözüm yöntemlerinde pratik formülleri ve şıklardan gitme taktiklerini tercih edin.`
      });
    }

    if (matrix.slowWrong.length > 0) {
      recommendations.push({
        type: 'danger',
        icon: '⚠️',
        title: 'Zaman Tuzaklarına Dikkat',
        desc: `${matrix.slowWrong.length} soruda hem süre aşılmış hem yanlış yapılmış. ALES stratejisi: 60 saniyeyi geçen ve sonuca ulaştırmayan sorularda inatlaşmayıp işaret koyarak hemen bir sonraki soruya geçin (Turlama Tekniği).`
      });
    }

    if (matrix.fastWrong.length > 0) {
      recommendations.push({
        type: 'info',
        icon: '🎯',
        title: 'Dikkatsizlik Kontrolü',
        desc: `${matrix.fastWrong.length} soru çok hızlı çözülmesine rağmen yanlış yapılmış. İşaretleme yapmadan önce soru kökündeki 'olamaz / kesinlikle / asal' gibi anahtar ifadelere 3 saniye ayırın.`
      });
    }

    if (subjectStats.mantik && subjectStats.mantik.total > 0) {
      recommendations.push({
        type: 'neutral',
        icon: '🧩',
        title: 'Sözel Mantık Stratejisi',
        desc: `Sözel mantıkta ilk soruda kurulan tablo kalan 3 soruya hız kazandırır. Çizim alanını aktif kullanarak tablo kurma temponuzu koruyun.`
      });
    }

    return {
      total,
      correct: correctCount,
      wrong: wrongCount,
      accuracy,
      netScore,
      totalTimeSec,
      avgTimeSec,
      avgTargetSec,
      timeDiffSec,
      canvasRate,
      matrix,
      subjectStats,
      recommendations,
      enrichedAttempts: enrichedAttempts.reverse() // En son çözülenler üstte
    };
  }

  /**
   * Analiz Dashboard'unu DOM'a basar
   */
  render(container) {
    if (!container) return;

    const attempts = FirestoreService.getAttempts();
    const metrics = this.computeMetrics(attempts, this.app.allQuestions || []);

    const hasData = metrics.total > 0;

    container.innerHTML = `
      <div class="analytics-container">
        <!-- Dashboard Üst Başlık & Eylem Butonları -->
        <div class="analytics-header">
          <div>
            <div class="analytics-title-group">
              <h2 class="analytics-title">Performans & Hız Analizi</h2>
              <span class="analytics-badge">${hasData ? `${metrics.total} Soru İncelendi` : 'Henüz Veri Yok'}</span>
            </div>
            <p class="analytics-subtitle">ALES Sayısal & Sözel Testleri Süre Yönetimi, Doğruluk ve Net Gelişimi</p>
          </div>

          <div class="analytics-actions">
            <button class="btn-secondary" id="btn-seed-sample" title="Zengin analizi önizlemek için örnek simülasyon verisi yükler">
              <span>🧪 ${hasData ? 'Örnek Verileri Güncelle' : 'Örnek Veri Yükle'}</span>
            </button>
            ${hasData ? `
              <button class="btn-text-danger" id="btn-clear-stats" title="Tüm çözüm geçmişini sıfırlar">
                <span>🗑️ Sıfırla</span>
              </button>
            ` : ''}
            <button class="btn-primary" id="btn-return-quiz">
              <span>✍️ Soru Çözümüne Dön</span>
            </button>
          </div>
        </div>

        ${!hasData ? this.renderEmptyState() : this.renderDashboardContent(metrics)}
      </div>
    `;

    this.attachEventListeners(container);
  }

  renderEmptyState() {
    return `
      <div class="analytics-empty-state">
        <div class="empty-icon-pulse">📊</div>
        <h3>Henüz Çözülmüş Soru Bulunmuyor</h3>
        <p>Soruları çözdükçe soru başına harcadığınız süreler, hedef süre karşılaştırmaları, hız-isabet matrisi ve ALES net tahmininiz burada anlık olarak analiz edilecek.</p>
        <div class="empty-cta-group">
          <button class="btn-primary" id="btn-empty-seed">
            <span>🧪 Örnek Simülasyon Verisi Yükle (Önizle)</span>
          </button>
          <button class="btn-secondary" id="btn-empty-start">
            <span>✍️ İlk Soruyu Çözmeye Başla</span>
          </button>
        </div>
      </div>
    `;
  }

  renderDashboardContent(metrics) {
    const timeStatusClass = metrics.timeDiffSec >= 0 ? 'text-success' : 'text-danger';
    const timeStatusSign = metrics.timeDiffSec >= 0 ? '-' : '+';
    const timeStatusAbs = Math.abs(metrics.timeDiffSec);

    return `
      <!-- 1. KPI ÖZET KARTLARI (HERO METRICS) -->
      <div class="analytics-kpi-grid">
        <!-- Kart 1: Net Skor -->
        <div class="kpi-card">
          <div class="kpi-card-header">
            <span class="kpi-label">ALES Net Tahmini</span>
            <span class="kpi-icon-badge">🎯</span>
          </div>
          <div class="kpi-value-row">
            <span class="kpi-value text-accent">${metrics.netScore}</span>
            <span class="kpi-subtext">/ ${metrics.total} Soru</span>
          </div>
          <div class="kpi-footer">
            <span class="kpi-tag tag-success">Doğru: ${metrics.correct}</span>
            <span class="kpi-tag tag-danger">Yanlış: ${metrics.wrong}</span>
          </div>
        </div>

        <!-- Kart 2: Doğruluk Oranı -->
        <div class="kpi-card">
          <div class="kpi-card-header">
            <span class="kpi-label">Başarı & İsabet</span>
            <span class="kpi-icon-badge">📈</span>
          </div>
          <div class="kpi-value-row">
            <span class="kpi-value text-success">%${metrics.accuracy}</span>
            <div class="mini-progress-track">
              <div class="mini-progress-fill" style="width: ${metrics.accuracy}%"></div>
            </div>
          </div>
          <div class="kpi-footer">
            <span class="kpi-hint">${metrics.accuracy >= 70 ? '🟢 İdeal Sınav Seviyesi' : '🟠 Geliştirilmeli'}</span>
          </div>
        </div>

        <!-- Kart 3: Ortalama Süre -->
        <div class="kpi-card">
          <div class="kpi-card-header">
            <span class="kpi-label">Ort. Çözüm Süresi</span>
            <span class="kpi-icon-badge">⏱️</span>
          </div>
          <div class="kpi-value-row">
            <span class="kpi-value">${metrics.avgTimeSec} <small>sn</small></span>
            <span class="kpi-trend ${timeStatusClass}">
              ${metrics.timeDiffSec >= 0 ? '⚡️' : '⚠️'} ${timeStatusSign}${timeStatusAbs} sn
            </span>
          </div>
          <div class="kpi-footer">
            <span class="kpi-hint">Hedef Süre: ${metrics.avgTargetSec} sn / soru</span>
          </div>
        </div>

        <!-- Kart 4: Karalama Tahtası Kullanımı -->
        <div class="kpi-card">
          <div class="kpi-card-header">
            <span class="kpi-label">Tahta / Çizim Kullanımı</span>
            <span class="kpi-icon-badge">✏️</span>
          </div>
          <div class="kpi-value-row">
            <span class="kpi-value text-secondary">%${metrics.canvasRate}</span>
            <span class="kpi-subtext">${metrics.total} sorunun ${Math.round(metrics.total * metrics.canvasRate / 100)}'inde</span>
          </div>
          <div class="kpi-footer">
            <span class="kpi-hint">Sayısal & Mantık sorularında aktif</span>
          </div>
        </div>
      </div>

      <!-- 2. İKİ SÜTUNLU DERİNLEMESİNE ANALİZ (ZAMAN MATRİSİ & BRANŞLAR) -->
      <div class="analytics-split-grid">
        <!-- Sol: Zaman Yönetimi & Hız Matrisi -->
        <div class="analytics-card">
          <div class="card-header-clean">
            <div>
              <h3 class="card-title">Zaman Yönetimi & Hız Matrisi</h3>
              <p class="card-desc">Soruların süre ve doğruluk dağılımı (ALES taktiksel matrisi)</p>
            </div>
            <span class="card-badge-dot">4 Çeyrek</span>
          </div>

          <div class="matrix-grid">
            <div class="matrix-cell matrix-fast-correct">
              <div class="matrix-cell-header">
                <span class="matrix-title">🟢 Hızlı & Doğru</span>
                <span class="matrix-count">${metrics.matrix.fastCorrect.length} Soru</span>
              </div>
              <p class="matrix-desc">Hedef sürenin altında doğru çözüldü (İdeal ALES avantajı).</p>
            </div>

            <div class="matrix-cell matrix-slow-correct">
              <div class="matrix-cell-header">
                <span class="matrix-title">🟡 Zaman Alan Doğrular</span>
                <span class="matrix-count">${metrics.matrix.slowCorrect.length} Soru</span>
              </div>
              <p class="matrix-desc">Doğru yapıldı ancak hedef süreyi aştı (Hız pratiği gerekir).</p>
            </div>

            <div class="matrix-cell matrix-fast-wrong">
              <div class="matrix-cell-header">
                <span class="matrix-title">🟠 Acele Edilmiş Yanlışlar</span>
                <span class="matrix-count">${metrics.matrix.fastWrong.length} Soru</span>
              </div>
              <p class="matrix-desc">Hızlı çözüldü fakat yanlış yapıldı (Dikkatsizlik riski).</p>
            </div>

            <div class="matrix-cell matrix-slow-wrong">
              <div class="matrix-cell-header">
                <span class="matrix-title">🔴 Zaman Kaybettiren Yanlışlar</span>
                <span class="matrix-count">${metrics.matrix.slowWrong.length} Soru</span>
              </div>
              <p class="matrix-desc">Hem vakit kaybettirdi hem yanlış yapıldı (Turlama stratejisi).</p>
            </div>
          </div>

          <!-- Süre Karşılaştırma Çubuk Grafiği (Son Sorular) -->
          <div class="timeline-chart-section">
            <div class="chart-header">
              <span class="chart-label">Son Çözülen Soruların Süre Grafiği (sn)</span>
              <span class="chart-benchmark-legend"><span class="legend-line"></span> Hedef Süre (75 sn)</span>
            </div>
            <div class="chart-bars-container">
              ${this.renderTimelineBars(metrics.enrichedAttempts.slice(0, 14))}
            </div>
          </div>
        </div>

        <!-- Sağ: Ders Bazlı Başarı & Taktiksel Tavsiyeler -->
        <div class="analytics-card">
          <div class="card-header-clean">
            <div>
              <h3 class="card-title">Ders ve Konu Dağılımı</h3>
              <p class="card-desc">Alanlara göre doğruluk ve harcanan ortalama süre</p>
            </div>
          </div>

          <div class="subject-breakdown-list">
            ${this.renderSubjectBars(metrics.subjectStats)}
          </div>

          <!-- ALES Taktiksel Tavsiye Alanı -->
          <div class="recommendations-container">
            <h4 class="rec-header">💡 Size Özel ALES Taktikleri</h4>
            <div class="rec-list">
              ${metrics.recommendations.map(r => `
                <div class="rec-card rec-${r.type}">
                  <span class="rec-icon">${r.icon}</span>
                  <div class="rec-content">
                    <span class="rec-title">${r.title}</span>
                    <p class="rec-desc">${r.desc}</p>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        </div>
      </div>

      <!-- 3. DETAYLI ÇÖZÜM GEÇMİŞİ TABLOSU -->
      <div class="analytics-card full-width">
        <div class="card-header-clean">
          <div>
            <h3 class="card-title">Son Çözüm Denemeleri</h3>
            <p class="card-desc">Soru bazında süre analizi ve sonuç dökümü</p>
          </div>
        </div>

        <div class="history-table-wrapper">
          <table class="history-table">
            <thead>
              <tr>
                <th>Soru Konusu</th>
                <th>Ders</th>
                <th>Sonuç</th>
                <th>Harcanan Süre</th>
                <th>Hedef Süre</th>
                <th>Süre Farkı</th>
                <th>Çizim Tahtası</th>
              </tr>
            </thead>
            <tbody>
              ${metrics.enrichedAttempts.slice(0, 15).map(att => `
                <tr>
                  <td class="font-medium">${att.questionTitle}</td>
                  <td><span class="table-subject-tag ${att.subject}">${att.subject}</span></td>
                  <td>
                    ${att.isCorrect 
                      ? '<span class="status-badge success">✓ Doğru</span>' 
                      : '<span class="status-badge danger">✗ Yanlış</span>'}
                  </td>
                  <td class="font-mono">${att.timeSpent} sn</td>
                  <td class="font-mono text-muted">${att.targetSec} sn</td>
                  <td>
                    <span class="time-diff-badge ${att.timeDiff >= 0 ? 'faster' : 'slower'}">
                      ${att.timeDiff >= 0 ? `-${att.timeDiff} sn (Hızlı)` : `+${Math.abs(att.timeDiff)} sn (Yavaş)`}
                    </span>
                  </td>
                  <td>${att.usedCanvas ? '✏️ Kullanıldı' : '<span class="text-muted">—</span>'}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  }

  renderTimelineBars(attempts) {
    if (!attempts || attempts.length === 0) return '<p class="text-muted">Grafik için soru verisi yok.</p>';

    // Çubukları tersine çevirerek kronolojik (soldan sağa) göster
    const items = [...attempts].reverse();
    const maxTime = Math.max(120, ...items.map(i => i.timeSpent));

    return items.map((item, idx) => {
      const heightPercent = Math.min(100, Math.round((item.timeSpent / maxTime) * 100));
      const targetHeightPercent = Math.round((item.targetSec / maxTime) * 100);
      const isFast = item.timeSpent <= item.targetSec;
      
      let barClass = 'bar-correct-fast';
      if (!item.isCorrect) barClass = 'bar-wrong';
      else if (!isFast) barClass = 'bar-correct-slow';

      return `
        <div class="timeline-bar-column" title="Soru: ${item.questionTitle}&#10;Süre: ${item.timeSpent} sn (Hedef: ${item.targetSec} sn)&#10;Sonuç: ${item.isCorrect ? 'Doğru' : 'Yanlış'}">
          <div class="timeline-bar-track">
            <div class="timeline-target-line" style="bottom: ${targetHeightPercent}%"></div>
            <div class="timeline-bar-fill ${barClass}" style="height: ${heightPercent}%"></div>
          </div>
          <span class="timeline-bar-label">S${idx + 1}</span>
        </div>
      `;
    }).join('');
  }

  renderSubjectBars(subjectStats) {
    const list = Object.values(subjectStats).filter(s => s.total > 0);
    if (list.length === 0) return '<p class="text-muted">Henüz ders bazlı veri oluşmadı.</p>';

    return list.map(s => `
      <div class="subject-stat-row">
        <div class="subject-stat-header">
          <span class="subject-stat-title">${s.title}</span>
          <span class="subject-stat-counts">${s.correct}/${s.total} Doğru • %${s.accuracy}</span>
        </div>
        <div class="subject-progress-track">
          <div class="subject-progress-fill" style="width: ${s.accuracy}%"></div>
        </div>
        <div class="subject-stat-footer">
          <span>Ort. Süre: <strong>${s.avgTime} sn</strong></span>
          <span class="text-muted">Hedef: ${s.avgTarget} sn</span>
        </div>
      </div>
    `).join('');
  }

  attachEventListeners(container) {
    // Soru çözümüne dön butonları
    const returnBtns = container.querySelectorAll('#btn-return-quiz, #btn-empty-start');
    returnBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        this.app.switchMode('all');
      });
    });

    // Örnek simülasyon verisi yükle butonları
    const seedBtns = container.querySelectorAll('#btn-seed-sample, #btn-empty-seed');
    seedBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        FirestoreService.seedSampleAttempts(this.app.allQuestions || []);
        this.render(container);
      });
    });

    // Sıfırla butonu
    const clearBtn = container.querySelector('#btn-clear-stats');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        if (confirm('Tüm soru çözüm geçmişiniz sıfırlanacak. Emin misiniz?')) {
          FirestoreService.clearAttempts();
          this.render(container);
        }
      });
    }
  }
}
