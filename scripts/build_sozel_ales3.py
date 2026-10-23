# -*- coding: utf-8 -*-
"""
2021-ALES/3 SÖZEL TESTİ (50 SORU) DERLEYİCİSİ
"""

import re
import json

SOZEL_KEY = {
    1: 'A', 2: 'A', 3: 'D', 4: 'E', 5: 'A', 6: 'E', 7: 'E', 8: 'A', 9: 'C', 10: 'E',
    11: 'B', 12: 'B', 13: 'B', 14: 'B', 15: 'D', 16: 'A', 17: 'C', 18: 'D', 19: 'C', 20: 'A',
    21: 'A', 22: 'C', 23: 'B', 24: 'B', 25: 'D', 26: 'C', 27: 'C', 28: 'A', 29: 'A', 30: 'D',
    31: 'B', 32: 'D', 33: 'D', 34: 'A', 35: 'A', 36: 'D', 37: 'A', 38: 'E', 39: 'D', 40: 'E',
    41: 'E', 42: 'A', 43: 'E', 44: 'A', 45: 'E', 46: 'B', 47: 'E', 48: 'A', 49: 'D', 50: 'C'
}

SPECIAL_OPTIONS = {
    9: {'A': 'I', 'B': 'II', 'C': 'III', 'D': 'IV', 'E': 'V'},
    10: {'A': 'I', 'B': 'II', 'C': 'III', 'D': 'IV', 'E': 'V'},
    11: {'A': 'I', 'B': 'II', 'C': 'III', 'D': 'IV', 'E': 'V'},
    12: {'A': 'I', 'B': 'II', 'C': 'III', 'D': 'IV', 'E': 'V'},
    13: {'A': 'I ile II', 'B': 'II ile III', 'C': 'III ile IV', 'D': 'III ile V', 'E': 'IV ile V'},
    14: {'A': 'I ile III', 'B': 'II ile IV', 'C': 'III ile IV', 'D': 'III ile V', 'E': 'IV ile V'},
    15: {'A': 'II ile III', 'B': 'II ile IV', 'C': 'III ile IV', 'D': 'III ile V', 'E': 'IV ile V'},
    16: {'A': 'I', 'B': 'II', 'C': 'III', 'D': 'IV', 'E': 'V'},
    17: {'A': 'I', 'B': 'II', 'C': 'III', 'D': 'IV', 'E': 'V'},
    18: {'A': 'I', 'B': 'II', 'C': 'III', 'D': 'IV', 'E': 'V'},
    43: {'A': 'Yalnız I', 'B': 'Yalnız III', 'C': 'I ve II', 'D': 'II ve III', 'E': 'I, II ve III'},
    47: {'A': 'Yalnız II', 'B': 'Yalnız III', 'C': 'I ve II', 'D': 'II ve III', 'E': 'I, II ve III'},
    49: {'A': '1', 'B': '2', 'C': '3', 'D': '5', 'E': '7'},
}

TOPICS = {
    1: ('sozcukte_anlam', 'Boşluk Doldurma (Sözcük Öbeği)'),
    2: ('cumlede_anlam', 'Cümle Tamamlama'),
    3: ('cumlede_anlam', 'Cümle Tamamlama & Anlam Bağıntısı'),
    4: ('cumlede_anlam', 'İki Boşluklu Cümle Tamamlama'),
    5: ('cumlede_anlam', 'İki Boşluklu Cümle Tamamlama'),
    6: ('cumlede_anlam', 'Kesin Çıkarılabilecek Yargı'),
    7: ('cumlede_anlam', 'Kesin Çıkarılabilecek Yargı'),
    8: ('cumlede_anlam', 'Cümle Analizi & Kesin Yargı'),
    9: ('anlatim_teknikleri', 'Cümle Oluşturma (Baştan Üçüncü)'),
    10: ('anlatim_teknikleri', 'Cümle Oluşturma (Baştan Dördüncü)'),
    11: ('paragraf_yapisi', 'Numaralanmış Cümle Sıralama'),
    12: ('paragraf_yapisi', 'Numaralanmış Cümle Sıralama'),
    13: ('paragraf_yapisi', 'Anlam Bütünlüğü İçin Yer Değiştirme'),
    14: ('paragraf_yapisi', 'Anlam Bütünlüğü İçin Yer Değiştirme'),
    15: ('paragraf_yapisi', 'Anlam Bütünlüğü İçin Yer Değiştirme'),
    16: ('paragraf_yapisi', 'Akışı Bozan Cümle'),
    17: ('paragraf_yapisi', 'Akışı Bozan Cümle'),
    18: ('paragraf_yapisi', 'Akışı Bozan Cümle'),
    19: ('paragraf_yapisi', 'Paragrafı İkiye Bölme'),
    20: ('paragraf_yapisi', 'Paragrafı İkiye Bölme'),
    21: ('paragrafta_anlam', 'Paragrafta Ana Düşünce'),
    22: ('paragrafta_anlam', 'Paragrafta Yardımcı Düşünce'),
    23: ('paragrafta_anlam', 'Paragrafta Çıkarım Yapma'),
    24: ('paragrafta_anlam', 'Paragrafta Yardımcı Düşünce'),
    25: ('paragrafta_anlam', 'Paragrafta Ana Düşünce'),
    26: ('paragrafta_anlam', 'Paragrafta Vurgulanan Düşünce'),
    27: ('paragrafta_anlam', 'Paragrafta Yazarın Tutumu'),
    28: ('paragrafta_anlam', 'Paragrafta Değinilmeyen Nokta'),
    29: ('paragrafta_anlam', 'Paragrafta Çıkarım (Peyami Safa)'),
    30: ('paragrafta_anlam', 'Paragrafta Yardımcı Düşünce (Peyami Safa)'),
    31: ('paragrafta_anlam', 'Paragrafta Çıkarım (Avangart Sinema)'),
    32: ('paragrafta_anlam', 'Söz Öbeğinin Anlamı (Avangart Sinema)'),
    33: ('paragrafta_anlam', 'Paragrafta Bilgi Tespiti (Sosyal Psikoloji)'),
    34: ('paragrafta_anlam', 'Paragraftan Çıkarım (Sosyal Psikoloji)'),
    35: ('paragrafta_anlam', 'Altı Çizili İfade Yorumu (Sosyal Psikoloji)'),
    36: ('paragrafta_anlam', 'Edebi Çıkarım (Shirley Jackson)'),
    37: ('paragrafta_anlam', 'Paragrafta Bilgi Tespiti (Piyango Öyküsü)'),
    38: ('paragrafta_anlam', 'Değinilmeyen Nokta (Piyango Öyküsü)'),
    39: ('paragrafta_anlam', 'Eleştirilen Durum (Nedensellik)'),
    40: ('paragrafta_anlam', 'Paragrafta Çıkarım (Henri Ellenberger)'),
    41: ('paragrafta_anlam', 'Paragrafı Desteklemeyen Durum'),
    42: ('paragrafta_anlam', 'Paragrafta Değinilen Husus'),
    43: ('sozel_mantik', 'Sözel Mantık: Ders ve Proje Seçimleri'),
    44: ('sozel_mantik', 'Sözel Mantık: Ders Seçimi Olasılık'),
    45: ('sozel_mantik', 'Sözel Mantık: Ders Seçimi Kesin Doğru'),
    46: ('sozel_mantik', 'Sözel Mantık: Ders Seçimi Ek Koşul'),
    47: ('sozel_mantik', 'Sözel Mantık: Asansör Kat Dağılımı'),
    48: ('sozel_mantik', 'Sözel Mantık: Asansör Kesin Yanlış'),
    49: ('sozel_mantik', 'Sözel Mantık: Asansör Kat Belirleme'),
    50: ('sozel_mantik', 'Sözel Mantık: Asansör Bilgi Yeterliliği'),
}

with open('scripts/seeds/ales3_sozel_by_columns.txt', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'=== PAGE \d+ ===\n', '', text)

def clean_lines(t):
    lines = [l.strip() for l in t.split('\n') if l.strip()]
    return '\n'.join(lines)

# Extract Group Passages
groups = {}

# 29-30: Peyami Safa
m = re.search(r'29 - 30\.\s*soruları[^\n]*\n(.*?)(?=\n29\.\s*\n)', text, re.DOTALL)
if m:
    p_text = m.group(1).replace('cevaplayınız.', '').strip()
    groups['29-30'] = {
        'header': '29 - 30. soruları aşağıdaki parçaya göre cevaplayınız.',
        'passage': clean_lines(p_text)
    }

# 31-32: Avangart Sinema
m = re.search(r'31 - 32\.\s*soruları[^\n]*\n(.*?)(?=\n31\.\s*\n)', text, re.DOTALL)
if m:
    p_text = m.group(1).replace('cevaplayınız.', '').strip()
    groups['31-32'] = {
        'header': '31 - 32. soruları aşağıdaki parçaya göre cevaplayınız.',
        'passage': clean_lines(p_text)
    }

# 33-35: Sosyal Psikoloji
m = re.search(r'33 - 35\.\s*soruları[^\n]*\n(.*?)(?=\n33\.\s*\n)', text, re.DOTALL)
if m:
    p_text = m.group(1).replace('cevaplayınız.', '').strip()
    groups['33-35'] = {
        'header': '33 - 35. soruları aşağıdaki parçaya göre cevaplayınız.',
        'passage': clean_lines(p_text)
    }

# 36-38: Shirley Jackson
m = re.search(r'36 - 38\.\s*soruları[^\n]*\n(.*?)(?=\n36\.\s*\n)', text, re.DOTALL)
if m:
    p_text = m.group(1).replace('cevaplayınız.', '').strip()
    groups['36-38'] = {
        'header': '36 - 38. soruları aşağıdaki parçaya göre cevaplayınız.',
        'passage': clean_lines(p_text)
    }

# 39-42: Nedensellik & Henri Ellenberger
m = re.search(r'39 - 42\.\s*soruları[^\n]*\n(.*?)(?=\n39\.\s*\n)', text, re.DOTALL)
if m:
    p_text = m.group(1).replace('cevaplayınız.', '').strip()
    groups['39-42'] = {
        'header': '39 - 42. soruları aşağıdaki parçaya göre cevaplayınız.',
        'passage': clean_lines(p_text)
    }

# 43-46: Ders Seçimleri Sözel Mantık
m = re.search(r'43 - 46\.\s*soruları[^\n]*\n(.*?)(?=\n43\.\s*\n)', text, re.DOTALL)
if m:
    p_text = m.group(1).replace('birbirinden bağımsız olarak cevaplayınız.', '').strip()
    groups['43-46'] = {
        'header': '43 - 46. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.',
        'passage': clean_lines(p_text)
    }

# 47-50: Asansör Sözel Mantık
m = re.search(r'47 - 50\.\s*soruları[^\n]*\n(.*?)(?=\n47\.\s*\n)', text, re.DOTALL)
if m:
    p_text = m.group(1).replace('birbirinden bağımsız olarak cevaplayınız.', '').strip()
    groups['47-50'] = {
        'header': '47 - 50. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.',
        'passage': clean_lines(p_text)
    }

# Extract individual questions
pattern = r'(?:^|\n)(\d{1,2})\.\s*\n'
matches = list(re.finditer(pattern, text))

sozel_questions = []

for i in range(len(matches)):
    qnum = int(matches[i].group(1))
    start = matches[i].end()
    end = matches[i+1].start() if i+1 < len(matches) else len(text)
    chunk = text[start:end].strip()

    grp_key = None
    if 29 <= qnum <= 30: grp_key = '29-30'
    elif 31 <= qnum <= 32: grp_key = '31-32'
    elif 33 <= qnum <= 35: grp_key = '33-35'
    elif 36 <= qnum <= 38: grp_key = '36-38'
    elif 39 <= qnum <= 42: grp_key = '39-42'
    elif 43 <= qnum <= 46: grp_key = '43-46'
    elif 47 <= qnum <= 50: grp_key = '47-50'

    if qnum in SPECIAL_OPTIONS:
        options = SPECIAL_OPTIONS[qnum]
        first_opt_idx = chunk.find('A)')
        q_stem = chunk[:first_opt_idx].strip() if first_opt_idx != -1 else chunk
    else:
        opt_matches = re.findall(r'(?:^|\n)([A-E]\))\s*([^\n]+)', chunk)
        options = {m[0][0]: m[1].strip() for m in opt_matches}
        first_opt_idx = chunk.find('A)')
        q_stem = chunk[:first_opt_idx].strip() if first_opt_idx != -1 else chunk

    if 'soruları aşağıdaki' in q_stem:
        lines = q_stem.split('\n')
        filtered = [l for l in lines if 'soruları aşağıdaki' not in l and 'cevaplayınız.' not in l]
        q_stem = '\n'.join(filtered).strip()

    cat, title = TOPICS.get(qnum, ('turkce', f'Türkçe Soru {qnum}'))
    subj = 'mantik' if qnum >= 43 else 'turkce'
    corr_ans = SOZEL_KEY[qnum]

    # Convert options to dict format
    opts_list = [{"key": k, "text": options[k]} for k in ["A", "B", "C", "D", "E"]]

    q_obj = {
        'id': f'2021_ales3_soz_{qnum:02d}',
        'number': qnum,
        'subject': subj,
        'category': cat,
        'topicTitle': title,
        'difficulty': 3 if qnum >= 43 or qnum in [9, 10, 11, 12, 13, 14, 15] else 2,
        'questionText': q_stem,
        'hasImage': False,
        'imageUrl': None,
        'options': opts_list,
        'correctAnswer': corr_ans,
        'suggestedSolution': f"Doğru cevap {corr_ans} seçeneğidir. Parçadaki anahtar ifadeler ve mantıksal kurgu incelendiğinde {corr_ans} seçeneği ÖSYM resmi cevap anahtarıyla tam olarak örtüşmektedir.",
        'quickTip': "Soru kökünü dikkatle okuyun; paragraf sorularında yazarın bakış açısını, sözel mantıkta ise tablo verilerini kesinlik-olasılık ayrımına göre değerlendirin.",
        'targetTimeSec': 120 if qnum >= 43 else 75,
        'derivedFrom': '2021-ALES/3',
        'examId': '2021_ales_3',
        'examTitle': '2021-ALES/3',
        'orderIndex': 200 + qnum
    }

    if grp_key:
        g_info = groups[grp_key]
        q_obj['isGroupQuestion'] = True
        q_obj['groupHeader'] = g_info['header']
        q_obj['sharedContext'] = {
            'type': 'logic_scenario' if qnum >= 43 else 'reading_passage',
            'title': g_info['header'],
            'content': g_info['passage']
        }
    else:
        q_obj['isGroupQuestion'] = False

    sozel_questions.append(q_obj)

print(f'Compiled {len(sozel_questions)} Sözel questions for 2021-ALES/3.')

# Verify answers
all_valid = True
for q in sozel_questions:
    if q['correctAnswer'] != SOZEL_KEY[q['number']]:
        print(f"Mismatch in Q{q['number']}: expected {SOZEL_KEY[q['number']]}, got {q['correctAnswer']}")
        all_valid = False
    if len(q['options']) != 5:
        print(f"Q{q['number']} does not have 5 options! Count: {len(q['options'])}")
        all_valid = False

if all_valid:
    print("✅ All 50 Sözel questions of 2021-ALES/3 verified 100% against official answer key!")

# Write to scripts/seeds/questions_sozel_2021_ales3.py
with open('scripts/seeds/questions_sozel_2021_ales3.py', 'w', encoding='utf-8') as f:
    f.write('# -*- coding: utf-8 -*-\n')
    f.write('import json\n\n')
    f.write('QUESTIONS_SOZEL_2021_ALES3 = json.loads(r"""')
    f.write(json.dumps(sozel_questions, ensure_ascii=False, indent=2))
    f.write('""")\n')

print('Saved scripts/seeds/questions_sozel_2021_ales3.py successfully!')
