#!/usr/bin/env python3
"""
scripts/generators/ales2_svg_generator.py
2021-ALES/2 sınavındaki tüm şekil, diyagram ve geometri soruları için
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
      .geo-shaded-yellow { fill: rgba(245, 158, 11, 0.28); stroke: #f59e0b; stroke-width: 2; stroke-linejoin: round; }
      .geo-shaded-purple { fill: rgba(168, 85, 247, 0.28); stroke: #a855f7; stroke-width: 2; stroke-linejoin: round; }
      .geo-shaded-green { fill: rgba(34, 197, 94, 0.28); stroke: #22c55e; stroke-width: 2; stroke-linejoin: round; }
      .geo-shaded-red { fill: rgba(244, 63, 94, 0.28); stroke: #f43f5e; stroke-width: 2; stroke-linejoin: round; }
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

def generate_q20_pie():
    """Soru 20: Daire Grafikleri (Şekil 1: Toplam Dersler, Şekil 2: Zorunlu Dersler)"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 220" width="100%" height="200">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- Şekil 1 (Toplam Dersler) -->
  <g transform="translate(105, 100)">
    <circle cx="0" cy="0" r="70" class="geo-line" />
    <!-- 144° analiz (üst-sağ), 144° cebir (sol), 72° geometri (alt) -->
    <!-- 0° sağ: (70, 0). 144° saat yönü: (70*cos(144°), 70*sin(144°)) = (-56.6, 41.1) -->
    <!-- 216°: (-56.6, -41.1) -->
    <line x1="0" y1="0" x2="70" y2="0" class="geo-line" />
    <line x1="0" y1="0" x2="-56.6" y2="41.1" class="geo-line" />
    <line x1="0" y1="0" x2="-56.6" y2="-41.1" class="geo-line" />
    
    <!-- Alan Dolguları & Etiketler -->
    <text x="18" y="-35" class="geo-text">analiz</text>
    <text x="25" y="-15" class="geo-text-muted">144°</text>

    <text x="-38" y="0" class="geo-text">cebir</text>
    <text x="-15" y="15" class="geo-text-muted">144°</text>

    <text x="0" y="45" class="geo-text">geometri</text>
    <text x="0" y="105" class="geo-text-muted" font-weight="700">Şekil 1</text>
  </g>

  <!-- Şekil 2 (Zorunlu Dersler) -->
  <g transform="translate(315, 100)">
    <circle cx="0" cy="0" r="70" class="geo-line" />
    <!-- 180° analiz (üst yarı: -70 to 70 yatay çizgi) -->
    <line x1="-70" y1="0" x2="70" y2="0" class="geo-line" />
    <!-- 120° geometri (alt sağ: 0° to 120°), 60° cebir (alt sol: 120° to 180°) -->
    <!-- 120°: (70*cos(60°), 70*sin(60°)) = (35, 60.6) -->
    <!-- cebir 60°, geometri 120°: çizgi 120° saat yönü = (70*cos(120), 70*sin(120)) = (-35, 60.6) -->
    <line x1="0" y1="0" x2="35" y2="60.6" class="geo-line" />

    <text x="0" y="-35" class="geo-text">analiz</text>
    <text x="-32" y="30" class="geo-text">cebir</text>
    <text x="-25" y="48" class="geo-text-muted">60°</text>

    <text x="32" y="30" class="geo-text">geometri</text>
    <text x="25" y="48" class="geo-text-muted">120°</text>
    <text x="0" y="105" class="geo-text-muted" font-weight="700">Şekil 2</text>
  </g>
</svg>"""
    return save_svg("ales2_q20_pie.svg", svg)

def generate_q21_map():
    """Soru 21: A, B, C, D, E, F Ülkelerinin Sınır Haritası"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 260" width="100%" height="240">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- B Ülkesi (Sol) -->
  <path d="M 40,80 Q 25,120 45,160 Q 70,180 95,150 L 95,100 Q 80,75 40,80 Z" class="geo-shaded-red" />
  <text x="65" y="125" class="geo-text" font-weight="700">B</text>

  <!-- A Ülkesi (Üst Orta) -->
  <path d="M 95,100 L 95,75 Q 120,50 160,60 L 175,100 L 125,120 Z" class="geo-shaded" />
  <text x="135" y="85" class="geo-text" font-weight="700">A</text>

  <!-- E Ülkesi (En Üst Sağ) -->
  <path d="M 160,60 Q 185,35 225,50 Q 245,75 220,95 L 185,85 Z" class="geo-shaded-yellow" />
  <text x="200" y="65" class="geo-text" font-weight="700">E</text>

  <!-- D Ülkesi (Orta Sağ) -->
  <path d="M 175,100 L 185,85 L 220,95 L 235,135 L 185,150 L 175,100 Z" class="geo-shaded-purple" />
  <text x="200" y="118" class="geo-text" font-weight="700">D</text>

  <!-- C Ülkesi (Alt Orta) -->
  <path d="M 95,150 L 95,100 L 125,120 L 175,100 L 185,150 L 165,190 Q 120,195 95,150 Z" class="geo-shaded-yellow" />
  <text x="140" y="150" class="geo-text" font-weight="700">C</text>

  <!-- F Ülkesi (Alt Sağ) -->
  <path d="M 185,150 L 235,135 Q 255,175 230,205 L 185,195 L 185,150 Z" class="geo-shaded-green" />
  <text x="215" y="170" class="geo-text" font-weight="700">F</text>
</svg>"""
    return save_svg("ales2_q21_map.svg", svg)

def generate_q25_barchart():
    """Soru 25 & 26: Meslek Anketi Tercih Eden / Etmeyen Sütun Grafiği"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 240" width="100%" height="220">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- Eksenler -->
  <line x1="45" y1="185" x2="350" y2="185" class="geo-line" stroke-width="1.8" />
  <line x1="45" y1="185" x2="45" y2="25" class="geo-line" stroke-width="1.8" />
  <text x="45" y="15" class="geo-text-muted">Öğrenci sayısı</text>
  <text x="350" y="200" class="geo-text-muted">Meslek adı</text>

  <!-- Kılavuz Çizgileri -->
  <line x1="45" y1="145" x2="340" y2="145" stroke="var(--border-subtle, rgba(255,255,255,0.08))" stroke-dasharray="3 3" />
  <line x1="45" y1="105" x2="340" y2="105" stroke="var(--border-subtle, rgba(255,255,255,0.08))" stroke-dasharray="3 3" />
  <line x1="45" y1="65" x2="340" y2="65" stroke="var(--border-subtle, rgba(255,255,255,0.08))" stroke-dasharray="3 3" />

  <!-- Sütunlar (A, B, C, D, E) -->
  <!-- A: tercih eden (mavi, h=50), tercih etmeyen (sarı, h=120) -->
  <g transform="translate(65, 0)">
    <rect x="0" y="135" width="18" height="50" class="geo-shaded" />
    <rect x="18" y="65" width="18" height="120" class="geo-shaded-yellow" />
    <text x="18" y="200" class="geo-text">A</text>
  </g>

  <!-- B: tercih eden (mavi, h=60), tercih etmeyen (sarı, h=140) -->
  <g transform="translate(125, 0)">
    <rect x="0" y="125" width="18" height="60" class="geo-shaded" />
    <rect x="18" y="45" width="18" height="140" class="geo-shaded-yellow" />
    <text x="18" y="200" class="geo-text">B</text>
  </g>

  <!-- C: tercih eden (mavi, h=90), tercih etmeyen (sarı, h=75) -->
  <g transform="translate(185, 0)">
    <rect x="0" y="95" width="18" height="90" class="geo-shaded" />
    <rect x="18" y="110" width="18" height="75" class="geo-shaded-yellow" />
    <text x="18" y="200" class="geo-text">C</text>
  </g>

  <!-- D: tercih eden (mavi, h=72), tercih etmeyen (sarı, h=85) -->
  <g transform="translate(245, 0)">
    <rect x="0" y="113" width="18" height="72" class="geo-shaded" />
    <rect x="18" y="100" width="18" height="85" class="geo-shaded-yellow" />
    <text x="18" y="200" class="geo-text">D</text>
  </g>

  <!-- E: tercih eden (mavi, h=140), tercih etmeyen (sarı, h=40) -->
  <g transform="translate(305, 0)">
    <rect x="0" y="45" width="18" height="140" class="geo-shaded" />
    <rect x="18" y="145" width="18" height="40" class="geo-shaded-yellow" />
    <text x="18" y="200" class="geo-text">E</text>
  </g>

  <!-- Lejant -->
  <rect x="180" y="25" width="14" height="14" class="geo-shaded" />
  <text x="235" y="32" class="geo-text-muted">: tercih eden</text>
  <rect x="180" y="45" width="14" height="14" class="geo-shaded-yellow" />
  <text x="242" y="52" class="geo-text-muted">: tercih etmeyen</text>
</svg>"""
    return save_svg("ales2_q25_barchart.svg", svg)

def generate_q27_network():
    """Soru 27: 5 Daire ve 6 Kare Mutlak Fark Düzeneği (a, b ve 1'ler)"""
    # 3 üst daire: x = 60, 160, 260, y = 45
    # 2 alt daire: x = 110, 210, y = 145
    # 2 üst kare: (110, 45) [a], (210, 45) [b]
    # 4 alt kare: (85, 95) [1], (135, 95) [1], (185, 95) [1], (235, 95) [1]
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 190" width="100%" height="170">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- Bağlantı Çizgileri -->
  <line x1="60" y1="45" x2="260" y2="45" class="geo-line" stroke-width="1.8" />
  <line x1="60" y1="45" x2="110" y2="145" class="geo-line" stroke-width="1.8" />
  <line x1="160" y1="45" x2="110" y2="145" class="geo-line" stroke-width="1.8" />
  <line x1="160" y1="45" x2="210" y2="145" class="geo-line" stroke-width="1.8" />
  <line x1="260" y1="45" x2="210" y2="145" class="geo-line" stroke-width="1.8" />

  <!-- Kareler (Önce kareler arka plan dolgusuyla çizilir) -->
  <!-- a karesi -->
  <rect x="98" y="33" width="24" height="24" rx="3" fill="var(--bg-card, #1e293b)" stroke="#f59e0b" stroke-width="1.8" />
  <text x="110" y="45" class="geo-text-accent">a</text>

  <!-- b karesi -->
  <rect x="198" y="33" width="24" height="24" rx="3" fill="var(--bg-card, #1e293b)" stroke="#f59e0b" stroke-width="1.8" />
  <text x="210" y="45" class="geo-text-accent">b</text>

  <!-- 4 Alt Kare (her biri '1') -->
  <rect x="73" y="83" width="24" height="24" rx="3" fill="var(--bg-card, #1e293b)" stroke="#38bdf8" stroke-width="1.5" />
  <text x="85" y="95" class="geo-text">1</text>

  <rect x="123" y="83" width="24" height="24" rx="3" fill="var(--bg-card, #1e293b)" stroke="#38bdf8" stroke-width="1.5" />
  <text x="135" y="95" class="geo-text">1</text>

  <rect x="173" y="83" width="24" height="24" rx="3" fill="var(--bg-card, #1e293b)" stroke="#38bdf8" stroke-width="1.5" />
  <text x="185" y="95" class="geo-text">1</text>

  <rect x="223" y="83" width="24" height="24" rx="3" fill="var(--bg-card, #1e293b)" stroke="#38bdf8" stroke-width="1.5" />
  <text x="235" y="95" class="geo-text">1</text>

  <!-- 5 Daire -->
  <circle cx="60" cy="45" r="16" fill="var(--bg-card, #1e293b)" stroke="var(--text-primary, #f1f5f9)" stroke-width="2" />
  <circle cx="160" cy="45" r="16" fill="var(--bg-card, #1e293b)" stroke="var(--text-primary, #f1f5f9)" stroke-width="2" />
  <circle cx="260" cy="45" r="16" fill="var(--bg-card, #1e293b)" stroke="var(--text-primary, #f1f5f9)" stroke-width="2" />

  <circle cx="110" cy="145" r="16" fill="var(--bg-card, #1e293b)" stroke="var(--text-primary, #f1f5f9)" stroke-width="2" />
  <circle cx="210" cy="145" r="16" fill="var(--bg-card, #1e293b)" stroke="var(--text-primary, #f1f5f9)" stroke-width="2" />
</svg>"""
    return save_svg("ales2_q27_network.svg", svg)

def generate_q28_network():
    """Soru 28: Daire ve Kare Mutlak Fark Düzeneği (4, y, 2, 3, 2, x, z)"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 190" width="100%" height="170">
  <defs>{COMMON_STYLE}</defs>
  
  <line x1="60" y1="45" x2="260" y2="45" class="geo-line" stroke-width="1.8" />
  <line x1="60" y1="45" x2="110" y2="145" class="geo-line" stroke-width="1.8" />
  <line x1="160" y1="45" x2="110" y2="145" class="geo-line" stroke-width="1.8" />
  <line x1="160" y1="45" x2="210" y2="145" class="geo-line" stroke-width="1.8" />
  <line x1="260" y1="45" x2="210" y2="145" class="geo-line" stroke-width="1.8" />

  <!-- Kareler -->
  <rect x="98" y="33" width="24" height="24" rx="3" fill="var(--bg-card, #1e293b)" stroke="#38bdf8" stroke-width="1.5" />
  <rect x="198" y="33" width="24" height="24" rx="3" fill="var(--bg-card, #1e293b)" stroke="#f59e0b" stroke-width="1.8" />
  <text x="210" y="45" class="geo-text-accent">z</text>

  <rect x="73" y="83" width="24" height="24" rx="3" fill="var(--bg-card, #1e293b)" stroke="#38bdf8" stroke-width="1.5" />
  <text x="85" y="95" class="geo-text">2</text>

  <rect x="123" y="83" width="24" height="24" rx="3" fill="var(--bg-card, #1e293b)" stroke="#38bdf8" stroke-width="1.5" />
  <text x="135" y="95" class="geo-text">3</text>

  <rect x="173" y="83" width="24" height="24" rx="3" fill="var(--bg-card, #1e293b)" stroke="#38bdf8" stroke-width="1.5" />
  <text x="185" y="95" class="geo-text">2</text>

  <rect x="223" y="83" width="24" height="24" rx="3" fill="var(--bg-card, #1e293b)" stroke="#f59e0b" stroke-width="1.8" />
  <text x="235" y="95" class="geo-text-accent">x</text>

  <!-- Daireler: Sol üst = 4, Sağ üst = y -->
  <circle cx="60" cy="45" r="16" fill="var(--bg-card, #1e293b)" stroke="var(--text-primary, #f1f5f9)" stroke-width="2" />
  <text x="60" y="45" class="geo-text">4</text>

  <circle cx="160" cy="45" r="16" fill="var(--bg-card, #1e293b)" stroke="var(--text-primary, #f1f5f9)" stroke-width="2" />

  <circle cx="260" cy="45" r="16" fill="var(--bg-card, #1e293b)" stroke="var(--text-primary, #f1f5f9)" stroke-width="2" />
  <text x="260" y="45" class="geo-text-accent">y</text>

  <circle cx="110" cy="145" r="16" fill="var(--bg-card, #1e293b)" stroke="var(--text-primary, #f1f5f9)" stroke-width="2" />
  <circle cx="210" cy="145" r="16" fill="var(--bg-card, #1e293b)" stroke="var(--text-primary, #f1f5f9)" stroke-width="2" />
</svg>"""
    return save_svg("ales2_q28_network.svg", svg)

def generate_q35_scale():
    """Soru 35: Eşit Kollu Terazi (Dengede: 1 Kare + 2 Üçgen = 1 Üçgen + 3 Daire)"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 160" width="100%" height="150">
  <defs>{COMMON_STYLE}</defs>
  <!-- Terazi Direği ve Tabanı -->
  <line x1="140" y1="40" x2="140" y2="135" class="geo-line" stroke-width="3" />
  <line x1="115" y1="135" x2="165" y2="135" class="geo-line" stroke-width="4" stroke-linecap="round" />
  <polygon points="140,30 132,45 148,45" fill="var(--text-primary, #f1f5f9)" />

  <!-- Yatay Kol -->
  <line x1="50" y1="40" x2="230" y2="40" class="geo-line" stroke-width="3" />

  <!-- Sol Kefe -->
  <line x1="50" y1="40" x2="30" y2="85" class="geo-sec" stroke-width="1.5" />
  <line x1="50" y1="40" x2="70" y2="85" class="geo-sec" stroke-width="1.5" />
  <line x1="25" y1="85" x2="75" y2="85" class="geo-line" stroke-width="2.5" />
  <!-- Sol Cisimler: 1 Kare, 2 Üçgen -->
  <rect x="30" y="68" width="15" height="15" class="geo-shaded" />
  <polygon points="53,68 46,83 60,83" class="geo-shaded-yellow" />
  <polygon points="67,68 60,83 74,83" class="geo-shaded-yellow" />

  <!-- Sağ Kefe -->
  <line x1="230" y1="40" x2="210" y2="85" class="geo-sec" stroke-width="1.5" />
  <line x1="230" y1="40" x2="250" y2="85" class="geo-sec" stroke-width="1.5" />
  <line x1="205" y1="85" x2="255" y2="85" class="geo-line" stroke-width="2.5" />
  <!-- Sağ Cisimler: 1 Üçgen, 3 Daire -->
  <polygon points="214,68 207,83 221,83" class="geo-shaded-yellow" />
  <circle cx="228" cy="76" r="6" class="geo-shaded-red" />
  <circle cx="240" cy="76" r="6" class="geo-shaded-red" />
  <circle cx="234" cy="64" r="6" class="geo-shaded-red" />
</svg>"""
    return save_svg("ales2_q35_scale.svg", svg)

def generate_q36_scale():
    """Soru 36: 2 Terazi (1. Terazi Dengede, 2. Terazi Dengesiz)"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 180" width="100%" height="165">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- 1. Terazi (Dengede) -->
  <g transform="translate(10, 10)">
    <line x1="100" y1="40" x2="100" y2="135" class="geo-line" stroke-width="2.5" />
    <line x1="80" y1="135" x2="120" y2="135" class="geo-line" stroke-width="3" />
    <line x1="30" y1="40" x2="170" y2="40" class="geo-line" stroke-width="2.5" />
    
    <!-- Sol Kefe: 1 daire, 1 üçgen, 1 kare -->
    <line x1="30" y1="40" x2="15" y2="80" class="geo-sec" stroke-width="1.2" />
    <line x1="30" y1="40" x2="45" y2="80" class="geo-sec" stroke-width="1.2" />
    <line x1="10" y1="80" x2="50" y2="80" class="geo-line" stroke-width="2" />
    <circle cx="18" cy="72" r="5" class="geo-shaded-red" />
    <polygon points="28,65 23,78 33,78" class="geo-shaded-yellow" />
    <rect x="36" y="65" width="12" height="13" class="geo-shaded" />

    <!-- Sağ Kefe: 3 daire, 1 kare -->
    <line x1="170" y1="40" x2="155" y2="80" class="geo-sec" stroke-width="1.2" />
    <line x1="170" y1="40" x2="185" y2="80" class="geo-sec" stroke-width="1.2" />
    <line x1="150" y1="80" x2="190" y2="80" class="geo-line" stroke-width="2" />
    <circle cx="158" cy="73" r="5" class="geo-shaded-red" />
    <circle cx="168" cy="73" r="5" class="geo-shaded-red" />
    <circle cx="163" cy="63" r="5" class="geo-shaded-red" />
    <rect x="176" y="66" width="12" height="13" class="geo-shaded" />

    <text x="100" y="155" class="geo-text-muted" font-weight="700">1. terazi</text>
  </g>

  <!-- 2. Terazi (Dengede değil: Sol kefe daha aşağıda) -->
  <g transform="translate(220, 10)">
    <line x1="100" y1="40" x2="100" y2="135" class="geo-line" stroke-width="2.5" />
    <line x1="80" y1="135" x2="120" y2="135" class="geo-line" stroke-width="3" />
    <!-- Eğik Kol: sol aşağıda (y=50), sağ yukarıda (y=30) -->
    <line x1="30" y1="50" x2="170" y2="30" class="geo-line" stroke-width="2.5" />

    <!-- Sol Kefe: 1 kare, 1 üçgen (Aşağıda) -->
    <line x1="30" y1="50" x2="15" y2="95" class="geo-sec" stroke-width="1.2" />
    <line x1="30" y1="50" x2="45" y2="95" class="geo-sec" stroke-width="1.2" />
    <line x1="10" y1="95" x2="50" y2="95" class="geo-line" stroke-width="2" />
    <rect x="16" y="80" width="13" height="13" class="geo-shaded" />
    <polygon points="38,80 32,94 44,94" class="geo-shaded-yellow" />

    <!-- Sağ Kefe: 3 üçgen, 1 daire (Yukarıda) -->
    <line x1="170" y1="30" x2="155" y2="70" class="geo-sec" stroke-width="1.2" />
    <line x1="170" y1="30" x2="185" y2="70" class="geo-sec" stroke-width="1.2" />
    <line x1="150" y1="70" x2="190" y2="70" class="geo-line" stroke-width="2" />
    <polygon points="158,56 153,69 163,69" class="geo-shaded-yellow" />
    <polygon points="168,56 163,69 173,69" class="geo-shaded-yellow" />
    <polygon points="178,56 173,69 183,69" class="geo-shaded-yellow" />
    <circle cx="168" cy="46" r="4.5" class="geo-shaded-red" />

    <text x="100" y="155" class="geo-text-muted" font-weight="700">2. terazi</text>
  </g>
</svg>"""
    return save_svg("ales2_q36_scale.svg", svg)

def generate_q37_scale():
    """Soru 37: 2 Terazi (Her İkisi de Dengede)"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 180" width="100%" height="165">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- 1. Terazi (3 kare = 2 üçgen + 1 daire) -->
  <g transform="translate(10, 10)">
    <line x1="100" y1="40" x2="100" y2="135" class="geo-line" stroke-width="2.5" />
    <line x1="80" y1="135" x2="120" y2="135" class="geo-line" stroke-width="3" />
    <line x1="30" y1="40" x2="170" y2="40" class="geo-line" stroke-width="2.5" />
    
    <!-- Sol: 3 Kare -->
    <line x1="30" y1="40" x2="15" y2="80" class="geo-sec" stroke-width="1.2" />
    <line x1="30" y1="40" x2="45" y2="80" class="geo-sec" stroke-width="1.2" />
    <line x1="10" y1="80" x2="50" y2="80" class="geo-line" stroke-width="2" />
    <rect x="15" y="66" width="12" height="12" class="geo-shaded" />
    <rect x="29" y="66" width="12" height="12" class="geo-shaded" />
    <rect x="22" y="52" width="12" height="12" class="geo-shaded" />

    <!-- Sağ: 2 Üçgen, 1 Daire -->
    <line x1="170" y1="40" x2="155" y2="80" class="geo-sec" stroke-width="1.2" />
    <line x1="170" y1="40" x2="185" y2="80" class="geo-sec" stroke-width="1.2" />
    <line x1="150" y1="80" x2="190" y2="80" class="geo-line" stroke-width="2" />
    <polygon points="160,66 154,79 166,79" class="geo-shaded-yellow" />
    <polygon points="172,66 166,79 178,79" class="geo-shaded-yellow" />
    <circle cx="184" cy="72" r="5" class="geo-shaded-red" />
  </g>

  <!-- 2. Terazi (1 kare + 1 üçgen = 2 daire) -->
  <g transform="translate(220, 10)">
    <line x1="100" y1="40" x2="100" y2="135" class="geo-line" stroke-width="2.5" />
    <line x1="80" y1="135" x2="120" y2="135" class="geo-line" stroke-width="3" />
    <line x1="30" y1="40" x2="170" y2="40" class="geo-line" stroke-width="2.5" />

    <!-- Sol: 1 Kare, 1 Üçgen -->
    <line x1="30" y1="40" x2="15" y2="80" class="geo-sec" stroke-width="1.2" />
    <line x1="30" y1="40" x2="45" y2="80" class="geo-sec" stroke-width="1.2" />
    <line x1="10" y1="80" x2="50" y2="80" class="geo-line" stroke-width="2" />
    <rect x="16" y="66" width="13" height="13" class="geo-shaded" />
    <polygon points="38,66 32,80 44,80" class="geo-shaded-yellow" />

    <!-- Sağ: 2 Daire -->
    <line x1="170" y1="40" x2="155" y2="80" class="geo-sec" stroke-width="1.2" />
    <line x1="170" y1="40" x2="185" y2="80" class="geo-sec" stroke-width="1.2" />
    <line x1="150" y1="80" x2="190" y2="80" class="geo-line" stroke-width="2" />
    <circle cx="163" cy="72" r="6" class="geo-shaded-red" />
    <circle cx="177" cy="72" r="6" class="geo-shaded-red" />
  </g>
</svg>"""
    return save_svg("ales2_q37_scale.svg", svg)

def generate_q41_table():
    """Soru 41: 3x4 Tablo Boyama (a, b, c, d ve Mavi Boyalı Hücreler)"""
    w, h = 42, 34
    sx, sy = 25, 20
    # Mavi boyalılar: (0,0), (0,2), (1,1), (1,2)
    blues = {(0,0), (0,2), (1,1), (1,2)}

    cells = []
    # Grid
    for r in range(3):
        for c in range(4):
            x = sx + c*w
            y = sy + r*h
            is_blue = (r, c) in blues
            cls = 'class="geo-shaded"' if is_blue else 'fill="none" stroke="var(--text-primary, #f1f5f9)" stroke-width="1.5"'
            cells.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" {cls} />')

    # Değerler:
    # Row 0: Col 0 blue, Col 1 'b', Col 2 'c' (blue), Col 3 'd'
    # Row 1: Col 0 is 7, Col 1 is 12 (blue), Col 2 is 10 (blue), Col 3 is 2
    # Row 2: Col 1 is 'a', Col 2 is 3
    texts = [
        (0, 1, "b", "geo-text"),
        (0, 2, "c", "geo-text-accent"),
        (0, 3, "d", "geo-text"),
        (1, 0, "7", "geo-text"),
        (1, 1, "12", "geo-text-accent"),
        (1, 2, "10", "geo-text-accent"),
        (1, 3, "2", "geo-text"),
        (2, 1, "a", "geo-text"),
        (2, 2, "3", "geo-text"),
    ]
    for r, c, val, cls in texts:
        cx = sx + c*w + w/2
        cy = sy + r*h + h/2
        cells.append(f'<text x="{cx}" y="{cy}" class="{cls}">{val}</text>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 145" width="100%" height="135">
  <defs>{COMMON_STYLE}</defs>
  {''.join(cells)}
</svg>"""
    return save_svg("ales2_q41_table.svg", svg)

def generate_q42_table():
    """Soru 42: 3x4 Tablo Boyama (Boyanmamış Tablo: 1..12 Sayıları)"""
    w, h = 42, 34
    sx, sy = 25, 20
    cells = []
    # Grid
    for r in range(3):
        for c in range(4):
            x = sx + c*w
            y = sy + r*h
            cells.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="var(--text-primary, #f1f5f9)" stroke-width="1.5" />')

    # Row 0: 1, 6, 7, 11
    # Row 1: 5, 3, 12, 10
    # Row 2: 2, 4, 9, 8
    nums = [
        [1, 6, 7, 11],
        [5, 3, 12, 10],
        [2, 4, 9, 8]
    ]
    for r in range(3):
        for c in range(4):
            cx = sx + c*w + w/2
            cy = sy + r*h + h/2
            cells.append(f'<text x="{cx}" y="{cy}" class="geo-text">{nums[r][c]}</text>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 145" width="100%" height="135">
  <defs>{COMMON_STYLE}</defs>
  {''.join(cells)}
</svg>"""
    return save_svg("ales2_q42_table.svg", svg)

def generate_q43_table():
    """Soru 43: 3x4 Tablo Boyama (Tamamlanmış Tablo ve x Bilinmeyeni)"""
    w, h = 42, 34
    sx, sy = 25, 20
    # Boyalı hücreler: (0,0), (0,1), (0,2), (1,0), (1,2)
    blues = {(0,0), (0,1), (0,2), (1,0), (1,2)}

    cells = []
    for r in range(3):
        for c in range(4):
            x = sx + c*w
            y = sy + r*h
            cls = 'class="geo-shaded"' if (r, c) in blues else 'fill="none" stroke="var(--text-primary, #f1f5f9)" stroke-width="1.5"'
            cells.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" {cls} />')

    # Değerler: Row 1 Col 1 = 9, Row 1 Col 3 = 3, Row 2 Col 1 = x
    texts = [
        (1, 1, "9", "geo-text"),
        (1, 3, "3", "geo-text"),
        (2, 1, "x", "geo-text-accent"),
    ]
    for r, c, val, cls in texts:
        cx = sx + c*w + w/2
        cy = sy + r*h + h/2
        cells.append(f'<text x="{cx}" y="{cy}" class="{cls}">{val}</text>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 145" width="100%" height="135">
  <defs>{COMMON_STYLE}</defs>
  {''.join(cells)}
</svg>"""
    return save_svg("ales2_q43_table.svg", svg)

def generate_q44_triangle():
    """Soru 44: İkizkenar Üçgen ABC (|AB|=|AC|, 38°, 81°, x)"""
    # A = (50, 230), B = (270, 230), C = (160, 50)
    # D noktası BC üzerinde.
    # m(CAD) = 38°, m(ADC) = 81°, m(BAD) = x
    # Hesap: C açısı = 180 - (38 + 81) = 61°.
    # |AB| = |AC| => B açısı = 61°. A tepe açısı = 180 - 122 = 58°.
    # x = m(BAD) = 58 - 38 = 20°.
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 270" width="100%" height="250">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- ABC Üçgeni -->
  <polygon points="160,45 45,225 275,225" class="geo-line" />
  
  <!-- D noktası BC üzerinde: C=(160,45), B=(275,225) -->
  <!-- D koordinatı: t ≈ 0.65 => (160 + 0.65*115, 45 + 0.65*180) = (235, 162) -->
  <line x1="45" y1="225" x2="235" y2="162" class="geo-sec" />

  <!-- Eşitlik İşaretleri (|AB| = |AC|) -->
  <!-- AC üzerinde çift çizgi -->
  <line x1="97" y1="130" x2="108" y2="140" class="geo-line" stroke-width="1.8" />
  <line x1="102" y1="126" x2="113" y2="136" class="geo-line" stroke-width="1.8" />
  <!-- AB üzerinde çift çizgi -->
  <line x1="155" y1="220" x2="155" y2="230" class="geo-line" stroke-width="1.8" />
  <line x1="160" y1="220" x2="160" y2="230" class="geo-line" stroke-width="1.8" />

  <!-- 38° Açı Yayı (A köşesinde üst parça) -->
  <path d="M 67,190 A 35,35 0 0,1 78,202" class="geo-angle-arc" />
  <text x="96" y="195" class="geo-text-muted">38°</text>

  <!-- x Açı Yayı (A köşesinde alt parça) -->
  <path d="M 78,202 A 38,38 0 0,1 82,225" class="geo-angle-arc" stroke-width="2" />
  <text x="102" y="218" class="geo-text-accent">x</text>

  <!-- 81° Açı Yayı (D noktasında) -->
  <path d="M 216,168 A 20,20 0 0,1 228,148" class="geo-angle-arc" />
  <text x="200" y="152" class="geo-text-muted">81°</text>

  <!-- Nokta Etiketleri -->
  <text x="160" y="30" class="geo-text">C</text>
  <text x="30" y="232" class="geo-text">A</text>
  <text x="290" y="232" class="geo-text">B</text>
  <text x="250" y="162" class="geo-text">D</text>
</svg>"""
    return save_svg("ales2_q44_triangle.svg", svg)

def generate_q45_triangle():
    """Soru 45: Eşkenar Üçgen ABC (|AC|=8, |CE|=|EB|, |AD|=|DE|, Boyalı DBE Alanı)"""
    # Eşkenar üçgen: A=(45, 230), B=(265, 230), C=(155, 39.5)
    # E orta nokta BC: C=(155, 39.5), B=(265, 230) => E=(210, 134.8)
    # D noktası AB üzerinde: |AD| = |DE|
    # D ≈ (135, 230)
    # Boyalı üçgen DBE: noktaları D=(135, 230), B=(265, 230), E=(210, 134.8)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 310 270" width="100%" height="250">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- Boyalı DBE Üçgeni -->
  <polygon points="135,230 265,230 210,135" class="geo-shaded" />

  <!-- ABC Eşkenar Üçgeni -->
  <polygon points="155,40 45,230 265,230" class="geo-line" />
  
  <!-- [DE] Doğru Parçası -->
  <line x1="135" y1="230" x2="210" y2="135" class="geo-sec" stroke-width="2.2" />

  <!-- Eşitlik İşaretleri (|CE| = |EB|) -->
  <line x1="180" y1="85" x2="185" y2="90" class="geo-line" stroke-width="1.8" />
  <line x1="235" y1="180" x2="240" y2="185" class="geo-line" stroke-width="1.8" />

  <!-- Eşitlik İşaretleri (|AD| = |DE|) -->
  <line x1="88" y1="225" x2="88" y2="235" class="geo-line" stroke-width="1.8" />
  <line x1="92" y1="225" x2="92" y2="235" class="geo-line" stroke-width="1.8" />
  <line x1="170" y1="180" x2="178" y2="186" class="geo-line" stroke-width="1.8" />
  <line x1="173" y1="176" x2="181" y2="182" class="geo-line" stroke-width="1.8" />

  <!-- Kenar Uzunluğu: |AC| = 8 -->
  <text x="85" y="125" class="geo-text-muted">8</text>

  <!-- Noktalar -->
  <text x="155" y="25" class="geo-text">C</text>
  <text x="30" y="238" class="geo-text">A</text>
  <text x="280" y="238" class="geo-text">B</text>
  <text x="135" y="246" class="geo-text">D</text>
  <text x="228" y="135" class="geo-text">E</text>
</svg>"""
    return save_svg("ales2_q45_triangle.svg", svg)

def generate_q46_rhombus():
    """Soru 46: Eşkenar Dörtgen ABCD ve Eşkenar Üçgen AFE (30° Açıları, EF=6)"""
    # A = (50, 130)
    # D = (160, 35)
    # B = (130, 235)
    # C = (240, 140)
    # AFE eşkenar üçgen, EF = 6
    # E on CD, F on BC
    # m(DAE) = m(BAF) = 30°
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 310 270" width="100%" height="250">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- ABCD Eşkenar Dörtgeni -->
  <polygon points="50,130 160,35 240,140 130,235" class="geo-line" />

  <!-- AFE Eşkenar Üçgeni -->
  <!-- E=(200, 88) on CD, F=(185, 188) on BC -->
  <polygon points="50,130 200,88 185,188" class="geo-sec" fill="rgba(56, 189, 248, 0.12)" />

  <!-- 30° Açı Yayları -->
  <text x="115" y="65" class="geo-text-muted">30°</text>
  <text x="98" y="180" class="geo-text-muted">30°</text>

  <!-- Kenar Uzunluğu EF = 6 -->
  <text x="202" y="138" class="geo-text-accent">6</text>

  <!-- Noktalar -->
  <text x="32" y="130" class="geo-text">A</text>
  <text x="160" y="20" class="geo-text">D</text>
  <text x="120" y="250" class="geo-text">B</text>
  <text x="255" y="140" class="geo-text">C</text>
  <text x="212" y="82" class="geo-text">E</text>
  <text x="195" y="200" class="geo-text">F</text>
</svg>"""
    return save_svg("ales2_q46_rhombus.svg", svg)

def generate_q47_rectangles():
    """Soru 47: İki Dikdörtgen ABCD ve EBMN (A-K-L-M Doğrusal, Boyalı Alan)"""
    # Dikdörtgen ABCD: A=(30, 190), B=(170, 190), C=(170, 90), D=(30, 90)
    # E noktası AB üzerinde: |AE| = 6, |EB| = 8 => A=(30), E=(90), B=(170). Genişlik=140.
    # Dikdörtgen EBMN: E=(90, 190), B=(170, 190), M=(170, 40), N=(90, 40)
    # C noktası BM üzerinde: B=(170, 190), C=(170, 90), M=(170, 40) => |BC|=8 (100px), |CM|=5 (50px).
    # A, K, L, M doğrusal doğrusu: A=(30, 190) to M=(170, 40).
    # K on CD, L on NM.
    # Boyalı bölge: çokgen
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 290 240" width="100%" height="220">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- Boyalı Alan -->
  <polygon points="90,190 170,190 170,90 90,90" class="geo-shaded" />
  
  <!-- ABCD Dikdörtgeni -->
  <rect x="30" y="90" width="140" height="100" class="geo-line" />
  
  <!-- EBMN Dikdörtgeni -->
  <rect x="90" y="40" width="80" height="150" class="geo-line" />

  <!-- Doğrusal Doğru (A-K-L-M) -->
  <line x1="30" y1="190" x2="170" y2="40" class="geo-accent" stroke-width="2.2" />

  <!-- Ölçüler -->
  <text x="60" y="205" class="geo-text">6</text>
  <text x="130" y="205" class="geo-text">8</text>
  <text x="180" y="140" class="geo-text">8</text>
  <text x="180" y="65" class="geo-text">5</text>

  <!-- Noktalar -->
  <text x="20" y="195" class="geo-text">A</text>
  <text x="90" y="205" class="geo-text">E</text>
  <text x="175" y="205" class="geo-text">B</text>
  <text x="182" y="95" class="geo-text">C</text>
  <text x="180" y="35" class="geo-text">M</text>
  <text x="20" y="85" class="geo-text">D</text>
  <text x="82" y="85" class="geo-text">K</text>
  <text x="100" y="105" class="geo-text">L</text>
</svg>"""
    return save_svg("ales2_q47_rectangles.svg", svg)

def generate_q48_circle():
    """Soru 48: Çember [AB] Çaplı (O Merkez, 30°, 110°, x)"""
    # Merkez O=(150, 130), R=90
    # A=(60, 130), B=(240, 130)
    # CAB = 30° => C=(150 - 90*cos(60°), 130 - 90*sin(60°)) = (195, 52)
    # AB ve CD doğruları E noktasında kesişiyor.
    # BEC = 110°
    # BOD = x
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 310 260" width="100%" height="240">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- Çember -->
  <circle cx="150" cy="130" r="90" class="geo-line" />
  
  <!-- AB Çapı -->
  <line x1="60" y1="130" x2="240" y2="130" class="geo-line" />

  <!-- AC Kirişi -->
  <line x1="60" y1="130" x2="195" y2="52" class="geo-line" />

  <!-- CD Kirişi (E=(185, 130) üzerinden geçer) -->
  <line x1="195" y1="52" x2="175" y2="208" class="geo-sec" stroke-width="2.2" />

  <!-- OD Yarıçapı -->
  <line x1="150" y1="130" x2="175" y2="208" class="geo-line" stroke-dasharray="3 3" />

  <!-- Açı Yayları -->
  <!-- CAB = 30° -->
  <path d="M 85,130 A 25,25 0 0,0 82,118" class="geo-angle-arc" />
  <text x="105" y="120" class="geo-text-muted">30°</text>

  <!-- BEC = 110° -->
  <path d="M 190,105 A 25,25 0 0,0 172,130" class="geo-angle-arc" />
  <text x="215" y="105" class="geo-text-muted">110°</text>

  <!-- BOD = x -->
  <path d="M 166,130 A 16,16 0 0,1 158,145" class="geo-angle-arc" stroke-width="2" />
  <text x="160" y="155" class="geo-text-accent">x</text>

  <!-- Noktalar -->
  <circle cx="150" cy="130" r="2.5" class="geo-point" />
  <text x="142" y="142" class="geo-text">O</text>
  <text x="45" y="130" class="geo-text">A</text>
  <text x="252" y="130" class="geo-text">B</text>
  <text x="202" y="42" class="geo-text">C</text>
  <text x="180" y="222" class="geo-text">D</text>
  <text x="195" y="142" class="geo-text">E</text>
</svg>"""
    return save_svg("ales2_q48_circle.svg", svg)

def generate_q49_keypad():
    """Soru 49: 3x3 Tuş Takımı Ekran Kilidi Çizge Şifresi ve Seçenekler"""
    # 3x3 Grid: 1..9
    # Örneğin 4-3-6-7-8-9 şifresi sarıya boyalı
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 260" width="100%" height="240">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- Telefon Gövdesi Mockup -->
  <rect x="70" y="10" width="180" height="240" rx="16" fill="var(--bg-card, #1e293b)" stroke="var(--border-subtle, rgba(255,255,255,0.18))" stroke-width="2" />
  <rect x="140" y="18" width="40" height="4" rx="2" fill="var(--text-muted, #64748b)" />

  <!-- 3x3 Tuşlar -->
  <!-- 4-3-6-7-8-9 Örnek Çizge Bağlantı Çizgisi: 4 (105,125) -> 3 (215,75) -> 6 (215,125) -> 7 (105,175) -> 8 (160,175) -> 9 (215,175) -->
  <polyline points="105,125 215,75 215,125 105,175 160,175 215,175" stroke="#f59e0b" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none" />

  <!-- Tuş Daireleri -->
  <!-- Satır 1: 1, 2, 3 (3 sarı) -->
  <circle cx="105" cy="75" r="16" fill="var(--bg-secondary, #334155)" stroke="var(--border-subtle, rgba(255,255,255,0.1))" />
  <text x="105" y="75" class="geo-text">1</text>

  <circle cx="160" cy="75" r="16" fill="var(--bg-secondary, #334155)" stroke="var(--border-subtle, rgba(255,255,255,0.1))" />
  <text x="160" y="75" class="geo-text">2</text>

  <circle cx="215" cy="75" r="16" fill="#f59e0b" fill-opacity="0.85" stroke="#f59e0b" stroke-width="2" />
  <text x="215" y="75" class="geo-text" fill="#0f172a">3</text>

  <!-- Satır 2: 4, 5, 6 (4 ve 6 sarı) -->
  <circle cx="105" cy="125" r="16" fill="#f59e0b" fill-opacity="0.85" stroke="#f59e0b" stroke-width="2" />
  <text x="105" y="125" class="geo-text" fill="#0f172a">4</text>

  <circle cx="160" cy="125" r="16" fill="var(--bg-secondary, #334155)" stroke="var(--border-subtle, rgba(255,255,255,0.1))" />
  <text x="160" y="125" class="geo-text">5</text>

  <circle cx="215" cy="125" r="16" fill="#f59e0b" fill-opacity="0.85" stroke="#f59e0b" stroke-width="2" />
  <text x="215" y="125" class="geo-text" fill="#0f172a">6</text>

  <!-- Satır 3: 7, 8, 9 (hepsi sarı) -->
  <circle cx="105" cy="175" r="16" fill="#f59e0b" fill-opacity="0.85" stroke="#f59e0b" stroke-width="2" />
  <text x="105" y="175" class="geo-text" fill="#0f172a">7</text>

  <circle cx="160" cy="175" r="16" fill="#f59e0b" fill-opacity="0.85" stroke="#f59e0b" stroke-width="2" />
  <text x="160" y="175" class="geo-text" fill="#0f172a">8</text>

  <circle cx="215" cy="175" r="16" fill="#f59e0b" fill-opacity="0.85" stroke="#f59e0b" stroke-width="2" />
  <text x="215" y="175" class="geo-text" fill="#0f172a">9</text>

  <!-- Alt Bilgi -->
  <text x="160" y="222" class="geo-text-muted" font-size="11">Örnek: 4-3-6-7-8-9 Şifresi</text>
</svg>"""
    return save_svg("ales2_q49_keypad.svg", svg)

def generate_q50_cube_mockups():
    """Soru 50: Küp Oda İç Tasarım Maketleri (I, II, III, IV)"""
    # 4 izometrik oda maketi
    # Sol duvar, sağ duvar, zemin
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 320" width="100%" height="300">
  <defs>{COMMON_STYLE}</defs>
  
  <!-- Maket I (Sol: Pencere, Sağ: TV & Sehpa) -->
  <g transform="translate(30, 20)">
    <rect x="0" y="0" width="150" height="120" rx="6" fill="var(--bg-card, #1e293b)" stroke="var(--border-subtle, rgba(255,255,255,0.12))" />
    <text x="15" y="18" class="geo-text-accent" font-weight="700">I.</text>
    <!-- Zemin -->
    <polygon points="75,65 130,85 75,105 20,85" fill="rgba(245, 158, 11, 0.15)" stroke="var(--border-subtle, rgba(255,255,255,0.2))" />
    <!-- Sol Duvar -->
    <polygon points="20,40 75,20 75,65 20,85" fill="rgba(255,255,255,0.03)" stroke="var(--border-subtle, rgba(255,255,255,0.2))" />
    <!-- Sağ Duvar -->
    <polygon points="75,20 130,40 130,85 75,65" fill="rgba(255,255,255,0.06)" stroke="var(--border-subtle, rgba(255,255,255,0.2))" />
    <!-- Pencere (Sol Duvar) -->
    <polygon points="32,55 58,45 58,68 32,78" fill="#38bdf8" fill-opacity="0.4" stroke="#38bdf8" stroke-width="1.2" />
    <!-- TV & Kırmızı Sehpa (Sağ Duvar) -->
    <polygon points="90,48 112,56 112,72 90,64" fill="#f43f5e" fill-opacity="0.6" stroke="#f43f5e" stroke-width="1.2" />
  </g>

  <!-- Maket II (Sol: Kapı, Sağ: Pencere) -->
  <g transform="translate(200, 20)">
    <rect x="0" y="0" width="150" height="120" rx="6" fill="var(--bg-card, #1e293b)" stroke="var(--border-subtle, rgba(255,255,255,0.12))" />
    <text x="15" y="18" class="geo-text-accent" font-weight="700">II.</text>
    <polygon points="75,65 130,85 75,105 20,85" fill="rgba(245, 158, 11, 0.15)" stroke="var(--border-subtle, rgba(255,255,255,0.2))" />
    <polygon points="20,40 75,20 75,65 20,85" fill="rgba(255,255,255,0.03)" stroke="var(--border-subtle, rgba(255,255,255,0.2))" />
    <polygon points="75,20 130,40 130,85 75,65" fill="rgba(255,255,255,0.06)" stroke="var(--border-subtle, rgba(255,255,255,0.2))" />
    <!-- Kapı (Sol Duvar) -->
    <polygon points="38,48 58,40 58,78 38,86" fill="#a16207" fill-opacity="0.5" stroke="#a16207" stroke-width="1.2" />
    <!-- Pencere (Sağ Duvar) -->
    <polygon points="92,48 118,58 118,80 92,70" fill="#38bdf8" fill-opacity="0.4" stroke="#38bdf8" stroke-width="1.2" />
  </g>

  <!-- Maket III (Sol: 2 Tablo, Sağ: Kapı) -->
  <g transform="translate(30, 160)">
    <rect x="0" y="0" width="150" height="120" rx="6" fill="var(--bg-card, #1e293b)" stroke="var(--border-subtle, rgba(255,255,255,0.12))" />
    <text x="15" y="18" class="geo-text-accent" font-weight="700">III.</text>
    <polygon points="75,65 130,85 75,105 20,85" fill="rgba(245, 158, 11, 0.15)" stroke="var(--border-subtle, rgba(255,255,255,0.2))" />
    <polygon points="20,40 75,20 75,65 20,85" fill="rgba(255,255,255,0.03)" stroke="var(--border-subtle, rgba(255,255,255,0.2))" />
    <polygon points="75,20 130,40 130,85 75,65" fill="rgba(255,255,255,0.06)" stroke="var(--border-subtle, rgba(255,255,255,0.2))" />
    <!-- 2 Tablo (Sol Duvar) -->
    <polygon points="28,52 44,46 44,62 28,68" fill="#22c55e" fill-opacity="0.5" stroke="#22c55e" stroke-width="1" />
    <polygon points="50,44 66,38 66,54 50,60" fill="#f59e0b" fill-opacity="0.5" stroke="#f59e0b" stroke-width="1" />
    <!-- Kapı (Sağ Duvar) -->
    <polygon points="95,54 115,62 115,96 95,88" fill="#a16207" fill-opacity="0.5" stroke="#a16207" stroke-width="1.2" />
  </g>

  <!-- Maket IV (Sol: TV & Sehpa, Sağ: 2 Tablo) -->
  <g transform="translate(200, 160)">
    <rect x="0" y="0" width="150" height="120" rx="6" fill="var(--bg-card, #1e293b)" stroke="var(--border-subtle, rgba(255,255,255,0.12))" />
    <text x="15" y="18" class="geo-text-accent" font-weight="700">IV.</text>
    <polygon points="75,65 130,85 75,105 20,85" fill="rgba(245, 158, 11, 0.15)" stroke="var(--border-subtle, rgba(255,255,255,0.2))" />
    <polygon points="20,40 75,20 75,65 20,85" fill="rgba(255,255,255,0.03)" stroke="var(--border-subtle, rgba(255,255,255,0.2))" />
    <polygon points="75,20 130,40 130,85 75,65" fill="rgba(255,255,255,0.06)" stroke="var(--border-subtle, rgba(255,255,255,0.2))" />
    <!-- TV & Kırmızı Sehpa (Sol Duvar) -->
    <polygon points="35,62 58,54 58,78 35,86" fill="#f43f5e" fill-opacity="0.6" stroke="#f43f5e" stroke-width="1.2" />
    <!-- 2 Tablo (Sağ Duvar) -->
    <polygon points="84,46 100,52 100,68 84,62" fill="#22c55e" fill-opacity="0.5" stroke="#22c55e" stroke-width="1" />
    <polygon points="106,54 122,60 122,76 106,70" fill="#f59e0b" fill-opacity="0.5" stroke="#f59e0b" stroke-width="1" />
  </g>
</svg>"""
    return save_svg("ales2_q50_cube_mockups.svg", svg)

def save_svg(filename: str, content: str):
    path = SVG_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return content, f"/assets/questions/svg/{filename}"

def generate_all_ales2_svgs():
    """2021-ALES/2 için tüm SVG çizimlerini üretir ve haritayı döndürür."""
    m = {}
    m["q20"], m["q20_url"] = generate_q20_pie()
    m["q21"], m["q21_url"] = generate_q21_map()
    m["q25"], m["q25_url"] = generate_q25_barchart()
    m["q27"], m["q27_url"] = generate_q27_network()
    m["q28"], m["q28_url"] = generate_q28_network()
    m["q35"], m["q35_url"] = generate_q35_scale()
    m["q36"], m["q36_url"] = generate_q36_scale()
    m["q37"], m["q37_url"] = generate_q37_scale()
    m["q41"], m["q41_url"] = generate_q41_table()
    m["q42"], m["q42_url"] = generate_q42_table()
    m["q43"], m["q43_url"] = generate_q43_table()
    m["q44"], m["q44_url"] = generate_q44_triangle()
    m["q45"], m["q45_url"] = generate_q45_triangle()
    m["q46"], m["q46_url"] = generate_q46_rhombus()
    m["q47"], m["q47_url"] = generate_q47_rectangles()
    m["q48"], m["q48_url"] = generate_q48_circle()
    m["q49"], m["q49_url"] = generate_q49_keypad()
    m["q50"], m["q50_url"] = generate_q50_cube_mockups()
    return m

if __name__ == "__main__":
    res = generate_all_ales2_svgs()
    print(f"Generated {len(res)//2} SVG files for 2021-ALES/2.")
