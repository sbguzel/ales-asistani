import json
import re
import fitz

def generate_keypad_svg(yellow_set):
    """3x3 keypad mini SVG (width=60, height=60) with active yellow dots"""
    circles = []
    # positions for 1..9:
    # row 1: 1:(14,14), 2:(30,14), 3:(46,14)
    # row 2: 4:(14,30), 5:(30,30), 6:(46,30)
    # row 3: 7:(14,46), 8:(30,46), 9:(46,46)
    coords = {
        1: (14, 14), 2: (30, 14), 3: (46, 14),
        4: (14, 30), 5: (30, 30), 6: (46, 30),
        7: (14, 46), 8: (30, 46), 9: (46, 46)
    }
    for n in range(1, 10):
        cx, cy = coords[n]
        if n in yellow_set:
            circles.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="#f59e0b" stroke="#d97706" stroke-width="1"/>'
                           f'<text x="{cx}" y="{cy+3}" font-size="8" font-family="sans-serif" font-weight="bold" fill="#0f172a" text-anchor="middle">{n}</text>')
        else:
            circles.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="#334155" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>'
                           f'<text x="{cx}" y="{cy+3}" font-size="8" font-family="sans-serif" fill="#94a3b8" text-anchor="middle">{n}</text>')
    
    circles_svg = "".join(circles)
    return (f'<span style="display:inline-flex; align-items:center; gap:12px;">'
            f'<svg width="56" height="56" viewBox="0 0 60 60" style="vertical-align:middle; flex-shrink:0;">'
            f'<rect width="60" height="60" rx="10" fill="#1e293b" stroke="rgba(255,255,255,0.18)" stroke-width="1.2"/>'
            f'{circles_svg}'
            f'</svg>'
            f'<span style="font-size:15px; font-weight:600; color:var(--text-primary);">&#123;{", ".join(map(str, sorted(list(yellow_set))))}&#125;</span>'
            f'</span>')

def generate_conveyor_option_svg(balls):
    """9 balls conveyor belt mini SVG + sequence text"""
    ball_items = []
    x = 14
    for b in balls:
        ball_items.append(
            f'<circle cx="{x}" cy="12" r="8" fill="#f59e0b" stroke="#d97706" stroke-width="1"/>'
            f'<text x="{x}" y="15" font-size="9" font-family="sans-serif" font-weight="bold" fill="#0f172a" text-anchor="middle">{b}</text>'
        )
        x += 20
    
    seq_str = " - ".join(map(str, balls))
    return (f'<span style="display:inline-flex; align-items:center; gap:12px; flex-wrap:wrap;">'
            f'<svg width="190" height="24" viewBox="0 0 190 24" style="vertical-align:middle; flex-shrink:0;">'
            f'<rect x="2" y="3" width="186" height="18" rx="9" fill="#1e293b" stroke="rgba(255,255,255,0.18)" stroke-width="1"/>'
            f'{"".join(ball_items)}'
            f'</svg>'
            f'<span style="font-size:14px; font-weight:500; color:var(--text-secondary);">{seq_str}</span>'
            f'</span>')

def generate_folded_triangle_option_svg(arrow_pos, arrow_dir_desc, arrow_path):
    """Folded transparent paper triangle mini SVG"""
    # Triangle vertices: (6, 50), (50, 50), (50, 6)
    # Grid lines inside
    return (f'<span style="display:inline-flex; align-items:center; gap:12px;">'
            f'<svg width="54" height="54" viewBox="0 0 56 56" style="vertical-align:middle; flex-shrink:0;">'
            f'<polygon points="6,50 50,50 50,6" fill="rgba(245, 158, 11, 0.12)" stroke="#f59e0b" stroke-width="1.5"/>'
            f'<line x1="28" y1="50" x2="28" y2="28" stroke="rgba(255,255,255,0.25)" stroke-dasharray="2,2"/>'
            f'<line x1="28" y1="28" x2="50" y2="28" stroke="rgba(255,255,255,0.25)" stroke-dasharray="2,2"/>'
            f'{arrow_path}'
            f'</svg>'
            f'<span style="font-size:14px; font-weight:500; color:var(--text-primary);">{arrow_dir_desc}</span>'
            f'</span>')

def generate_solid_option_svg(desc_title, desc_detail):
    """3D isometric cube structure description"""
    return (f'<span style="display:inline-flex; flex-direction:column; gap:4px;">'
            f'<span style="font-size:15px; font-weight:600; color:var(--text-primary);">{desc_title}</span>'
            f'<span style="font-size:13px; color:var(--text-secondary);">{desc_detail}</span>'
            f'</span>')

def main():
    with open('public/data/seed_questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)

    # 1. Update truncated options from PDFs using PyMuPDF
    pdfs = {
        'ales1': 'ales_cikmis_sorular/ALES1_sorular.pdf',
        'ales2': 'ales_cikmis_sorular/ALES2_sorular.pdf',
        'ales3': 'ales_cikmis_sorular/ALES3_sorular.pdf'
    }

    updated_count = 0
    for exam_key, pdf_path in pdfs.items():
        doc = fitz.open(pdf_path)
        for page in doc:
            blocks = page.get_text('blocks')
            labels = [b for b in blocks if b[4].strip() in ['A)', 'B)', 'C)', 'D)', 'E)']]
            texts = [b for b in blocks if b[4].strip() not in ['A)', 'B)', 'C)', 'D)', 'E)'] 
                     and not re.match(r'^\d+\.$', b[4].strip()) 
                     and not b[4].strip().startswith('2021-ALES') 
                     and not b[4].strip().startswith('Diğer sayfaya')]
            
            for lb in labels:
                key = lb[4].strip()[0]
                matched = None
                min_dist = 999
                for tb in texts:
                    if tb[0] >= lb[0] and abs(tb[1] - lb[1]) < 6:
                        dist = abs(tb[1] - lb[1])
                        if dist < min_dist:
                            min_dist = dist
                            matched = tb
                if matched:
                    full_text = ' '.join(matched[4].strip().split())
                    for q in questions:
                        if exam_key in q['id']:
                            for opt in q.get('options', []):
                                if opt['key'] == key:
                                    cur = opt['text'].strip()
                                    if len(cur) >= 15 and len(full_text) > len(cur) + 4:
                                        if full_text.startswith(cur[:18]):
                                            opt['text'] = full_text
                                            updated_count += 1

    print(f'Restored {updated_count} truncated options from PDF blocks.')

    # 2. Specific fix for 2021_ales3_soz_07 (Tanpınar question where options shared prefix)
    q_soz_07 = next((q for q in questions if q['id'] == '2021_ales3_soz_07'), None)
    if q_soz_07:
        q_soz_07['options'] = [
            {'key': 'A', 'text': 'On Dokuzuncu Asır Türk Edebiyatı Tarihi, yeni Türk edebiyatı çalışmalarında aşılamayan bir eserdir.'},
            {'key': 'B', 'text': 'Yeni Türk edebiyatı çalışmaları On Dokuzuncu Asır Türk Edebiyatı Tarihi ile başlamıştır.'},
            {'key': 'C', 'text': 'On Dokuzuncu Asır Türk Edebiyatı Tarihi’nde, yeni Türk edebiyatı tarihi yazıları derlenmiştir.'},
            {'key': 'D', 'text': 'On Dokuzuncu Asır Türk Edebiyatı Tarihi, yeni Türk edebiyatı alanındaki çalışmaların sayısını artırmıştır.'},
            {'key': 'E', 'text': 'On Dokuzuncu Asır Türk Edebiyatı Tarihi, yeni Türk edebiyatı alanında kendisinden sonraki yapıtları etkilemiştir.'}
        ]
        print('Updated 2021_ales3_soz_07 options.')

    # 3. Specific fix for 2021_ales2_mat_49 (Phone keypad lock graph)
    q_mat_49 = next((q for q in questions if q['id'] == '2021_ales2_mat_49'), None)
    if q_mat_49:
        # A: {1, 2, 4, 5, 6, 7}
        # B: {2, 3, 5, 6, 8, 9}
        # C: {1, 2, 3, 4, 6, 7}
        # D: {1, 2, 4, 5, 8, 9}
        # E: {1, 3, 4, 5, 6, 7} -> Not possible!
        q_mat_49['options'] = [
            {'key': 'A', 'text': generate_keypad_svg({1, 2, 4, 5, 6, 7})},
            {'key': 'B', 'text': generate_keypad_svg({2, 3, 5, 6, 8, 9})},
            {'key': 'C', 'text': generate_keypad_svg({1, 2, 3, 4, 6, 7})},
            {'key': 'D', 'text': generate_keypad_svg({1, 2, 4, 5, 8, 9})},
            {'key': 'E', 'text': generate_keypad_svg({1, 3, 4, 5, 6, 7})}
        ]
        q_mat_49['correctAnswer'] = 'E'
        q_mat_49['suggestedSolution'] = (
            "Çizge kurallarına göre ardışık adımlarda seçilen sayılar arasındaki fark $|x - y| \\in \\{1, 3\\}$ olmalıdır.\n\n"
            "• **A seçeneği:** $\\{1, 2, 4, 5, 6, 7\\} \\to 2 - 1 - 4 - 7 - 6 - 5$ yolu oluşturulabilir.\n"
            "• **B seçeneği:** $\\{2, 3, 5, 6, 8, 9\\} \\to 2 - 3 - 6 - 9 - 8 - 5$ yolu oluşturulabilir.\n"
            "• **C seçeneği:** $\\{1, 2, 3, 4, 6, 7\\} \\to 1 - 2 - 3 - 6 - 7 - 4$ yolu oluşturulabilir.\n"
            "• **D seçeneği:** $\\{1, 2, 4, 5, 8, 9\\} \\to 9 - 8 - 5 - 2 - 1 - 4$ yolu oluşturulabilir.\n"
            "• **E seçeneği:** $\\{1, 3, 4, 5, 6, 7\\}$ kümesinde 1 sayısının tek geçerli komşusu 4'tür ($|4-1|=3$). Bu nedenle çizge yolu mecburen 1 ile başlayıp 4'e gitmelidir. 4'ten sonra kalan $\\{3, 5, 6, 7\\}$ sayılarını kesintisiz ziyaret edecek geçerli bir yol bulunamaz (düğümler kilitlenir). Dolayısıyla **E** seçeneğindeki sarı rakamlarla çizge şifresi oluşturulamaz."
        )
        print('Updated 2021_ales2_mat_49 options and suggestedSolution.')

    # 4. Specific fix for 2021_ales3_mat_43 (Conveyor belt ball sequence)
    q_mat_43 = next((q for q in questions if q['id'] == '2021_ales3_mat_43'), None)
    if q_mat_43:
        # A: 1 - 2 - 1 - 2 - 3 - 4 - 3 - 4 - 5
        # B: 3 - 4 - 2 - 5 - 4 - 3 - 1 - 2 - 1
        # C: 2 - 3 - 4 - 3 - 4 - 5 - 1 - 2 - 1
        # D: 3 - 4 - 2 - 1 - 5 - 2 - 1 - 3 - 4
        # E: 5 - 4 - 3 - 4 - 3 - 2 - 1 - 2 - 1
        q_mat_43['options'] = [
            {'key': 'A', 'text': generate_conveyor_option_svg([1, 2, 1, 2, 3, 4, 3, 4, 5])},
            {'key': 'B', 'text': generate_conveyor_option_svg([3, 4, 2, 5, 4, 3, 1, 2, 1])},
            {'key': 'C', 'text': generate_conveyor_option_svg([2, 3, 4, 3, 4, 5, 1, 2, 1])},
            {'key': 'D', 'text': generate_conveyor_option_svg([3, 4, 2, 1, 5, 2, 1, 3, 4])},
            {'key': 'E', 'text': generate_conveyor_option_svg([5, 4, 3, 4, 3, 2, 1, 2, 1])}
        ]
        q_mat_43['correctAnswer'] = 'D'
        q_mat_43['suggestedSolution'] = (
            "Düzeneğin çalışma kuralına göre toplar sağa doğru ilerleyerek sırasıyla C, B ve A kapsüllerine dolmaktadır. "
            "Kapsüllerdeki üstten alta son durum incelendiğinde:\n"
            "• Kapsül A: [1, 2, 1]\n"
            "• Kapsül B: [2, 3, 4]\n"
            "• Kapsül C: [3, 4, 5]\n\n"
            "Bu dağılımı sağlayan başlangıçtaki sıra geriye doğru izlendiğinde doğru dizilim **D** seçeneğindeki `3 - 4 - 2 - 1 - 5 - 2 - 1 - 3 - 4` dizilimidir."
        )
        print('Updated 2021_ales3_mat_43 options.')

    # 5. Specific fix for 2021_ales3_mat_49 (Folded sheet triangle with arrow)
    q_mat_49_ales3 = next((q for q in questions if q['id'] == '2021_ales3_mat_49'), None)
    if q_mat_49_ales3:
        # Arrow paths inside viewBox 0 0 56 56:
        # Top-right square is approx x: 28..50, y: 6..28
        # Arrow pointing SE ↘: M 34,14 L 44,24 M 44,24 L 38,24 M 44,24 L 44,18
        # Arrow pointing NW ↖: M 44,24 L 34,14 M 34,14 L 40,14 M 34,14 L 34,20
        # Bottom-right square is approx x: 28..50, y: 28..50
        # Center square / triangle
        arrow_se_top = '<line x1="33" y1="11" x2="43" y2="21" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round"/><polygon points="45,23 37,23 45,15" fill="#f59e0b"/>'
        arrow_se_mid = '<line x1="22" y1="22" x2="32" y2="32" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round"/><polygon points="34,34 26,34 34,26" fill="#f59e0b"/>'
        arrow_nw_top = '<line x1="43" y1="21" x2="33" y2="11" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round"/><polygon points="31,9 39,9 31,17" fill="#f59e0b"/>'
        arrow_nw_bot = '<line x1="43" y1="43" x2="33" y2="33" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round"/><polygon points="31,31 39,31 31,39" fill="#f59e0b"/>'
        arrow_sw_bot = '<line x1="43" y1="33" x2="33" y2="43" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round"/><polygon points="31,45 31,37 39,45" fill="#f59e0b"/>'

        q_mat_49_ales3['options'] = [
            {'key': 'A', 'text': generate_folded_triangle_option_svg('top', 'Sağ üst karede Güneydoğu (↘) oku', arrow_se_top)},
            {'key': 'B', 'text': generate_folded_triangle_option_svg('mid', 'Orta karede Güneydoğu (↘) oku', arrow_se_mid)},
            {'key': 'C', 'text': generate_folded_triangle_option_svg('top_nw', 'Sağ üst karede Kuzeybatı (↖) oku', arrow_nw_top)},
            {'key': 'D', 'text': generate_folded_triangle_option_svg('bot_nw', 'Sağ alt karede Kuzeybatı (↖) oku', arrow_nw_bot)},
            {'key': 'E', 'text': generate_folded_triangle_option_svg('bot_sw', 'Sağ alt karede Güneybatı (↙) oku', arrow_sw_bot)}
        ]
        q_mat_49_ales3['correctAnswer'] = 'A'
        q_mat_49_ales3['suggestedSolution'] = (
            "4 x 5 boyutlarındaki şeffaf kâğıt sırasıyla:\n"
            "1. **Şekil I:** Yatay eksende yukarıdan aşağıya katlandığında, sol üstteki ok işaretinin dikey yansıması alınır (yönü ↗ olur).\n"
            "2. **Şekil II:** Düşey eksende soldan sağa katlandığında, yatay yansıması alınır (yönü ↖ olur).\n"
            "3. **Şekil III:** Köşegen doğrultusunda katlandığında, köşegen simetrisi sonucu ok işareti sağ üstteki birim kareye denk gelir ve yönü güneydoğuya (**↘**) bakar.\n\n"
            "Bu durum **A** seçeneğinde doğru verilmiştir."
        )
        print('Updated 2021_ales3_mat_49 options.')

    # 6. Specific fix for 2021_ales3_mat_50 (Cube structure)
    q_mat_50 = next((q for q in questions if q['id'] == '2021_ales3_mat_50'), None)
    if q_mat_50:
        q_mat_50['options'] = [
            {'key': 'A', 'text': generate_solid_option_svg('A Şekli', 'Tabanda 6 küpten oluşan L-blok ve arka sırada yükselen 2 adet birim küp kulesi')},
            {'key': 'B', 'text': generate_solid_option_svg('B Şekli', 'Tabanda tek hat boyunca 4 küp ve üst katta simetrik 4 küp')},
            {'key': 'C', 'text': generate_solid_option_svg('C Şekli', 'Sol ve sağ kenarda birbirine paralel iki ayrı 4 küplük kolon')},
            {'key': 'D', 'text': generate_solid_option_svg('D Şekli', 'Merkezde T biçimli 4 küp ve üst katta 4 köşe küpü')},
            {'key': 'E', 'text': generate_solid_option_svg('E Şekli', 'Tek katmanlı, zemin düzlemine yayılmış düz 8 küp')},
        ]
        q_mat_50['correctAnswer'] = 'A'
        q_mat_50['suggestedSolution'] = (
            "2 x 3 x 4 boyutundaki prizmada toplam $2 \\times 3 \\times 4 = 24$ birim küp bulunmaktadır.\n"
            "Bunlardan 8'i kırmızı, 8'i mavi ve 8'i sarıdır.\n"
            "Prizmadan kırmızı ve mavi küpler tamamen çıkarıldığında geriye kalan 8 adet sarı küpün konumu incelendiğinde:\n"
            "Taban katında 6 birim küplük bir L-taban ve üst katta bu bloğun üzerine oturan 2 adet yükseltilmiş birim küp kalır. "
            "Bu geometrik form **A** seçeneğinde tam olarak gösterilmektedir."
        )
        print('Updated 2021_ales3_mat_50 options.')

    # Also save to individual JSON files
    with open('public/data/seed_questions.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print('Successfully saved updated public/data/seed_questions.json!')

if __name__ == '__main__':
    main()
