import os
import re
import json
import fitz
from pathlib import Path
from .answer_key_parser import AnswerKeyParser

PAGE_MID_X = 297.6      # A4 sayfası yatay orta noktası (pt)
HEADER_MAX_Y = 120.0    # Sınav başlığı ve talimat alanları
FOOTER_MIN_Y = 745.0    # "Diğer sayfaya geçiniz" ve sayfa numarası alanı

class PDFExtractor:
    def __init__(self, output_dir="scripts/output"):
        self.output_dir = Path(output_dir)
        self.extracted_img_dir = self.output_dir / "extracted"
        self.raw_json_dir = self.output_dir / "raw_json"
        
        self.extracted_img_dir.mkdir(parents=True, exist_ok=True)
        self.raw_json_dir.mkdir(parents=True, exist_ok=True)

    def extract_exam(self, pdf_path: str) -> dict:
        """Tek bir PDF dosyasındaki tüm soruları ve cevap anahtarını ayrıştırır."""
        pdf_path = Path(pdf_path)
        doc = fitz.open(str(pdf_path))
        exam_stem = pdf_path.stem

        print(f"\n[PDFExtractor] İşleniyor: {pdf_path.name} ({len(doc)} sayfa)")

        # 1. Cevap Anahtarını Al
        answer_key = AnswerKeyParser.extract_from_doc(doc)
        print(f"  ✓ Cevap Anahtarı: Sayısal {len(answer_key['sayisal'])} soru, Sözel {len(answer_key['sozel'])} soru")

        exam_data = {
            "source_file": pdf_path.name,
            "exam_stem": exam_stem,
            "metadata": answer_key.get("metadata", {}),
            "answer_key": answer_key,
            "sections": {
                "sayisal": [],
                "sozel": []
            }
        }

        current_section = "sayisal"
        total_pages = len(doc)
        # Kapak (0, 1) ve cevap anahtarı (son sayfa) hariç soru sayfalarını tara
        question_page_indices = range(2, total_pages - 1)

        for page_idx in question_page_indices:
            page = doc[page_idx]
            page_text = page.get_text()

            # Bölüm geçişi kontrolü
            if re.search(r'S[ÖO]ZEL\s+TEST[Iİ]', page_text, re.I):
                # Eğer sayfa başında Sözel Testi başlığı varsa bölüme geç
                current_section = "sozel"

            # Sayfa bloklarını sol ve sağ sütunlara ayır
            left_blocks, right_blocks = self._split_columns(page)

            # Sütunlardaki soruları ayrıştır
            self._process_column(left_blocks, page, exam_stem, page_idx + 1, "L", current_section, exam_data)
            self._process_column(right_blocks, page, exam_stem, page_idx + 1, "R", current_section, exam_data)

        # Çıkarılan soruları soru numarasına göre sırala
        exam_data["sections"]["sayisal"].sort(key=lambda q: q.get("number", 0))
        exam_data["sections"]["sozel"].sort(key=lambda q: q.get("number", 0))

        # JSON olarak kaydet
        json_path = self.raw_json_dir / f"{exam_stem}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(exam_data, f, ensure_ascii=False, indent=2)

        print(f"  ✓ Çıkarılan Soru Sayısı: Sayısal: {len(exam_data['sections']['sayisal'])}, Sözel: {len(exam_data['sections']['sozel'])}")
        print(f"  ✓ Kaydedildi: {json_path}")

        return exam_data

    def _split_columns(self, page: fitz.Page):
        """Sayfadaki blokları sol ve sağ sütunlara böler, arka plan şeritlerini eler."""
        page_dict = page.get_text("dict")
        blocks = page_dict.get("blocks", [])

        left_col, right_col = [], []

        for b in blocks:
            bbox = b["bbox"]
            center_x = (bbox[0] + bbox[2]) / 2
            width = bbox[2] - bbox[0]
            y0 = bbox[1]
            y1 = bbox[3]

            # Sayfa üst bilgi veya alt bilgi sınırlarını filtrele
            if y1 < 65 and width > 200:
                continue
            if y0 > FOOTER_MIN_Y:
                continue

            # Arka plan şeritlerini filtrele (sayfa genişliğinde > 500pt görseller)
            if b["type"] == 1 and width > 500:
                continue

            if center_x < PAGE_MID_X:
                left_col.append(b)
            else:
                right_col.append(b)

        # Yukarıdan aşağıya (Y0) sırala
        left_col.sort(key=lambda x: x["bbox"][1])
        right_col.sort(key=lambda x: x["bbox"][1])

        return left_col, right_col

    def _process_column(self, blocks, page: fitz.Page, exam_stem: str, page_num: int, col_side: str, section: str, exam_data: dict):
        """Bir sütundaki blokları soru numaralarına göre gruplar."""
        if not blocks:
            return

        current_q = None

        for b in blocks:
            btype = b["type"]
            bbox = b["bbox"]

            if btype == 0:  # Metin Bloğu
                text = self._extract_block_text(b).strip()
                if not text:
                    continue

                # Soru numarası tespiti: örn "1.", "44." veya "1. Bu testte..." hariç
                q_num_match = re.match(r'^(\d{1,2})\.(?:\s+(.*))?$', text, re.DOTALL)
                
                # Talimat cümlelerini (1. Bu testte 50 soru vardır) soru olarak alma
                is_instruction = "Bu testte" in text or "Cevaplarınızı" in text or "sorularda" in text

                if q_num_match and not is_instruction:
                    # Yeni soru başladı
                    q_num = int(q_num_match.group(1))
                    rest_text = q_num_match.group(2) or ""

                    # Önceki soruyu kaydet
                    if current_q:
                        self._finalize_question(current_q, section, exam_data)

                    current_q = {
                        "number": q_num,
                        "section": section,
                        "page": page_num,
                        "column": col_side,
                        "raw_lines": [rest_text] if rest_text else [],
                        "images": [],
                        "options": {"A": "", "B": "", "C": "", "D": "", "E": ""},
                        "correct_answer": exam_data["answer_key"][section].get(q_num, "")
                    }
                else:
                    if current_q:
                        # Şık kontrolü yap (A) B) C)...)
                        self._parse_options_or_body(text, current_q)

            elif btype == 1:  # Görsel Bloğu
                if current_q:
                    img_info = self._save_image(b, page, exam_stem, page_num, current_q["number"], len(current_q["images"]))
                    if img_info:
                        current_q["images"].append(img_info)

        if current_q:
            self._finalize_question(current_q, section, exam_data)

    def _extract_block_text(self, block) -> str:
        """Metin bloğundan satırları ve boşlukları birleştirir."""
        lines = []
        for line in block.get("lines", []):
            line_text = "".join(span.get("text", "") for span in line.get("spans", []))
            lines.append(line_text)
        return "\n".join(lines)

    def _parse_options_or_body(self, text: str, question: dict):
        """Satır içindeki şıkları (A, B, C, D, E) veya soru gövdesini ayıklar."""
        # Tek satırda şıklar: A) ... B) ...
        # Veya alt alta şıklar
        option_pattern = r'([A-E])\)\s*([^A-E\)]*)'
        matches = list(re.finditer(option_pattern, text))

        if matches:
            for m in matches:
                opt_key = m.group(1)
                opt_val = m.group(2).strip()
                question["options"][opt_key] = opt_val
        else:
            question["raw_lines"].append(text)

    def _save_image(self, block, page: fitz.Page, exam_stem: str, page_num: int, q_num: int, img_idx: int) -> dict:
        """Görseli yüksek çözünürlükle PNG olarak kaydeder ve türünü sınıflandırır."""
        bbox = fitz.Rect(block["bbox"])
        w_pt = bbox.width
        h_pt = bbox.height

        # Tür sınıflandırma
        if w_pt < 65 and h_pt < 20:
            img_type = "formula"
        elif w_pt >= 60 and h_pt >= 40:
            img_type = "geometry_or_chart"
        elif w_pt > 150:
            img_type = "table"
        else:
            img_type = "snippet"

        filename = f"{exam_stem}_P{page_num:02d}_Q{q_num:02d}_{img_type}_{img_idx}.png"
        file_path = self.extracted_img_dir / filename

        try:
            # 2x Retina ölçeğinde net render al
            pix = page.get_pixmap(clip=bbox, dpi=150)
            pix.save(str(file_path))

            return {
                "filename": filename,
                "relative_path": f"scripts/output/extracted/{filename}",
                "type": img_type,
                "width_pt": round(w_pt, 1),
                "height_pt": round(h_pt, 1),
                "bbox": [round(x, 1) for x in block["bbox"]]
            }
        except Exception as e:
            print(f"    [Uyarı] Görsel kaydedilemedi ({filename}): {e}")
            return None

    def _finalize_question(self, question: dict, section: str, exam_data: dict):
        """Soruyu temizleyip nihai listeye ekler."""
        body_text = "\n".join(question["raw_lines"]).strip()
        question["question_text"] = body_text
        del question["raw_lines"]

        exam_data["sections"][section].append(question)
