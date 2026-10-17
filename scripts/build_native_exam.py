#!/usr/bin/env python3
"""
scripts/build_native_exam.py
2021-ALES/1 sınavını ekran görüntüsü OLMADAN,
tamamen yerel metin, KaTeX matematik formülleri, Python SVG geometri çizimleri
ve yapılandırılmış şıklar olarak derler.
"""

import json
from pathlib import Path
from generators.geometry_generator import generate_all_svgs

def build_native_questions():
    # 1. Geometri SVG'lerini üret
    svg_map = generate_all_svgs()

    questions = [
        # --- MATEMATİK BÖLÜMÜ ---
        {
            "id": "2021_ales1_mat_01",
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
            "quickTip": "💡 ALES Taktiği: $\\sqrt{6}$ ile $\\sqrt{3}$ çarpımı $\\sqrt{18} = 3\\sqrt{2}$ yapar, payda doğrudan $\\sqrt{2}/\\sqrt{3}$'e düşer.",
            "targetTimeSec": 60,
            "derivedFrom": "2021-ALES/1-S3"
        },
        {
            "id": "2021_ales1_mat_04",
            "subject": "matematik",
            "category": "faktoriyel",
            "topicTitle": "Faktöriyel Sadeleştirme",
            "difficulty": 2,
            "questionText": "$$\\frac{\\frac{2}{3!} + \\frac{2}{4!}}{\\frac{3}{6!}}$$\n\nişleminin sonucu kaçtır?",
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
            "suggestedSolution": "Pay kısmında ortak payda yapalım:\n$\\frac{2}{3!} + \\frac{2}{4!} = \\frac{2 \\cdot 4 + 2}{4!} = \\frac{10}{24}$\nPayda: $\\frac{3}{6!} = \\frac{3}{720} = \\frac{1}{240}$\n\nBölme: $\\frac{10/24}{1/240} = \\frac{10}{24} \\cdot 240 = 10 \\cdot 10 = 100$ bulunur.",
            "quickTip": "💡 ALES Taktiği: $240 / 24 = 10$ olduğunu hemen görerek $10 \\times 10 = 100$ deyin.",
            "targetTimeSec": 50,
            "derivedFrom": "2021-ALES/1-S4"
        },
        {
            "id": "2021_ales1_mat_05",
            "subject": "matematik",
            "category": "basamak_kavrami",
            "topicTitle": "Alt Alta Çıkarma ve Basamak Değeri",
            "difficulty": 3,
            "questionText": "$A, B$ ve $C$ birer rakam olmak üzere,\n\n$$\\begin{array}{rr} & A5B \\\\ - & CA3 \\\\ \\hline & B79 \\end{array}$$\n\nolduğuna göre, $A + B + C$ toplamı kaçtır?",
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
            "suggestedSolution": "Birler basamağı: $B - 3 = 9$ olamaz, onluk alınmış: $(10 + B) - 3 = 9 \\implies B = 2$.\nOnlar basamağı: Onluk verildiği için 5 yerine 4 kaldı. $4 - A = 7$ olamayacağından yüzlükten onluk alınmış: $14 - A = 7 \\implies A = 7$.\nYüzler basamağı: $A$ bir eksildi ($7 - 1 = 6$). $6 - C = B \\implies 6 - C = 2 \\implies C = 4$.\n\nToplam: $A + B + C = 7 + 2 + 4 = 13$ bulunur.",
            "quickTip": "💡 ALES Taktiği: Çıkarma işlemlerinde eldeleri sağdan sola adım adım takip edin.",
            "targetTimeSec": 65,
            "derivedFrom": "2021-ALES/1-S5"
        },
        {
            "id": "2021_ales1_mat_14",
            "subject": "matematik",
            "category": "bolunebilme",
            "topicTitle": "Basamak ve Bölünebilme Kuralları",
            "difficulty": 3,
            "questionText": "Üç basamaklı $ABC$ doğal sayısı 9'a ve üç basamaklı $CBA$ doğal sayısı 5'e tam bölünmektedir.\n\nBuna göre, bu koşulu sağlayan kaç farklı $ABC$ doğal sayısı vardır?",
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
            "suggestedSolution": "$CBA$ üç basamaklı sayısı 5'e tam bölünüyorsa birler basamağı olan $A \\in \\{0, 5\\}$ olmalıdır. Ancak $ABC$ üç basamaklı bir sayı olduğundan yüzler basamağı $A \\neq 0$ olmalıdır. Dolayısıyla $A = 5$'tir.\n\n$CBA$ üç basamaklı olduğundan $C \\neq 0$'dır.\n$ABC = 5BC$ sayısı 9'a tam bölünüyorsa rakamları toplamı 9'un katı olmalıdır: $5 + B + C = 9k$.\n$B$ ve $C$ rakamları için $C \\in \\{1, 2, \\dots, 9\\}$ denendiğinde toplam 10 farklı $(B, C)$ çifti elde edilir.",
            "quickTip": "💡 ALES Taktiği: $A=0$ olamayacağını tespit etmek ilk ve en kritik elemedir.",
            "targetTimeSec": 70,
            "derivedFrom": "2021-ALES/1-S14"
        },
        {
            "id": "2021_ales1_mat_15",
            "subject": "matematik",
            "category": "basamak_cozumleme",
            "topicTitle": "Doğal Sayılarda Basamak Çözümleme",
            "difficulty": 3,
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
            "suggestedSolution": "Basamakları açalım:\n$A + (10A + B) + (100A + 10A + B) = 974$\n$121A + 2B = 974$\n\n$A$ bir rakam olduğuna göre: $974 / 121 \\approx 8.04 \\implies A = 8$ olur.\n$121 \\cdot 8 + 2B = 968 + 2B = 974 \\implies 2B = 6 \\implies B = 3$.\n\nİstenen çarpım: $A \\cdot B = 8 \\cdot 3 = 24$ bulunur.",
            "quickTip": "💡 ALES Taktiği: $121A + 2B = 974$ denkleminde $A$ katsayısı çok büyük olduğu için $A$ değeri tek bir ihtimalle ($A=8$) doğrudan çıkar.",
            "targetTimeSec": 60,
            "derivedFrom": "2021-ALES/1-S15"
        },
        {
            "id": "2021_ales1_mat_16",
            "subject": "matematik",
            "category": "kar_zarar_problemleri",
            "topicTitle": "Kâr - Zarar ve Denklem Kurma",
            "difficulty": 3,
            "questionText": "Bir balıkçı dükkânındaki bir kasa hamsinin tamamı;\n* Kilogramı 30 TL'den satılırsa 138 TL kâr,\n* Kilogramı 20 TL'den satılırsa 92 TL zarar ediliyor.\n\nBuna göre, bu kasada kaç kilogram hamsi vardır?",
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
            "suggestedSolution": "Kasada $x$ kg hamsi ve maliyeti $M$ olsun:\n$30x = M + 138$\n$20x = M - 92$\n\nİki denklemi birbirinden çıkaralım:\n$30x - 20x = (M + 138) - (M - 92)$\n$10x = 230 \\implies x = 23$ kg bulunur.",
            "quickTip": "💡 ALES Taktiği: Fiyat farkı ($30 - 20 = 10$) TL başına, toplam kasa farkı kâr + zarar ($138 + 92 = 230$) TL'dir. Direkt $230 / 10 = 23$ kg.",
            "targetTimeSec": 55,
            "derivedFrom": "2021-ALES/1-S16"
        },

        # --- GEOMETRİ BÖLÜMÜ (PYTHON SVG ÇİZİMLERİ İLE) ---
        {
            "id": "2021_ales1_mat_44",
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
            "suggestedSolution": "1. Karenin kenar uzunluğu 6 birimdir. $|AK| = 2, |KB| = 4$; $|LC| = 2, |BL| = 4$; $|CM| = 2, |MD| = 4$; $|NA| = 2, |DN| = 4$'tür.\n2. Şekil karenin merkezine ($(3, 3)$ noktasına) göre $180^\\circ$ dönme simetrisine sahiptir. $[KM]$ ve $[NL]$ doğruları tam karenin merkezi olan $P(3, 3)$ noktasında kesişir.\n3. Boyalı $AKPN$ dörtgenini $AP$ doğru parçası ile iki üçgene ayıralım:\n   * $\\triangle AKP$'nin tabanı $|AK| = 2$, yüksekliği $P$'nin $AB$'ye uzaklığı olan 3 birimdir: $\\text{Alan} = \\frac{2 \\cdot 3}{2} = 3$.\n   * $\\triangle ANP$'nin tabanı $|NA| = 2$, yüksekliği $P$'nin $AD$'ye uzaklığı olan 3 birimdir: $\\text{Alan} = \\frac{2 \\cdot 3}{2} = 3$.\n   * $\\text{Alan}(AKPN) = 3 + 3 = 6$ birimkaredir.\n4. Simetri gereği diğer boyalı $CLPM$ dörtgeninin alanı da 6 birimkaredir.\n5. Toplam boyalı alan: $6 + 6 = 12$ birimkare bulunur.",
            "quickTip": "💡 ALES Taktiği: Kesişim noktası $P$ merkezdedir (kenarlara uzaklık 3 birim). Tabanı 2, yüksekliği 3 olan dört simetrik üçgen vardır: $4 \\times \\frac{2 \\times 3}{2} = 12$.",
            "targetTimeSec": 70,
            "derivedFrom": "2021-ALES/1-S46"
        },
        {
            "id": "2021_ales1_mat_47",
            "subject": "matematik",
            "category": "geometri_dikdortgen",
            "topicTitle": "Dikdörtgende Alan Parçalama ve Oran",
            "difficulty": 3,
            "questionText": "$ABCD$ dikdörtgendir.\n* $|AE| = |EB|$\n* $\\frac{|DG|}{|GC|} = \\frac{|CF|}{|FB|} = \\frac{2}{3}$\n\nŞekilde $E, F$ ve $G$ noktaları $ABCD$ dikdörtgeninin kenarları üzerindedir.\n\nBuna göre, $EFCG$ dörtgeninin alanının $ABCD$ dikdörtgeninin alanına oranı kaçtır?",
            "hasImage": True,
            "svgContent": svg_map[47]["content"],
            "imageUrl": svg_map[47]["url"],
            "options": [
                {"key": "A", "text": "$\\frac{2}{5}$"},
                {"key": "B", "text": "$\\frac{4}{5}$"},
                {"key": "C", "text": "$\\frac{2}{3}$"},
                {"key": "D", "text": "$\\frac{1}{3}$"},
                {"key": "E", "text": "$\\frac{1}{2}$"}
            ],
            "correctAnswer": "A",
            "suggestedSolution": "1. Dikdörtgenin kenarlarına oranları rahat bölünebilen değerler verelim: $|AB| = |DC| = 10$, $|AD| = |BC| = 5$ olsun. $\\text{Alan}(ABCD) = 10 \\cdot 5 = 50$.\n2. $E$ noktası $AB$'nin orta noktası olduğundan $|AE| = |EB| = 5$'tir.\n3. $\\frac{|DG|}{|GC|} = \\frac{2}{3}$ ve $|DC| = 10$ olduğundan: $|DG| = 4, |GC| = 6$.\n4. $\\frac{|CF|}{|FB|} = \\frac{2}{3}$ ve $|BC| = 5$ olduğundan: $|CF| = 2, |FB| = 3$.\n5. Dikdörtgenden beyaz bölgelerin alanını çıkaralım:\n   * $AEGD$ dik yamuğunun alanı: $\\frac{|AE| + |DG|}{2} \\cdot |AD| = \\frac{5 + 4}{2} \\cdot 5 = \\frac{45}{2} = 22.5$\n   * $EBF$ dik üçgeninin alanı: $\\frac{|EB| \\cdot |FB|}{2} = \\frac{5 \\cdot 3}{2} = 7.5$\n   * Beyaz alanlar toplamı: $22.5 + 7.5 = 30$\n6. $EFCG$ dörtgeninin alanı: $50 - 30 = 20$.\n7. İstenen oran: $\\frac{\\text{Alan}(EFCG)}{\\text{Alan}(ABCD)} = \\frac{20}{50} = \\frac{2}{5}$ bulunur.",
            "quickTip": "💡 ALES Taktiği: Oran sorularında kenarlara paydaların katı sayısal değerler verin ($10$ ve $5$). Tüm alandan dik yamuk ve dik üçgeni çıkararak 20 saniyede sonuca ulaşın.",
            "targetTimeSec": 75,
            "derivedFrom": "2021-ALES/1-S47"
        },
        {
            "id": "2021_ales1_mat_48",
            "subject": "matematik",
            "category": "geometri_cember",
            "topicTitle": "Çemberde Kiriş ve Uzunluk",
            "difficulty": 3,
            "questionText": "$C$ noktası, $O$ merkezli yarım çemberin üzerindedir.\n* $D \\in [AC]$\n* $|AD| = 14 \\text{ birim}$\n* $|DC| = 2 \\text{ birim}$\n* $|AO| = 10 \\text{ birim}$\n* $|OD| = x$\n\nBuna göre, $x$ kaç birimdir?",
            "hasImage": True,
            "svgContent": svg_map[48]["content"],
            "imageUrl": svg_map[48]["url"],
            "options": [
                {"key": "A", "text": "6"},
                {"key": "B", "text": "8"},
                {"key": "C", "text": "$6\\sqrt{2}$"},
                {"key": "D", "text": "$8\\sqrt{2}$"},
                {"key": "E", "text": "$6\\sqrt{3}$"}
            ],
            "correctAnswer": "C",
            "suggestedSolution": "1. $[AB]$ çap ve $O$ merkez olduğundan çemberin yarıçapı $R = |AO| = |OB| = |OC| = 10$ birimdir.\n2. $|AC| = |AD| + |DC| = 14 + 2 = 16$ birimlik bir kiriştir.\n3. $AOC$ üçgeninde $|OA| = |OC| = 10$ olduğundan bu üçgen ikizkenardır.\n4. $O$ merkezinden $[AC]$ kirişine bir $OH$ dikmesi indirelim ($[OH] \\perp [AC]$).\n   Kirişe indirilen dikme kirişi iki eşit parçaya böler: $|AH| = |HC| = \\frac{16}{2} = 8$ birim.\n5. $OHA$ dik üçgeninde hipotenüs 10, dik kenar 8 olduğundan (6-8-10 özel üçgeni) $|OH| = 6$ birim bulunur.\n6. Şimdi $D$ noktasının konumuna bakalım: $|AD| = 14$ ve $|AH| = 8$ olduğundan $|HD| = |AD| - |AH| = 14 - 8 = 6$ birimdir.\n7. $OHD$ üçgeninde: $[OH] \\perp [HD]$, $|OH| = 6$ ve $|HD| = 6$ birimdir.\n   Yani $OHD$ üçgeni bir $45^\\circ-45^\\circ-90^\\circ$ ikizkenar dik üçgenidir!\n8. Pisagor teoreminden hipotenüs $x = |OD| = 6\\sqrt{2}$ birim bulunur.",
            "quickTip": "💡 ALES Taktiği: Çemberde kiriş gördüğünüzde merkezden hemen dik indirin! Kiriş ikiye bölünür ($8, 8$), 6-8-10 üçgeninden dikme 6 çıkar. $HD = 14 - 8 = 6$ olunca $6-6-6\\sqrt{2}$ kendiliğinden gelir.",
            "targetTimeSec": 70,
            "derivedFrom": "2021-ALES/1-S48"
        },

        # --- TÜRKÇE & SÖZEL BÖLÜMÜ ---
        {
            "id": "2021_ales1_turkce_01",
            "subject": "turkce",
            "category": "cumlede_anlam",
            "topicTitle": "Cümlede Boşluk Tamamlama",
            "difficulty": 2,
            "questionText": "Sanat eylemi; insanın hissettiği bir duyguyu ---- sonra bu duyguyu başkalarının da aynen hissedebilmesi için hareket, çizgi, renk, ses veya sözcüklerle ----.\n\n**Bu cümlede boş bırakılan yerlere anlam akışına göre aşağıdakilerden hangisi getirilmelidir?**",
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
            "suggestedSolution": "Sanat eylemi insanın duyguyu 'içselleştirmesi' ve bunu başkalarına 'aktarması' sürecidir. Anlam bütünlüğü B seçeneğinde tam olarak sağlanmaktadır.",
            "quickTip": "💡 ALES Taktiği: İkinci boşluktaki 'başkalarının da aynen hissetmesi için' ifadesi doğrudan 'aktarmasıdır' kavramına işaret eder.",
            "targetTimeSec": 45,
            "derivedFrom": "2021-ALES/1-T01"
        },
        {
            "id": "2021_ales1_turkce_02",
            "subject": "turkce",
            "category": "cumlede_anlam",
            "topicTitle": "Cümlede Anlam İlişkisi",
            "difficulty": 2,
            "questionText": "Bilge Karasu’nun eserleri, metnin boşluklarını okurun kendi ---- tamamlamasını gerektirdiği ve ona farklı okuma ---- sunduğu için okuma uğraşını bir tür oyuna veya serüvene dönüştürür.\n\n**Bu cümlede boş bırakılan yerlere sırasıyla hangisi getirilmelidir?**",
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
            "suggestedSolution": "Okurun kendi 'birikimleriyle' metnin boşluklarını tamamlaması ve metnin 'farklı okuma olanakları' sunması edebi dilde en yetkin ve uyumlu kullanımdır.",
            "quickTip": "💡 ALES Taktiği: 'Okuma olanakları' tamlaması edebiyat eleştirisinde kalıplaşmış bir ifadedir.",
            "targetTimeSec": 45,
            "derivedFrom": "2021-ALES/1-T02"
        },
        {
            "id": "2021_ales1_turkce_03",
            "subject": "turkce",
            "category": "paragrafta_anlam",
            "topicTitle": "Paragrafta Ana Düşünce",
            "difficulty": 2,
            "questionText": "Franz Kafka’nın Dönüşüm adlı eseri, insanın kapitalist düzendeki yerini konu alır. Gregor Samsa bir sabah kendini bir böceğe dönüşmüş olarak bulduğunda bile ilk aklına gelen şey işe geç kalıp kalmadığıdır. Bu absürt durum, sistemin insan bilincini ne denli rehin aldığının en çarpıcı göstergesidir.\n\n**Bu parçada asıl anlatılmak istenen aşağıdakilerden hangisidir?**",
            "hasImage": False,
            "imageUrl": None,
            "options": [
                {"key": "A", "text": "İnsanın iş hayatındaki sorumlulukları diğer tüm durumlardan önce gelir."},
                {"key": "B", "text": "Birey, sistemin dayattığı mekanik düzen içinde kendi varoluşuna bile yabancılaşmaktadır."},
                {"key": "C", "text": "Kafka eserlerinde toplumun beklentilerini gerçekçi bir üslupla aktarır."},
                {"key": "D", "text": "Dönüşüm romanı insanın doğa karşısındaki çaresizliğini işlemektedir."},
                {"key": "E", "text": "Modern toplumlarda çalışanların yaşadığı kaygılar psikolojik kökenlidir."}
            ],
            "correctAnswer": "B",
            "suggestedSolution": "Parçada Samsa'nın böceğe dönüşmesine rağmen yalnızca işe geç kalmayı dert etmesi, sistemin insan bilincini rehin alarak kendi varlığına bile yabancılaşması olarak açıklanmıştır (B seçeneği).",
            "quickTip": "💡 ALES Taktiği: 'En çarpıcı göstergesidir' vurgusu parçanın ana fikrine doğrudan giden köprüdür.",
            "targetTimeSec": 50,
            "derivedFrom": "2021-ALES/1-T03"
        },

        # --- SÖZEL MANTIK BÖLÜMÜ ---
        {
            "id": "2021_ales1_mantik_43",
            "subject": "mantik",
            "category": "sozel_mantik_tablo",
            "topicTitle": "Sözel Mantık: İl Sunumları ve Sıralama",
            "difficulty": 4,
            "questionText": "Ali, Banu, Ceyda, Deniz, Elçin, Fatma, Gamze, Hale ve İrem adlı 9 öğrenci üçer kişilik gruplara ayrılarak Kütahya, Mersin ve Niğde illerini tanıtan birer sunum hazırlamışlardır. Gruplardaki kişiler ve sunum sıralamasıyla ilgili bilinenler şunlardır:\n* Sunumlarda sırasıyla **Kütahya, Mersin ve Niğde** illeri tanıtılmıştır.\n* Her il tanıtılırken grup üyeleri, adlarının **alfabetik sırasına** göre söz almıştır.\n* Elçin, kendi grubu içinde söz alan ilk öğrencidir.\n* Fatma, tüm öğrenciler arasında söz alan son öğrencidir.\n* Ali ve Gamze, Kütahya ilini tanıtan gruptadır.\n\n**Buna göre; Banu, Ceyda ve Hale adlı öğrencilerden hangileri Mersin’i tanıtmış olabilir?**",
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
            "suggestedSolution": "Analiz Adımları:\n1. Kütahya Grubu: Ali ve Gamze kesin buradadır. Yanlarına 3. kişi gereklidir.\n2. Fatma tüm öğrenciler arasında SON öğrencidir. Sunum sırası Kütahya -> Mersin -> Niğde olduğuna göre Fatma kesinlikle **Niğde** grubundadır ve o grubun son konuşmacısıdır.\n3. Elçin kendi grubunda İLK öğrencidir. Alfabetik kural gereği Elçin'den önce gelen öğrenciler (Ali, Banu, Ceyda, Deniz) Elçin'in grubunda olamaz. Bu nedenle Banu ve Ceyda Elçin ile aynı grupta yer alamaz.\n4. Kütahya grubunda Ali (A) ve Gamze (G) vardır. Yanlarına Banu (B) veya Ceyda (C) gelmelidir.\n5. Dolayısıyla Mersin grubunda Banu veya Ceyda olamaz; Hale (H) Mersin grubunda yer alabilir. Doğru cevap Yalnız III (C seçeneği).",
            "quickTip": "💡 ALES Taktiği: 'Alfabetik sıra' ve 'ilk konuşmacı' kuralında, o harften önceki kişileri o gruptan derhal eleyin.",
            "targetTimeSec": 90,
            "derivedFrom": "2021-ALES/1-M43"
        },
        {
            "id": "2021_ales1_mantik_47",
            "subject": "mantik",
            "category": "sozel_mantik_eslestirme",
            "topicTitle": "Sözel Mantık: Figüran ve Film Eşleştirmesi",
            "difficulty": 4,
            "questionText": "Kemal, Levent ve Melek adlı üç figüran A, B, C, D ve E filmlerinde rol almıştır. Figüranların rol aldıkları filmlere ilişkin kimi bilgiler şu şekildedir:\n* Her figüran en az bir filmde rol almıştır.\n* B ve D filmlerinde birer, diğer filmlerde (A, C, E) ikişer figüran rol almıştır.\n* Kemal E filminde, Levent de B filminde rol almıştır.\n* Melek iki filmde rol almıştır.\n* Kemal ve Levent eşit sayıda filmde rol almıştır.\n* Kemal ile Melek sadece C filminde birlikte rol almıştır.\n\n**Buna göre; Kemal, Levent ve Melek adlı figüranlardan hangileri D filminde rol almış olabilir?**",
            "hasImage": False,
            "imageUrl": None,
            "options": [
                {"key": "A", "text": "Yalnız I"},
                {"key": "B", "text": "I ve II"},
                {"key": "C", "text": "I ve III"},
                {"key": "D", "text": "II ve III"},
                {"key": "E", "text": "I, II ve III"}
            ],
            "correctAnswer": "A",
            "suggestedSolution": "Kişi/Film tablosu kuralım:\nToplam roller: A(2) + B(1) + C(2) + D(1) + E(2) = 8 rol.\nMelek 2 filmde rol almıştır.\nGeriye kalan roller: 8 - 2 = 6 rol.\nKemal ve Levent eşit sayıda filmde rol aldığına göre her biri $6/2 = 3$'er filmde rol almıştır.\nMelek sadece C filminde Kemal ile birliktedir. Melek B'de rol alamaz (B'de sadece Levent var). Melek'in diğer rolü zorunlu olarak D veya A olabilir.\nTüm kısıtlamalar uygulandığında D filminde yalnızca Kemal'in yer alabileceği kesinleşir.",
            "quickTip": "💡 ALES Taktiği: Toplam kontenjan hesabını (8 rol) yapıp kişi sayılarına ($2 + 3 + 3 = 8$) dağıtmak soruyu 30 saniyede çözer.",
            "targetTimeSec": 90,
            "derivedFrom": "2021-ALES/1-M47"
        }
    ]

    out_file = Path("public/data/seed_questions.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(questions)} adet yerel, KaTeX destekli ve SVG çizimli soru '{out_file}' dosyasına aktarıldı!")

if __name__ == "__main__":
    build_native_questions()
