#!/usr/bin/env python3
"""
scripts/generators/geometry_generator.py
Geometri soruları için şeffaf, vektörel ve karanlık/aydınlık tema uyumlu
matematiksel olarak kesin ÖSYM SVG çizimleri üretir.
"""

from pathlib import Path

SVG_DIR = Path("public/assets/questions/svg")
SVG_DIR.mkdir(parents=True, exist_ok=True)

COMMON_STYLE = """
    <style>
      .geo-line { stroke: var(--text-primary, #f1f5f9); stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .geo-sec { stroke: var(--accent-primary, #38bdf8); stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .geo-accent { stroke: var(--zen-warning, #f59e0b); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .geo-shaded { fill: var(--geo-shaded-fill, rgba(56, 189, 248, 0.28)); stroke: var(--geo-shaded-stroke, var(--accent-primary, #38bdf8)); stroke-width: 2.2; stroke-linejoin: round; }
      .geo-text { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif; font-size: 15px; font-weight: 600; fill: var(--text-primary, #f1f5f9); text-anchor: middle; dominant-baseline: central; }
      .geo-text-muted { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif; font-size: 13px; font-weight: 500; fill: var(--text-secondary, #94a3b8); text-anchor: middle; dominant-baseline: central; }
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
        .geo-right-angle { stroke: var(--text-muted, #64748b); }
        .geo-angle-arc { stroke: var(--zen-warning, #d97706); }
      }
    </style>
"""

def generate_q44_svg():
    """
    Soru 44: ABC eşkenar üçgen, KLM ikizkenar dik üçgen.
    [KL] ⊥ [KM], m(ADK) = 48°, m(CEL) = x.
    Hesaplanan x = 147°.
    """
    # Koordinatlar:
    # A = (50, 240), B = (270, 240), C = (160, 49.5)
    # K = (105, 145) üzerinde AC
    # D = (190, 240) üzerinde AB
    # L = (226, 280)
    # M = (235, 42)
    # E = (230, 171) üzerinde BC
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 310" width="100%" height="280">
  <defs>
    {COMMON_STYLE}
  </defs>

  <!-- ABC Eşkenar Üçgeni -->
  <polygon points="160,48 50,238 270,238" class="geo-line" />

  <!-- KLM İkizkenar Dik Üçgeni ([KL] ve [KM]) -->
  <line x1="105" y1="143" x2="226" y2="280" class="geo-sec" />
  <line x1="105" y1="143" x2="235" y2="42" class="geo-sec" />
  <line x1="235" y1="42" x2="226" y2="280" class="geo-sec" />

  <!-- K Köşesinde Dik Açı Sembolü -->
  <path d="M 112,135 L 120,142 L 113,150" class="geo-right-angle" />
  <circle cx="115" cy="142" r="1.5" class="geo-point" />

  <!-- 48° Açı Yayı (D noktasında) -->
  <path d="M 172,238 A 18,18 0 0,1 176,224" class="geo-angle-arc" />
  <text x="148" y="222" class="geo-text-muted">48°</text>

  <!-- x Açısı Yayı (E noktasında) -->
  <path d="M 218,150 A 20,20 0 0,0 228,188" class="geo-angle-arc" stroke-width="2" />
  <text x="202" y="171" class="geo-text-accent">x</text>

  <!-- Nokta İsimleri & Köşeler -->
  <text x="160" y="32" class="geo-text">C</text>
  <text x="36" y="244" class="geo-text">A</text>
  <text x="284" y="244" class="geo-text">B</text>
  
  <text x="88" y="143" class="geo-text">K</text>
  <text x="248" y="38" class="geo-text">M</text>
  <text x="238" y="292" class="geo-text">L</text>
  <text x="188" y="255" class="geo-text">D</text>
  <text x="246" y="168" class="geo-text">E</text>
</svg>"""
    out_path = SVG_DIR / "geo_ucgen_aci_q44.svg"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    return svg_content, f"/assets/questions/svg/{out_path.name}"

def generate_q45_svg():
    """
    Soru 45: ABC eşkenar üçgen, [AC] ⊥ [DE], [DE] ⊥ [EF],
    |DA| = 1, |DC| = 5.
    DEF dik üçgeninin alanı: 2√3.
    """
    # A = (50, 240), B = (290, 240), C = (170, 32.2)
    # D = (70, 205.4)
    # E = (130, 240)
    # F = (210, 101.4)
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 280" width="100%" height="250">
  <defs>
    {COMMON_STYLE}
  </defs>

  <!-- ABC Eşkenar Üçgeni -->
  <polygon points="170,32 50,240 290,240" class="geo-line" />

  <!-- Boyalı Dik Üçgen (DEF) -->
  <polygon points="70,205 130,240 210,101" class="geo-shaded" />

  <!-- D noktasındaki dik açı sembolü ([AC] ⊥ [DE]) -->
  <path d="M 77,193 L 88,199 L 81,211" class="geo-right-angle" />
  <circle cx="82" cy="201" r="1.5" class="geo-point" />

  <!-- E noktasındaki dik açı sembolü ([DE] ⊥ [EF]) -->
  <path d="M 120,234 L 126,224 L 136,230" class="geo-right-angle" />
  <circle cx="127" cy="229" r="1.5" class="geo-point" />

  <!-- Kenar Uzunlukları -->
  <text x="48" y="218" class="geo-text-muted">1</text>
  <text x="110" y="112" class="geo-text-muted">5</text>

  <!-- Köşe Harfleri -->
  <text x="170" y="16" class="geo-text">C</text>
  <text x="36" y="246" class="geo-text">A</text>
  <text x="304" y="246" class="geo-text">B</text>
  <text x="56" y="196" class="geo-text">D</text>
  <text x="130" y="258" class="geo-text">E</text>
  <text x="226" y="98" class="geo-text">F</text>
</svg>"""
    out_path = SVG_DIR / "geo_ucgen_alan_q45.svg"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    return svg_content, f"/assets/questions/svg/{out_path.name}"

def generate_q46_svg():
    """
    Soru 46: ABCD Karesi (|AB| = 6).
    |AK| = |LC| = 2, |CM| = |NA| = 2.
    Kare içerisinde KM ve NL doğruları çizilerek oluşturulan iki boyalı dörtgen.
    Toplam alan: 12 birimkare.
    """
    # Kare: A=(50, 250), B=(250, 250), C=(250, 50), D=(50, 50)
    # Boyut: 200x200 (scale: 200/6 = 33.33 px / birim)
    # 2 birim = 66.7 px, 4 birim = 133.3 px
    # K = (117, 250) üzerinde AB (AK = 2)
    # L = (250, 117) üzerinde BC (LC = 2 -> 50 + 66.7 = 116.7)
    # M = (183, 50) üzerinde CD (CM = 2 -> 250 - 66.7 = 183.3)
    # N = (50, 183) üzerinde AD (NA = 2 -> 250 - 66.7 = 183.3)
    # Kesişim P = (150, 150) (tam kare merkezi)
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 300" width="100%" height="260">
  <defs>
    {COMMON_STYLE}
  </defs>

  <!-- Boyalı Dörtgen 1: AKPN -->
  <polygon points="50,250 117,250 150,150 50,183" class="geo-shaded" />

  <!-- Boyalı Dörtgen 2: CLPM -->
  <polygon points="250,50 250,117 150,150 183,50" class="geo-shaded" />

  <!-- ABCD Karesi Çerçevesi -->
  <rect x="50" y="50" width="200" height="200" class="geo-line" />

  <!-- Kesit Doğruları [KM] ve [NL] -->
  <line x1="117" y1="250" x2="183" y2="50" class="geo-sec" />
  <line x1="50" y1="183" x2="250" y2="117" class="geo-sec" />

  <!-- Uzunluk Etiketleri (2) -->
  <text x="83" y="266" class="geo-text-muted">2</text>
  <text x="34" y="216" class="geo-text-muted">2</text>
  <text x="216" y="34" class="geo-text-muted">2</text>
  <text x="266" y="83" class="geo-text-muted">2</text>

  <!-- Köşe Harfleri -->
  <text x="36" y="50" class="geo-text">D</text>
  <text x="264" y="50" class="geo-text">C</text>
  <text x="36" y="256" class="geo-text">A</text>
  <text x="264" y="256" class="geo-text">B</text>

  <text x="117" y="268" class="geo-text">K</text>
  <text x="266" y="117" class="geo-text">L</text>
  <text x="183" y="34" class="geo-text">M</text>
  <text x="34" y="183" class="geo-text">N</text>
</svg>"""
    out_path = SVG_DIR / "geo_kare_alan_q46.svg"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    return svg_content, f"/assets/questions/svg/{out_path.name}"

def generate_q47_svg():
    """
    Soru 47: ABCD dikdörtgen, |AE| = |EB|, |DG|/|GC| = |CF|/|FB| = 2/3.
    EFCG dörtgeni boyalı/işaretli.
    Alan oranı: Alan(EFCG) / Alan(ABCD) = 2/5.
    """
    # Dikdörtgen: A=(50, 200), B=(290, 200), C=(290, 60), D=(50, 60)
    # Genişlik = 240, Yükseklik = 140
    # E = midpoint of AB = (170, 200)
    # DG / GC = 2/3 -> DG = 2/5 * 240 = 96 -> G = (146, 60)
    # CF / FB = 2/3 -> CF = 2/5 * 140 = 56 -> F = (290, 116)
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 350 250" width="100%" height="230">
  <defs>
    {COMMON_STYLE}
  </defs>

  <!-- Boyalı Bölge: EFCG Dörtgeni -->
  <polygon points="170,200 290,116 290,60 146,60" class="geo-shaded" />

  <!-- ABCD Dikdörtgeni -->
  <rect x="50" y="60" width="240" height="140" class="geo-line" />

  <!-- Ayırıcı Doğrular [GE] ve [EF] -->
  <line x1="146" y1="60" x2="170" y2="200" class="geo-sec" />
  <line x1="170" y1="200" x2="290" y2="116" class="geo-sec" />

  <!-- Eşitlik Çentikleri (|AE| = |EB|) -->
  <line x1="108" y1="195" x2="112" y2="205" class="geo-line" stroke-width="1.8" />
  <line x1="228" y1="195" x2="232" y2="205" class="geo-line" stroke-width="1.8" />

  <!-- Köşe Harfleri -->
  <text x="36" y="60" class="geo-text">D</text>
  <text x="304" y="60" class="geo-text">C</text>
  <text x="36" y="206" class="geo-text">A</text>
  <text x="304" y="206" class="geo-text">B</text>

  <text x="170" y="218" class="geo-text">E</text>
  <text x="146" y="44" class="geo-text">G</text>
  <text x="306" y="116" class="geo-text">F</text>
</svg>"""
    out_path = SVG_DIR / "geo_dikdortgen_oran_q47.svg"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    return svg_content, f"/assets/questions/svg/{out_path.name}"

def generate_q48_svg():
    """
    Soru 48: O merkezli yarım çember. D ∈ [AC].
    |AD| = 14, |DC| = 2, |AO| = 10, |OD| = x.
    Hesaplanan x = 6√2.
    """
    # Çap AB: A=(40, 200), B=(280, 200), O=(160, 200), Yarıçap R=120 px
    # C noktası yarım çember üzerinde:
    # cos(OAC) = 0.8, sin(OAC) = 0.6
    # AC uzunluğu = 16 birim -> 192 px
    # C = (40 + 192*0.8, 200 - 192*0.6) = (193.6, 84.8)
    # D noktası AC üzerinde (AD = 14 birim -> 168 px):
    # D = (40 + 168*0.8, 200 - 168*0.6) = (174.4, 99.2)
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 330 250" width="100%" height="230">
  <defs>
    {COMMON_STYLE}
  </defs>

  <!-- Çap [AB] -->
  <line x1="40" y1="200" x2="280" y2="200" class="geo-line" />

  <!-- Yarım Çember Yayı -->
  <path d="M 40,200 A 120,120 0 0,1 280,200" class="geo-line" stroke-width="2.5" />

  <!-- Kiriş [AC] -->
  <line x1="40" y1="200" x2="194" y2="85" class="geo-line" />

  <!-- x Doğru Parçası [OD] -->
  <line x1="160" y1="200" x2="174" y2="99" class="geo-sec" stroke-width="2.4" />

  <!-- O ve D Noktaları -->
  <circle cx="160" cy="200" r="3" class="geo-point" />
  <circle cx="174" cy="99" r="3" class="geo-point" />
  <circle cx="194" cy="85" r="3" class="geo-point" />

  <!-- Uzunluk Değerleri -->
  <text x="100" y="216" class="geo-text-muted">10</text>
  <text x="100" y="132" class="geo-text-muted">14</text>
  <text x="190" y="74" class="geo-text-muted">2</text>
  <text x="178" y="152" class="geo-text-accent">x</text>

  <!-- Köşe ve Merkez Harfleri -->
  <text x="24" y="204" class="geo-text">A</text>
  <text x="296" y="204" class="geo-text">B</text>
  <text x="160" y="218" class="geo-text">O</text>
  <text x="164" y="88" class="geo-text">D</text>
  <text x="208" y="76" class="geo-text">C</text>
</svg>"""
    out_path = SVG_DIR / "geo_cember_yarim_q48.svg"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    return svg_content, f"/assets/questions/svg/{out_path.name}"

def generate_all_svgs():
    """
    Tüm geometri SVG'lerini üretir ve hem SVG içeriklerini hem URL'lerini döner.
    """
    svg_44, url_44 = generate_q44_svg()
    svg_45, url_45 = generate_q45_svg()
    svg_46, url_46 = generate_q46_svg()
    svg_47, url_47 = generate_q47_svg()
    svg_48, url_48 = generate_q48_svg()

    return {
        44: {"content": svg_44, "url": url_44},
        45: {"content": svg_45, "url": url_45},
        46: {"content": svg_46, "url": url_46},
        47: {"content": svg_47, "url": url_47},
        48: {"content": svg_48, "url": url_48}
    }

if __name__ == "__main__":
    res = generate_all_svgs()
    print(f"Başarıyla {len(res)} adet matematiksel kesinlikte geometri SVG'si üretildi!")
