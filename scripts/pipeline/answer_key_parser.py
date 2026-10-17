import re
import fitz

class AnswerKeyParser:
    """
    ÖSYM ALES PDF'lerinin son sayfasındaki cevap anahtarını ayrıştırır.
    Format: 'SAYISAL TESTİ' ve 'SÖZEL TESTİ' altında 1-50 arası soru ve A-E şık eşleşmeleri.
    """

    @staticmethod
    def extract_from_doc(doc: fitz.Document) -> dict:
        """PDF dökümanının son sayfasını okuyup cevap anahtarı sözlüğünü döndürür."""
        # Son sayfadan başlayarak cevap anahtarını içeren sayfayı ara
        last_page_idx = len(doc) - 1
        page_text = doc[last_page_idx].get_text()

        # Eğer son sayfada cevap anahtarı yoksa bir önceki sayfayı dene
        if not re.search(r'SAYISAL\s+TEST[Iİ]', page_text, re.I):
            if last_page_idx > 0:
                prev_text = doc[last_page_idx - 1].get_text()
                if re.search(r'SAYISAL\s+TEST[Iİ]', prev_text, re.I):
                    page_text = prev_text

        return AnswerKeyParser.parse_text(page_text)

    @staticmethod
    def parse_text(text: str) -> dict:
        """Cevap anahtarı metnini parse eder."""
        answers = {
            "metadata": {
                "exam_title": "",
                "exam_code": "",
                "exam_date": ""
            },
            "sayisal": {},
            "sozel": {}
        }

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        current_section = None

        # Başlık meta verilerini yakala (ilk 3 satır)
        for line in lines[:5]:
            if "AKADEMİK PERSONEL" in line or "ALES" in line:
                if not answers["metadata"]["exam_title"]:
                    answers["metadata"]["exam_title"] = line
            if re.match(r'\d{4}\s*-\s*ALES/\d', line):
                answers["metadata"]["exam_code"] = line
            if re.match(r'\d{2}-\d{2}-\d{4}', line):
                answers["metadata"]["exam_date"] = line

        for line in lines:
            # Bölüm tespiti (SAYISAL TESTİ veya SÖZEL TESTİ)
            if re.search(r'SAYISAL\s+TEST[Iİ]', line, re.I):
                current_section = "sayisal"
                continue
            elif re.search(r'S[ÖO]ZEL\s+TEST[Iİ]', line, re.I):
                current_section = "sozel"
                continue

            if current_section:
                # Soru ve cevap eşleşmesi: örn "1.   B" veya "14. D"
                match = re.match(r'^(\d+)\.\s*([A-E])$', line)
                if match:
                    q_num = int(match.group(1))
                    opt = match.group(2)
                    answers[current_section][q_num] = opt

        return answers
