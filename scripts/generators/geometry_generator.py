#!/usr/bin/env python3
"""
scripts/generators/geometry_generator.py
Geometri soruları için şeffaf, vektörel ve karanlık/aydınlık tema uyumlu
özgün SVG çizimleri üretir.
"""

from pathlib import Path

SVG_DIR = Path("public/assets/questions/svg")
SVG_DIR.mkdir(parents=True, exist_ok=True)

def generate_q44_svg():
    """
    Soru 44: ABC eşkenar üçgen, KLM ikizkenar dik üçgen.
    Vektörel SVG çizimi.
    """
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 320" width="100%" height="260">
  <defs>
    <style>
      .geo-line { stroke: #38bdf8; stroke-width: 2.5; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .geo-sec-line { stroke: #818cf8; stroke-width: 2.5; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .geo-text { font-family: -apple-system, sans-serif; font-size: 14px; font-weight: 600; fill: #f1f5f9; }
      .geo-angle { stroke: #fbbf24; stroke-width: 2; fill: none; }
      .geo-fill { fill: rgba(56, 189, 248, 0.08); }
    </style>
  </defs>

  <!-- ABC Eşkenar Üçgeni -->
  <polygon points="120,40 40,240 240,240" class="geo-fill" />
  <polygon points="120,40 40,240 240,240" class="geo-line" />

  <!-- KLM İkizkenar Dik Üçgeni -->
  <polygon points="76,140 180,40 160,290" class="geo-sec-line" />

  <!-- Açı ve diklik sembolleri -->
  <rect x="76" y="132" width="10" height="10" fill="none" stroke="#fbbf24" stroke-width="1.5" transform="rotate(-45 76 132)" />
  <path d="M 125,240 A 20,20 0 0,0 108,224" class="geo-angle" />
  <text x="96" y="234" class="geo-text" font-size="12">48°</text>

  <!-- x açısı yayı -->
  <path d="M 166,135 A 18,18 0 0,1 176,155" class="geo-angle" stroke="#f43f5e" />
  <text x="150" y="152" class="geo-text" fill="#f43f5e">x</text>

  <!-- Köşe Harfleri -->
  <text x="115" y="30" class="geo-text">C</text>
  <text x="24" y="248" class="geo-text">A</text>
  <text x="248" y="248" class="geo-text">B</text>
  <text x="56" y="142" class="geo-text">K</text>
  <text x="185" y="36" class="geo-text">M</text>
  <text x="165" y="305" class="geo-text">L</text>
  <text x="110" y="258" class="geo-text">D</text>
  <text x="182" y="145" class="geo-text">E</text>
</svg>"""
    out_path = SVG_DIR / "geo_ucgen_aci_q44.svg"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    return f"/assets/questions/svg/{out_path.name}"

def generate_q45_svg():
    """
    Soru 45: ABC üçgeninde taralı bölgenin alanı.
    """
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 280" width="100%" height="240">
  <defs>
    <style>
      .geo-line { stroke: #38bdf8; stroke-width: 2.5; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .geo-text { font-family: -apple-system, sans-serif; font-size: 14px; font-weight: 600; fill: #f1f5f9; }
      .geo-shaded { fill: rgba(244, 63, 94, 0.25); stroke: #f43f5e; stroke-width: 2; }
    </style>
  </defs>

  <!-- ABC Üçgeni -->
  <polygon points="120,40 50,220 280,220" class="geo-line" />

  <!-- D, E, F noktaları ve Taralı Üçgen (DEF) -->
  <polygon points="85,130 180,90 140,220" class="geo-shaded" />

  <!-- Köşe ve Kenar Etiketleri -->
  <text x="115" y="30" class="geo-text">C</text>
  <text x="35" y="228" class="geo-text">A</text>
  <text x="290" y="228" class="geo-text">B</text>
  <text x="68" y="132" class="geo-text">D</text>
  <text x="190" y="90" class="geo-text">F</text>
  <text x="135" y="238" class="geo-text">E</text>
  <text x="50" y="180" class="geo-text" font-size="12">5</text>
  <text x="100" y="80" class="geo-text" font-size="12">3</text>
</svg>"""
    out_path = SVG_DIR / "geo_ucgen_alan_q45.svg"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    return f"/assets/questions/svg/{out_path.name}"

def generate_q46_svg():
    """
    Soru 46: ABCD Karesi ve boyalı bölgeler.
    """
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 280" width="100%" height="240">
  <defs>
    <style>
      .geo-line { stroke: #38bdf8; stroke-width: 2.5; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .geo-text { font-family: -apple-system, sans-serif; font-size: 14px; font-weight: 600; fill: #f1f5f9; }
      .geo-shaded { fill: rgba(56, 189, 248, 0.3); stroke: #38bdf8; stroke-width: 2; }
    </style>
  </defs>

  <!-- ABCD Karesi -->
  <rect x="60" y="40" width="180" height="180" class="geo-line" />

  <!-- Boyalı üçgen bölgeler -->
  <polygon points="60,40 120,40 60,100" class="geo-shaded" />
  <polygon points="240,220 180,220 240,160" class="geo-shaded" />

  <!-- Köşe Harfleri -->
  <text x="45" y="40" class="geo-text">D</text>
  <text x="248" y="40" class="geo-text">C</text>
  <text x="45" y="228" class="geo-text">A</text>
  <text x="248" y="228" class="geo-text">B</text>
  <text x="85" y="32" class="geo-text">K</text>
  <text x="205" y="238" class="geo-text">M</text>
</svg>"""
    out_path = SVG_DIR / "geo_kare_alan_q46.svg"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    return f"/assets/questions/svg/{out_path.name}"

def generate_q47_svg():
    """
    Soru 47: ABCD dikdörtgeninde alan oranı.
    """
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240" width="100%" height="220">
  <defs>
    <style>
      .geo-line { stroke: #38bdf8; stroke-width: 2.5; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .geo-text { font-family: -apple-system, sans-serif; font-size: 14px; font-weight: 600; fill: #f1f5f9; }
      .geo-shaded { fill: rgba(16, 185, 129, 0.25); stroke: #10b981; stroke-width: 2; }
    </style>
  </defs>

  <!-- ABCD Dikdörtgeni -->
  <rect x="50" y="40" width="220" height="140" class="geo-line" />

  <!-- EFCG Dörtgeni (Taralı) -->
  <polygon points="120,40 270,40 270,130 180,180" class="geo-shaded" />

  <!-- Harfler -->
  <text x="35" y="40" class="geo-text">D</text>
  <text x="278" y="40" class="geo-text">C</text>
  <text x="35" y="188" class="geo-text">A</text>
  <text x="278" y="188" class="geo-text">B</text>
  <text x="115" y="30" class="geo-text">E</text>
  <text x="280" y="135" class="geo-text">F</text>
  <text x="175" y="198" class="geo-text">G</text>
</svg>"""
    out_path = SVG_DIR / "geo_dikdortgen_oran_q47.svg"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    return f"/assets/questions/svg/{out_path.name}"

def generate_q48_svg():
    """
    Soru 48: Yarım çember ve x uzunluğu.
    """
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240" width="100%" height="220">
  <defs>
    <style>
      .geo-line { stroke: #38bdf8; stroke-width: 2.5; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .geo-text { font-family: -apple-system, sans-serif; font-size: 14px; font-weight: 600; fill: #f1f5f9; }
      .geo-accent { stroke: #fbbf24; stroke-width: 2; stroke-dasharray: 4,4; fill: none; }
    </style>
  </defs>

  <!-- Çap [AB] ve Merkez O -->
  <line x1="50" y1="180" x2="270" y2="180" class="geo-line" />
  <circle cx="160" cy="180" r="3" fill="#38bdf8" />
  
  <!-- Yarım Çember Yayı -->
  <path d="M 50,180 A 110,110 0 0,1 270,180" class="geo-line" />

  <!-- C Noktası ve Üçgen Bağlantıları -->
  <line x1="50" y1="180" x2="110" y2="88" class="geo-line" />
  <line x1="110" y1="88" x2="270" y2="180" class="geo-line" />
  <circle cx="110" cy="88" r="3" fill="#fbbf24" />

  <!-- x çizgisi ve dikme -->
  <line x1="110" y1="88" x2="110" y2="180" class="geo-accent" />

  <!-- Etiketler -->
  <text x="35" y="186" class="geo-text">A</text>
  <text x="278" y="186" class="geo-text">B</text>
  <text x="156" y="200" class="geo-text">O</text>
  <text x="105" y="76" class="geo-text">C</text>
  <text x="116" y="140" class="geo-text" fill="#fbbf24">x</text>
</svg>"""
    out_path = SVG_DIR / "geo_cember_yarim_q48.svg"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    return f"/assets/questions/svg/{out_path.name}"

def generate_all_svgs():
    return {
        44: generate_q44_svg(),
        45: generate_q45_svg(),
        46: generate_q46_svg(),
        47: generate_q47_svg(),
        48: generate_q48_svg()
    }

if __name__ == "__main__":
    svgs = generate_all_svgs()
    print(f"Başarıyla {len(svgs)} adet vektörel geometri SVG dosyası üretildi!")
