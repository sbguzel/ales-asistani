#!/usr/bin/env python3
"""
scripts/generators/ales1_svg_generator.py
2021-ALES/1 sınavında ekran resmi olarak bulunan tüm şekil ve diyagramları
saf vektörel, tema uyumlu ve matematiksel olarak kesin SVG formatında üretir.
"""

from pathlib import Path

SVG_DIR = Path("public/assets/questions/svg")
SVG_DIR.mkdir(parents=True, exist_ok=True)

COMMON_STYLE = """
    <style>
      .geo-line { stroke: var(--text-primary, #f1f5f9); stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .geo-sec { stroke: var(--accent-primary, #38bdf8); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .geo-accent { stroke: var(--zen-warning, #f59e0b); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .geo-shaded { fill: var(--geo-shaded-fill, rgba(56, 189, 248, 0.28)); stroke: var(--geo-shaded-stroke, var(--accent-primary, #38bdf8)); stroke-width: 2; stroke-linejoin: round; }
      .geo-shaded-yellow { fill: rgba(245, 158, 11, 0.28); stroke: #f59e0b; stroke-width: 2; stroke-linejoin: round; }
      .geo-shaded-red { fill: rgba(244, 63, 94, 0.28); stroke: #f43f5e; stroke-width: 2; stroke-linejoin: round; }
      .geo-text { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif; font-size: 14px; font-weight: 600; fill: var(--text-primary, #f1f5f9); text-anchor: middle; dominant-baseline: central; }
      .geo-text-muted { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif; font-size: 12px; font-weight: 500; fill: var(--text-secondary, #94a3b8); text-anchor: middle; dominant-baseline: central; }
      .geo-text-accent { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif; font-size: 15px; font-weight: 700; fill: var(--zen-warning, #f59e0b); text-anchor: middle; dominant-baseline: central; }
      .geo-point { fill: var(--text-primary, #f1f5f9); }
      .geo-right-angle { stroke: var(--text-muted, #94a3b8); stroke-width: 1.5; fill: none; }
      .geo-angle-arc { stroke: var(--zen-warning, #f59e0b); stroke-width: 1.8; fill: none; }
      .geo-dashed { stroke-dasharray: 4 4; }
      .cell-bg { fill: rgba(255, 255, 255, 0.04); }
      .cell-highlight { fill: rgba(56, 189, 248, 0.25); stroke: var(--accent-primary, #38bdf8); stroke-width: 2; }
      .cell-highlight-yellow { fill: rgba(245, 158, 11, 0.25); stroke: #f59e0b; stroke-width: 2; }

      @media (prefers-color-scheme: light) {
        .geo-line { stroke: var(--text-primary, #0f172a); }
        .geo-sec { stroke: var(--accent-primary, #0284c7); }
        .geo-shaded { fill: var(--geo-shaded-fill, rgba(2, 132, 199, 0.20)); stroke: var(--accent-primary, #0284c7); }
        .geo-text { fill: var(--text-primary, #0f172a); }
        .geo-text-muted { fill: var(--text-secondary, #475569); }
        .geo-text-accent { fill: var(--zen-warning, #d97706); }
        .geo-point { fill: var(--text-primary, #0f172a); }
        .cell-bg { fill: rgba(0, 0, 0, 0.02); }
      }
    </style>
"""

def generate_q21_calendar():
    """Mayıs Ayı Takvimi (1, 8, 16, 22, 30 Mayıs işaretli)"""
    # 2021 Mayıs: 1 Mayıs Cumartesi günü başlar. Toplam 31 gün.
    days_of_week = ["Pt", "Sa", "Ça", "Pe", "Cu", "Ct", "Pz"]
    highlighted = {1, 8, 16, 22, 30}
    
    # 7 sütun x 6 satır (başlık dahil)
    col_w = 42
    row_h = 32
    start_x = 20
    start_y = 50

    cells = []
    # Gün başlıkları
    for c, dow in enumerate(days_of_week):
        x = start_x + c * col_w + col_w / 2
        cells.append(f'<text x="{x}" y="{start_y - 12}" class="geo-text-muted">{dow}</text>')

    # 1 Mayıs Cumartesi = sütun 5 (0-indexed: Pt=0, Sa=1, Ça=2, Pe=3, Cu=4, Ct=5, Pz=6)
    cur_col = 5
    cur_row = 0
    for day in range(1, 32):
        cx = start_x + cur_col * col_w + col_w / 2
        cy = start_y + cur_row * row_h + row_h / 2
        if day in highlighted:
            cells.append(f'<circle cx="{cx}" cy="{cy}" r="14" class="geo-shaded-yellow" />')
            cells.append(f'<text x="{cx}" y="{cy}" class="geo-text-accent">{day}</text>')
        else:
            cells.append(f'<text x="{cx}" y="{cy}" class="geo-text">{day}</text>')
        
        cur_col += 1
        if cur_col == 7:
            cur_col = 0
            cur_row += 1

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 334 260" width="100%" height="240">
  <defs>{COMMON_STYLE}</defs>
  <rect x="10" y="10" width="314" height="236" rx="12" fill="none" stroke="var(--border-subtle, rgba(255,255,255,0.12))" stroke-width="1.5" />
  <text x="167" y="26" class="geo-text" font-size="15" letter-spacing="1">MAYIS</text>
  <line x1="10" y1="36" x2="324" y2="36" stroke="var(--border-subtle, rgba(255,255,255,0.1))" stroke-width="1" />
  {''.join(cells)}
</svg>"""
    return save_svg("ales1_q21_calendar.svg", svg)

def generate_q25_balls():
    """Soru 25: 7 Teğet Top (Üst 3, Alt 4)"""
    r = 22
    start_x = 45
    start_y = 50
    # Üst sıra: 3 top
    # Alt sıra: 4 top (üst sıradakilere teğet, yani x ofset r kadar)
    # y ofset: sqrt( (2r)^2 - r^2 ) = r * sqrt(3) ≈ 1.732 * 22 ≈ 38.1
    dy = 38.1
    top_y = start_y
    bot_y = start_y + dy

    # Top centers
    # Bot row: 4 circles at x = start_x, start_x + 2r, start_x + 4r, start_x + 6r
    # Top row: 3 circles at x = start_x + r, start_x + 3r, start_x + 5r
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 230 140" width="100%" height="130">
  <defs>{COMMON_STYLE}</defs>
  <!-- Üst 3 top -->
  <circle cx="{start_x + r}" cy="{top_y}" r="{r}" class="geo-shaded" />
  <circle cx="{start_x + 3*r}" cy="{top_y}" r="{r}" class="geo-shaded" />
  <circle cx="{start_x + 5*r}" cy="{top_y}" r="{r}" class="geo-shaded" />
  <text x="{start_x + 5*r}" y="{top_y}" class="geo-text">1</text>

  <!-- Alt 4 top -->
  <circle cx="{start_x}" cy="{bot_y}" r="{r}" class="geo-shaded" />
  <text x="{start_x}" y="{bot_y}" class="geo-text">7</text>

  <circle cx="{start_x + 2*r}" cy="{bot_y}" r="{r}" class="geo-shaded-yellow" />
  <text x="{start_x + 2*r}" y="{bot_y}" class="geo-text-accent">x</text>

  <circle cx="{start_x + 4*r}" cy="{bot_y}" r="{r}" class="geo-shaded" />
  <circle cx="{start_x + 6*r}" cy="{bot_y}" r="{r}" class="geo-shaded" />
</svg>"""
    return save_svg("ales1_q25_balls.svg", svg)

def generate_q26_balls():
    """Soru 26: Ortada 'a' topu, çevresinde teğet 5 top (1 ve 6 konumlandırılmış)"""
    r = 22
    cx, cy = 110, 80
    # 6 çevre konumu (60° aralıklarla: 0, 60, 120, 180, 240, 300 derece)
    # R_orbit = 2*r = 44
    import math
    
    # Şekle göre:
    # Merkezde 'a'
    # Üstte (90°): '1' (x=cx, y=cy-44)
    # Sol (150°): boş (x=cx - 44*cos(30), y=cy - 44*sin(30)) -> wait, 60 deg steps:
    # angles: 90 (top: 1), 150 (top-left), 210 (bottom-left: 6), 270 (bottom), 330 (bottom-right), 30 (top-right)
    # In diagram: top=1, bottom-left=6, bottom-right, right, left
    
    coords = {
        "top": (cx, cy - 2*r, "1", "geo-text"),
        "top_left": (cx - math.sqrt(3)*r, cy - r, "", ""),
        "bot_left": (cx - math.sqrt(3)*r, cy + r, "6", "geo-text"),
        "bot_right": (cx, cy + 2*r, "", ""),
        "right": (cx + math.sqrt(3)*r, cy - r, "", ""),
    }

    circles = []
    # Çevre topları
    for name, (px, py, txt, cls) in coords.items():
        circles.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" class="geo-shaded" />')
        if txt:
            circles.append(f'<text x="{px:.1f}" y="{py:.1f}" class="{cls}">{txt}</text>')

    # Merkez top
    circles.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" class="geo-shaded-yellow" />')
    circles.append(f'<text x="{cx}" y="{cy}" class="geo-text-accent">a</text>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 160" width="100%" height="150">
  <defs>{COMMON_STYLE}</defs>
  {''.join(circles)}
</svg>"""
    return save_svg("ales1_q26_balls.svg", svg)

def generate_q27_stores_table():
    """Soru 27 & 28: Mağaza Satış Fiyatı ve Puan Tablosu"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 220" width="100%" height="200">
  <defs>{COMMON_STYLE}</defs>
  <!-- Tablo Çerçevesi -->
  <rect x="15" y="15" width="310" height="190" rx="8" class="geo-line" fill="var(--bg-card, rgba(30, 41, 59, 0.5))" />
  <!-- Başlık Satırı -->
  <rect x="15" y="15" width="310" height="35" rx="8" fill="rgba(56, 189, 248, 0.12)" />
  <line x1="15" y1="50" x2="325" y2="50" class="geo-line" stroke-width="1.5" />
  
  <!-- Dikey Çizgiler -->
  <line x1="90" y1="15" x2="90" y2="205" class="geo-line" stroke-width="1.2" />
  <line x1="165" y1="15" x2="165" y2="205" class="geo-line" stroke-width="1.2" />

  <!-- Yatay Satır Çizgileri -->
  <line x1="15" y1="81" x2="325" y2="81" stroke="var(--border-subtle, rgba(255,255,255,0.1))" stroke-width="1" />
  <line x1="15" y1="112" x2="325" y2="112" stroke="var(--border-subtle, rgba(255,255,255,0.1))" stroke-width="1" />
  <line x1="15" y1="143" x2="325" y2="143" stroke="var(--border-subtle, rgba(255,255,255,0.1))" stroke-width="1" />
  <line x1="15" y1="174" x2="325" y2="174" stroke="var(--border-subtle, rgba(255,255,255,0.1))" stroke-width="1" />

  <!-- Başlıklar -->
  <text x="52" y="33" class="geo-text" font-weight="700">Mağaza</text>
  <text x="127" y="33" class="geo-text" font-weight="700">Puan</text>
  <text x="245" y="33" class="geo-text" font-weight="700">Satış Fiyatı</text>

  <!-- Satırlar: A, B, C, D, E -->
  <!-- A: 96, 40 TL 80 kuruş -->
  <text x="52" y="66" class="geo-text">A</text>
  <text x="127" y="66" class="geo-text-accent">96</text>
  <text x="245" y="66" class="geo-text">40 TL 80 kuruş</text>

  <!-- B: [boş], 44 TL 50 kuruş -->
  <text x="52" y="97" class="geo-text">B</text>
  <text x="127" y="97" class="geo-text-muted">—</text>
  <text x="245" y="97" class="geo-text">44 TL 50 kuruş</text>

  <!-- C: 81, 42 TL 10 kuruş -->
  <text x="52" y="128" class="geo-text">C</text>
  <text x="127" y="128" class="geo-text-accent">81</text>
  <text x="245" y="128" class="geo-text">42 TL 10 kuruş</text>

  <!-- D: 88, 42 TL 70 kuruş -->
  <text x="52" y="159" class="geo-text">D</text>
  <text x="127" y="159" class="geo-text-accent">88</text>
  <text x="245" y="159" class="geo-text">42 TL 70 kuruş</text>

  <!-- E: [boş], 40 TL 20 kuruş -->
  <text x="52" y="190" class="geo-text">E</text>
  <text x="127" y="190" class="geo-text-muted">—</text>
  <text x="245" y="190" class="geo-text">40 TL 20 kuruş</text>
</svg>"""
    return save_svg("ales1_q27_stores_table.svg", svg)

def generate_q32_pie():
    """Soru 32: Daire Grafiği (90°, 120°, 150°)"""
    # Merkez (100, 100), R = 75
    # Dilim 1: 0° -> 90° (üst-sağ çeyrek: 90°)
    # Dilim 2: 90° -> 210° (120°)
    # Dilim 3: 210° -> 360° (150°)
    # Koordinatlar:
    # 0°: (175, 100) -> sağ
    # 90°: (100, 25) -> yukarı
    # 210°: (100 - 75*cos30, 100 + 75*sin30) = (100 - 64.95, 100 + 37.5) = (35.05, 137.5)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="180">
  <defs>{COMMON_STYLE}</defs>
  <circle cx="100" cy="100" r="75" class="geo-line" />
  <!-- Yarıçap çizgileri -->
  <line x1="100" y1="100" x2="175" y2="100" class="geo-line" />
  <line x1="100" y1="100" x2="100" y2="25" class="geo-line" />
  <line x1="100" y1="100" x2="35.05" y2="137.5" class="geo-line" />

  <!-- 90° Dik Açı Sembolü -->
  <path d="M 100,86 L 114,86 L 114,100" class="geo-right-angle" />
  <circle cx="107" cy="93" r="1.5" class="geo-point" />

  <!-- 120° Yayı ve Yazısı -->
  <path d="M 116,100 A 16,16 0 0,1 86.1,108" class="geo-angle-arc" />
  <text x="108" y="130" class="geo-text">120°</text>
</svg>"""
    return save_svg("ales1_q32_pie.svg", svg)

def generate_q33_pie():
    """Soru 33: Daire Grafiği (144°, 120°, 96°)"""
    # Merkez (100, 100), R = 75
    # Çizgiler: 0° (sağa: 175, 100), 120° (aşağı-sol), 264° (120+144 = 264°)
    import math
    cx, cy, r = 100, 100, 75
    # 1. çizgi: sağ (0°) -> (cx+r, cy) = (175, 100)
    # 2. çizgi: 120° saat yönü -> (100 + 75*cos(120°), 100 + 75*sin(120°)) = (100 - 37.5, 100 + 64.95) = (62.5, 165)
    # 3. çizgi: 120° + 144° = 264° saat yönü -> (100 + 75*cos(264°), 100 + 75*sin(264°)) = (100 - 7.8, 100 - 74.6) = (92.2, 25.4)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="180">
  <defs>{COMMON_STYLE}</defs>
  <circle cx="100" cy="100" r="75" class="geo-line" />
  <line x1="100" y1="100" x2="175" y2="100" class="geo-line" />
  <line x1="100" y1="100" x2="62.5" y2="165" class="geo-line" />
  <line x1="100" y1="100" x2="92.2" y2="25.4" class="geo-line" />

  <!-- 120° Yayı ve Açısı -->
  <path d="M 118,100 A 18,18 0 0,1 91,115.6" class="geo-angle-arc" />
  <text x="125" y="128" class="geo-text">120°</text>

  <!-- 144° Yayı ve Açısı -->
  <path d="M 91,115.6 A 18,18 0 0,1 98.1,82" class="geo-angle-arc" />
  <text x="60" y="98" class="geo-text">144°</text>
</svg>"""
    return save_svg("ales1_q33_pie.svg", svg)

def generate_q34_pie():
    """Soru 34: 12 Yıl Sonraki Yaş Dağılım Grafiği (105°, 120°, 135°)"""
    # Merkez (100, 100), R = 75
    # Dilimler: 120° (alt), 105° (sağ-üst), 135° (sol-üst)
    # 0° (175, 100), 120° (62.5, 165), 120+135=255° (80.6, 27.6)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="180">
  <defs>{COMMON_STYLE}</defs>
  <circle cx="100" cy="100" r="75" class="geo-line" />
  <line x1="100" y1="100" x2="175" y2="100" class="geo-line" />
  <line x1="100" y1="100" x2="62.5" y2="165" class="geo-line" />
  <line x1="100" y1="100" x2="80.6" y2="27.6" class="geo-line" />

  <!-- Açı Etiketleri -->
  <text x="125" y="130" class="geo-text">120°</text>
  <text x="135" y="70" class="geo-text-accent">105°</text>
  <text x="60" y="85" class="geo-text-muted">135°</text>
</svg>"""
    return save_svg("ales1_q34_pie.svg", svg)

def generate_q41_grid():
    """Soru 41: 4x10 Boyutlarında Sayı Tablosu"""
    col_w = 28
    row_h = 28
    start_x = 15
    start_y = 15

    # 4 satır, 10 sütun
    # Satır 1: sütun 3=4, sütun 10=?
    # Satır 2: sütun 4=3, sütun 10=?
    # Satır 3: sütun 5=8, sütun 10=?
    # Satır 4: sütun 6=0, sütun 10=?
    content = []
    # Grid çizgileri
    for r in range(5):
        y = start_y + r * row_h
        content.append(f'<line x1="{start_x}" y1="{y}" x2="{start_x + 10*col_w}" y2="{y}" class="geo-line" stroke-width="1.2" />')
    for c in range(11):
        x = start_x + c * col_w
        content.append(f'<line x1="{x}" y1="{start_y}" x2="{x}" y2="{start_y + 4*row_h}" class="geo-line" stroke-width="1.2" />')

    # Değerler
    values = [
        (0, 2, "4", "geo-text"),
        (1, 3, "3", "geo-text"),
        (2, 4, "8", "geo-text"),
        (3, 5, "0", "geo-text"),
        # Soru işaretleri son sütunda (c=9)
        (0, 9, "?", "geo-text-accent"),
        (1, 9, "?", "geo-text-accent"),
        (2, 9, "?", "geo-text-accent"),
        (3, 9, "?", "geo-text-accent"),
    ]
    for r, c, val, cls in values:
        cx = start_x + c * col_w + col_w / 2
        cy = start_y + r * row_h + row_h / 2
        content.append(f'<text x="{cx}" y="{cy}" class="{cls}">{val}</text>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 310 142" width="100%" height="130">
  <defs>{COMMON_STYLE}</defs>
  {''.join(content)}
</svg>"""
    return save_svg("ales1_q41_grid.svg", svg)

def generate_q42_grid():
    """Soru 42: 4x10 Boyutlarında Sayı Tablosu (1. Sütun ?, Sonra a, b, c, d)"""
    col_w = 28
    row_h = 28
    start_x = 15
    start_y = 15

    content = []
    for r in range(5):
        y = start_y + r * row_h
        content.append(f'<line x1="{start_x}" y1="{y}" x2="{start_x + 10*col_w}" y2="{y}" class="geo-line" stroke-width="1.2" />')
    for c in range(11):
        x = start_x + c * col_w
        content.append(f'<line x1="{x}" y1="{start_y}" x2="{x}" y2="{start_y + 4*row_h}" class="geo-line" stroke-width="1.2" />')

    values = [
        (0, 0, "?", "geo-text-accent"),
        (1, 0, "?", "geo-text-accent"),
        (2, 0, "?", "geo-text-accent"),
        (3, 0, "?", "geo-text-accent"),
        (0, 1, "a", "geo-text"),
        (1, 2, "b", "geo-text"),
        (2, 3, "c", "geo-text"),
        (3, 4, "d", "geo-text"),
    ]
    for r, c, val, cls in values:
        cx = start_x + c * col_w + col_w / 2
        cy = start_y + r * row_h + row_h / 2
        content.append(f'<text x="{cx}" y="{cy}" class="{cls}">{val}</text>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 310 142" width="100%" height="130">
  <defs>{COMMON_STYLE}</defs>
  {''.join(content)}
</svg>"""
    return save_svg("ales1_q42_grid.svg", svg)

def generate_q43_grid():
    """Soru 43: 4x10 Tablosu (x, y, z ve ? Sütunu)"""
    col_w = 28
    row_h = 28
    start_x = 15
    start_y = 15

    content = []
    for r in range(5):
        y = start_y + r * row_h
        content.append(f'<line x1="{start_x}" y1="{y}" x2="{start_x + 10*col_w}" y2="{y}" class="geo-line" stroke-width="1.2" />')
    for c in range(11):
        x = start_x + c * col_w
        content.append(f'<line x1="{x}" y1="{start_y}" x2="{x}" y2="{start_y + 4*row_h}" class="geo-line" stroke-width="1.2" />')

    values = [
        (0, 3, "z", "geo-text"),
        (1, 1, "y", "geo-text"),
        (2, 1, "z", "geo-text"),
        (3, 4, "x", "geo-text"),
        (3, 6, "y", "geo-text"),
        # Soru işaretleri sütun 5'te (c=5)
        (0, 5, "?", "geo-text-accent"),
        (1, 5, "?", "geo-text-accent"),
        (2, 5, "?", "geo-text-accent"),
        (3, 5, "?", "geo-text-accent"),
    ]
    for r, c, val, cls in values:
        cx = start_x + c * col_w + col_w / 2
        cy = start_y + r * row_h + row_h / 2
        content.append(f'<text x="{cx}" y="{cy}" class="{cls}">{val}</text>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 310 142" width="100%" height="130">
  <defs>{COMMON_STYLE}</defs>
  {''.join(content)}
</svg>"""
    return save_svg("ales1_q43_grid.svg", svg)

def generate_q49_prisms():
    """Soru 49: Dikdörtgenler Prizmaları ve Birleşim Görünümleri"""
    # 2 temel prizma:
    # Sol: 1x2x3 (ön 3, yükseklik 1, derinlik 2)
    # Sağ: 2x3x4 (ön 3, yükseklik 2, derinlik 4)
    # Üst yüz sarı, ön yüz kırmızı/pembe, sağ yüz mavi
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 320" width="100%" height="300">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- Sol Prizma (1 x 2 x 3) -->
  <g transform="translate(30, 20)">
    <!-- Ön Yüz (3 x 1) -->
    <rect x="15" y="45" width="75" height="25" fill="#f43f5e" fill-opacity="0.75" stroke="#f43f5e" stroke-width="1.8" />
    <!-- Üst Yüz -->
    <polygon points="15,45 35,25 110,25 90,45" fill="#f59e0b" fill-opacity="0.8" stroke="#f59e0b" stroke-width="1.8" />
    <!-- Sağ Yüz -->
    <polygon points="90,45 110,25 110,50 90,70" fill="#38bdf8" fill-opacity="0.8" stroke="#38bdf8" stroke-width="1.8" />
    <!-- Ölçüler -->
    <text x="52" y="80" class="geo-text">3</text>
    <text x="5" y="58" class="geo-text">1</text>
    <text x="112" y="65" class="geo-text">2</text>
  </g>

  <!-- Sağ Prizma (2 x 3 x 4) -->
  <g transform="translate(190, 10)">
    <!-- Ön Yüz (3 x 2) -->
    <rect x="15" y="45" width="75" height="50" fill="#f43f5e" fill-opacity="0.75" stroke="#f43f5e" stroke-width="1.8" />
    <!-- Üst Yüz -->
    <polygon points="15,45 45,15 120,15 90,45" fill="#f59e0b" fill-opacity="0.8" stroke="#f59e0b" stroke-width="1.8" />
    <!-- Sağ Yüz -->
    <polygon points="90,45 120,15 120,65 90,95" fill="#38bdf8" fill-opacity="0.8" stroke="#38bdf8" stroke-width="1.8" />
    <!-- Ölçüler -->
    <text x="52" y="105" class="geo-text">3</text>
    <text x="5" y="70" class="geo-text">2</text>
    <text x="122" y="80" class="geo-text">4</text>
  </g>

  <!-- Ayırıcı Çizgi -->
  <line x1="20" y1="125" x2="360" y2="125" stroke="var(--border-subtle, rgba(255,255,255,0.15))" stroke-width="1" />

  <!-- Görünümler: I, II, III -->
  <!-- I. Görünüm (Doğru) -->
  <g transform="translate(30, 140)">
    <text x="10" y="40" class="geo-text-accent" font-weight="700">I.</text>
    <rect x="40" y="25" width="75" height="40" fill="#f59e0b" fill-opacity="0.75" stroke="#f59e0b" stroke-width="1.5" />
    <polygon points="40,25 65,5 140,5 115,25" fill="#f59e0b" fill-opacity="0.75" stroke="#f59e0b" stroke-width="1.5" />
    <polygon points="115,25 140,5 140,45 115,65" fill="#38bdf8" fill-opacity="0.75" stroke="#38bdf8" stroke-width="1.5" />
  </g>

  <!-- II. Görünüm (Yanlış) -->
  <g transform="translate(200, 140)">
    <text x="10" y="40" class="geo-text" font-weight="700">II.</text>
    <rect x="40" y="25" width="75" height="40" fill="#f43f5e" fill-opacity="0.75" stroke="#f43f5e" stroke-width="1.5" />
    <polygon points="40,25 65,5 140,5 115,25" fill="#f59e0b" fill-opacity="0.75" stroke="#f59e0b" stroke-width="1.5" />
    <polygon points="115,25 140,5 140,45 115,65" fill="#38bdf8" fill-opacity="0.75" stroke="#38bdf8" stroke-width="1.5" />
  </g>

  <!-- III. Görünüm (Doğru) -->
  <g transform="translate(115, 225)">
    <text x="10" y="40" class="geo-text-accent" font-weight="700">III.</text>
    <rect x="40" y="15" width="45" height="60" fill="#f43f5e" fill-opacity="0.75" stroke="#f43f5e" stroke-width="1.5" />
    <polygon points="40,15 65,-5 110,-5 85,15" fill="#38bdf8" fill-opacity="0.75" stroke="#38bdf8" stroke-width="1.5" />
    <polygon points="85,15 110,-5 110,55 85,75" fill="#f59e0b" fill-opacity="0.75" stroke="#f59e0b" stroke-width="1.5" />
  </g>
</svg>"""
    return save_svg("ales1_q49_prisms.svg", svg)

def generate_q50_sticks():
    """Soru 50: Masa Üzerindeki Çubuklar (a, b, c, d, e, f)"""
    # Masa: kare çerçeve
    # Sıralama ve üst üste binme:
    # d en altta (dikey sol)
    # b (sol-orta -> sağ-üst)
    # e (sol-alt -> sağ-orta)
    # a (sol-alt -> sağ-alt)
    # f (sol-orta -> sağ-orta)
    # c en üstte (yatay)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 250" width="100%" height="230">
  <defs>{COMMON_STYLE}</defs>
  <!-- Masa Yüzeyi -->
  <rect x="25" y="15" width="230" height="220" rx="8" fill="rgba(244, 63, 94, 0.08)" stroke="#f43f5e" stroke-opacity="0.4" stroke-width="2" />

  <!-- d Çubuğu (Dikey sol) -->
  <g transform="rotate(-6, 65, 120)">
    <rect x="55" y="25" width="20" height="195" rx="3" fill="#cbd5e1" stroke="#334155" stroke-width="1.5" />
    <text x="65" y="38" class="geo-text" fill="#0f172a">d</text>
    <text x="65" y="208" class="geo-text" fill="#0f172a">d</text>
  </g>

  <!-- b Çubuğu -->
  <g transform="rotate(22, 140, 110)">
    <rect x="20" y="100" width="180" height="18" rx="3" fill="#cbd5e1" stroke="#334155" stroke-width="1.5" />
    <text x="190" y="109" class="geo-text" fill="#0f172a">b</text>
  </g>

  <!-- e Çubuğu -->
  <g transform="rotate(38, 140, 130)">
    <rect x="30" y="122" width="180" height="18" rx="3" fill="#cbd5e1" stroke="#334155" stroke-width="1.5" />
    <text x="200" y="131" class="geo-text" fill="#0f172a">e</text>
  </g>

  <!-- a Çubuğu -->
  <g transform="rotate(12, 140, 160)">
    <rect x="25" y="152" width="185" height="18" rx="3" fill="#cbd5e1" stroke="#334155" stroke-width="1.5" />
    <text x="200" y="161" class="geo-text" fill="#0f172a">a</text>
  </g>

  <!-- f Çubuğu -->
  <g transform="rotate(8, 140, 125)">
    <rect x="20" y="116" width="185" height="18" rx="3" fill="#cbd5e1" stroke="#334155" stroke-width="1.5" />
    <text x="195" y="125" class="geo-text" fill="#0f172a">f</text>
  </g>

  <!-- c Çubuğu (En üstte, yatay) -->
  <g>
    <rect x="20" y="108" width="155" height="20" rx="3" fill="#cbd5e1" stroke="#334155" stroke-width="1.8" />
    <text x="165" y="118" class="geo-text" fill="#0f172a">c</text>
  </g>
</svg>"""
    return save_svg("ales1_q50_sticks.svg", svg)

def save_svg(filename: str, content: str):
    path = SVG_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return content, f"/assets/questions/svg/{filename}"

def generate_all_ales1_svgs():
    """2021-ALES/1 için tüm SVG çizimlerini üretir ve haritayı döndürür."""
    m = {}
    m["q21"], m["q21_url"] = generate_q21_calendar()
    m["q25"], m["q25_url"] = generate_q25_balls()
    m["q26"], m["q26_url"] = generate_q26_balls()
    m["q27"], m["q27_url"] = generate_q27_stores_table()
    m["q32"], m["q32_url"] = generate_q32_pie()
    m["q33"], m["q33_url"] = generate_q33_pie()
    m["q34"], m["q34_url"] = generate_q34_pie()
    m["q41"], m["q41_url"] = generate_q41_grid()
    m["q42"], m["q42_url"] = generate_q42_grid()
    m["q43"], m["q43_url"] = generate_q43_grid()
    m["q49"], m["q49_url"] = generate_q49_prisms()
    m["q50"], m["q50_url"] = generate_q50_sticks()
    return m

if __name__ == "__main__":
    res = generate_all_ales1_svgs()
    print(f"Generated {len(res)//2} SVG files for 2021-ALES/1.")
