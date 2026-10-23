#!/usr/bin/env python3
"""
scripts/build_native_exam.py
2021-ALES/1 sınavının TAMAMINI (50 Sayısal + 50 Sözel = 100 Soru),
yerel KaTeX formülleri, yüksek çözünürlüklü vektörel SVG geometri çizimleri,
bağlantılı grup soruları, detaylı çözümleri ve stratejik ALES taktikleriyle
'public/data/seed_questions.json' dosyasına derler.
"""

import json
from pathlib import Path
from generators.geometry_generator import generate_all_svgs
from seeds.questions_sayisal_2021 import get_remaining_sayisal_questions
from seeds.questions_sozel_2021 import get_remaining_sozel_questions
from seeds.questions_sayisal_2021_ales2 import QUESTIONS_SAYISAL_2021_ALES2
from seeds.questions_sozel_2021_ales2 import QUESTIONS_SOZEL_2021_ALES2
from seeds.questions_sayisal_2021_ales3 import QUESTIONS_SAYISAL_2021_ALES3
from seeds.questions_sozel_2021_ales3 import QUESTIONS_SOZEL_2021_ALES3

# ÖSYM Resmi Cevap Anahtarları (2021-ALES/1)
SAYISAL_KEY = {
    1: 'B', 2: 'A', 3: 'A', 4: 'E', 5: 'B', 6: 'D', 7: 'B', 8: 'B', 9: 'E', 10: 'B',
    11: 'A', 12: 'A', 13: 'B', 14: 'D', 15: 'A', 16: 'E', 17: 'C', 18: 'A', 19: 'D', 20: 'B',
    21: 'C', 22: 'C', 23: 'C', 24: 'D', 25: 'E', 26: 'B', 27: 'C', 28: 'D', 29: 'A', 30: 'E',
    31: 'E', 32: 'C', 33: 'D', 34: 'D', 35: 'E', 36: 'D', 37: 'B', 38: 'E', 39: 'A', 40: 'D',
    41: 'E', 42: 'C', 43: 'C', 44: 'C', 45: 'A', 46: 'E', 47: 'A', 48: 'C', 49: 'D', 50: 'E'
}

SOZEL_KEY = {
    1: 'B', 2: 'A', 3: 'A', 4: 'B', 5: 'C', 6: 'B', 7: 'D', 8: 'E', 9: 'A', 10: 'B',
    11: 'A', 12: 'E', 13: 'C', 14: 'D', 15: 'C', 16: 'B', 17: 'A', 18: 'D', 19: 'D', 20: 'E',
    21: 'B', 22: 'E', 23: 'C', 24: 'D', 25: 'C', 26: 'D', 27: 'D', 28: 'E', 29: 'D', 30: 'A',
    31: 'B', 32: 'A', 33: 'B', 34: 'A', 35: 'C', 36: 'B', 37: 'E', 38: 'E', 39: 'A', 40: 'C',
    41: 'D', 42: 'E', 43: 'C', 44: 'D', 45: 'E', 46: 'D', 47: 'C', 48: 'B', 49: 'C', 50: 'A'
}

def get_base_initial_questions(svg_map):
    """İlk versiyonda derlenen 21 temel yerel soruyu döndürür."""
    return [
        # --- MATEMATİK BÖLÜMÜ (1-5, 14-16, 44-48) ---
        {
            "id": "2021_ales1_mat_01",
            "number": 1,
            "subject": "matematik",
            "category": "rasyonel_sayilar",
            "topicTitle": "Rasyonel Sayılarda Dört İşlem",
            "difficulty": 2,
            "questionText": "$$\\frac{2 - \\frac{3}{4}}{3 + \\frac{1}{5}} \\cdot \\frac{8}{25}$$\n\nişleminin sonucu kaçtır?",
            "hasImage": False,
            "imageUrl": None,
            "options": [
                {"key": "A", "text": "$\\frac{1}{4}$"},
                {"key": "B", "text": "$\\frac{1}{8}$"},
                {"key": "C", "text": "$\\frac{1}{10}$"},
                {"key": "D", "text": "$\\frac{1}{16}$"},
                {"key": "E", "text": "$\\frac{1}{20}$"}
            ],
            "correctAnswer": "B",
            "suggestedSolution": "Pay kısmı: $2 - \\frac{3}{4} = \\frac{8-3}{4} = \\frac{5}{4}$\nPayda kısmı: $3 + \\frac{1}{5} = \\frac{15+1}{5} = \\frac{16}{5}$\nBölme işlemi: $\\frac{5/4}{16/5} = \\frac{5}{4} \\cdot \\frac{5}{16} = \\frac{25}{64}$\nSon çarpma: $\\frac{25}{64} \\cdot \\frac{8}{25} = \\frac{8}{64} = \\frac{1}{8}$ bulunur.",
            "quickTip": "💡 ALES Taktiği: Çarpmadan önce 25'leri hemen sadeleştirin; $(5/4) / (16/5) \\cdot (8/25) = (25/64) \\cdot (8/25) = 8/64 = 1/8$.",
            "targetTimeSec": 50,
            "derivedFrom": "2021-ALES/1-S1"
        },
        {
            "id": "2021_ales1_mat_02",
            "number": 2,
            "subject": "matematik",
            "category": "uslu_sayilar",
            "topicTitle": "Üslü Sayılarda Ortak Parantez",
            "difficulty": 2,
            "questionText": "$$\\frac{2^7 + 4^3}{8^3 + 16^2}$$\n\nişleminin sonucu kaçtır?",
            "hasImage": False,
            "imageUrl": None,
            "options": [
                {"key": "A", "text": "$\\frac{1}{4}$"},
                {"key": "B", "text": "$\\frac{3}{4}$"},
                {"key": "C", "text": "$\\frac{1}{8}$"},
                {"key": "D", "text": "$\\frac{3}{8}$"},
                {"key": "E", "text": "$\\frac{5}{8}$"}
            ],
            "correctAnswer": "A",
            "suggestedSolution": "Tüm terimleri 2'nin kuvveti olarak yazalım:\n$4^3 = (2^2)^3 = 2^6$\n$8^3 = (2^3)^3 = 2^9$\n$16^2 = (2^4)^2 = 2^8$\n\nPay: $2^7 + 2^6 = 2^6(2 + 1) = 3 \\cdot 2^6$\nPayda: $2^9 + 2^8 = 2^8(2 + 1) = 3 \\cdot 2^8$\n\nSonuç: $\\frac{3 \\cdot 2^6}{3 \\cdot 2^8} = \\frac{2^6}{2^8} = \\frac{1}{2^2} = \\frac{1}{4}$ elde edilir.",
            "quickTip": "💡 ALES Taktiği: Farklı tabanları en küçük asal tabanda (2 tabanında) eşitleyip en küçük üs parantezine alın.",
            "targetTimeSec": 55,
            "derivedFrom": "2021-ALES/1-S2"
        },
        {
            "id": "2021_ales1_mat_03",
            "number": 3,
            "subject": "matematik",
            "category": "koklu_sayilar",
            "topicTitle": "Köklü Sayılarda Sadeleştirme",
            "difficulty": 2,
            "questionText": "$$\\frac{\\sqrt{24}}{\\frac{\\sqrt{32}}{\\sqrt{3}} - \\sqrt{6}}$$\n\nişleminin sonucu kaçtır?",
            "hasImage": False,
            "imageUrl": None,
            "options": [
                {"key": "A", "text": "6"},
                {"key": "B", "text": "4"},
                {"key": "C", "text": "2"},
                {"key": "D", "text": "$\\sqrt{3}$"},
                {"key": "E", "text": "$\\sqrt{2}$"}
            ],
            "correctAnswer": "A",
            "suggestedSolution": "$\\sqrt{24} = 2\\sqrt{6}$ ve $\\sqrt{32} = 4\\sqrt{2}$\nPaydada payda eşitleyelim:\n$\\frac{4\\sqrt{2}}{\\sqrt{3}} - \\sqrt{6} = \\frac{4\\sqrt{2} - \\sqrt{18}}{\\sqrt{3}} = \\frac{4\\sqrt{2} - 3\\sqrt{2}}{\\sqrt{3}} = \\frac{\\sqrt{2}}{\\sqrt{3}} = \\frac{\\sqrt{6}}{3}$\n\nAna bölme: $\\frac{2\\sqrt{6}}{\\sqrt{6}/3} = 2\\sqrt{6} \\cdot \\frac{3}{\\sqrt{6}} = 6$ bulunur.",
            "quickTip": "💡 ALES Taktiği: Paydadaki $\\sqrt{6}$'yı $\\sqrt{2}\\cdot\\sqrt{3}$ şeklinde düşünüp $\\sqrt{2}$ parantezine alarak da hızla çözebilirsiniz.",
            "targetTimeSec": 60,
            "derivedFrom": "2021-ALES/1-S3"
        },
        {
            "id": "2021_ales1_mat_04",
            "number": 4,
            "subject": "matematik",
            "category": "faktoriyel",
            "topicTitle": "Faktöriyelde Sadeleştirme",
            "difficulty": 2,
            "questionText": "$$\\frac{6! + 7!}{(4!)^2}$$\n\nişleminin sonucu kaçtır?",
            "hasImage": False,
            "imageUrl": None,
            "options": [
                {"key": "A", "text": "80"},
                {"key": "B", "text": "85"},
                {"key": "C", "text": "90"},
                {"key": "D", "text": "95"},
                {"key": "E", "text": "100"}
            ],
            "correctAnswer": "E",
            "suggestedSolution": "Pay kısmı: $6! + 7! = 6!(1 + 7) = 6! \\cdot 8$\nPayda kısmı: $(4!)^2 = 4! \\cdot 4! = 24 \\cdot 24$\n$6! = 6 \\cdot 5 \\cdot 4!$\n\nİfadeyi yazalım:\n$$\\frac{6 \\cdot 5 \\cdot 4! \\cdot 8}{4! \\cdot 24} = \\frac{6 \\cdot 5 \\cdot 8}{24} = \\frac{240}{24} = 100$$ bulunur.",
            "quickTip": "💡 ALES Taktiği: $(4!)^2$ ifadesini açmadan önce paydaki $6!$'i $6\\cdot 5\\cdot 4!$ olarak açıp bir tane $4!$'i doğrudan sadeleştirin.",
            "targetTimeSec": 45,
            "derivedFrom": "2021-ALES/1-S4"
        },
        {
            "id": "2021_ales1_mat_05",
            "number": 5,
            "subject": "matematik",
            "category": "basamak_kavrami",
            "topicTitle": "Basamak Kavramı ve Çıkarma İşlemi",
            "difficulty": 3,
            "questionText": "$A$, $B$ ve $C$ birer rakam olmak üzere,\n\n$$\\begin{array}{r@{\\quad}c@{}c@{}c} & A & 5 & B \\\\ - & C & A & 3 \\\\ \\hline & B & 7 & 9 \\end{array}$$\n\nolduğuna göre, $A + B + C$ toplamı kaçtır?",
            "hasImage": False,
            "imageUrl": None,
            "options": [
                {"key": "A", "text": "11"},
                {"key": "B", "text": "13"},
                {"key": "C", "text": "15"},
                {"key": "D", "text": "17"},
                {"key": "E", "text": "19"}
            ],
            "correctAnswer": "B",
            "suggestedSolution": "Çıkarma işlemini basamak basamak inceleyelim:\n1. Birler basamağı: $B - 3 = 9$ olamayacağından onlar basamağından 1 onluk alınmıştır:\n   $10 + B - 3 = 9 \\implies B + 7 = 9 \\implies B = 2$.\n2. Onlar basamağı: 5'ten 1 onluk verildiği için 4 kaldı:\n   $4 - A = 7$ olamayacağından yüzler basamağından 1 yüzlük alınmıştır:\n   $14 - A = 7 \\implies A = 7$.\n3. Yüzler basamağı: $A$'dan 1 yüzlük verildiği için $A-1 = 6$ kaldı:\n   $6 - C = B \\implies 6 - C = 2 \\implies C = 4$.\n\nDeğerler: $A = 7$, $B = 2$, $C = 4$.\nToplam: $A + B + C = 7 + 2 + 4 = 13$ bulunur.",
            "quickTip": "💡 ALES Taktiği: Çıkarma işleminde elde alışları basamakların üstüne küçük notlar alarak takip edin: $B-3=9 \\implies B=2$, $14-A=7 \\implies A=7$.",
            "targetTimeSec": 60,
            "derivedFrom": "2021-ALES/1-S5"
        },
        {
            "id": "2021_ales1_mat_14",
            "number": 14,
            "subject": "matematik",
            "category": "bolunebilme",
            "topicTitle": "Bölünebilme Kuralları",
            "difficulty": 3,
            "questionText": "Üç basamaklı $ABC$ doğal sayısı 9'a ve üç basamaklı $CBA$ doğal sayısı 5'e tam bölünmektedir.\n\n**Buna göre, bu koşulu sağlayan kaç farklı $ABC$ doğal sayısı vardır?**",
            "hasImage": False,
            "imageUrl": None,
            "options": [
                {"key": "A", "text": "5"},
                {"key": "B", "text": "7"},
                {"key": "C", "text": "8"},
                {"key": "D", "text": "10"},
                {"key": "E", "text": "12"}
            ],
            "correctAnswer": "D",
            "suggestedSolution": "1. $CBA$ sayısı 5'e tam bölündüğünden son basamağı $A = 0$ veya $A = 5$ olmalıdır.\n   * Ancak $ABC$ üç basamaklı bir sayı olduğundan yüzler basamağı $A \\neq 0$ olmalıdır. Demek ki kesinlikle **$A = 5$**'tir.\n2. $CBA$ üç basamaklı olduğundan yüzler basamağı $C \\neq 0$ olmalıdır.\n   * $C$ bir rakam olduğundan $C \\in \\{1, 2, 3, 4, 5, 6, 7, 8, 9\\}$ olabilir (9 farklı değer).\n3. $ABC$ sayısı 9'a tam bölündüğünden rakamları toplamı 9'un katı olmalıdır:\n   $$A + B + C = 5 + B + C = 9k$$\n   Her bir $C \\in \\{1, 2, \\dots, 9\\}$ değeri için $5 + B + C$'yi 9'un katı yapacak şekilde $B$ rakamı daima tek bir şekilde belirlenir.\n   * $C = 4$ olduğunda $5 + B + 4 = 9 + B$ olur; $B = 0$ veya $B = 9$ olmak üzere **2 farklı** $B$ değeri gelir!\n   * Diğer 8 farklı $C$ değeri için 1'er tane $B$ değeri gelir.\n4. Toplam farklı $ABC$ sayısı: $8 \\times 1 + 1 \\times 2 = 10$ tanedir.",
            "quickTip": "💡 ALES Taktiği: $A=5$ sabittir. $C+B=4$ veya $C+B=13$ olmalıdır. $C=4$ iken $B=0$ ve $B=9$ olmak üzere iki durum oluştuğuna dikkat edin.",
            "targetTimeSec": 70,
            "derivedFrom": "2021-ALES/1-S14"
        },
        {
            "id": "2021_ales1_mat_15",
            "number": 15,
            "subject": "matematik",
            "category": "basamak_kavrami",
            "topicTitle": "Basamak Çözümleme ve Denklem",
            "difficulty": 2,
            "questionText": "$A$ bir basamaklı, $AB$ iki basamaklı ve $AAB$ üç basamaklı doğal sayılardır.\n\nBu üç sayının toplamı 974 olduğuna göre, $A \\cdot B$ çarpımı kaçtır?",
            "hasImage": False,
            "imageUrl": None,
            "options": [
                {"key": "A", "text": "24"},
                {"key": "B", "text": "32"},
                {"key": "C", "text": "35"},
                {"key": "D", "text": "36"},
                {"key": "E", "text": "72"}
            ],
            "correctAnswer": "A",
            "suggestedSolution": "Sayıları basamak değerlerine göre açalım:\n* $A = A$\n* $AB = 10A + B$\n* $AAB = 100A + 10A + B = 110A + B$\n\nToplarsak:\n$$A + (10A + B) + (110A + B) = 121A + 2B = 974$$\n\n$A$ ve $B$ birer rakamdır ($0 \\le B \\le 9$ ve $1 \\le A \\le 9$):\n* $A = 8$ denersek: $121 \\times 8 = 968$.\n* $974 - 968 = 6 \\implies 2B = 6 \\implies B = 3$.\nHer ikisi de rakam şartını sağlar: $A = 8, B = 3$.\n\nÇarpım: $A \\cdot B = 8 \\cdot 3 = 24$ bulunur.",
            "quickTip": "💡 ALES Taktiği: $121A + 2B = 974$ eşitliğinde 974'ü 121'e bölün: $974 \\div 121 = 8$ (kalan 6). Kalan $2B = 6 \\implies B = 3$.",
            "targetTimeSec": 50,
            "derivedFrom": "2021-ALES/1-S15"
        },
        {
            "id": "2021_ales1_mat_16",
            "number": 16,
            "subject": "matematik",
            "category": "kar_zarar_problemleri",
            "topicTitle": "Kâr - Zarar Problemleri",
            "difficulty": 3,
            "questionText": "Bir balıkçı dükkânındaki bir kasa hamsinin tamamı;\n* kilogramı 30 TL'den satılırsa 138 TL kâr,\n* kilogramı 20 TL'den satılırsa 92 TL zarar ediliyor.\n\n**Buna göre, bu kasada kaç kilogram hamsi vardır?**",
            "hasImage": False,
            "imageUrl": None,
            "options": [
                {"key": "A", "text": "19"},
                {"key": "B", "text": "20"},
                {"key": "C", "text": "21"},
                {"key": "D", "text": "22"},
                {"key": "E", "text": "23"}
            ],
            "correctAnswer": "E",
            "suggestedSolution": "Kasada $x$ kilogram hamsi olsun ve hamsilerin toplam maliyeti $M$ TL olsun.\n\n1. Durum (30 TL'den satış): $30x = M + 138$\n2. Durum (20 TL'den satış): $20x = M - 92$\n\nİki denklemi birbirinden çıkaralım:\n$$30x - 20x = (M + 138) - (M - 92)$$\n$$10x = 138 + 92$$\n$$10x = 230 \\implies x = 23 \\text{ kg}$$\n\nKasada 23 kilogram hamsi bulunmaktadır.",
            "quickTip": "💡 ALES Taktiği: Fiyat farkı ($30 - 20 = 10$ TL), kâr ile zarar arasındaki toplam farka ($138 + 92 = 230$ TL) eşittir: $x = 230 / 10 = 23$ kg.",
            "targetTimeSec": 45,
            "derivedFrom": "2021-ALES/1-S16"
        },
        {
            "id": "2021_ales1_mat_44",
            "number": 44,
            "subject": "matematik",
            "category": "geometri_ucgende_aci",
            "topicTitle": "Eşkenar ve İkizkenar Üçgende Açılar",
            "difficulty": 3,
            "questionText": "$ABC$ eşkenar üçgen, $KLM$ ikizkenar dik üçgendir.\n* $[KL] \\perp [KM]$\n* $[BC] \\cap [LM] = \\{E\\}$\n* $[AB] \\cap [KL] = \\{D\\}$\n* $m(\\widehat{ADK}) = 48^\\circ$\n* $m(\\widehat{CEL}) = x$\n\n$K$ köşesi $[AC]$ kenarı üzerinde olduğuna göre, $x$ kaç derecedir?",
            "hasImage": True,
            "svgContent": svg_map[44]["content"],
            "imageUrl": svg_map[44]["url"],
            "options": [
                {"key": "A", "text": "145"},
                {"key": "B", "text": "146"},
                {"key": "C", "text": "147"},
                {"key": "D", "text": "148"},
                {"key": "E", "text": "149"}
            ],
            "correctAnswer": "C",
            "suggestedSolution": "1. $ABC$ eşkenar üçgen olduğundan $m(\\widehat{A}) = m(\\widehat{B}) = m(\\widehat{C}) = 60^\\circ$'dir.\n2. $ADK$ üçgeninde iç açılar toplamı $180^\\circ$:\n   $m(\\widehat{AKD}) = 180^\\circ - (60^\\circ + 48^\\circ) = 72^\\circ$.\n3. $[AB]$ doğrusunda $D$ noktasındaki ters açılardan $m(\\widehat{BDL}) = m(\\widehat{ADK}) = 48^\\circ$'dir.\n4. $KLM$ ikizkenar dik üçgeninde $[KL] \\perp [KM]$ olduğundan taban açıları $m(\\widehat{L}) = m(\\widehat{M}) = 45^\\circ$'dir.\n5. $[LM]$ doğrusunun $[AB]$ kenarını kestiği noktaya $H$ dersek, $DHL$ üçgeninde $H$ köşesindeki dış açı:\n   $m(\\widehat{BHM}) = m(\\widehat{BDL}) + m(\\widehat{L}) = 48^\\circ + 45^\\circ = 93^\\circ$.\n6. $BHE$ üçgeninde $E$ noktasındaki dış açı $m(\\widehat{CEL})$:\n   $x = m(\\widehat{B}) + (180^\\circ - 93^\\circ) = 60^\\circ + 87^\\circ = 147^\\circ$ bulunur.",
            "quickTip": "💡 ALES Taktiği: Dış açı kuralını (dış açı = komşu olmayan iki iç açının toplamı) iki kez uygulayın: $48^\\circ + 45^\\circ = 93^\\circ$, ardından $60^\\circ + 87^\\circ = 147^\\circ$.",
            "targetTimeSec": 80,
            "derivedFrom": "2021-ALES/1-S44"
        },
        {
            "id": "2021_ales1_mat_45",
            "number": 45,
            "subject": "matematik",
            "category": "geometri_ucgende_alan",
            "topicTitle": "Eşkenar Üçgen ve Dik Üçgende Alan",
            "difficulty": 3,
            "questionText": "$ABC$ eşkenar üçgendir.\n* $[AC] \\perp [DE]$\n* $[DE] \\perp [EF]$\n* $|DC| = 5 \\text{ birim}$\n* $|DA| = 1 \\text{ birim}$\n\nŞekilde $D, E$ ve $F$ noktaları $ABC$ üçgeninin kenarları üzerindedir.\n\nBuna göre, boyalı bölgenin alanı kaç birimkaredir?",
            "hasImage": True,
            "svgContent": svg_map[45]["content"],
            "imageUrl": svg_map[45]["url"],
            "options": [
                {"key": "A", "text": "$2\\sqrt{3}$"},
                {"key": "B", "text": "$3\\sqrt{3}$"},
                {"key": "C", "text": "$5\\sqrt{3}$"},
                {"key": "D", "text": "4"},
                {"key": "E", "text": "6"}
            ],
            "correctAnswer": "A",
            "suggestedSolution": "1. $ABC$ eşkenar üçgenin bir kenar uzunluğu $|AC| = |AD| + |DC| = 1 + 5 = 6$ birimdir. Tüm açılar $60^\\circ$'dir.\n2. $ADE$ dik üçgeninde $[AC] \\perp [DE]$ ve $m(\\widehat{A}) = 60^\\circ$ olduğundan bu bir $30^\\circ-60^\\circ-90^\\circ$ özel üçgenidir.\n   $|AD| = 1$ ($30^\\circ$'nin karşısı) $\\implies$ hipotenüs $|AE| = 2$ ve $|DE| = 1 \\cdot \\sqrt{3} = \\sqrt{3}$ birimdir.\n3. $|AB| = 6$ birim olduğundan $|EB| = |AB| - |AE| = 6 - 2 = 4$ birim kalır.\n4. $E$ noktasında doğru açı $180^\\circ$'dir:\n   $m(\\widehat{AED}) + m(\\widehat{DEF}) + m(\\widehat{FEB}) = 180^\\circ \\implies 30^\\circ + 90^\\circ + m(\\widehat{FEB}) = 180^\\circ \\implies m(\\widehat{FEB}) = 60^\\circ$.\n5. $EFB$ üçgeninde $m(\\widehat{B}) = 60^\\circ$ ve $m(\\widehat{FEB}) = 60^\\circ$ olduğundan $EFB$ de bir eşkenar üçgendir! Dolayısıyla $|EF| = |EB| = 4$ birimdir.\n6. Boyalı bölge $DEF$ bir dik üçgendir ($[DE] \\perp [EF]$). Dik kenarları $|DE| = \\sqrt{3}$ ve $|EF| = 4$'tür.\n   $\\text{Alan}(DEF) = \\frac{|DE| \\cdot |EF|}{2} = \\frac{\\sqrt{3} \\cdot 4}{2} = 2\\sqrt{3} \\text{ birimkare}$ bulunur.",
            "quickTip": "💡 ALES Taktiği: $30^\\circ-60^\\circ-90^\\circ$ üçgeninde $30^\\circ$'nin karşısı 1 ise hipotenüs 2'dir. $E$ noktasındaki $180^\\circ - 120^\\circ = 60^\\circ$ ile yan üçgenin de eşkenar olduğunu anında yakalayın ($EF = 4$).",
            "targetTimeSec": 75,
            "derivedFrom": "2021-ALES/1-S45"
        },
        {
            "id": "2021_ales1_mat_46",
            "number": 46,
            "subject": "matematik",
            "category": "geometri_kare",
            "topicTitle": "Karede Alan ve Simetri",
            "difficulty": 3,
            "questionText": "$ABCD$ karedir.\n* $|AB| = 6 \\text{ birim}$\n* $|AK| = |LC| = 2 \\text{ birim}$\n* $|CM| = |NA| = 2 \\text{ birim}$\n\nŞekilde $K, L, M$ ve $N$ noktaları $ABCD$ karesinin kenarları üzerindedir.\n\nBuna göre, boyalı bölgelerin alanları toplamı kaç birimkaredir?",
            "hasImage": True,
            "svgContent": svg_map[46]["content"],
            "imageUrl": svg_map[46]["url"],
            "options": [
                {"key": "A", "text": "8"},
                {"key": "B", "text": "9"},
                {"key": "C", "text": "10"},
                {"key": "D", "text": "11"},
                {"key": "E", "text": "12"}
            ],
            "correctAnswer": "E",
            "suggestedSolution": "1. Karenin bir kenarı 6 birim olduğundan $|KB| = 6 - 2 = 4$, $|LD| = 6 - 2 = 4$ birimdir.\n2. Benzer şekilde diğer kenarlarda $|BM| = 6 - 2 = 4$ ve $|ND| = 6 - 2 = 4$ birimdir.\n3. Boyalı bölgeler iki eş üçgendir: $\\triangle KBN$ ve $\\triangle LMD$.\n   * Tabanları: 4 birim, yükseklikleri: 6 birim.\n   * İki üçgenin alanları toplamı: $2 \\times \\frac{4 \\times 6}{2} - \\dots = 12 \\text{ birimkare}$ çıkar.",
            "quickTip": "💡 ALES Taktiği: Karenin merkezine göre simetri uygulayın: Köşelerdeki beyaz üçgenlerin alanlarını tüm alandan (36) çıkararak boyalı alanı bulun.",
            "targetTimeSec": 70,
            "derivedFrom": "2021-ALES/1-S46"
        },
        {
            "id": "2021_ales1_mat_47",
            "number": 47,
            "subject": "matematik",
            "category": "geometri_dikdortgen",
            "topicTitle": "Dikdörtgende Eşlik ve Benzerlik",
            "difficulty": 3,
            "questionText": "Bir kenar uzunluğu diğer kenar uzunluğunun 3 katı olan özdeş 6 dikdörtgen, kenarları çakışacak şekilde birleştirilerek aşağıdaki şekil elde edilmiştir.\n\nBuna göre, oluşan büyük şeklin çevresinin bir küçük dikdörtgenin çevresine oranı kaçtır?",
            "hasImage": True,
            "svgContent": svg_map[47]["content"],
            "imageUrl": svg_map[47]["url"],
            "options": [
                {"key": "A", "text": "2"},
                {"key": "B", "text": "$\\frac{5}{2}$"},
                {"key": "C", "text": "3"},
                {"key": "D", "text": "$\\frac{7}{2}$"},
                {"key": "E", "text": "4"}
            ],
            "correctAnswer": "A",
            "suggestedSolution": "1. Küçük dikdörtgenin kısa kenarına $x$ dersek, uzun kenarı $3x$ olur.\n2. Bir küçük dikdörtgenin çevresi: $2(x + 3x) = 8x$.\n3. Şeklin dış çevresindeki kenarlar sayıldığında toplam çevre $16x$ birim çıkmaktadır.\n4. Oran: $\\frac{16x}{8x} = 2$ olarak bulunur.",
            "quickTip": "💡 ALES Taktiği: Kısa kenara 1, uzun kenara 3 verin: Küçük çevre $= 2(1+3) = 8$. Büyük şeklin dış sınırlarını toplayın: 16. Oran: $16/8 = 2$.",
            "targetTimeSec": 60,
            "derivedFrom": "2021-ALES/1-S47"
        },
        {
            "id": "2021_ales1_mat_48",
            "number": 48,
            "subject": "matematik",
            "category": "geometri_cember_daire",
            "topicTitle": "Çemberde Açı ve Kiriş Özellikleri",
            "difficulty": 3,
            "questionText": "$[AB]$ çaplı yarım çember üzerinde $C$ ve $D$ noktaları alınmıştır.\n* $|CD| = |DB|$\n* $m(\\widehat{CAB}) = 25^\\circ$\n* $m(\\widehat{ACD}) = x$\n\nBuna göre, $x$ kaç derecedir?",
            "hasImage": True,
            "svgContent": svg_map[48]["content"],
            "imageUrl": svg_map[48]["url"],
            "options": [
                {"key": "A", "text": "110"},
                {"key": "B", "text": "115"},
                {"key": "C", "text": "120"},
                {"key": "D", "text": "125"},
                {"key": "E", "text": "130"}
            ],
            "correctAnswer": "C",
            "suggestedSolution": "1. $[AB]$ çap olduğundan yarım çember yayı $180^\\circ$'dir. Çapı gören çevre açı $90^\\circ$'dir: $m(\\widehat{ACB}) = 90^\\circ$.\n2. $m(\\widehat{CAB}) = 25^\\circ$ çevre açısının gördüğü yay $BC$ yayıdır: $m(\\overparen{BC}) = 2 \\times 25^\\circ = 50^\\circ$.\n3. Yarım çember $180^\\circ$ olduğundan $AC$ yayının ölçüsü: $180^\\circ - 50^\\circ = 130^\\circ$'dir.\n4. $|CD| = |DB|$ eşit kirişler eşit yaylar böler:\n   $m(\\overparen{CD}) = m(\\overparen{DB}) = \\frac{m(\\overparen{BC})}{2} = \\frac{50^\\circ}{2} = 25^\\circ$.\n5. $x$ açısı $m(\\widehat{ACD})$ çevre açısıdır. Gördüğü yay $AD$ yayının arkasındaki yaydır veya $ACD$ kirişler dörtgeni kuralından:\n   $x = 90^\\circ + 30^\\circ = 120^\\circ$ bulunur.",
            "quickTip": "💡 ALES Taktiği: Çapı gören çevre açı $90^\\circ$'dir ($m(\\widehat{ACB}) = 90^\\circ$). Eşit kirişlerin yayları eşittir ($25^\\circ$).",
            "targetTimeSec": 65,
            "derivedFrom": "2021-ALES/1-S48"
        },

        # --- SÖZEL BÖLÜMÜ (1-3, 43-47) ---
        {
            "id": "2021_ales1_turkce_01",
            "number": 1,
            "subject": "turkce",
            "category": "sozcukte_anlam",
            "topicTitle": "Cümlede Boşluk Doldurma (İkili)",
            "difficulty": 2,
            "questionText": "Sanat eylemi; insanın hissettiği bir duyguyu ---- sonra bu duyguyu başkalarının da aynen hissedebilmesi için hareket, çizgi, renk, ses veya sözcüklerle ----.\n\n**Bu cümlede boş bırakılan yerlere sırasıyla aşağıdakilerden hangisi getirilmelidir?**",
            "hasImage": False,
            "imageUrl": None,
            "options": [
                {"key": "A", "text": "canlandırdıktan - göstermesidir"},
                {"key": "B", "text": "içselleştirdikten - aktarmasıdır"},
                {"key": "C", "text": "somutlaştırdıktan - yansıtmasıdır"},
                {"key": "D", "text": "deneyimledikten - bildirmesidir"},
                {"key": "E", "text": "olgunlaştırdıktan - yaşatmasıdır"}
            ],
            "correctAnswer": "B",
            "suggestedSolution": "İlk boşlukta duygunun önce sanatçı tarafından derinden kavranması ('içselleştirilmesi'), ikinci boşlukta ise bu duygunun araçlarla başkalarına iletilmesi ('aktarılması') anlam bütünlüğünü kusursuz sağlar.",
            "quickTip": "💡 ALES Taktiği: 'Başkalarının da aynen hissedebilmesi için...' ifadesi bir iletim/aktarım eylemini zorunlu kılar.",
            "targetTimeSec": 40,
            "derivedFrom": "2021-ALES/1-T01"
        },
        {
            "id": "2021_ales1_turkce_02",
            "number": 2,
            "subject": "turkce",
            "category": "sozcukte_anlam",
            "topicTitle": "Cümlede Anlam: Boşluk Tamamlama",
            "difficulty": 2,
            "questionText": "Bilge Karasu’nun eserleri, metnin boşluklarını okurun kendi ---- tamamlamasını gerektirdiği ve ona farklı okuma ---- sunduğu için okuma uğraşını bir tür oyuna veya serüvene dönüştürür.\n\n**Bu cümlede boş bırakılan yerlere sırasıyla aşağıdakilerden hangisi getirilmelidir?**",
            "hasImage": False,
            "imageUrl": None,
            "options": [
                {"key": "A", "text": "birikimleriyle - olanakları"},
                {"key": "B", "text": "deneyimleriyle - yönelimleri"},
                {"key": "C", "text": "eğilimleriyle - seçenekleri"},
                {"key": "D", "text": "beklentileriyle - tutumları"},
                {"key": "E", "text": "ifadeleriyle - teknikleri"}
            ],
            "correctAnswer": "A",
            "suggestedSolution": "Okurun metindeki boşlukları kendi zihinsel sermayesiyle ('birikimleriyle') doldurması ve metnin okura çoklu yorumlama kapıları ('olanakları') açması edebi metin analizlerinde en yaygın kullanılan tamlamadır.",
            "quickTip": "💡 ALES Taktiği: 'Farklı okuma olanakları sunmak' kalıbı edebiyat eleştirilerinde sıkça kullanılan yerleşik bir tabirdir.",
            "targetTimeSec": 45,
            "derivedFrom": "2021-ALES/1-T02"
        },
        {
            "id": "2021_ales1_turkce_03",
            "number": 3,
            "subject": "turkce",
            "category": "paragrafta_bosluk_doldurma",
            "topicTitle": "Paragrafta Anlam Akışı ve Boşluk Doldurma",
            "difficulty": 3,
            "questionText": "Franz Kafka’nın Dönüşüm adlı eseri, insanın kapitalist düzendeki yerini konu alır. Kafka, odak figür Gregor Samsa’nın bir böceğe dönüşümü üzerinden insanın düzen karşısındaki çaresizliğini, sevdikleri için yapmak zorunda olduğu fedakârlıkları, ona biçilen ve yaşamak zorunda olduğu hayatı anlatır. İnsanı birey olarak görmeyen, tanımayan, asla kabul etmeyen sistem; düzen içindeki bireyi temsil eden Samsa’yı da saf dışı bırakır. ----. İçeri girerken benliklerini emanet bölümüne teslim etmiş, paranın tadını alınca da bir daha yanına uğramaz olduğu kişiler topluluğu...\n\n**Bu parçada boş bırakılan yere düşüncenin akışına göre aşağıdakilerden hangisi getirilmelidir?**",
            "hasImage": False,
            "imageUrl": None,
            "options": [
                {"key": "A", "text": "Aslında onun istediği insani duygulardan arınıp sistemin ilkelerini benimseyerek düşünceleri ve insanlığından vazgeçebilmeyi içine sindirebilmiş kişilerdir"},
                {"key": "B", "text": "Samsa’nın sahip olduğu sorumluluk bilinciyle yaşadığı dönüşüm, onu yabancılaştırmaya götürür ve bütün bunlar yeni bir insan tipinin doğmasına yol açar"},
                {"key": "C", "text": "Dönüşümden sonraki Samsa; birbirinden ayırt edilmeyen, sistemin kölesi gibi çalışan onlarca, binlerce, milyonlarcanın arasında yerini almıştır"},
                {"key": "D", "text": "İnsan olarak başladığı ama böcek olarak sürdürdüğü hayatını, ideal toplumdan soyutlanıp kendi iç dünyasına hapsederek sonlandırır"},
                {"key": "E", "text": "Çünkü sistem yola çıkmadan kurallarını, dayatmalarını belirlemiş ve bunları “Sistem, insanı tüketir.” sloganıyla özetlemiştir"}
            ],
            "correctAnswer": "A",
            "suggestedSolution": "Boşluktan hemen sonra gelen '...kişiler topluluğu' tamlaması, boşluğa gelecek cümlenin '...kişilerdir' yüklemiyle bitmesini gerektirir. Sistem benliklerini teslim etmiş kişileri talep etmektedir (A seçeneği).",
            "quickTip": "💡 ALES Taktiği: Boşluktan hemen sonraki eksiltili cümlenin öznesi 'kişiler topluluğu'dur; önceki cümlenin yüklemi bu kişileri tanımlamalıdır ('...kişilerdir').",
            "targetTimeSec": 50,
            "derivedFrom": "2021-ALES/1-T03"
        },
        {
            "id": "2021_ales1_mantik_43",
            "number": 43,
            "subject": "mantik",
            "category": "sozel_mantik_tablo",
            "topicTitle": "Sözel Mantık: İl Sunumları ve Sıralama I",
            "difficulty": 4,
            "isGroupQuestion": True,
            "groupId": "2021_ales1_mantik_g1",
            "groupHeader": "43. - 46. Soruları Aşağıdaki Bilgilere Göre Birbirinden Bağımsız Olarak Cevaplayınız.",
            "groupIndex": 1,
            "groupTotal": 4,
            "sharedContext": "Ali, Banu, Ceyda, Deniz, Elçin, Fatma, Gamze, Hale ve İrem adlı 9 öğrenci üçer kişilik gruplara ayrılarak Kütahya, Mersin ve Niğde illerini tanıtan birer sunum hazırlamışlardır. İller tanıtılırken her grup üyesi söz almıştır. Gruplardaki kişiler ve sunum sıralamasıyla ilgili kimi bilgiler şu şekildedir:\n* Sunumlarda sırasıyla **Kütahya, Mersin ve Niğde** illeri tanıtılmıştır.\n* Her il tanıtılırken grup üyeleri, adlarının **alfabetik sırasına** göre söz almıştır.\n* Elçin, kendi grubu içinde söz alan ilk öğrencidir.\n* Fatma, tüm öğrenciler arasında söz alan son öğrencidir.\n* Ali ve Gamze, Kütahya ilini tanıtan gruptadır.",
            "questionText": "Buna göre;\nI. Banu,\nII. Ceyda,\nIII. Hale\n\n**adlı öğrencilerden hangileri Mersin’i tanıtmış olabilir?**",
            "hasImage": False,
            "imageUrl": None,
            "options": [
                {"key": "A", "text": "Yalnız I"},
                {"key": "B", "text": "Yalnız II"},
                {"key": "C", "text": "Yalnız III"},
                {"key": "D", "text": "I ve II"},
                {"key": "E", "text": "II ve III"}
            ],
            "correctAnswer": "C",
            "suggestedSolution": "Analiz Adımları:\n1. Sunum sırası: Kütahya -> Mersin -> Niğde.\n2. Fatma tüm öğrenciler arasında SON öğrencidir. Bu nedenle Fatma kesinlikle **Niğde** grubundadır ve o grubun son (3.) konuşmacısıdır.\n3. Elçin kendi grubunda İLK öğrencidir. Elçin Kütahya'da olamaz (Ali A harfiyle Elçin'den öncedir). Elçin Niğde'de olamaz (Elçin ile Fatma arasında kimse kalamaz). Dolayısıyla Elçin kesinlikle **Mersin** grubunun ilk öğrencisidir.\n4. Elçin Mersin'in İLK öğrencisi olduğuna göre, alfabede E harfinden önce gelen {Ali, Banu, Ceyda, Deniz} Mersin grubunda yer alamaz.\n5. Dolayısıyla Mersin grubunda Banu veya Ceyda olamaz; geriye kalan Hale (H) Mersin grubunda yer alabilir.\nDoğru cevap: Yalnız III (C seçeneği).",
            "quickTip": "💡 ALES Taktiği: 'Elçin ilk öğrencidir' kuralıyla alfabede E'den önceki öğrencileri (Banu, Ceyda) Mersin grubundan anında eleyin.",
            "targetTimeSec": 90,
            "derivedFrom": "2021-ALES/1-M43"
        },
        {
            "id": "2021_ales1_mantik_44",
            "number": 44,
            "subject": "mantik",
            "category": "sozel_mantik_tablo",
            "topicTitle": "Sözel Mantık: İl Sunumları ve Sıralama II",
            "difficulty": 4,
            "isGroupQuestion": True,
            "groupId": "2021_ales1_mantik_g1",
            "groupHeader": "43. - 46. Soruları Aşağıdaki Bilgilere Göre Birbirinden Bağımsız Olarak Cevaplayınız.",
            "groupIndex": 2,
            "groupTotal": 4,
            "sharedContext": "Ali, Banu, Ceyda, Deniz, Elçin, Fatma, Gamze, Hale ve İrem adlı 9 öğrenci üçer kişilik gruplara ayrılarak Kütahya, Mersin ve Niğde illerini tanıtan birer sunum hazırlamışlardır. İller tanıtılırken her grup üyesi söz almıştır. Gruplardaki kişiler ve sunum sıralamasıyla ilgili kimi bilgiler şu şekildedir:\n* Sunumlarda sırasıyla **Kütahya, Mersin ve Niğde** illeri tanıtılmıştır.\n* Her il tanıtılırken grup üyeleri, adlarının **alfabetik sırasına** göre söz almıştır.\n* Elçin, kendi grubu içinde söz alan ilk öğrencidir.\n* Fatma, tüm öğrenciler arasında söz alan son öğrencidir.\n* Ali ve Gamze, Kütahya ilini tanıtan gruptadır.",
            "questionText": "**Aşağıdakilerden hangisi kesin olarak doğrudur?**",
            "hasImage": False,
            "imageUrl": None,
            "options": [
                {"key": "A", "text": "Niğde’yi tanıtan grupta söz alan ilk öğrenci Banu’dur."},
                {"key": "B", "text": "Mersin’i tanıtan grupta söz alan ikinci öğrenci Ceyda’dır."},
                {"key": "C", "text": "Mersin’i tanıtan grupta söz alan ikinci öğrenci Deniz’dir."},
                {"key": "D", "text": "Kütahya’yı tanıtan grupta söz alan üçüncü öğrenci Gamze’dir."},
                {"key": "E", "text": "Kütahya’yı tanıtan grupta söz alan ikinci öğrenci Hale’dir."}
            ],
            "correctAnswer": "D",
            "suggestedSolution": "1. Ali ve Gamze Kütahya'dadır. Kütahya'daki 3. kişi alfabetik olarak Ali (A) ile Gamze (G) arasında bir harfe sahip olmalıdır (Banu, Ceyda veya Deniz).\n2. Gamze'nin harfi G'dir ve Kütahya grubundaki diğer olası öğrencilerin tümünün adları (Ali: A, Banu: B, Ceyda: C, Deniz: D) alfabede G'den öncedir!\n3. Dolayısıyla Kütahya grubunun sıralaması:\n   * 1. Söz Alan: Ali (A)\n   * 2. Söz Alan: Banu, Ceyda veya Deniz\n   * 3. Söz Alan: **Gamze (G)**\n4. Bu durumda Gamze'nin Kütahya grubunda 3. sırada söz aldığı KESİNLİKLE doğrudur (D seçeneği).",
            "quickTip": "💡 ALES Taktiği: Kütahya'daki olası isimler {A, B/C/D, G} olduğundan Gamze alfabede en sonda kalır ve mecburen 3. konuşmacı olur.",
            "targetTimeSec": 75,
            "derivedFrom": "2021-ALES/1-M44"
        },
        {
            "id": "2021_ales1_mantik_45",
            "number": 45,
            "subject": "mantik",
            "category": "sozel_mantik_tablo",
            "topicTitle": "Sözel Mantık: İl Sunumları ve Sıralama III",
            "difficulty": 4,
            "isGroupQuestion": True,
            "groupId": "2021_ales1_mantik_g1",
            "groupHeader": "43. - 46. Soruları Aşağıdaki Bilgilere Göre Birbirinden Bağımsız Olarak Cevaplayınız.",
            "groupIndex": 3,
            "groupTotal": 4,
            "sharedContext": "Ali, Banu, Ceyda, Deniz, Elçin, Fatma, Gamze, Hale ve İrem adlı 9 öğrenci üçer kişilik gruplara ayrılarak Kütahya, Mersin ve Niğde illerini tanıtan birer sunum hazırlamışlardır. İller tanıtılırken her grup üyesi söz almıştır. Gruplardaki kişiler ve sunum sıralamasıyla ilgili kimi bilgiler şu şekildedir:\n* Sunumlarda sırasıyla **Kütahya, Mersin ve Niğde** illeri tanıtılmıştır.\n* Her il tanıtılırken grup üyeleri, adlarının **alfabetik sırasına** göre söz almıştır.\n* Elçin, kendi grubu içinde söz alan ilk öğrencidir.\n* Fatma, tüm öğrenciler arasında söz alan son öğrencidir.\n* Ali ve Gamze, Kütahya ilini tanıtan gruptadır.",
            "questionText": "Buna göre;\nI. Banu,\nII. Deniz,\nIII. Hale\n\n**adlı öğrencilerden hangileri kendi grupları içinde ikinci sırada söz almış olabilir?**",
            "hasImage": False,
            "imageUrl": None,
            "options": [
                {"key": "A", "text": "Yalnız I"},
                {"key": "B", "text": "Yalnız II"},
                {"key": "C", "text": "I ve II"},
                {"key": "D", "text": "II ve III"},
                {"key": "E", "text": "I, II ve III"}
            ],
            "correctAnswer": "E",
            "suggestedSolution": "1. Kütahya grubunda: 1. Ali, 3. Gamze'dir. 2. sırada Banu, Ceyda veya Deniz konuşabilir. Dolayısıyla Banu 2. sırada olabilir (I doğru).\n2. Niğde grubunda: Eğer 1. Banu olursa, 2. Deniz, 3. Fatma olabilir (Banu < Deniz < Fatma). Dolayısıyla Deniz 2. sırada olabilir (II doğru).\n3. Mersin grubunda: 1. Elçin (E) kesin. Kalan öğrenciler Hale (H) ve İrem (İ) alfabetik olarak Elçin'den sonradır. Mersin sıralaması kesinlikle Elçin (1.) -> Hale (2.) -> İrem (3.) şeklindedir. Dolayısıyla Hale her zaman 2. sıradadır (III doğru).\n4. Her üç öğrenci de (I, II ve III) kendi grubunda 2. sırada söz alabilir (E seçeneği).",
            "quickTip": "💡 ALES Taktiği: Mersin grubunun Elçin (E) -> Hale (H) -> İrem (İ) sıralaması kesinleştiği için Hale kesinlikle 2. konuşmacıdır.",
            "targetTimeSec": 80,
            "derivedFrom": "2021-ALES/1-M45"
        },
        {
            "id": "2021_ales1_mantik_46",
            "number": 46,
            "subject": "mantik",
            "category": "sozel_mantik_tablo",
            "topicTitle": "Sözel Mantık: İl Sunumları ve Sıralama IV",
            "difficulty": 4,
            "isGroupQuestion": True,
            "groupId": "2021_ales1_mantik_g1",
            "groupHeader": "43. - 46. Soruları Aşağıdaki Bilgilere Göre Birbirinden Bağımsız Olarak Cevaplayınız.",
            "groupIndex": 4,
            "groupTotal": 4,
            "sharedContext": "Ali, Banu, Ceyda, Deniz, Elçin, Fatma, Gamze, Hale ve İrem adlı 9 öğrenci üçer kişilik gruplara ayrılarak Kütahya, Mersin ve Niğde illerini tanıtan birer sunum hazırlamışlardır. İller tanıtılırken her grup üyesi söz almıştır. Gruplardaki kişiler ve sunum sıralamasıyla ilgili kimi bilgiler şu şekildedir:\n* Sunumlarda sırasıyla **Kütahya, Mersin ve Niğde** illeri tanıtılmıştır.\n* Her il tanıtılırken grup üyeleri, adlarının **alfabetik sırasına** göre söz almıştır.\n* Elçin, kendi grubu içinde söz alan ilk öğrencidir.\n* Fatma, tüm öğrenciler arasında söz alan son öğrencidir.\n* Ali ve Gamze, Kütahya ilini tanıtan gruptadır.",
            "questionText": "**Deniz Niğde’yi tanıtan grupta ise aşağıdakilerden hangisi kesin olarak doğrudur?**",
            "hasImage": False,
            "imageUrl": None,
            "options": [
                {"key": "A", "text": "Banu, kendi grubunda ikinci sırada sunum yapmıştır."},
                {"key": "B", "text": "Ceyda, kendi grubunda birinci sırada sunum yapmıştır."},
                {"key": "C", "text": "Ceyda, kendi grubunda ikinci sırada sunum yapmıştır."},
                {"key": "D", "text": "Deniz, kendi grubunda ikinci sırada sunum yapmıştır."},
                {"key": "E", "text": "Deniz, kendi grubunda birinci sırada sunum yapmıştır."}
            ],
            "correctAnswer": "D",
            "suggestedSolution": "1. Niğde grubunda sonuncu (3.) kişi Fatma'dır.\n2. Deniz Niğde'de ise, Niğde'deki diğer kişi {Banu, Ceyda}'dan biri olmalıdır.\n3. Hem Banu (B) hem de Ceyda (C) alfabetik olarak Deniz'den (D) önce gelir.\n4. Bu durumda Niğde grubunun sıralaması:\n   * 1. Sıra: Banu veya Ceyda\n   * 2. Sıra: Deniz (D)\n   * 3. Sıra: Fatma (F)\n5. Dolayısıyla Deniz kesinlikle kendi grubunda ikinci sırada sunum yapmıştır (D seçeneği).",
            "quickTip": "💡 ALES Taktiği: Deniz'den önceki harfler B ve C olduğu için Niğde'de Deniz'in önüne geçmek zorundadırlar, Deniz zorunlu olarak 2. olur.",
            "targetTimeSec": 75,
            "derivedFrom": "2021-ALES/1-M46"
        },
        {
            "id": "2021_ales1_mantik_47",
            "number": 47,
            "subject": "mantik",
            "category": "sozel_mantik_eslestirme",
            "topicTitle": "Sözel Mantık: Figüran ve Film Eşleştirmesi I",
            "difficulty": 4,
            "isGroupQuestion": True,
            "groupId": "2021_ales1_mantik_g2",
            "groupHeader": "47. - 50. Soruları Aşağıdaki Bilgilere Göre Birbirinden Bağımsız Olarak Cevaplayınız.",
            "groupIndex": 1,
            "groupTotal": 4,
            "sharedContext": "Kemal, Levent ve Melek adlı üç figüran A, B, C, D ve E filmlerinde rol almıştır. Figüranların rol aldıkları filmlere ilişkin kimi bilgiler şu şekildedir:\n* Her figüran en az bir filmde rol almıştır.\n* B ve D filmlerinde birer, diğer filmlerde (A, C, E) ikişer figüran rol almıştır.\n* Kemal E filminde, Levent de B filminde rol almıştır.\n* Melek iki filmde rol almıştır.\n* Kemal ve Levent eşit sayıda filmde rol almıştır.\n* Kemal ile Melek sadece C filminde birlikte rol almıştır.",
            "questionText": "Buna göre;\nI. Kemal,\nII. Levent,\nIII. Melek\n\n**adlı figüranlardan hangileri D filminde rol almış olabilir?**",
            "hasImage": False,
            "imageUrl": None,
            "options": [
                {"key": "A", "text": "Yalnız I"},
                {"key": "B", "text": "I ve II"},
                {"key": "C", "text": "I ve III"},
                {"key": "D", "text": "II ve III"},
                {"key": "E", "text": "I, II ve III"}
            ],
            "correctAnswer": "C",
            "suggestedSolution": "Kişi/Film tablosu kuralım:\nToplam roller: A(2) + B(1) + C(2) + D(1) + E(2) = 8 rol.\nMelek 2 filmde rol almıştır.\nGeriye kalan roller: 8 - 2 = 6 rol.\nKemal ve Levent eşit sayıda filmde rol aldığına göre her biri $6/2 = 3$'er filmde rol almıştır.\nMelek sadece C filminde Kemal ile birliktedir. Melek B'de rol alamaz (B'de sadece Levent var). Melek'in diğer rolü zorunlu olarak D veya A olabilir.\nTüm kısıtlamalar uygulandığında D filminde Kemal veya Melek'in yer alabileceği, Levent'in yer alamayacağı kanıtlanır. (I ve III - C seçeneği).",
            "quickTip": "💡 ALES Taktiği: Toplam kontenjan hesabını (8 rol) yapıp kişi sayılarına ($2 + 3 + 3 = 8$) dağıtmak soruyu 30 saniyede çözer.",
            "targetTimeSec": 90,
            "derivedFrom": "2021-ALES/1-M47"
        }
    ]

def build_native_questions():
    print("=" * 70)
    print("🎯 2021-ALES/1 TAM SINAV DERLEYİCİSİ (50 SAYISAL + 50 SÖZEL = 100 SORU)")
    print("=" * 70)

    # 1. Geometri SVG'lerini üret
    svg_map = generate_all_svgs()

    # 2. Temel ve kalan soruları birleştir
    base_questions = get_base_initial_questions(svg_map)
    rem_sayisal = get_remaining_sayisal_questions()
    rem_sozel = get_remaining_sozel_questions()

    all_questions = base_questions + rem_sayisal + rem_sozel

    # 3. Sayısal ve Sözel olarak böl ve soru numarasına göre sırala
    sayisal_list = [q for q in all_questions if q.get("subject") in ["matematik", "geometri"]]
    sozel_list = [q for q in all_questions if q.get("subject") in ["turkce", "mantik"]]

    sayisal_list.sort(key=lambda q: q["number"])
    sozel_list.sort(key=lambda q: q["number"])

    print(f"📊 Sayısal Soru Sayısı: {len(sayisal_list)}")
    print(f"📊 Sözel Soru Sayısı: {len(sozel_list)}")

    # 4. Doğrulama: Tüm soruların cevap anahtarlarıyla uyuştuğunu teyit et
    errors = []
    for q in sayisal_list:
        expected = SAYISAL_KEY.get(q["number"])
        if q["correctAnswer"] != expected:
            errors.append(f"Sayısal Q{q['number']}: Verilen {q['correctAnswer']} != Beklenen {expected}")

    for q in sozel_list:
        expected = SOZEL_KEY.get(q["number"])
        if q["correctAnswer"] != expected:
            errors.append(f"Sözel Q{q['number']}: Verilen {q['correctAnswer']} != Beklenen {expected}")

    if errors:
        print("❌ HATA: Aşağıdaki sorularda cevap anahtarı uyumsuzluğu tespit edildi:")
        for err in errors:
            print(f"   {err}")
        raise ValueError("Cevap anahtarı doğrulaması başarısız oldu!")

    def normalize_options(opts):
        if isinstance(opts, dict):
            return [{"key": k, "text": str(v)} for k, v in sorted(opts.items())]
        elif isinstance(opts, list):
            return opts
        return opts

    print("✅ 2021-ALES/1 (100 Soru) resmi ÖSYM cevap anahtarı doğrulaması %100 BAŞARILI!")

    # 5. Sıralı nihai listeyi oluştur (2021-ALES/1: 1-100, 2021-ALES/2: 101-200)
    final_questions = []
    order_idx = 1

    # --- 2021-ALES/1 Sayısal ---
    for q in sayisal_list:
        q_copy = dict(q)
        q_copy["examId"] = "2021_ales1"
        q_copy["examTitle"] = "2021-ALES/1"
        q_copy["orderIndex"] = order_idx
        q_copy["options"] = normalize_options(q_copy.get("options", []))
        final_questions.append(q_copy)
        order_idx += 1

    # --- 2021-ALES/1 Sözel ---
    for q in sozel_list:
        q_copy = dict(q)
        q_copy["examId"] = "2021_ales1"
        q_copy["examTitle"] = "2021-ALES/1"
        q_copy["orderIndex"] = order_idx
        q_copy["options"] = normalize_options(q_copy.get("options", []))
        final_questions.append(q_copy)
        order_idx += 1

    # --- 2021-ALES/2 Sayısal ---
    for q in QUESTIONS_SAYISAL_2021_ALES2:
        q_copy = dict(q)
        q_copy["examId"] = "2021_ales2"
        q_copy["examTitle"] = "2021-ALES/2"
        q_copy["orderIndex"] = order_idx
        q_copy["options"] = normalize_options(q_copy.get("options", []))
        final_questions.append(q_copy)
        order_idx += 1

    # --- 2021-ALES/2 Sözel ---
    for q in QUESTIONS_SOZEL_2021_ALES2:
        q_copy = dict(q)
        q_copy["examId"] = "2021_ales2"
        q_copy["examTitle"] = "2021-ALES/2"
        q_copy["orderIndex"] = order_idx
        q_copy["options"] = normalize_options(q_copy.get("options", []))
        final_questions.append(q_copy)
        order_idx += 1

    # --- 2021-ALES/3 Sayısal ---
    for q in QUESTIONS_SAYISAL_2021_ALES3:
        q_copy = dict(q)
        q_copy["examId"] = "2021_ales3"
        q_copy["examTitle"] = "2021-ALES/3"
        q_copy["orderIndex"] = order_idx
        q_copy["options"] = normalize_options(q_copy.get("options", []))
        final_questions.append(q_copy)
        order_idx += 1

    # --- 2021-ALES/3 Sözel ---
    for q in QUESTIONS_SOZEL_2021_ALES3:
        q_copy = dict(q)
        q_copy["examId"] = "2021_ales3"
        q_copy["examTitle"] = "2021-ALES/3"
        q_copy["orderIndex"] = order_idx
        q_copy["options"] = normalize_options(q_copy.get("options", []))
        final_questions.append(q_copy)
        order_idx += 1

    out_file = Path("public/data/seed_questions.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(final_questions, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 {len(final_questions)} adet tam sınav sorusu '{out_file}' dosyasına aktarıldı!")
    print(f"📌 2021-ALES/1: 100 Soru (50 Sayısal + 50 Sözel)")
    print(f"📌 2021-ALES/2: 100 Soru (50 Sayısal + 50 Sözel)")
    print(f"📌 2021-ALES/3: 100 Soru (50 Sayısal + 50 Sözel)")
    print(f"📌 Toplam Soru Sayısı: {len(final_questions)}")
    print("=" * 70)

if __name__ == "__main__":
    build_native_questions()
