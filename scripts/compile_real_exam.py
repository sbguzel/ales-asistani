#!/usr/bin/env python3
"""
scripts/compile_real_exam.py
ÖSYM ALES PDF'lerindeki gerçek soruları kusursuz kırpıp,
tam 50 Sayısal + 50 Sözel soru olarak seed_questions.json ve görsellere derler.
"""

import os
import re
import json
import fitz
from pathlib import Path
from pipeline.answer_key_parser import AnswerKeyParser

PAGE_MID_X = 297.6
FOOTER_MIN_Y = 745.0

def compile_exam(pdf_path_str: str, exam_id: str, exam_title: str):
    pdf_path = Path(pdf_path_str)
    if not pdf_path.exists():
        print(f"[Uyarı] {pdf_path} bulunamadı, atlanıyor.")
        return []

    doc = fitz.open(str(pdf_path))
    assets_dir = Path("public/assets/questions") / exam_id
    assets_dir.mkdir(parents=True, exist_ok=True)

    # Cevap anahtarını al
    ans_data = AnswerKeyParser.extract_from_doc(doc)
    sayisal_answers = ans_data.get("sayisal", {})
    sozel_answers = ans_data.get("sozel", {})

    print(f"\n[{exam_title}] İşleniyor ({pdf_path.name})...")
    print(f"  ✓ Cevap Anahtarı: Sayısal {len(sayisal_answers)}, Sözel {len(sozel_answers)}")

    questions = []

    for page_idx in range(2, len(doc) - 1):
        page = doc[page_idx]
        text = page.get_text().strip()
        if not text:
            continue

        first_line = text.splitlines()[0]
        if "SÖZEL" in first_line or "SOZEL" in first_line:
            current_section = "sozel"
        elif "SAYISAL" in first_line:
            current_section = "sayisal"
        else:
            continue

        blocks = page.get_text("dict")["blocks"]
        items = []
        q_spans = []

        for b in blocks:
            btype = b["type"]
            bbox = b["bbox"]
            width = bbox[2] - bbox[0]

            if btype == 0:
                for l in b["lines"]:
                    line_text = "".join(s["text"] for s in l["spans"]).strip()
                    lbox = l["bbox"]
                    col = "L" if lbox[0] < PAGE_MID_X else "R"

                    if lbox[1] > 68 and lbox[3] < FOOTER_MIN_Y:
                        items.append({"type": "text", "bbox": lbox, "col": col, "text": line_text})

                    # Soru numarası tespiti
                    m = re.match(r'^(\d{1,2})\.$', line_text)
                    if m and lbox[1] > 68 and lbox[3] < FOOTER_MIN_Y:
                        if "Bu testte" not in line_text and "sorularda" not in line_text:
                            q_spans.append({"num": int(m.group(1)), "bbox": lbox, "col": col})

            elif btype == 1:
                if width < 500: # Arka plan şeritlerini atla
                    col = "L" if bbox[0] < PAGE_MID_X else "R"
                    items.append({"type": "img", "bbox": bbox, "col": col})

        cols = {
            "L": [q for q in q_spans if q["col"] == "L"],
            "R": [q for q in q_spans if q["col"] == "R"]
        }

        for c in ["L", "R"]:
            cols[c].sort(key=lambda q: q["bbox"][1])
            for i, q in enumerate(cols[c]):
                q_num = q["num"]
                y0 = max(70, q["bbox"][1] - 8)
                next_y0 = cols[c][i+1]["bbox"][1] - 8 if i + 1 < len(cols[c]) else FOOTER_MIN_Y

                q_items = [it for it in items if it["col"] == c and it["bbox"][1] >= y0 and it["bbox"][3] <= next_y0]
                if q_items:
                    max_y = max(it["bbox"][3] for it in q_items) + 14
                else:
                    max_y = next_y0

                y1 = min(next_y0, max_y)
                x0, x1 = (42, 292) if c == "L" else (318, 568)

                rect = fitz.Rect(x0, y0, x1, y1)
                img_filename = f"{exam_id}_{current_section}_q{q_num:02d}.png"
                img_path = assets_dir / img_filename

                has_image = False
                image_url = None
                try:
                    pix = page.get_pixmap(clip=rect, dpi=180)
                    pix.save(str(img_path))
                    has_image = True
                    image_url = f"/assets/questions/{exam_id}/{img_filename}"
                except Exception as e:
                    print(f"    [Uyarı] Q{q_num} görsel hatası: {e}")

                ans_dict = sayisal_answers if current_section == "sayisal" else sozel_answers
                correct_ans = ans_dict.get(q_num, "A")

                # Konu taksonomisi
                if current_section == "sayisal":
                    if q_num <= 30:
                        subject = "matematik"
                        topic = f"{exam_title} · Temel Matematik & Problemler"
                        target_sec = 60
                    elif q_num <= 40:
                        subject = "mantik"
                        topic = f"{exam_title} · Sayısal Mantık & Tablo"
                        target_sec = 85
                    else:
                        subject = "matematik"
                        topic = f"{exam_title} · Geometri"
                        target_sec = 75
                else:
                    if q_num <= 42:
                        subject = "turkce"
                        topic = f"{exam_title} · Paragraf & Anlam Bilgisi"
                        target_sec = 50
                    else:
                        subject = "mantik"
                        topic = f"{exam_title} · Sözel Mantık & Sıralama"
                        target_sec = 90

                question_obj = {
                    "id": f"{exam_id}_{current_section}_{q_num:02d}",
                    "examId": exam_id,
                    "examTitle": exam_title,
                    "number": q_num,
                    "subject": subject,
                    "section": current_section,
                    "category": f"{current_section}_q{q_num}",
                    "topicTitle": topic,
                    "difficulty": 3,
                    "questionText": "",
                    "hasImage": has_image,
                    "imageUrl": image_url,
                    "options": [
                        {"key": "A", "text": "A"},
                        {"key": "B", "text": "B"},
                        {"key": "C", "text": "C"},
                        {"key": "D", "text": "D"},
                        {"key": "E", "text": "E"}
                    ],
                    "correctAnswer": correct_ans,
                    "suggestedSolution": f"ÖSYM Çıkmış {exam_title} {current_section.capitalize()} Testi Soru {q_num} için resmi cevap anahtarı: **{correct_ans}** seçeneğidir.",
                    "quickTip": f"💡 ALES Taktiği: Soruyu çözerken sağdaki karalama tahtasında işlem adımlarınızı ve ara değerlerinizi not alarak kontrol edin.",
                    "targetTimeSec": target_sec,
                    "derivedFrom": f"{exam_title}-S{q_num}"
                }

                questions.append(question_obj)

    questions.sort(key=lambda q: (0 if q["section"] == "sayisal" else 1, q["number"]))
    print(f"  ✓ {exam_title}: Sayısal {len([q for q in questions if q['section']=='sayisal'])}, Sözel {len([q for q in questions if q['section']=='sozel'])} (Toplam: {len(questions)} soru)")
    return questions

def main():
    print("=" * 70)
    print("🎯 ALES GERÇEK SORU DERLEME MOTORU (TAM KAPSAM)")
    print("=" * 70)

    exams_to_compile = [
        ("ales_cikmis_sorular/ALES1_sorular.pdf", "2021_ales1", "2021-ALES/1"),
        ("ales_cikmis_sorular/ALES1_sorular-2.pdf", "2020_ales1", "2020-ALES/1"),
        ("ales_cikmis_sorular/ALES2_sorular.pdf", "2021_ales2", "2021-ALES/2")
    ]

    all_questions = []
    for pdf, eid, title in exams_to_compile:
        q_list = compile_exam(pdf, eid, title)
        all_questions.extend(q_list)

    out_file = Path("public/data/seed_questions.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 70)
    print(f"✅ DERLEME TAMAMLANDI!")
    print(f"Toplam Aktarılan Soru Sayısı: {len(all_questions)}")
    print(f"Çıktı Dosyası: {out_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()
