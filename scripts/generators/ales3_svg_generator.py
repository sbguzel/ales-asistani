#!/usr/bin/env python3
"""
scripts/generators/ales3_svg_generator.py
2021-ALES/3 sınavındaki tüm şekil, diyagram ve geometri soruları için
yüksek çözünürlüklü, saf vektörel ve tema uyumlu SVG çizimleri üretir.
"""

from pathlib import Path
import math

SVG_DIR = Path("public/assets/questions/svg")
SVG_DIR.mkdir(parents=True, exist_ok=True)

COMMON_STYLE = """
    <style>
      .geo-line { stroke: var(--text-primary, #f1f5f9); stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .geo-sec { stroke: var(--accent-primary, #38bdf8); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .geo-accent { stroke: var(--zen-warning, #f59e0b); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .geo-shaded { fill: var(--geo-shaded-fill, rgba(56, 189, 248, 0.28)); stroke: var(--geo-shaded-stroke, var(--accent-primary, #38bdf8)); stroke-width: 2; stroke-linejoin: round; }
      .geo-shaded-yellow { fill: rgba(245, 158, 11, 0.35); stroke: #f59e0b; stroke-width: 2; stroke-linejoin: round; }
      .geo-shaded-red { fill: rgba(244, 63, 94, 0.35); stroke: #f43f5e; stroke-width: 2; stroke-linejoin: round; }
      .geo-shaded-blue { fill: rgba(56, 189, 248, 0.35); stroke: #38bdf8; stroke-width: 2; stroke-linejoin: round; }
      .geo-text { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif; font-size: 14px; font-weight: 600; fill: var(--text-primary, #f1f5f9); text-anchor: middle; dominant-baseline: central; }
      .geo-text-muted { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif; font-size: 12px; font-weight: 500; fill: var(--text-secondary, #94a3b8); text-anchor: middle; dominant-baseline: central; }
      .geo-text-accent { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif; font-size: 15px; font-weight: 700; fill: var(--zen-warning, #f59e0b); text-anchor: middle; dominant-baseline: central; }
      .geo-point { fill: var(--text-primary, #f1f5f9); }
      .geo-right-angle { stroke: var(--text-muted, #94a3b8); stroke-width: 1.5; fill: none; }
      .geo-angle-arc { stroke: var(--zen-warning, #f59e0b); stroke-width: 1.8; fill: none; }
      .geo-dashed { stroke-dasharray: 4 4; }

      @media (prefers-color-scheme: light) {
        .geo-line { stroke: var(--text-primary, #0f172a); }
        .geo-sec { stroke: var(--accent-primary, #0284c7); }
        .geo-shaded { fill: var(--geo-shaded-fill, rgba(2, 132, 199, 0.20)); stroke: var(--accent-primary, #0284c7); }
        .geo-text { fill: var(--text-primary, #0f172a); }
        .geo-text-muted { fill: var(--text-secondary, #475569); }
        .geo-text-accent { fill: var(--zen-warning, #d97706); }
        .geo-point { fill: var(--text-primary, #0f172a); }
      }
    </style>
"""

def generate_q25_chart():
    """Soru 25: 5 Üst, 6 Alt Teğet Daireler (4, 11, 6 ve a, b, c)"""
    r = 18
    sx, sy = 30, 40
    dy = math.sqrt(3) * r  # ≈ 31.18

    # Üst 5 daire: x = sx + r + i*2r
    # Alt 6 daire: x = sx + i*2r
    top_y = sy
    bot_y = sy + dy

    # Üst daireler: i=0 (4), i=1 (boş), i=2 (11, sarı), i=3 (boş), i=4 (6)
    # Alt daireler: 0 (1), 1 (a), 2 (9), 3 (b), 4 (c), 5 (2)
    top_items = [
        (0, "4", "geo-shaded", "geo-text"),
        (1, "", "geo-shaded", ""),
        (2, "11", "geo-shaded-yellow", "geo-text-accent"),
        (3, "", "geo-shaded", ""),
        (4, "6", "geo-shaded", "geo-text"),
    ]
    bot_items = [
        (0, "1", "geo-shaded", "geo-text"),
        (1, "a", "geo-shaded", "geo-text-accent"),
        (2, "9", "geo-shaded", "geo-text"),
        (3, "b", "geo-shaded", "geo-text-accent"),
        (4, "c", "geo-shaded", "geo-text-accent"),
        (5, "2", "geo-shaded", "geo-text"),
    ]

    elements = []
    for idx, txt, c_cls, t_cls in top_items:
        cx = sx + r + idx * 2 * r
        elements.append(f'<circle cx="{cx:.1f}" cy="{top_y:.1f}" r="{r}" class="{c_cls}" />')
        if txt:
            elements.append(f'<text x="{cx:.1f}" y="{top_y:.1f}" class="{t_cls}">{txt}</text>')

    for idx, txt, c_cls, t_cls in bot_items:
        cx = sx + idx * 2 * r
        elements.append(f'<circle cx="{cx:.1f}" cy="{bot_y:.1f}" r="{r}" class="{c_cls}" />')
        if txt:
            elements.append(f'<text x="{cx:.1f}" y="{bot_y:.1f}" class="{t_cls}">{txt}</text>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 250 120" width="100%" height="110">
  <defs>{COMMON_STYLE}</defs>
  {''.join(elements)}
</svg>"""
    return save_svg("ales3_q25_chart.svg", svg)

def generate_q26_chart():
    """Soru 26: 5 Üst, 6 Alt Teğet Daireler (6, 3 sarı ve 7, 9, x, y)"""
    r = 18
    sx, sy = 30, 40
    dy = math.sqrt(3) * r
    top_y = sy
    bot_y = sy + dy

    top_items = [
        (0, "", "geo-shaded", ""),
        (1, "", "geo-shaded", ""),
        (2, "", "geo-shaded", ""),
        (3, "6", "geo-shaded-yellow", "geo-text-accent"),
        (4, "3", "geo-shaded-yellow", "geo-text-accent"),
    ]
    bot_items = [
        (0, "7", "geo-shaded", "geo-text"),
        (1, "9", "geo-shaded", "geo-text"),
        (2, "x", "geo-shaded", "geo-text-accent"),
        (3, "y", "geo-shaded", "geo-text-accent"),
        (4, "", "geo-shaded", ""),
        (5, "", "geo-shaded", ""),
    ]

    elements = []
    for idx, txt, c_cls, t_cls in top_items:
        cx = sx + r + idx * 2 * r
        elements.append(f'<circle cx="{cx:.1f}" cy="{top_y:.1f}" r="{r}" class="{c_cls}" />')
        if txt:
            elements.append(f'<text x="{cx:.1f}" y="{top_y:.1f}" class="{t_cls}">{txt}</text>')

    for idx, txt, c_cls, t_cls in bot_items:
        cx = sx + idx * 2 * r
        elements.append(f'<circle cx="{cx:.1f}" cy="{bot_y:.1f}" r="{r}" class="{c_cls}" />')
        if txt:
            elements.append(f'<text x="{cx:.1f}" y="{bot_y:.1f}" class="{t_cls}">{txt}</text>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 250 120" width="100%" height="110">
  <defs>{COMMON_STYLE}</defs>
  {''.join(elements)}
</svg>"""
    return save_svg("ales3_q26_chart.svg", svg)

def generate_q27_matrix():
    """Soru 27: 2x2 Matris Kutuları Denkliği ([5, B] / [1, 3] = [2, 8] / [4, 6])"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 110" width="100%" height="100">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- Sol Kutu (5, B / 1, 3) -->
  <g transform="translate(30, 20)">
    <rect x="0" y="0" width="70" height="70" rx="4" class="geo-line" fill="var(--bg-card, #1e293b)" />
    <line x1="35" y1="0" x2="35" y2="70" class="geo-line" stroke-width="1.5" />
    <line x1="0" y1="35" x2="70" y2="35" class="geo-line" stroke-width="1.5" />
    <text x="17.5" y="17.5" class="geo-text">5</text>
    <text x="52.5" y="17.5" class="geo-text-accent">B</text>
    <text x="17.5" y="52.5" class="geo-text">1</text>
    <text x="52.5" y="52.5" class="geo-text">3</text>
  </g>

  <!-- Eşittir İşareti -->
  <text x="130" y="55" class="geo-text" font-size="22" font-weight="700">=</text>

  <!-- Sağ Kutu (2, 8 / 4, 6) -->
  <g transform="translate(160, 20)">
    <rect x="0" y="0" width="70" height="70" rx="4" class="geo-line" fill="var(--bg-card, #1e293b)" />
    <line x1="35" y1="0" x2="35" y2="70" class="geo-line" stroke-width="1.5" />
    <line x1="0" y1="35" x2="70" y2="35" class="geo-line" stroke-width="1.5" />
    <text x="17.5" y="17.5" class="geo-text">2</text>
    <text x="52.5" y="17.5" class="geo-text">8</text>
    <text x="17.5" y="52.5" class="geo-text">4</text>
    <text x="52.5" y="52.5" class="geo-text">6</text>
  </g>
</svg>"""
    return save_svg("ales3_q27_matrix.svg", svg)

def generate_q28_matrix():
    """Soru 28: 2x2 Matris Kutusu ([A, B] / [2, 3] = 25)"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 110" width="100%" height="100">
  <defs>{COMMON_STYLE}</defs>
  
  <g transform="translate(40, 20)">
    <rect x="0" y="0" width="70" height="70" rx="4" class="geo-line" fill="var(--bg-card, #1e293b)" />
    <line x1="35" y1="0" x2="35" y2="70" class="geo-line" stroke-width="1.5" />
    <line x1="0" y1="35" x2="70" y2="35" class="geo-line" stroke-width="1.5" />
    <text x="17.5" y="17.5" class="geo-text-accent">A</text>
    <text x="52.5" y="17.5" class="geo-text-accent">B</text>
    <text x="17.5" y="52.5" class="geo-text">2</text>
    <text x="52.5" y="52.5" class="geo-text">3</text>
  </g>

  <!-- Eşittir 25 -->
  <text x="135" y="55" class="geo-text" font-size="20" font-weight="700">=</text>
  <text x="175" y="55" class="geo-text-accent" font-size="22" font-weight="700">25</text>
</svg>"""
    return save_svg("ales3_q28_matrix.svg", svg)

def generate_q38_squares():
    """Soru 38: Kare Köşeleri (1, 3, 5, 7)"""
    # Tek kare: (50, 30) to (170, 150)
    # Köşeler: Sol-üst: 1, Sağ-üst: 3, Sağ-alt: 5, Sol-alt: 7
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 180" width="100%" height="160">
  <defs>{COMMON_STYLE}</defs>
  <rect x="50" y="30" width="120" height="120" class="geo-line" />
  
  <!-- Köşe Noktaları -->
  <circle cx="50" cy="30" r="3" class="geo-point" />
  <circle cx="170" cy="30" r="3" class="geo-point" />
  <circle cx="170" cy="150" r="3" class="geo-point" />
  <circle cx="50" cy="150" r="3" class="geo-point" />

  <!-- Köşe Sayıları -->
  <text x="36" y="20" class="geo-text">1</text>
  <text x="184" y="20" class="geo-text">3</text>
  <text x="184" y="160" class="geo-text">5</text>
  <text x="36" y="160" class="geo-text">7</text>
</svg>"""
    return save_svg("ales3_q38_squares.svg", svg)

def generate_q39_squares():
    """Soru 39: İç İçe 3 Kare (A, B, 1, 3, 4, 5)"""
    # Dış kare: (40, 20) to (180, 160)
    # 2. kare: (110, 20), (180, 90), (110, 160), (40, 90)
    # 3. kare: (75, 55), (145, 55), (145, 125), (75, 125)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 230 185" width="100%" height="170">
  <defs>{COMMON_STYLE}</defs>
  <!-- Dış Kare -->
  <rect x="40" y="20" width="140" height="140" class="geo-line" />
  <!-- Orta Kare -->
  <polygon points="110,20 180,90 110,160 40,90" class="geo-sec" stroke-width="1.8" />
  <!-- İç Kare -->
  <rect x="75" y="55" width="70" height="70" class="geo-accent" stroke-width="1.8" />

  <!-- Sayılar & Harfler -->
  <text x="30" y="12" class="geo-text">1</text>
  <text x="190" y="12" class="geo-text">3</text>
  <text x="30" y="168" class="geo-text-accent">A</text>
  <text x="190" y="168" class="geo-text-accent">B</text>

  <!-- Orta Kare Köşe Sayıları -->
  <text x="30" y="90" class="geo-text">5</text>
  <text x="110" y="172" class="geo-text">4</text>
  <text x="110" y="38" class="geo-text">1</text>
</svg>"""
    return save_svg("ales3_q39_squares.svg", svg)

def generate_q40_squares():
    """Soru 40: 3. Adımda Tamamlanan Kareler Düzenegi (A Değeri)"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 230 185" width="100%" height="170">
  <defs>{COMMON_STYLE}</defs>
  <rect x="40" y="20" width="140" height="140" class="geo-line" />
  <polygon points="110,20 180,90 110,160 40,90" class="geo-sec" stroke-width="1.8" />
  <rect x="75" y="55" width="70" height="70" class="geo-accent" stroke-width="1.8" />

  <text x="30" y="12" class="geo-text-accent">A</text>
  <text x="192" y="168" class="geo-text">4</text>
  <text x="68" y="48" class="geo-text">1</text>
  <text x="152" y="132" class="geo-text">1</text>
</svg>"""
    return save_svg("ales3_q40_squares.svg", svg)

def generate_q41_conveyor():
    """Soru 41: Bant ve A, B, C Kapsülleri (9 Top: 1, 2, 3, 4, 5, 4, 3, 2, 1)"""
    # Bant: soldan sağa eğik 3D platform
    # Sağ uçta 3 dikey kapsül: A, B, C
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 160" width="100%" height="145">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- Bant Platformu -->
  <polygon points="30,45 270,45 250,75 10,75" fill="var(--bg-secondary, #334155)" stroke="var(--border-subtle, rgba(255,255,255,0.2))" stroke-width="1.5" />
  <!-- Bant Sağ Kapağı -->
  <polygon points="270,45 295,45 275,75 250,75" fill="var(--bg-card, #1e293b)" stroke="var(--border-subtle, rgba(255,255,255,0.2))" stroke-width="1.5" />

  <!-- 3 Kapsül (A, B, C) -->
  <!-- Kapsül A -->
  <rect x="290" y="65" width="16" height="55" rx="8" class="geo-line" fill="rgba(56, 189, 248, 0.12)" />
  <text x="298" y="135" class="geo-text" font-weight="700">A</text>

  <!-- Kapsül B -->
  <rect x="316" y="65" width="16" height="55" rx="8" class="geo-line" fill="rgba(56, 189, 248, 0.12)" />
  <text x="324" y="135" class="geo-text" font-weight="700">B</text>

  <!-- Kapsül C -->
  <rect x="342" y="65" width="16" height="55" rx="8" class="geo-line" fill="rgba(56, 189, 248, 0.12)" />
  <text x="350" y="135" class="geo-text" font-weight="700">C</text>

  <!-- Bant Üzerindeki 9 Top (1, 2, 3, 4, 5, 4, 3, 2, 1) -->
  <!-- x pozisyonları: 45'ten 245'e kadar 25px aralıkla -->
  {''.join([
    f'<circle cx="{45 + i*23}" cy="48" r="10" class="geo-shaded-yellow" />'
    f'<text x="{45 + i*23}" y="48" class="geo-text" fill="#0f172a">{num}</text>'
    for i, num in enumerate([1, 2, 3, 4, 5, 4, 3, 2, 1])
  ])}

  <!-- Hareket Oku -->
  <line x1="255" y1="35" x2="280" y2="35" stroke="var(--accent-primary, #38bdf8)" stroke-width="2" marker-end="url(#arrow)" />
</svg>"""
    return save_svg("ales3_q41_conveyor.svg", svg)

def generate_q42_conveyor():
    """Soru 42: Bant ve Kapsüller (1, 2, 3, x, 1, 4, 5, 2, 4)"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 160" width="100%" height="145">
  <defs>{COMMON_STYLE}</defs>
  
  <polygon points="30,45 270,45 250,75 10,75" fill="var(--bg-secondary, #334155)" stroke="var(--border-subtle, rgba(255,255,255,0.2))" stroke-width="1.5" />
  <polygon points="270,45 295,45 275,75 250,75" fill="var(--bg-card, #1e293b)" stroke="var(--border-subtle, rgba(255,255,255,0.2))" stroke-width="1.5" />

  <rect x="290" y="65" width="16" height="55" rx="8" class="geo-line" fill="rgba(56, 189, 248, 0.12)" />
  <text x="298" y="135" class="geo-text" font-weight="700">A</text>

  <rect x="316" y="65" width="16" height="55" rx="8" class="geo-line" fill="rgba(56, 189, 248, 0.12)" />
  <text x="324" y="135" class="geo-text" font-weight="700">B</text>

  <rect x="342" y="65" width="16" height="55" rx="8" class="geo-line" fill="rgba(56, 189, 248, 0.12)" />
  <text x="350" y="135" class="geo-text" font-weight="700">C</text>

  <!-- 9 Top: 1, 2, 3, x, 1, 4, 5, 2, 4 -->
  {''.join([
    f'<circle cx="{45 + i*23}" cy="48" r="10" class="geo-shaded-yellow" />'
    f'<text x="{45 + i*23}" y="48" class="geo-text" fill="#0f172a">{num}</text>'
    for i, num in enumerate(['1', '2', '3', 'x', '1', '4', '5', '2', '4'])
  ])}
</svg>"""
    return save_svg("ales3_q42_conveyor.svg", svg)

def generate_q43_conveyor():
    """Soru 43: Kapsüllerdeki Topların Görünümü"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 160" width="100%" height="145">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- Kapsül A: Toplar 1, 2, 1 -->
  <g transform="translate(40, 20)">
    <rect x="0" y="0" width="28" height="95" rx="14" class="geo-line" fill="rgba(56, 189, 248, 0.12)" />
    <circle cx="14" cy="80" r="10" class="geo-shaded-yellow" />
    <text x="14" y="80" class="geo-text" fill="#0f172a">1</text>
    <circle cx="14" cy="56" r="10" class="geo-shaded-yellow" />
    <text x="14" y="56" class="geo-text" fill="#0f172a">2</text>
    <circle cx="14" cy="32" r="10" class="geo-shaded-yellow" />
    <text x="14" y="32" class="geo-text" fill="#0f172a">1</text>
    <text x="14" y="115" class="geo-text" font-weight="700">A</text>
  </g>

  <!-- Kapsül B: Üstten alta 2, 3, 4 -->
  <g transform="translate(100, 20)">
    <rect x="0" y="0" width="28" height="95" rx="14" class="geo-line" fill="rgba(56, 189, 248, 0.12)" />
    <circle cx="14" cy="32" r="10" class="geo-shaded-yellow" />
    <text x="14" y="32" class="geo-text" fill="#0f172a">2</text>
    <circle cx="14" cy="56" r="10" class="geo-shaded-yellow" />
    <text x="14" y="56" class="geo-text" fill="#0f172a">3</text>
    <circle cx="14" cy="80" r="10" class="geo-shaded-yellow" />
    <text x="14" y="80" class="geo-text" fill="#0f172a">4</text>
    <text x="14" y="115" class="geo-text" font-weight="700">B</text>
  </g>

  <!-- Kapsül C: Üstten alta 3, 4, 5 -->
  <g transform="translate(160, 20)">
    <rect x="0" y="0" width="28" height="95" rx="14" class="geo-line" fill="rgba(56, 189, 248, 0.12)" />
    <circle cx="14" cy="32" r="10" class="geo-shaded-yellow" />
    <text x="14" y="32" class="geo-text" fill="#0f172a">3</text>
    <circle cx="14" cy="56" r="10" class="geo-shaded-yellow" />
    <text x="14" y="56" class="geo-text" fill="#0f172a">4</text>
    <circle cx="14" cy="80" r="10" class="geo-shaded-yellow" />
    <text x="14" y="80" class="geo-text" fill="#0f172a">5</text>
    <text x="14" y="115" class="geo-text" font-weight="700">C</text>
  </g>
</svg>"""
    return save_svg("ales3_q43_conveyor.svg", svg)

def generate_q44_triangle():
    """Soru 44: ABC ve ABD Üçgenleri (|AB|=|BD|, |AC|=|CB|, 44°, 20°, x)"""
    # A = (45, 220), B = (215, 220), C = (130, 45)
    # AC = CB (İkizkenar ABC), m(ACB) = 44°
    # Taban açıları = (180 - 44)/2 = 68°.
    # Ray AD: m(CAD) = 20° => m(DAB) = 68 - 20 = 48°.
    # D noktası: |AB| = |BD| => ABD ikizkenar üçgen, m(BAD) = 48° = m(BDA).
    # m(ABD) = 180 - 96 = 84°.
    # m(CBD) = m(ABD) - m(ABC) = 84 - 68 = 16° = x!
    # D koordinatı: B=(215, 220), uzunluk 170, açı 180-84=96° => D=(198, 52)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 260" width="100%" height="240">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- ABC İkizkenar Üçgeni -->
  <polygon points="130,45 45,220 215,220" class="geo-line" />
  
  <!-- D Noktası ve ABD Çizgileri -->
  <line x1="45" y1="220" x2="198" y2="75" class="geo-sec" stroke-width="2.2" />
  <line x1="215" y1="220" x2="198" y2="75" class="geo-sec" stroke-width="2.2" />

  <!-- Eşitlik İşaretleri (|AB| = |BD|) -->
  <line x1="125" y1="215" x2="125" y2="225" class="geo-line" stroke-width="1.8" />
  <line x1="130" y1="215" x2="130" y2="225" class="geo-line" stroke-width="1.8" />
  <line x1="202" y1="145" x2="212" y2="147" class="geo-line" stroke-width="1.8" />
  <line x1="204" y1="149" x2="214" y2="151" class="geo-line" stroke-width="1.8" />

  <!-- Açı Yayları -->
  <!-- 44° (C açısı) -->
  <path d="M 120,70 A 25,25 0 0,0 142,70" class="geo-angle-arc" />
  <text x="130" y="85" class="geo-text-muted">44°</text>

  <!-- 20° (CAD) -->
  <path d="M 68,175 A 35,35 0 0,1 78,188" class="geo-angle-arc" />
  <text x="95" y="180" class="geo-text-muted">20°</text>

  <!-- x (CBD açısı) -->
  <path d="M 205,190 A 25,25 0 0,0 215,195" class="geo-angle-arc" stroke-width="2" />
  <text x="195" y="195" class="geo-text-accent">x</text>

  <!-- Noktalar -->
  <text x="130" y="30" class="geo-text">C</text>
  <text x="30" y="228" class="geo-text">A</text>
  <text x="230" y="228" class="geo-text">B</text>
  <text x="208" y="65" class="geo-text">D</text>
</svg>"""
    return save_svg("ales3_q44_triangle.svg", svg)

def generate_q45_triangle():
    """Soru 45: İkizkenar Üçgen ABC (|AB|=|AC|, 60°, BD=8, DC=2, Boyalı ADB Alanı)"""
    # A = (150, 50), B = (40, 210), C = (220, 210)
    # B, D, C doğrusal. BD=8, DC=2 => D=(184, 210)
    # m(ADB) = 60°
    # ADB boyalı alan
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 250" width="100%" height="230">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- Boyalı ADB Üçgeni -->
  <polygon points="150,50 40,210 184,210" class="geo-shaded" />

  <!-- ABC Üçgeni -->
  <polygon points="150,50 40,210 220,210" class="geo-line" />
  
  <!-- AD Çizgisi -->
  <line x1="150" y1="50" x2="184" y2="210" class="geo-sec" stroke-width="2.2" />

  <!-- Eşitlik İşaretleri (|AB| = |AC|) -->
  <line x1="90" y1="126" x2="98" y2="134" class="geo-line" stroke-width="1.8" />
  <line x1="180" y1="126" x2="188" y2="134" class="geo-line" stroke-width="1.8" />

  <!-- 60° Açı Yayı (D noktasında sol açı) -->
  <path d="M 164,210 A 20,20 0 0,1 179,190" class="geo-angle-arc" />
  <text x="155" y="195" class="geo-text-muted">60°</text>

  <!-- Ölçüler: BD = 8, DC = 2 -->
  <text x="112" y="225" class="geo-text">8</text>
  <text x="202" y="225" class="geo-text">2</text>

  <!-- Noktalar -->
  <text x="150" y="35" class="geo-text">A</text>
  <text x="25" y="215" class="geo-text">B</text>
  <text x="235" y="215" class="geo-text">C</text>
  <text x="188" y="225" class="geo-text">D</text>
</svg>"""
    return save_svg("ales3_q45_triangle.svg", svg)

def generate_q46_square():
    """Soru 46: Kare ABCD ve Köşegen [AC], Dış Nokta E (|AC|=|BE|, 25°, x)"""
    # Kare ABCD: A=(50, 190), B=(170, 190), C=(170, 70), D=(50, 70)
    # Köşegen AC çizili: (50, 190) to (170, 70)
    # E noktası: |BE| = |AC|, m(CBE) = 25°
    # m(ABE) = 90 + 25 = 115°.
    # E noktası sağ-üstte: B=(170, 190), uzunluk 120*sqrt(2) ≈ 170, açı 65° => E=(242, 35)
    # DE doğru parçası çizili: D=(50, 70) to E=(242, 35)
    # m(EDC) = x
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 290 240" width="100%" height="220">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- ABCD Karesi -->
  <rect x="50" y="70" width="120" height="120" class="geo-line" />
  
  <!-- AC Köşegeni -->
  <line x1="50" y1="190" x2="170" y2="70" class="geo-sec" stroke-width="2" />
  <!-- Eşitlik İşareti AC üzerinde -->
  <line x1="108" y1="126" x2="114" y2="134" class="geo-line" stroke-width="1.8" />

  <!-- BE Doğru Parçası -->
  <line x1="170" y1="190" x2="242" y2="35" class="geo-sec" stroke-width="2" />
  <line x1="202" y1="110" x2="210" y2="114" class="geo-line" stroke-width="1.8" />

  <!-- DE Doğru Parçası -->
  <line x1="50" y1="70" x2="242" y2="35" class="geo-line" stroke-width="1.8" />

  <!-- 25° Açı Yayı (CBE) -->
  <path d="M 170,165 A 25,25 0 0,1 184,168" class="geo-angle-arc" />
  <text x="185" y="152" class="geo-text-muted">25°</text>

  <!-- x Açı Yayı (EDC) -->
  <path d="M 75,66 A 25,25 0 0,0 75,70" class="geo-angle-arc" stroke-width="2" />
  <text x="86" y="62" class="geo-text-accent">x</text>

  <!-- Noktalar -->
  <text x="35" y="195" class="geo-text">A</text>
  <text x="170" y="205" class="geo-text">B</text>
  <text x="182" y="75" class="geo-text">C</text>
  <text x="35" y="65" class="geo-text">D</text>
  <text x="252" y="30" class="geo-text">E</text>
</svg>"""
    return save_svg("ales3_q46_square.svg", svg)

def generate_q47_square():
    """Soru 47: Dikdörtgen ABCD (E Noktası, F Orta Nokta, Boyalı CDF Alanı)"""
    # ABCD Dikdörtgen: A=(40, 180), B=(220, 180), C=(220, 60), D=(40, 60)
    # AB üzerinde E: AE=8, EB=2 => A=(40), E=(184), B=(220)
    # [CE] segment: C=(220, 60) to E=(184, 180)
    # F orta nokta CE: F=(202, 120), |CF| = |EF| = sqrt(5)
    # DF segment: D=(40, 60) to F=(202, 120)
    # Boyalı üçgen CDF: D=(40, 60), C=(220, 60), F=(202, 120)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 230" width="100%" height="210">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- Boyalı CDF Üçgeni -->
  <polygon points="40,60 220,60 202,120" class="geo-shaded" />

  <!-- ABCD Dikdörtgeni -->
  <rect x="40" y="60" width="180" height="120" class="geo-line" />
  
  <!-- [CE] ve [DF] Çizgileri -->
  <line x1="220" y1="60" x2="184" y2="180" class="geo-sec" stroke-width="2" />
  <line x1="40" y1="60" x2="202" y2="120" class="geo-line" stroke-width="2" />

  <!-- Eşitlik İşaretleri (|CF| = |EF|) -->
  <line x1="206" y1="88" x2="216" y2="92" class="geo-line" stroke-width="1.8" />
  <line x1="188" y1="148" x2="198" y2="152" class="geo-line" stroke-width="1.8" />

  <!-- Ölçüler: AE = 8, EB = 2 -->
  <text x="112" y="195" class="geo-text">8</text>
  <text x="202" y="195" class="geo-text">2</text>

  <!-- Noktalar -->
  <text x="25" y="185" class="geo-text">A</text>
  <text x="184" y="195" class="geo-text">E</text>
  <text x="232" y="185" class="geo-text">B</text>
  <text x="232" y="55" class="geo-text">C</text>
  <text x="25" y="55" class="geo-text">D</text>
  <text x="216" y="125" class="geo-text">F</text>
</svg>"""
    return save_svg("ales3_q47_square.svg", svg)

def generate_q48_circle():
    """Soru 48: Yarım Çember [AB] Çaplı (|DE|=|EB|, |OE|=|EC|, x Açısı)"""
    # Merkez O=(150, 160), R=100
    # A=(50, 160), B=(250, 160)
    # Yarım çember üstte: path from (50, 160) to (250, 160)
    # C noktası çember üzerinde, D noktası çember üzerinde.
    # D, E, B doğrusal. OC doğrusu ile DB kesişimi E.
    # |DE| = |EB| ve |OE| = |EC|
    # m(OAD) = x
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 310 200" width="100%" height="180">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- Yarım Çember Yayı -->
  <path d="M 50,160 A 100,100 0 0,1 250,160" class="geo-line" />
  <!-- AB Çapı -->
  <line x1="50" y1="160" x2="250" y2="160" class="geo-line" />

  <!-- Kirişler ve Yarıçaplar -->
  <!-- D=(79, 89), B=(250, 160) => DB Kirişi -->
  <line x1="79" y1="89" x2="250" y2="160" class="geo-sec" stroke-width="2" />
  <!-- C=(185, 65) => OC Yarıçapı (E=(164.5, 124.5) üzerinden) -->
  <line x1="150" y1="160" x2="185" y2="65" class="geo-sec" stroke-width="2" />
  <!-- AD Kirişi -->
  <line x1="50" y1="160" x2="79" y2="89" class="geo-line" />

  <!-- Eşitlik İşareti (|DE| = |EB|) -->
  <line x1="120" y1="102" x2="124" y2="110" class="geo-line" stroke-width="1.8" />
  <line x1="205" y1="138" x2="209" y2="146" class="geo-line" stroke-width="1.8" />

  <!-- Eşitlik İşareti (|OE| = |EC|) -->
  <line x1="153" y1="140" x2="161" y2="143" class="geo-line" stroke-width="1.8" />
  <line x1="154" y1="143" x2="162" y2="146" class="geo-line" stroke-width="1.8" />
  <line x1="170" y1="92" x2="178" y2="95" class="geo-line" stroke-width="1.8" />
  <line x1="171" y1="95" x2="179" y2="98" class="geo-line" stroke-width="1.8" />

  <!-- x Açı Yayı (OAD) -->
  <path d="M 72,160 A 22,22 0 0,0 66,140" class="geo-angle-arc" stroke-width="2" />
  <text x="82" y="145" class="geo-text-accent">x</text>

  <!-- Noktalar -->
  <circle cx="150" cy="160" r="2.5" class="geo-point" />
  <text x="150" y="175" class="geo-text">O</text>
  <text x="35" y="165" class="geo-text">A</text>
  <text x="262" y="165" class="geo-text">B</text>
  <text x="195" y="55" class="geo-text">C</text>
  <text x="70" y="78" class="geo-text">D</text>
  <text x="175" y="132" class="geo-text">E</text>
</svg>"""
    return save_svg("ales3_q48_circle.svg", svg)

def generate_q49_grid_sheet():
    """Soru 49: 4x5 Birim Kare Şeffaf Kâğıt Katlama (Şekil I, II, III ve Ok Yönü)"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 200" width="100%" height="180">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- Şekil I: 4x5 Grid (Ok sol üstte güneydoğu yönünde) -->
  <g transform="translate(15, 20)">
    <text x="45" y="10" class="geo-text-muted" font-weight="700">Şekil I</text>
    <!-- 4 satır, 5 sütun (her kare 18x18) -->
    <rect x="0" y="20" width="90" height="72" fill="none" stroke="var(--border-subtle, rgba(255,255,255,0.2))" />
    <!-- Yatay & Dikey Çizgiler -->
    <line x1="0" y1="38" x2="90" y2="38" stroke="var(--border-subtle, rgba(255,255,255,0.15))" />
    <line x1="0" y1="56" x2="90" y2="56" stroke="#38bdf8" stroke-width="1.8" stroke-dasharray="4 4" />
    <line x1="0" y1="74" x2="90" y2="74" stroke="var(--border-subtle, rgba(255,255,255,0.15))" />
    <line x1="18" y1="20" x2="18" y2="92" stroke="var(--border-subtle, rgba(255,255,255,0.15))" />
    <line x1="36" y1="20" x2="36" y2="92" stroke="var(--border-subtle, rgba(255,255,255,0.15))" />
    <line x1="54" y1="20" x2="54" y2="92" stroke="var(--border-subtle, rgba(255,255,255,0.15))" />
    <line x1="72" y1="20" x2="72" y2="92" stroke="var(--border-subtle, rgba(255,255,255,0.15))" />
    
    <!-- Ok İşareti (Sol-Üst Hücrede: 0-18 x 20-38) -->
    <line x1="3" y1="23" x2="15" y2="35" stroke="#f59e0b" stroke-width="2.5" />
    <polygon points="15,35 15,28 8,35" fill="#f59e0b" />

    <!-- Katlama Oku (Aşağı Doğru) -->
    <path d="M 98,40 Q 108,56 98,70" fill="none" stroke="#38bdf8" stroke-width="1.8" />
  </g>

  <!-- Şekil II: Yatay Katlanmış (2x5 Grid, Dikey Kesikli Doğru) -->
  <g transform="translate(145, 20)">
    <text x="45" y="10" class="geo-text-muted" font-weight="700">Şekil II</text>
    <rect x="0" y="38" width="90" height="36" fill="none" stroke="var(--border-subtle, rgba(255,255,255,0.2))" />
    <line x1="0" y1="56" x2="90" y2="56" stroke="var(--border-subtle, rgba(255,255,255,0.15))" />
    <line x1="45" y1="38" x2="45" y2="74" stroke="#38bdf8" stroke-width="1.8" stroke-dasharray="4 4" />

    <!-- Ok İşareti (Yansımış) -->
    <line x1="3" y1="71" x2="15" y2="59" stroke="#f59e0b" stroke-width="2.5" />
    <polygon points="15,59 8,59 15,66" fill="#f59e0b" />
  </g>

  <!-- Şekil III: Köşegen Katlama -->
  <g transform="translate(275, 20)">
    <text x="35" y="10" class="geo-text-muted" font-weight="700">Şekil III</text>
    <rect x="0" y="38" width="45" height="36" fill="none" stroke="var(--border-subtle, rgba(255,255,255,0.2))" />
    <line x1="0" y1="74" x2="45" y2="38" stroke="#38bdf8" stroke-width="1.8" stroke-dasharray="4 4" />
  </g>

  <!-- Doğru Sonuç (Seçenek A: Üçgen İçinde Ok) -->
  <g transform="translate(150, 120)">
    <polygon points="0,40 40,0 40,40" class="geo-shaded" />
    <!-- Ok -->
    <line x1="20" y1="12" x2="20" y2="30" stroke="#f59e0b" stroke-width="2.5" />
    <polygon points="20,30 16,23 24,23" fill="#f59e0b" />
    <text x="75" y="25" class="geo-text-accent">Sonuç (A)</text>
  </g>
</svg>"""
    return save_svg("ales3_q49_grid_sheet.svg", svg)

def generate_q50_solid():
    """Soru 50: 2x3x4 24 Birim Küp Prizması (8 Kırmızı, 8 Mavi, 8 Sarı)"""
    # 2x3x4 prizması izometrik görünüm
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 230" width="100%" height="210">
  <defs>{COMMON_STYLE}</defs>
  
  <g transform="translate(130, 40)">
    <!-- 2x3x4 Prizma Blokları -->
    <!-- Kat 1 (Üst Kat: Sarı ve Mavi Küpler) -->
    <!-- Üst Yüzey -->
    <polygon points="0,0 60,-35 120,0 60,35" fill="#f59e0b" fill-opacity="0.8" stroke="#f59e0b" stroke-width="1.5" />
    
    <!-- Ön Yüzey (Kırmızı Küpler) -->
    <polygon points="0,0 60,35 60,95 0,60" fill="#f43f5e" fill-opacity="0.8" stroke="#f43f5e" stroke-width="1.5" />
    
    <!-- Sağ Yüzey (Mavi Küpler) -->
    <polygon points="60,35 120,0 120,60 60,95" fill="#38bdf8" fill-opacity="0.8" stroke="#38bdf8" stroke-width="1.5" />

    <!-- Küp Izgaraları (2 x 3 x 4) -->
    <!-- Ön Yüz Bölmeleri (4 sütun x 2 satır) -->
    <line x1="15" y1="8.7" x2="15" y2="68.7" stroke="rgba(255,255,255,0.4)" stroke-width="1" />
    <line x1="30" y1="17.5" x2="30" y2="77.5" stroke="rgba(255,255,255,0.4)" stroke-width="1" />
    <line x1="45" y1="26.2" x2="45" y2="86.2" stroke="rgba(255,255,255,0.4)" stroke-width="1" />
    <line x1="0" y1="30" x2="60" y2="65" stroke="rgba(255,255,255,0.4)" stroke-width="1" />

    <!-- Sağ Yüz Bölmeleri (3 sütun x 2 satır) -->
    <line x1="80" y1="23.3" x2="80" y2="83.3" stroke="rgba(255,255,255,0.4)" stroke-width="1" />
    <line x1="100" y1="11.6" x2="100" y2="71.6" stroke="rgba(255,255,255,0.4)" stroke-width="1" />
    <line x1="60" y1="65" x2="120" y2="30" stroke="rgba(255,255,255,0.4)" stroke-width="1" />

    <!-- Üst Yüz Bölmeleri (4x3 ızgara) -->
    <line x1="20" y1="-11.6" x2="80" y2="23.3" stroke="rgba(255,255,255,0.4)" stroke-width="1" />
    <line x1="40" y1="-23.3" x2="100" y2="11.6" stroke="rgba(255,255,255,0.4)" stroke-width="1" />
    <line x1="15" y1="8.7" x2="75" y2="-26.3" stroke="rgba(255,255,255,0.4)" stroke-width="1" />
    <line x1="30" y1="17.5" x2="90" y2="-17.5" stroke="rgba(255,255,255,0.4)" stroke-width="1" />
    <line x1="45" y1="26.2" x2="105" y2="-8.8" stroke="rgba(255,255,255,0.4)" stroke-width="1" />
  </g>

  <!-- Lejant -->
  <text x="160" y="175" class="geo-text" font-size="13">2 × 3 × 4 Dikdörtgenler Prizması</text>
  <text x="160" y="195" class="geo-text-muted" font-size="12">8 Kırmızı, 8 Mavi, 8 Sarı Birim Küp</text>
</svg>"""
    return save_svg("ales3_q50_solid.svg", svg)

def save_svg(filename: str, content: str):
    path = SVG_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return content, f"/assets/questions/svg/{filename}"

def generate_all_ales3_svgs():
    """2021-ALES/3 için tüm SVG çizimlerini üretir ve haritayı döndürür."""
    m = {}
    m["q25"], m["q25_url"] = generate_q25_chart()
    m["q26"], m["q26_url"] = generate_q26_chart()
    m["q27"], m["q27_url"] = generate_q27_matrix()
    m["q28"], m["q28_url"] = generate_q28_matrix()
    m["q38"], m["q38_url"] = generate_q38_squares()
    m["q39"], m["q39_url"] = generate_q39_squares()
    m["q40"], m["q40_url"] = generate_q40_squares()
    m["q41"], m["q41_url"] = generate_q41_conveyor()
    m["q42"], m["q42_url"] = generate_q42_conveyor()
    m["q43"], m["q43_url"] = generate_q43_conveyor()
    m["q44"], m["q44_url"] = generate_q44_triangle()
    m["q45"], m["q45_url"] = generate_q45_triangle()
    m["q46"], m["q46_url"] = generate_q46_square()
    m["q47"], m["q47_url"] = generate_q47_square()
    m["q48"], m["q48_url"] = generate_q48_circle()
    m["q49"], m["q49_url"] = generate_q49_grid_sheet()
    m["q50"], m["q50_url"] = generate_q50_solid()
    return m

if __name__ == "__main__":
    res = generate_all_ales3_svgs()
    print(f"Generated {len(res)//2} SVG files for 2021-ALES/3.")
