import os

SVG_STYLE = """  <defs>
    <style>
      .geo-line { stroke: var(--text-primary, #f1f5f9); stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .geo-sec { stroke: var(--accent-primary, #38bdf8); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .geo-accent { stroke: var(--zen-warning, #f59e0b); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .geo-shaded { fill: var(--geo-shaded-fill, rgba(56, 189, 248, 0.28)); stroke: var(--geo-shaded-stroke, var(--accent-primary, #38bdf8)); stroke-width: 2; stroke-linejoin: round; }
      .geo-shaded-yellow { fill: rgba(245, 158, 11, 0.30); stroke: #f59e0b; stroke-width: 2; stroke-linejoin: round; }
      .geo-shaded-green { fill: rgba(34, 197, 94, 0.28); stroke: #22c55e; stroke-width: 2; stroke-linejoin: round; }
      .geo-shaded-red { fill: rgba(244, 63, 94, 0.30); stroke: #f43f5e; stroke-width: 2; stroke-linejoin: round; }
      .geo-text { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif; font-size: 14px; font-weight: 600; fill: var(--text-primary, #f1f5f9); text-anchor: middle; dominant-baseline: central; }
      .geo-text-muted { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif; font-size: 12px; font-weight: 500; fill: var(--text-secondary, #94a3b8); text-anchor: middle; dominant-baseline: central; }
      .geo-text-accent { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif; font-size: 15px; font-weight: 700; fill: var(--zen-warning, #f59e0b); text-anchor: middle; dominant-baseline: central; }
      .geo-point { fill: var(--text-primary, #f1f5f9); }
      .geo-right-angle { stroke: var(--text-muted, #94a3b8); stroke-width: 1.5; fill: none; }
      .geo-angle-arc { stroke: var(--zen-warning, #f59e0b); stroke-width: 1.8; fill: none; }

      @media (prefers-color-scheme: light) {
        .geo-line { stroke: var(--text-primary, #0f172a); }
        .geo-sec { stroke: var(--accent-primary, #0284c7); }
        .geo-shaded { fill: var(--geo-shaded-fill, rgba(2, 132, 199, 0.22)); stroke: var(--accent-primary, #0284c7); }
        .geo-text { fill: var(--text-primary, #0f172a); }
        .geo-text-muted { fill: var(--text-secondary, #475569); }
        .geo-text-accent { fill: var(--zen-warning, #d97706); }
        .geo-point { fill: var(--text-primary, #0f172a); }
      }
    </style>
  </defs>"""

def save_svg(filename, content):
    path = os.path.join("public/assets/questions/svg", filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Wrote", path)

def build_all():
    # 1. ales2_q20_pie.svg (Fix Şekil 1: analiz=144°, geometri=144°, cebir=72° unlabeled)
    ales2_q20 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 225" width="100%" height="205">
{SVG_STYLE}
  <!-- Şekil 1 (Toplam Dersler: analiz 144°, geometri 144°, cebir 72°) -->
  <g transform="translate(105, 95)">
    <circle cx="0" cy="0" r="70" class="geo-line" />
    <line x1="0" y1="0" x2="70" y2="0" class="geo-line" />
    <line x1="0" y1="0" x2="-56.6" y2="-41.1" class="geo-line" />
    <line x1="0" y1="0" x2="-56.6" y2="41.1" class="geo-line" />
    <text x="12" y="-38" class="geo-text">analiz</text>
    <text x="15" y="-16" class="geo-text-accent">144°</text>
    <text x="-44" y="0" class="geo-text">cebir</text>
    <text x="15" y="16" class="geo-text-accent">144°</text>
    <text x="12" y="42" class="geo-text">geometri</text>
    <text x="0" y="95" class="geo-text-muted" font-weight="700">Şekil 1</text>
  </g>
  <!-- Şekil 2 (Zorunlu Dersler: analiz 180°, cebir 60°, geometri 120°) -->
  <g transform="translate(315, 95)">
    <circle cx="0" cy="0" r="70" class="geo-line" />
    <line x1="-70" y1="0" x2="70" y2="0" class="geo-line" />
    <line x1="0" y1="0" x2="-35" y2="60.6" class="geo-line" />
    <text x="0" y="-35" class="geo-text">analiz</text>
    <text x="-38" y="28" class="geo-text">cebir</text>
    <text x="-22" y="14" class="geo-text-accent">60°</text>
    <text x="20" y="42" class="geo-text">geometri</text>
    <text x="18" y="18" class="geo-text-accent">120°</text>
    <text x="0" y="95" class="geo-text-muted" font-weight="700">Şekil 2</text>
  </g>
</svg>"""
    save_svg("ales2_q20_pie.svg", ales2_q20)

    # 2. ales2_q25_barchart.svg (5 dashed lines: y=160, 135, 110, 85, 60; baseline y=185)
    # Line 1 (y=160, h=25): E-yellow
    # Line 2 (y=135, h=50): A-blue, B-blue, C-yellow
    # Line 3 (y=110, h=75): C-blue, D-blue, D-yellow
    # Line 4 (y=85, h=100): A-yellow
    # Line 5 (y=60, h=125): B-yellow, E-blue
    ales2_q25 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 430 250" width="100%" height="235">
{SVG_STYLE}
  <!-- Eksenler -->
  <line x1="45" y1="185" x2="365" y2="185" class="geo-line" stroke-width="2" />
  <line x1="45" y1="195" x2="45" y2="25" class="geo-line" stroke-width="2" />
  <polygon points="45,20 40,30 50,30" fill="var(--text-primary, #f1f5f9)" />
  <polygon points="370,185 360,180 360,190" fill="var(--text-primary, #f1f5f9)" />
  <text x="105" y="22" class="geo-text">Öğrenci sayısı</text>
  <text x="395" y="178" class="geo-text">Meslek</text>
  <text x="395" y="195" class="geo-text">adı</text>

  <!-- 5 Yatay Kesikli Kılavuz Çizgisi -->
  <line x1="45" y1="160" x2="335" y2="160" stroke="var(--text-secondary, #94a3b8)" stroke-width="1.3" stroke-dasharray="4 4" />
  <line x1="45" y1="135" x2="310" y2="135" stroke="var(--text-secondary, #94a3b8)" stroke-width="1.3" stroke-dasharray="4 4" />
  <line x1="45" y1="110" x2="310" y2="110" stroke="var(--text-secondary, #94a3b8)" stroke-width="1.3" stroke-dasharray="4 4" />
  <line x1="45" y1="85" x2="310" y2="85" stroke="var(--text-secondary, #94a3b8)" stroke-width="1.3" stroke-dasharray="4 4" />
  <line x1="45" y1="60" x2="310" y2="60" stroke="var(--text-secondary, #94a3b8)" stroke-width="1.3" stroke-dasharray="4 4" />

  <!-- A: blue Line 2 (y=135,h=50), yellow Line 4 (y=85,h=100) -->
  <g transform="translate(62, 0)">
    <rect x="0" y="135" width="16" height="50" class="geo-shaded" />
    <rect x="20" y="85" width="16" height="100" class="geo-shaded-yellow" />
    <text x="18" y="203" class="geo-text">A</text>
  </g>
  <!-- B: blue Line 2 (y=135,h=50), yellow Line 5 (y=60,h=125) -->
  <g transform="translate(122, 0)">
    <rect x="0" y="135" width="16" height="50" class="geo-shaded" />
    <rect x="20" y="60" width="16" height="125" class="geo-shaded-yellow" />
    <text x="18" y="203" class="geo-text">B</text>
  </g>
  <!-- C: blue Line 3 (y=110,h=75), yellow Line 2 (y=135,h=50) -->
  <g transform="translate(182, 0)">
    <rect x="0" y="110" width="16" height="75" class="geo-shaded" />
    <rect x="20" y="135" width="16" height="50" class="geo-shaded-yellow" />
    <text x="18" y="203" class="geo-text">C</text>
  </g>
  <!-- D: blue Line 3 (y=110,h=75), yellow Line 3 (y=110,h=75) -->
  <g transform="translate(242, 0)">
    <rect x="0" y="110" width="16" height="75" class="geo-shaded" />
    <rect x="20" y="110" width="16" height="75" class="geo-shaded-yellow" />
    <text x="18" y="203" class="geo-text">D</text>
  </g>
  <!-- E: blue Line 5 (y=60,h=125), yellow Line 1 (y=160,h=25) -->
  <g transform="translate(302, 0)">
    <rect x="0" y="60" width="16" height="125" class="geo-shaded" />
    <rect x="20" y="160" width="16" height="25" class="geo-shaded-yellow" />
    <text x="18" y="203" class="geo-text">E</text>
  </g>

  <!-- Lejant -->
  <rect x="62" y="222" width="16" height="16" class="geo-shaded" />
  <text x="125" y="230" class="geo-text-muted">: tercih eden</text>
  <rect x="200" y="222" width="16" height="16" class="geo-shaded-yellow" />
  <text x="272" y="230" class="geo-text-muted">: tercih etmeyen</text>
</svg>"""
    save_svg("ales2_q25_barchart.svg", ales2_q25)

    # 3. ales2_q35_scale.svg (Left pan: 1 kare, 1 daire, 2 üçgen; Right pan: 1 üçgen, 4 daire)
    ales2_q35 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 155" width="100%" height="145">
{SVG_STYLE}
  <line x1="160" y1="30" x2="160" y2="135" class="geo-line" stroke-width="3.5" />
  <ellipse cx="160" cy="137" rx="30" ry="5" class="geo-shaded" />
  <line x1="70" y1="30" x2="250" y2="30" class="geo-line" stroke-width="3.5" />

  <!-- Sol Kefe: 1 kare, 1 daire, 2 üçgen -->
  <polygon points="70,30 30,90 110,90" class="geo-line" stroke-width="2" />
  <rect x="44" y="72" width="16" height="16" class="geo-shaded" />
  <circle cx="68" cy="81" r="7" class="geo-shaded-red" />
  <polygon points="83,72 76,88 90,88" class="geo-shaded-yellow" />
  <polygon points="97,72 90,88 104,88" class="geo-shaded-yellow" />

  <!-- Sağ Kefe: 1 üçgen, 4 daire -->
  <polygon points="250,30 210,90 290,90" class="geo-line" stroke-width="2" />
  <polygon points="232,72 225,88 239,88" class="geo-shaded-yellow" />
  <circle cx="248" cy="81" r="7" class="geo-shaded-red" />
  <circle cx="262" cy="81" r="7" class="geo-shaded-red" />
  <circle cx="276" cy="81" r="7" class="geo-shaded-red" />
  <circle cx="255" cy="68" r="7" class="geo-shaded-red" />
</svg>"""
    save_svg("ales2_q35_scale.svg", ales2_q35)

    # 4. ales2_q36_scale.svg
    # 1. terazi (dengede): Left = 1 daire, 3 kare, 1 üçgen; Right = 2 üçgen, 4 daire
    # 2. terazi (sağ kefe aşağıda): Left (yukarıda) = 1 daire, 2 kare, 2 üçgen; Right (aşağıda) = 3 üçgen, 1 daire
    ales2_q36 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 175" width="100%" height="165">
{SVG_STYLE}
  <!-- 1. Terazi (Dengede) -->
  <g transform="translate(10, 5)">
    <line x1="105" y1="30" x2="105" y2="135" class="geo-line" stroke-width="3" />
    <ellipse cx="105" cy="137" rx="26" ry="4.5" class="geo-shaded" />
    <line x1="40" y1="30" x2="170" y2="30" class="geo-line" stroke-width="3" />
    <!-- Sol Kefe: 1 daire, 3 kare (2 altta 1 üstte), 1 üçgen -->
    <polygon points="40,30 5,90 75,90" class="geo-line" stroke-width="1.8" />
    <circle cx="21" cy="82" r="6" class="geo-shaded-red" />
    <rect x="29" y="74" width="14" height="14" class="geo-shaded" />
    <rect x="44" y="74" width="14" height="14" class="geo-shaded" />
    <rect x="36.5" y="59" width="14" height="14" class="geo-shaded" />
    <polygon points="65,74 59,88 71,88" class="geo-shaded-yellow" />
    <!-- Sağ Kefe: 2 üçgen, 4 daire -->
    <polygon points="170,30 135,90 205,90" class="geo-line" stroke-width="1.8" />
    <polygon points="148,74 142,88 154,88" class="geo-shaded-yellow" />
    <polygon points="161,74 155,88 167,88" class="geo-shaded-yellow" />
    <circle cx="174" cy="82" r="6" class="geo-shaded-red" />
    <circle cx="186" cy="82" r="6" class="geo-shaded-red" />
    <circle cx="198" cy="82" r="6" class="geo-shaded-red" />
    <circle cx="180" cy="70" r="6" class="geo-shaded-red" />
    <text x="105" y="156" class="geo-text">1. terazi</text>
  </g>

  <!-- 2. Terazi (Sağ kefe daha aşağıda/ağır) -->
  <g transform="translate(235, 5)">
    <line x1="105" y1="30" x2="105" y2="135" class="geo-line" stroke-width="3" />
    <ellipse cx="105" cy="137" rx="26" ry="4.5" class="geo-shaded" />
    <!-- Eğik kol: sol yukarıda (40,20), sağ aşağıda (170,42) -->
    <line x1="40" y1="20" x2="170" y2="42" class="geo-line" stroke-width="3" />
    <!-- Sol Kefe (yukarıda): 1 daire, 2 üst üste kare, 2 üçgen -->
    <polygon points="40,20 5,78 75,78" class="geo-line" stroke-width="1.8" />
    <circle cx="21" cy="70" r="6" class="geo-shaded-red" />
    <rect x="30" y="62" width="14" height="14" class="geo-shaded" />
    <rect x="30" y="47" width="14" height="14" class="geo-shaded" />
    <polygon points="52,62 46,76 58,76" class="geo-shaded-yellow" />
    <polygon points="65,62 59,76 71,76" class="geo-shaded-yellow" />
    <!-- Sağ Kefe (aşağıda): 3 üçgen, 1 daire -->
    <polygon points="170,42 135,102 205,102" class="geo-line" stroke-width="1.8" />
    <polygon points="148,86 142,100 154,100" class="geo-shaded-yellow" />
    <polygon points="162,86 156,100 168,100" class="geo-shaded-yellow" />
    <polygon points="176,86 170,100 182,100" class="geo-shaded-yellow" />
    <circle cx="192" cy="94" r="6" class="geo-shaded-red" />
    <text x="105" y="156" class="geo-text">2. terazi</text>
  </g>
</svg>"""
    save_svg("ales2_q36_scale.svg", ales2_q36)

    # 5. ales2_q37_scale.svg
    # Sol terazi (dengede): Left = 1 üçgen, 4 daire; Right = 3 kare
    # Sağ terazi (dengede): Left = 2 üçgen, 1 kare, 1 daire; Right = 2 kare, 2 daire
    ales2_q37 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 160" width="100%" height="150">
{SVG_STYLE}
  <!-- Sol Terazi -->
  <g transform="translate(10, 5)">
    <line x1="105" y1="30" x2="105" y2="135" class="geo-line" stroke-width="3" />
    <ellipse cx="105" cy="137" rx="26" ry="4.5" class="geo-shaded" />
    <line x1="40" y1="30" x2="170" y2="30" class="geo-line" stroke-width="3" />
    <!-- Sol Kefe: 1 üçgen, 4 daire -->
    <polygon points="40,30 5,90 75,90" class="geo-line" stroke-width="1.8" />
    <polygon points="24,74 18,88 30,88" class="geo-shaded-yellow" />
    <circle cx="39" cy="82" r="6" class="geo-shaded-red" />
    <circle cx="51" cy="82" r="6" class="geo-shaded-red" />
    <circle cx="63" cy="82" r="6" class="geo-shaded-red" />
    <circle cx="45" cy="70" r="6" class="geo-shaded-red" />
    <!-- Sağ Kefe: 3 kare -->
    <polygon points="170,30 135,90 205,90" class="geo-line" stroke-width="1.8" />
    <rect x="155" y="74" width="14" height="14" class="geo-shaded" />
    <rect x="171" y="74" width="14" height="14" class="geo-shaded" />
    <rect x="163" y="59" width="14" height="14" class="geo-shaded" />
  </g>

  <!-- Sağ Terazi -->
  <g transform="translate(235, 5)">
    <line x1="105" y1="30" x2="105" y2="135" class="geo-line" stroke-width="3" />
    <ellipse cx="105" cy="137" rx="26" ry="4.5" class="geo-shaded" />
    <line x1="40" y1="30" x2="170" y2="30" class="geo-line" stroke-width="3" />
    <!-- Sol Kefe: 2 üçgen, 1 kare, 1 daire -->
    <polygon points="40,30 5,90 75,90" class="geo-line" stroke-width="1.8" />
    <polygon points="18,74 12,88 24,88" class="geo-shaded-yellow" />
    <polygon points="31,74 25,88 37,88" class="geo-shaded-yellow" />
    <rect x="41" y="74" width="14" height="14" class="geo-shaded" />
    <circle cx="63" cy="82" r="6" class="geo-shaded-red" />
    <!-- Sağ Kefe: 2 kare, 2 daire -->
    <polygon points="170,30 135,90 205,90" class="geo-line" stroke-width="1.8" />
    <rect x="147" y="74" width="14" height="14" class="geo-shaded" />
    <rect x="163" y="74" width="14" height="14" class="geo-shaded" />
    <circle cx="184" cy="82" r="6" class="geo-shaded-red" />
    <circle cx="196" cy="82" r="6" class="geo-shaded-red" />
  </g>
</svg>"""
    save_svg("ales2_q37_scale.svg", ales2_q37)

    # 6. ales2_q41_table.svg (Add missing 4 in row 3 col 4)
    ales2_q41 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 145" width="100%" height="135">
{SVG_STYLE}
  <!-- Row 1: [blue, white(b), blue(c), white(d)] -->
  <rect x="25" y="20" width="42" height="34" class="geo-shaded" />
  <rect x="67" y="20" width="42" height="34" fill="none" stroke="var(--text-primary, #f1f5f9)" stroke-width="1.5" />
  <rect x="109" y="20" width="42" height="34" class="geo-shaded" />
  <rect x="151" y="20" width="42" height="34" fill="none" stroke="var(--text-primary, #f1f5f9)" stroke-width="1.5" />
  <!-- Row 2: [white(7), blue(12), blue(10), white(2)] -->
  <rect x="25" y="54" width="42" height="34" fill="none" stroke="var(--text-primary, #f1f5f9)" stroke-width="1.5" />
  <rect x="67" y="54" width="42" height="34" class="geo-shaded" />
  <rect x="109" y="54" width="42" height="34" class="geo-shaded" />
  <rect x="151" y="54" width="42" height="34" fill="none" stroke="var(--text-primary, #f1f5f9)" stroke-width="1.5" />
  <!-- Row 3: [white, white(a), white(3), white(4)] -->
  <rect x="25" y="88" width="42" height="34" fill="none" stroke="var(--text-primary, #f1f5f9)" stroke-width="1.5" />
  <rect x="67" y="88" width="42" height="34" fill="none" stroke="var(--text-primary, #f1f5f9)" stroke-width="1.5" />
  <rect x="109" y="88" width="42" height="34" fill="none" stroke="var(--text-primary, #f1f5f9)" stroke-width="1.5" />
  <rect x="151" y="88" width="42" height="34" fill="none" stroke="var(--text-primary, #f1f5f9)" stroke-width="1.5" />
  <text x="88" y="37" class="geo-text-accent">b</text>
  <text x="130" y="37" class="geo-text-accent">c</text>
  <text x="172" y="37" class="geo-text-accent">d</text>
  <text x="46" y="71" class="geo-text">7</text>
  <text x="88" y="71" class="geo-text">12</text>
  <text x="130" y="71" class="geo-text">10</text>
  <text x="172" y="71" class="geo-text">2</text>
  <text x="88" y="105" class="geo-text-accent">a</text>
  <text x="130" y="105" class="geo-text">3</text>
  <text x="172" y="105" class="geo-text">4</text>
</svg>"""
    save_svg("ales2_q41_table.svg", ales2_q41)

    # 7. ales2_q43_table.svg (Row 1 all blue [ , , ,10], Row 2 all blue [ ,7,x,3], Row 3 all white [9,2, , ])
    ales2_q43 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 145" width="100%" height="135">
{SVG_STYLE}
  <!-- Row 1: all 4 blue -->
  <rect x="25" y="20" width="42" height="34" class="geo-shaded" />
  <rect x="67" y="20" width="42" height="34" class="geo-shaded" />
  <rect x="109" y="20" width="42" height="34" class="geo-shaded" />
  <rect x="151" y="20" width="42" height="34" class="geo-shaded" />
  <!-- Row 2: all 4 blue -->
  <rect x="25" y="54" width="42" height="34" class="geo-shaded" />
  <rect x="67" y="54" width="42" height="34" class="geo-shaded" />
  <rect x="109" y="54" width="42" height="34" class="geo-shaded" />
  <rect x="151" y="54" width="42" height="34" class="geo-shaded" />
  <!-- Row 3: all 4 white -->
  <rect x="25" y="88" width="42" height="34" fill="none" stroke="var(--text-primary, #f1f5f9)" stroke-width="1.5" />
  <rect x="67" y="88" width="42" height="34" fill="none" stroke="var(--text-primary, #f1f5f9)" stroke-width="1.5" />
  <rect x="109" y="88" width="42" height="34" fill="none" stroke="var(--text-primary, #f1f5f9)" stroke-width="1.5" />
  <rect x="151" y="88" width="42" height="34" fill="none" stroke="var(--text-primary, #f1f5f9)" stroke-width="1.5" />
  <text x="172" y="37" class="geo-text">10</text>
  <text x="88" y="71" class="geo-text">7</text>
  <text x="130" y="71" class="geo-text-accent">x</text>
  <text x="172" y="71" class="geo-text">3</text>
  <text x="46" y="105" class="geo-text">9</text>
  <text x="88" y="105" class="geo-text">2</text>
</svg>"""
    save_svg("ales2_q43_table.svg", ales2_q43)

    # 8. ales3_q17_toc.svg (NEW: Sevim's cookbook İçindekiler Şekil 1 & Şekil 2)
    ales3_q17 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 220" width="100%" height="205">
{SVG_STYLE}
  <!-- Şekil 1 -->
  <g transform="translate(20, 15)">
    <rect x="0" y="0" width="195" height="165" rx="8" class="geo-line" stroke-width="1.6" />
    <text x="97.5" y="22" class="geo-text" font-weight="700">İÇİNDEKİLER</text>
    <line x1="15" y1="36" x2="180" y2="36" stroke="var(--text-secondary, #94a3b8)" stroke-width="1" />
    <text x="15" y="54" class="geo-text" text-anchor="start" style="text-anchor:start">Çorbalar....................</text><text x="180" y="54" class="geo-text" style="text-anchor:end">1</text>
    <text x="15" y="76" class="geo-text" text-anchor="start" style="text-anchor:start">Salatalar...................</text><text x="180" y="76" class="geo-text" style="text-anchor:end">10</text>
    <text x="15" y="98" class="geo-text" text-anchor="start" style="text-anchor:start">Et yemekleri.............</text><text x="180" y="98" class="geo-text" style="text-anchor:end">15</text>
    <text x="15" y="120" class="geo-text" text-anchor="start" style="text-anchor:start">Sebze yemekleri.......</text><text x="180" y="120" class="geo-text" style="text-anchor:end">28</text>
    <text x="15" y="142" class="geo-text" text-anchor="start" style="text-anchor:start">Tatlılar......................</text><text x="180" y="142" class="geo-text" style="text-anchor:end">38</text>
    <text x="97.5" y="185" class="geo-text-muted" font-weight="700">Şekil 1</text>
  </g>
  <!-- Şekil 2 -->
  <g transform="translate(245, 15)">
    <rect x="0" y="0" width="195" height="165" rx="8" class="geo-line" stroke-width="1.6" />
    <text x="97.5" y="22" class="geo-text" font-weight="700">İÇİNDEKİLER</text>
    <line x1="15" y1="36" x2="180" y2="36" stroke="var(--text-secondary, #94a3b8)" stroke-width="1" />
    <text x="15" y="54" class="geo-text" style="text-anchor:start">Salatalar...................</text><text x="180" y="54" class="geo-text" style="text-anchor:end">1</text>
    <text x="15" y="76" class="geo-text" style="text-anchor:start">Çorbalar....................</text><text x="180" y="76" class="geo-text-accent" style="text-anchor:end">?</text>
    <text x="15" y="98" class="geo-text" style="text-anchor:start">Sebze yemekleri.......</text><text x="180" y="98" class="geo-text-accent" style="text-anchor:end">?</text>
    <text x="15" y="120" class="geo-text" style="text-anchor:start">Et yemekleri.............</text><text x="180" y="120" class="geo-text-accent" style="text-anchor:end">?</text>
    <text x="15" y="142" class="geo-text" style="text-anchor:start">Tatlılar......................</text><text x="180" y="142" class="geo-text" style="text-anchor:end">38</text>
    <text x="97.5" y="185" class="geo-text-muted" font-weight="700">Şekil 2</text>
  </g>
</svg>"""
    save_svg("ales3_q17_toc.svg", ales3_q17)

    # 9. ales3_q21_schedule.svg (NEW: Berna's weekly course schedule table)
    ales3_q21 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 210" width="100%" height="195">
{SVG_STYLE}
  <!-- Header Row (Cols 1..5) -->
  <rect x="105" y="15" width="335" height="30" class="geo-shaded" />
  <rect x="20" y="45" width="420" height="150" fill="none" stroke="var(--text-primary, #f1f5f9)" stroke-width="1.6" />
  <!-- Grid Lines -->
  <line x1="105" y1="15" x2="105" y2="195" class="geo-line" stroke-width="1.5" />
  <line x1="172" y1="15" x2="172" y2="195" class="geo-line" stroke-width="1.2" />
  <line x1="239" y1="15" x2="239" y2="195" class="geo-line" stroke-width="1.2" />
  <line x1="306" y1="15" x2="306" y2="195" class="geo-line" stroke-width="1.2" />
  <line x1="373" y1="15" x2="373" y2="195" class="geo-line" stroke-width="1.2" />
  <line x1="440" y1="15" x2="440" y2="195" class="geo-line" stroke-width="1.5" />
  <line x1="105" y1="15" x2="440" y2="15" class="geo-line" stroke-width="1.5" />
  <line x1="20" y1="75" x2="440" y2="75" class="geo-line" stroke-width="1.2" />
  <line x1="20" y1="105" x2="440" y2="105" class="geo-line" stroke-width="1.2" />
  <line x1="20" y1="135" x2="440" y2="135" class="geo-line" stroke-width="1.2" />
  <line x1="20" y1="165" x2="440" y2="165" class="geo-line" stroke-width="1.2" />

  <!-- Column Headers -->
  <text x="138.5" y="30" class="geo-text" font-size="12">1. Ders</text>
  <text x="205.5" y="30" class="geo-text" font-size="12">2. Ders</text>
  <text x="272.5" y="30" class="geo-text" font-size="12">3. Ders</text>
  <text x="339.5" y="30" class="geo-text" font-size="12">4. Ders</text>
  <text x="406.5" y="30" class="geo-text" font-size="12">5. Ders</text>

  <!-- Row Headers -->
  <text x="62.5" y="60" class="geo-text" font-size="13">Pazartesi</text>
  <text x="62.5" y="90" class="geo-text" font-size="13">Salı</text>
  <text x="62.5" y="120" class="geo-text" font-size="13">Çarşamba</text>
  <text x="62.5" y="150" class="geo-text" font-size="13">Perşembe</text>
  <text x="62.5" y="180" class="geo-text" font-size="13">Cuma</text>

  <!-- Pazartesi: İng, Mat, Mat -->
  <text x="138.5" y="60" class="geo-text-accent">İng.</text>
  <text x="205.5" y="60" class="geo-text">Mat.</text>
  <text x="272.5" y="60" class="geo-text">Mat.</text>

  <!-- Salı: Mat, Mat, İng -->
  <text x="138.5" y="90" class="geo-text">Mat.</text>
  <text x="205.5" y="90" class="geo-text">Mat.</text>
  <text x="272.5" y="90" class="geo-text-accent">İng.</text>

  <!-- Çarşamba: İng, İng, İng, Mat -->
  <text x="138.5" y="120" class="geo-text-accent">İng.</text>
  <text x="205.5" y="120" class="geo-text-accent">İng.</text>
  <text x="272.5" y="120" class="geo-text-accent">İng.</text>
  <text x="339.5" y="120" class="geo-text">Mat.</text>

  <!-- Perşembe: Mat, İng, İng, Mat, Mat -->
  <text x="138.5" y="150" class="geo-text">Mat.</text>
  <text x="205.5" y="150" class="geo-text-accent">İng.</text>
  <text x="272.5" y="150" class="geo-text-accent">İng.</text>
  <text x="339.5" y="150" class="geo-text">Mat.</text>
  <text x="406.5" y="150" class="geo-text">Mat.</text>

  <!-- Cuma: Mat, Mat, İng, İng -->
  <text x="138.5" y="180" class="geo-text">Mat.</text>
  <text x="205.5" y="180" class="geo-text">Mat.</text>
  <text x="272.5" y="180" class="geo-text-accent">İng.</text>
  <text x="339.5" y="180" class="geo-text-accent">İng.</text>
</svg>"""
    save_svg("ales3_q21_schedule.svg", ales3_q21)

    # 10. ales3_q22_clock.svg (NEW: Digital clock displays AB.CD, 2K.L4, 2L.K8)
    def clock_widget(tx, ty, c1, c2, c3, c4):
        cells = []
        vals = [c1, c2, ".", c3, c4]
        for idx, v in enumerate(vals):
            x = tx + idx * 34
            cells.append(f'<rect x="{x}" y="{ty}" width="30" height="34" rx="5" class="geo-shaded-green" />')
            cells.append(f'<text x="{x+15}" y="{ty+17}" class="geo-text" font-size="16" font-weight="700">{v}</text>')
        return f'<rect x="{tx-6}" y="{ty-6}" width="178" height="46" rx="8" fill="rgba(15,23,42,0.6)" stroke="var(--text-primary,#f1f5f9)" stroke-width="2" />' + "".join(cells)

    ales3_q22 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 135" width="100%" height="125">
{SVG_STYLE}
  {clock_widget(144, 14, "A", "B", "C", "D")}
  {clock_widget(30, 76, "2", "K", "L", "4")}
  <text x="230" y="93" class="geo-text-muted" font-size="14" font-weight="700">ve</text>
  {clock_widget(258, 76, "2", "L", "K", "8")}
</svg>"""
    save_svg("ales3_q22_clock.svg", ales3_q22)

    # 11. ales3_q32_table.svg (NEW: Kürşat video table)
    ales3_q32 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 155" width="100%" height="145">
{SVG_STYLE}
  <rect x="95" y="15" width="330" height="32" class="geo-shaded" />
  <rect x="20" y="47" width="405" height="96" fill="none" stroke="var(--text-primary, #f1f5f9)" stroke-width="1.6" />
  <line x1="95" y1="15" x2="95" y2="143" class="geo-line" stroke-width="1.5" />
  <line x1="205" y1="15" x2="205" y2="143" class="geo-line" stroke-width="1.2" />
  <line x1="315" y1="15" x2="315" y2="143" class="geo-line" stroke-width="1.2" />
  <line x1="425" y1="15" x2="425" y2="143" class="geo-line" stroke-width="1.5" />
  <line x1="95" y1="15" x2="425" y2="15" class="geo-line" stroke-width="1.5" />
  <line x1="20" y1="79" x2="425" y2="79" class="geo-line" stroke-width="1.2" />
  <line x1="20" y1="111" x2="425" y2="111" class="geo-line" stroke-width="1.2" />

  <text x="150" y="31" class="geo-text" font-size="13">Görüntülenme</text>
  <text x="260" y="31" class="geo-text" font-size="13">Beğeni</text>
  <text x="370" y="31" class="geo-text" font-size="13">Yeni Takipçi</text>

  <text x="57.5" y="63" class="geo-text" font-size="13">Ocak</text>
  <text x="57.5" y="95" class="geo-text" font-size="13">Şubat</text>
  <text x="57.5" y="127" class="geo-text" font-size="13">Mart</text>

  <text x="370" y="63" class="geo-text-accent" font-size="15">25</text>
  <text x="260" y="95" class="geo-text-accent" font-size="15">90</text>
  <text x="150" y="127" class="geo-text-accent" font-size="15">150</text>
</svg>"""
    save_svg("ales3_q32_table.svg", ales3_q32)

    # 12. ales3_q35_table.svg (NEW: Cheese milk percentages table)
    ales3_q35 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 155" width="100%" height="145">
{SVG_STYLE}
  <rect x="130" y="15" width="230" height="32" class="geo-shaded" />
  <rect x="25" y="47" width="335" height="96" fill="none" stroke="var(--text-primary, #f1f5f9)" stroke-width="1.6" />
  <line x1="130" y1="15" x2="130" y2="143" class="geo-line" stroke-width="1.5" />
  <line x1="245" y1="15" x2="245" y2="143" class="geo-line" stroke-width="1.2" />
  <line x1="360" y1="15" x2="360" y2="143" class="geo-line" stroke-width="1.5" />
  <line x1="130" y1="15" x2="360" y2="15" class="geo-line" stroke-width="1.5" />
  <line x1="25" y1="79" x2="360" y2="79" class="geo-line" stroke-width="1.2" />
  <line x1="25" y1="111" x2="360" y2="111" class="geo-line" stroke-width="1.2" />

  <text x="187.5" y="31" class="geo-text" font-size="13">Beyaz peynir</text>
  <text x="302.5" y="31" class="geo-text" font-size="13">Kaşar peyniri</text>

  <text x="77.5" y="63" class="geo-text" font-size="13">İnek sütü</text>
  <text x="77.5" y="95" class="geo-text" font-size="13">Koyun sütü</text>
  <text x="77.5" y="127" class="geo-text" font-size="13">Keçi sütü</text>

  <text x="187.5" y="63" class="geo-text-accent" font-size="14">% 50</text>
  <text x="302.5" y="63" class="geo-text" font-size="14">% 20</text>
  <text x="187.5" y="95" class="geo-text" font-size="14">% 25</text>
  <text x="302.5" y="95" class="geo-text-accent" font-size="14">% 40</text>
  <text x="187.5" y="127" class="geo-text" font-size="14">% 25</text>
  <text x="302.5" y="127" class="geo-text-accent" font-size="14">% 40</text>
</svg>"""
    save_svg("ales3_q35_table.svg", ales3_q35)

    # 13. ales3_q39_squares.svg (Fix vertex positions to match ales3_p14_361.png)
    ales3_q39 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 230 190" width="100%" height="175">
{SVG_STYLE}
  <!-- Dış Kare -->
  <rect x="40" y="20" width="140" height="140" class="geo-line" />
  <!-- Orta Kare -->
  <polygon points="110,20 180,90 110,160 40,90" class="geo-sec" stroke-width="1.8" />
  <!-- İç Kare -->
  <rect x="75" y="55" width="70" height="70" class="geo-accent" stroke-width="1.8" />

  <!-- Köşe Noktaları -->
  <circle cx="40" cy="20" r="2.5" class="geo-point" />
  <circle cx="180" cy="20" r="2.5" class="geo-point" />
  <circle cx="40" cy="160" r="2.5" class="geo-point" />
  <circle cx="180" cy="160" r="2.5" class="geo-point" />
  <circle cx="110" cy="20" r="2.5" class="geo-point" />
  <circle cx="180" cy="90" r="2.5" class="geo-point" />
  <circle cx="110" cy="160" r="2.5" class="geo-point" />
  <circle cx="40" cy="90" r="2.5" class="geo-point" />
  <circle cx="75" cy="55" r="2.5" class="geo-point" />
  <circle cx="145" cy="55" r="2.5" class="geo-point" />
  <circle cx="75" cy="125" r="2.5" class="geo-point" />
  <circle cx="145" cy="125" r="2.5" class="geo-point" />

  <!-- Dış Kare Köşeleri: 1 (sol-üst), 3 (sağ-üst), A (sol-alt), B (sağ-alt) -->
  <text x="30" y="14" class="geo-text">1</text>
  <text x="190" y="14" class="geo-text">3</text>
  <text x="30" y="168" class="geo-text-accent">A</text>
  <text x="190" y="168" class="geo-text-accent">B</text>

  <!-- Orta Kare Alt Köşesi: 4 -->
  <text x="110" y="174" class="geo-text">4</text>

  <!-- İç Kare Köşeleri: sol-alt=5, sağ-üst=1, sağ-alt=1 -->
  <text x="64" y="134" class="geo-text">5</text>
  <text x="156" y="46" class="geo-text">1</text>
  <text x="156" y="134" class="geo-text">1</text>
</svg>"""
    save_svg("ales3_q39_squares.svg", ales3_q39)

    # 14. ales3_q40_squares.svg (Fix vertex positions to match ales3_p14_369.png)
    ales3_q40 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 230 190" width="100%" height="175">
{SVG_STYLE}
  <!-- Dış Kare -->
  <rect x="40" y="20" width="140" height="140" class="geo-line" />
  <!-- Orta Kare -->
  <polygon points="110,20 180,90 110,160 40,90" class="geo-sec" stroke-width="1.8" />
  <!-- İç Kare -->
  <rect x="75" y="55" width="70" height="70" class="geo-accent" stroke-width="1.8" />

  <!-- Köşe Noktaları -->
  <circle cx="40" cy="20" r="2.5" class="geo-point" />
  <circle cx="180" cy="20" r="2.5" class="geo-point" />
  <circle cx="40" cy="160" r="2.5" class="geo-point" />
  <circle cx="180" cy="160" r="2.5" class="geo-point" />
  <circle cx="110" cy="20" r="2.5" class="geo-point" />
  <circle cx="180" cy="90" r="2.5" class="geo-point" />
  <circle cx="110" cy="160" r="2.5" class="geo-point" />
  <circle cx="40" cy="90" r="2.5" class="geo-point" />
  <circle cx="75" cy="55" r="2.5" class="geo-point" />
  <circle cx="145" cy="55" r="2.5" class="geo-point" />
  <circle cx="75" cy="125" r="2.5" class="geo-point" />
  <circle cx="145" cy="125" r="2.5" class="geo-point" />

  <!-- Dış Kare Köşeleri: A (sol-üst), 2 (sağ-üst), A (sol-alt), 4 (sağ-alt) -->
  <text x="30" y="14" class="geo-text-accent">A</text>
  <text x="190" y="14" class="geo-text">2</text>
  <text x="30" y="168" class="geo-text-accent">A</text>
  <text x="190" y="168" class="geo-text">4</text>

  <!-- İç Kare 4 Köşesi: 1, 1, 1, 1 -->
  <text x="64" y="46" class="geo-text">1</text>
  <text x="156" y="46" class="geo-text">1</text>
  <text x="64" y="134" class="geo-text">1</text>
  <text x="156" y="134" class="geo-text">1</text>
</svg>"""
    save_svg("ales3_q40_squares.svg", ales3_q40)

if __name__ == "__main__":
    build_all()

