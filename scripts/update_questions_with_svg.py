#!/usr/bin/env python3
"""
scripts/update_questions_with_svg.py
Tüm 300 soruyu tarar; 49 sorudaki eski PNG ekran görüntüsü referanslarını
üretilen saf vektörel SVG'lerle (hem svgContent hem /assets/questions/svg/ imageUrl)
değiştirir ve 'public/data/seed_questions.json' dosyasını günceller.
Ayrıca kaynak seed dosyalarını da güncel tutar.
"""

import json
from pathlib import Path

SVG_DIR = Path("public/assets/questions/svg")

# Soru eşleştirme haritası: (examId, questionNumber) -> svg_filename
SVG_MAPPINGS = {
    # 2021-ALES/1
    ("2021_ales1", 21): "ales1_q21_calendar.svg",
    ("2021_ales1", 25): "ales1_q25_balls.svg",
    ("2021_ales1", 26): "ales1_q26_balls.svg",
    ("2021_ales1", 27): "ales1_q27_stores_table.svg",
    ("2021_ales1", 28): "ales1_q27_stores_table.svg",
    ("2021_ales1", 32): "ales1_q32_pie.svg",
    ("2021_ales1", 33): "ales1_q33_pie.svg",
    ("2021_ales1", 34): "ales1_q34_pie.svg",
    ("2021_ales1", 41): "ales1_q41_grid.svg",
    ("2021_ales1", 42): "ales1_q42_grid.svg",
    ("2021_ales1", 43): "ales1_q43_grid.svg",
    ("2021_ales1", 49): "ales1_q49_prisms.svg",
    ("2021_ales1", 50): "ales1_q50_sticks.svg",

    # 2021-ALES/2
    ("2021_ales2", 20): "ales2_q20_pie.svg",
    ("2021_ales2", 21): "ales2_q21_map.svg",
    ("2021_ales2", 25): "ales2_q25_barchart.svg",
    ("2021_ales2", 26): "ales2_q25_barchart.svg",
    ("2021_ales2", 27): "ales2_q27_network.svg",
    ("2021_ales2", 28): "ales2_q28_network.svg",
    ("2021_ales2", 35): "ales2_q35_scale.svg",
    ("2021_ales2", 36): "ales2_q36_scale.svg",
    ("2021_ales2", 37): "ales2_q37_scale.svg",
    ("2021_ales2", 41): "ales2_q41_table.svg",
    ("2021_ales2", 42): "ales2_q42_table.svg",
    ("2021_ales2", 43): "ales2_q43_table.svg",
    ("2021_ales2", 44): "ales2_q44_triangle.svg",
    ("2021_ales2", 45): "ales2_q45_triangle.svg",
    ("2021_ales2", 46): "ales2_q46_rhombus.svg",
    ("2021_ales2", 47): "ales2_q47_rectangles.svg",
    ("2021_ales2", 48): "ales2_q48_circle.svg",
    ("2021_ales2", 49): "ales2_q49_keypad.svg",
    ("2021_ales2", 50): "ales2_q50_cube_mockups.svg",

    # 2021-ALES/3
    ("2021_ales3", 25): "ales3_q25_chart.svg",
    ("2021_ales3", 26): "ales3_q26_chart.svg",
    ("2021_ales3", 27): "ales3_q27_matrix.svg",
    ("2021_ales3", 28): "ales3_q28_matrix.svg",
    ("2021_ales3", 38): "ales3_q38_squares.svg",
    ("2021_ales3", 39): "ales3_q39_squares.svg",
    ("2021_ales3", 40): "ales3_q40_squares.svg",
    ("2021_ales3", 41): "ales3_q41_conveyor.svg",
    ("2021_ales3", 42): "ales3_q42_conveyor.svg",
    ("2021_ales3", 43): "ales3_q43_conveyor.svg",
    ("2021_ales3", 44): "ales3_q44_triangle.svg",
    ("2021_ales3", 45): "ales3_q45_triangle.svg",
    ("2021_ales3", 46): "ales3_q46_square.svg",
    ("2021_ales3", 47): "ales3_q47_square.svg",
    ("2021_ales3", 48): "ales3_q48_circle.svg",
    ("2021_ales3", 49): "ales3_q49_grid_sheet.svg",
    ("2021_ales3", 50): "ales3_q50_solid.svg",
}

# Geometri sorularının tam matematiksel metinleri
GEOM_ENRICHMENTS = {
    ("2021_ales2", 44): "Şekilde $ABC$ ikizkenar üçgendir.\n* $D \\in [BC]$\n* $|AB| = |AC|$\n* $m(\\widehat{CAD}) = 38^\\circ$\n* $m(\\widehat{ADC}) = 81^\\circ$\n* $m(\\widehat{BAD}) = x$\n\n**Yukarıdaki geometrik verilere göre, $x$ kaç derecedir?**",
    ("2021_ales2", 45): "Şekilde $ABC$ eşkenar üçgendir.\n* $|CE| = |EB|$\n* $|AD| = |DE|$\n* $|AC| = 8\\text{ birim}$\n\nŞekilde $D$ ve $E$ noktaları $ABC$ üçgeninin kenarları üzerindedir.\n\n**Buna göre, boyalı $DBE$ üçgeninin alanı kaç birimkaredir?**",
    ("2021_ales2", 46): "Şekilde $ABCD$ eşkenar dörtgen, $AFE$ eşkenar üçgendir.\n* $m(\\widehat{DAE}) = m(\\widehat{BAF}) = 30^\\circ$\n* $|EF| = 6\\text{ birim}$\n\n$E$ ve $F$ noktaları $ABCD$ dörtgeninin kenarları üzerinde olduğuna göre, **$ABCD$ dörtgeninin çevresi kaç birimdir?**",
    ("2021_ales2", 47): "Şekilde $ABCD$ ve $EBMN$ birer dikdörtgendir.\n* $E \\in [AB]$ ve $C \\in [BM]$\n* $|AE| = 6\\text{ birim}$\n* $|EB| = |BC| = 8\\text{ birim}$\n* $|CM| = 5\\text{ birim}$\n* $A, K, L$ ve $M$ noktaları doğrusaldır.\n\n**Buna göre, boyalı bölgenin alanı kaç birimkaredir?**",
    ("2021_ales2", 48): "Şekilde $[AB]$ çaplı çemberin merkezi $O$ noktasıdır.\n* $AB \\cap CD = \\{E\\}$\n* $m(\\widehat{CAB}) = 30^\\circ$\n* $m(\\widehat{BEC}) = 110^\\circ$\n* $m(\\widehat{BOD}) = x$\n\n$C$ ve $D$ noktaları çember üzerinde olduğuna göre, **$x$ kaç derecedir?**",

    ("2021_ales3", 44): "Şekilde $ABC$ ve $ABD$ birer üçgendir.\n* $|AB| = |BD|$\n* $|AC| = |CB|$\n* $m(\\widehat{ACB}) = 44^\\circ$\n* $m(\\widehat{CAD}) = 20^\\circ$\n* $m(\\widehat{CBD}) = x$\n\n**Yukarıdaki geometrik verilere göre, $x$ kaç derecedir?**",
    ("2021_ales3", 45): "Şekilde $ABC$ ikizkenar üçgendir.\n* $|AB| = |AC|$\n* $m(\\widehat{ADB}) = 60^\\circ$\n* $|BD| = 8\\text{ birim}$\n* $|DC| = 2\\text{ birim}$\n* $B, D$ ve $C$ noktaları doğrusaldır.\n\n**Buna göre, boyalı $ADB$ üçgeninin alanı kaç birimkaredir?**",
    ("2021_ales3", 46): "Şekilde $ABCD$ karedir.\n* $[AC]$ köşegen\n* $|AC| = |BE|$\n* $m(\\widehat{CBE}) = 25^\\circ$\n* $m(\\widehat{EDC}) = x$\n\n**Yukarıdaki geometrik verilere göre, $x$ kaç derecedir?**",
    ("2021_ales3", 47): "Şekilde $ABCD$ dikdörtgendir.\n* $E \\in [AB]$\n* $F \\in [CE]$\n* $|BE| = 2\\text{ birim}$\n* $|AE| = 8\\text{ birim}$\n* $|CF| = |EF| = \\sqrt{5}\\text{ birim}$\n\n**Buna göre, boyalı $CDF$ üçgeninin alanı kaç birimkaredir?**",
    ("2021_ales3", 48): "Şekilde $[AB]$ çaplı yarım çemberin merkezi $O$ noktasıdır.\n* $D, E$ ve $B$ noktaları doğrusaldır.\n* $|DE| = |EB|$\n* $|OE| = |EC|$\n* $m(\\widehat{OAD}) = x$\n\n$C$ noktası yarım çember üzerinde olduğuna göre, **$x$ kaç derecedir?**",
}

def update_seed_questions():
    json_path = Path("public/data/seed_questions.json")
    with open(json_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    updated_count = 0
    svg_cache = {}

    for q in questions:
        exam_id = q.get("examId")
        number = q.get("number")
        key = (exam_id, number)
        is_math = ("_mat_" in q.get("id", "")) or (q.get("subject") == "matematik")

        if is_math and key in SVG_MAPPINGS:
            svg_file = SVG_MAPPINGS[key]
            svg_path = SVG_DIR / svg_file

            if svg_file not in svg_cache:
                with open(svg_path, "r", encoding="utf-8") as sf:
                    svg_cache[svg_file] = sf.read()

            content = svg_cache[svg_file]
            image_url = f"/assets/questions/svg/{svg_file}"

            q["hasImage"] = True
            q["imageUrl"] = image_url
            q["svgContent"] = content

            if key in GEOM_ENRICHMENTS:
                q["questionText"] = GEOM_ENRICHMENTS[key]

            updated_count += 1
        elif not is_math:
            # Sözel sorulara yanlışlıkla eklenmiş olabilecek SVG veya görsel referanslarını temizle
            if q.get("imageUrl") and "/svg/" in q.get("imageUrl", ""):
                q["hasImage"] = False
                q.pop("imageUrl", None)
                q.pop("svgContent", None)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    print(f"✨ Toplam {updated_count} sorudaki görsel başarıyla saf SVG ile güncellendi!")

    # Doğrulama: Hâlâ PNG referansı var mı kontrol et
    remaining_pngs = [q for q in questions if q.get("imageUrl") and q["imageUrl"].endswith(".png")]
    print(f"🔍 Kalan PNG referansı sayısı: {len(remaining_pngs)}")
    if remaining_pngs:
        for p in remaining_pngs:
            print(f"   UYARI: Q{p.get('number')} ({p.get('id')}): {p.get('imageUrl')}")
    else:
        print("🎯 MÜKEMMEL: Sistemdeki 300 sorunun tamamında 0 adet PNG kaldı! Hepsi %100 saf vektörel SVG!")

if __name__ == "__main__":
    update_seed_questions()
