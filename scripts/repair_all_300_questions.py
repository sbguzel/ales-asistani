import json
import os
import re
import sys

sys.path.insert(0, os.path.abspath("scripts/seeds"))
from questions_sozel_2021_ales2 import QUESTIONS_SOZEL_2021_ALES2
from questions_sozel_2021_ales3 import QUESTIONS_SOZEL_2021_ALES3

def load_svg(filename):
    path = os.path.join("public/assets/questions/svg", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def make_opts(opt_list):
    keys = ["A", "B", "C", "D", "E"]
    return [{"key": keys[i], "text": str(opt_list[i])} for i in range(5)]

def set_group(q, group_id, group_header, idx, total, shared_context):
    q["isGroupQuestion"] = True
    q["groupId"] = group_id
    q["groupHeader"] = group_header
    q["groupIndex"] = idx
    q["groupTotal"] = total
    q["sharedContext"] = shared_context

def set_svg(q, filename):
    q["hasImage"] = True
    q["imageUrl"] = f"/assets/questions/svg/{filename}"
    q["svgContent"] = load_svg(filename)

def clear_svg(q):
    q["hasImage"] = False
    q["imageUrl"] = None
    q["svgContent"] = None

def main():
    with open("public/data/seed_questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    qmap = {q["id"]: q for q in questions}

    # =========================================================================
    # 1. RESTORE OVERWRITTEN SÖZEL MANTIK QUESTIONS (ALES2 44..48, ALES3 44..48)
    # =========================================================================
    soz2_map = {q["id"]: q for q in QUESTIONS_SOZEL_2021_ALES2}
    soz3_map = {q["id"]: q for q in QUESTIONS_SOZEL_2021_ALES3}

    for i in range(44, 49):
        qid2 = f"2021_ales2_soz_{i:02d}"
        orig2 = soz2_map[qid2]
        q2 = qmap[qid2]
        for k in ["questionText", "options", "correctAnswer", "suggestedSolution", "quickTip", "topicTitle", "category", "sharedContext", "isGroupQuestion", "groupId"]:
            if k in orig2:
                if k == "options" and isinstance(orig2[k], dict):
                    q2[k] = [{"key": ok, "text": ov} for ok, ov in orig2[k].items()]
                else:
                    q2[k] = orig2[k]

        qid3 = f"2021_ales3_soz_{i:02d}"
        orig3 = soz3_map[qid3]
        q3 = qmap[qid3]
        for k in ["questionText", "options", "correctAnswer", "suggestedSolution", "quickTip", "topicTitle", "category", "sharedContext", "isGroupQuestion", "groupId"]:
            if k in orig3:
                if k == "options" and isinstance(orig3[k], dict):
                    q3[k] = [{"key": ok, "text": ov} for ok, ov in orig3[k].items()]
                else:
                    q3[k] = orig3[k]

    # =========================================================================
    # 2. STRIP POLLUTED MATH SVGS FROM ALL 150 SÖZEL QUESTIONS
    # =========================================================================
    for q in questions:
        if any(tag in q["id"] for tag in ["_turkce_", "_mantik_", "_soz_"]):
            clear_svg(q)

    # =========================================================================
    # 3. NORMALIZE DICT sharedContext & GROUP METADATA ON ALES2 & ALES3 SÖZEL
    # =========================================================================
    ales2_soz_groups = [(29,30), (31,32), (33,35), (36,38), (39,42), (43,46), (47,50)]
    ales3_soz_groups = [(29,30), (31,32), (33,35), (36,38), (39,42), (43,46), (47,50)]

    for prefix, grp_list, src_map in [
        ("2021_ales2_soz", ales2_soz_groups, soz2_map),
        ("2021_ales3_soz", ales3_soz_groups, soz3_map)
    ]:
        for start, end in grp_list:
            total = end - start + 1
            gid = f"{prefix}_{start}_{end}"
            orig_first = src_map[f"{prefix}_{start:02d}"]
            sc_raw = orig_first.get("sharedContext")
            if isinstance(sc_raw, dict):
                header = sc_raw.get("title") or f"{start} - {end}. soruları aşağıdaki parçaya/bilgilere göre cevaplayınız."
                content = sc_raw.get("content", "")
            else:
                header = orig_first.get("groupHeader") or f"{start} - {end}. soruları aşağıdaki parçaya/bilgilere göre cevaplayınız."
                content = sc_raw or ""
            for idx, qnum in enumerate(range(start, end + 1), 1):
                q = qmap[f"{prefix}_{qnum:02d}"]
                set_group(q, gid, header, idx, total, content)
                if "groupPosition" in q:
                    del q["groupPosition"]

    # =========================================================================
    # 4. REPLACE THE 12 SYNTHETIC 2021-ALES/1 SÖZEL QUESTIONS WITH VERBATIM PDF
    # =========================================================================
    # Q04
    q04 = qmap["2021_ales1_turkce_04"]
    q04["questionText"] = (
        "Çalışma hayatına dâhil edilen çocuklar oyun oynama, öğrenme, hayal kurma ve dinlenme gibi temel "
        "ihtiyaçlardan mahrum bırakılmaktadır. Çalışan çocuklar, çocukluklarını yaşayamamanın ötesinde ağır "
        "ve sağlıksız çalışma koşulları nedeniyle bedensel, ruhsal ve sosyal anlamda zarar görme tehlikesiyle karşı "
        "karşıya kalmaktadır. Aslında hemen hemen her evde belirli bir yaşın üzerindeki çocuklar ev işlerinde çalışırlar. "
        "Bu çalışma kimi zaman küçük bir kardeşin bakımı veya evin derlenip toparlanması, kimi zaman da tarla ve "
        "bahçe işlerine yardım etme şeklinde olabilir. Bunlar genellikle yarı zamanlı, belirli bir zamanlaması "
        "olmayan, o andaki ihtiyaca göre şekillenen geçici işlerdir. ----.\n\n"
        "**Bu parçanın sonuna düşüncenin akışına göre aşağıdakilerden hangisi getirilmelidir?**"
    )
    q04["options"] = make_opts([
        "Daha çok gelişmemiş ülkelerde rastlanan çocuk çalışanlar, bu tür işlerin yanı sıra düşük bir ücret karşılığında satış elemanı veya kasiyer olarak da çalıştırılmaktadır",
        "Oysa çalışan çocuk kavramı ile çocuğun kendi evinin dışında başkasının işinde veya kendi ailesinin işinde üretime doğrudan katkı sağlayacak şekilde çalışması kastedilmektedir",
        "Ayrıca çocukların ağır sanayide çalıştırılması da bu kapsamda olup bu türden çalışma, ülkelerin büyük çoğunluğunda yasal denetim sahasının dışında kalmaktadır",
        "Buna karşın özellikle tehlikeli koşullar altında çalışan çocuklar, ekonomik etkinlik içinde yer alan çocuklardan farklı bir biçimde tanımlanmaktadır",
        "Bu koşullarda zorla çalıştırıldıkları işlerden aile içi işlere kadar değişik konumlarda çalışmaya devam eden çocuklar, ekonomik etkinlik içinde yer almaktadır"
    ])
    q04["correctAnswer"] = "B"
    q04["suggestedSolution"] = (
        "Parçada önce çalışan çocukların maruz kaldığı ağır koşullar belirtilmiş, ardından ev içinde yapılan "
        "geçici yardımların bundan farkı açıklanmıştır. Bu ayrımı netleştiren ifade **B** seçeneğindeki "
        "*'Oysa çalışan çocuk kavramı ile çocuğun kendi evinin dışında başkasının işinde veya kendi ailesinin işinde üretime doğrudan katkı sağlayacak şekilde çalışması kastedilmektedir'* cümlesidir."
    )

    # Q05
    q05 = qmap["2021_ales1_turkce_05"]
    q05["questionText"] = (
        "Beyninizin size kızmaması ve kendi bildiğini yapmaması için ona, ne istediğinizi onun anlayacağı dilden, açık bir "
        "biçimde iletmelisiniz. Beyin, ----. Ona \"Hafıza eğitimi alarak hatırlama gücümü artırmalıyım.\" derseniz "
        "beyniniz, \"artırmalıyım\" sözcüğünü kesinlik olmadığı için dikkate almayabilir. Bu nedenle kesin bir dil kullanın ve "
        "aynı cümleyi \"Hafıza eğitimi alarak hatırlama gücümü artıracağım.\" biçiminde söyleyin.\n\n"
        "**Bu parçada boş bırakılan yere düşüncenin akışına göre aşağıdakilerden hangisi getirilmelidir?**"
    )
    q05["options"] = make_opts([
        "gönderilen mesaja kendi fizyolojik durumuna göre karşılık verir",
        "zihinsel performans düzeyine göre anlar ve harekete geçer",
        "netlik içermeyen komutları yerine getirmeme eğilimine sahiptir",
        "doğru iletişim kurulduğu takdirde güçlü bir şekilde çalışır",
        "gelen uyarıcıların niteliğine göre sinir sistemine emirler verir"
    ])
    q05["correctAnswer"] = "C"
    q05["suggestedSolution"] = (
        "Boşluktan sonraki cümlede beynin *'artırmalıyım'* sözcüğünü kesinlik içermediği için dikkate almayabileceği "
        "belirtilmiştir. Dolayısıyla boşluğa **C** seçeneğindeki *'netlik içermeyen komutları yerine getirmeme eğilimine sahiptir'* ifadesi getirilmelidir."
    )

    # Q06
    q06 = qmap["2021_ales1_turkce_06"]
    q06["questionText"] = (
        "Ziya Osman Saba’nın İstanbul’u tüm yönleriyle öne çıkardığı ve öykücülüğümüzün en nadide örneklerinden "
        "olan *Mesut İnsanlar Fotoğrafhanesi* adlı eseri bu şehri en yalın hâliyle görebileceğimiz satırlarla doludur.\n\n"
        "**Bu cümleden kesin olarak çıkarılabilecek yargı aşağıdakilerden hangisidir?**"
    )
    q06["options"] = make_opts([
        "Mesut İnsanlar Fotoğrafhanesi, Ziya Osman Saba’nın İstanbul’u anlattığı öykülerinden oluşmaktadır.",
        "İstanbul’u bütün sadeliğiyle yansıtan ifadelerin yer aldığı Mesut İnsanlar Fotoğrafhanesi edebiyatımızın seçkin eserlerindendir.",
        "Ziya Osman Saba, öykülerinde İstanbul’u tüm sadeliğiyle anlatabilen nadir yazarlarımızdandır.",
        "Ziya Osman Saba’nın Mesut İnsanlar Fotoğrafhanesi adlı eserinde, İstanbul’u sade bir dille anlatan öyküler yer almaktadır.",
        "Mesut İnsanlar Fotoğrafhanesi, Ziya Osman Saba’nın eserleri arasında İstanbul’u anlattığı tek öykü kitabıdır."
    ])
    q06["correctAnswer"] = "B"
    q06["suggestedSolution"] = (
        "Öncül cümlede eserin *'öykücülüğümüzün en nadide örneklerinden olduğu'* (edebiyatımızın seçkin eserlerinden olduğu) "
        "ve *'bu şehri en yalın hâliyle görebileceğimiz satırlarla dolu olduğu'* (İstanbul'u bütün sadeliğiyle yansıtan ifadelerin yer aldığı) "
        "açıkça belirtilmiştir. Bu nedenle kesin olarak çıkarılabilecek yargı **B** seçeneğidir."
    )

    # Q19
    q19 = qmap["2021_ales1_turkce_19"]
    q19["questionText"] = (
        "Arkeoloji, geçmişe ait anlaşılması çaba gerektiren karmaşık detaylara odaklanır. Arkeologların ürettiği bilgi, "
        "zahmetsizce anlaşılabilecek türden bir bilgi olmadığından toplumda karşılık bulmaz. Buradaki "
        "eksikliği müzeler tamamlar. Müzelerde göze hoş görünen, ilgi çekici, ne olduğu anlaşılabilecek heykel, "
        "takı, para gibi buluntular sergilenir. Üstelik bunlar medya aracılığıyla “Arkeologlar şu muhteşem eseri buldu.” "
        "türünden çarpıcı ifadelerle geniş kitlelere duyurulur. <u>Tüm bunlar,</u> arkeolojinin amacına yönelik yanlış bir "
        "algının yerleşmesine yol açar.\n\n"
        "**Bu parçada altı çizili sözle aşağıdakilerden hangisine gönderme yapılmamıştır?**"
    )
    q19["options"] = make_opts([
        "Emek gerektirdiği için arkeolojinin ürettiği asıl bilgiyle ilgilenilmemesine",
        "Arkeolojik bilgilerin detay içermeleri sebebiyle anlaşılmasının kolay olmamasına",
        "Arkeolojik bilginin uygulama ve teşhir alanları olan müzelerde sergilenmesine",
        "Arkeolojinin maddi kazanç sağlayan bir alan olarak değerlendirilmesine",
        "Medyanın arkeolojik bilgiden ziyade ilgi çekici örnekleri ön plana çıkarmasına"
    ])
    q19["correctAnswer"] = "D"
    q19["suggestedSolution"] = (
        "Parçada arkeolojik bilginin karmaşıklığına (B), toplumda karşılık bulmamasına (A), müzelerde buluntuların "
        "sergilenmesine (C) ve medyanın çarpıcı örnekleri öne çıkarmasına (E) değinilmiştir; ancak arkeolojinin "
        "maddi kazanç sağlayan bir alan olarak değerlendirildiğine değinilmemiştir. Doğru cevap **D** seçeneğidir."
    )

    # Q20
    q20 = qmap["2021_ales1_turkce_20"]
    q20["questionText"] = (
        "Zamanın bilinmeyen dönemleri arasından aşıp gelen antik kentler; farklı dönemlerin, kültür ve uygarlıkların "
        "inanış ve yaşayış biçimlerinin tanıklığını yapar. Bu nedenle her uygarlığın kendi öyküsünü yazdığı bir kitap, "
        "kendi resmini yaptığı bir tablo gibidir. Bir antik kent, binlerce yıllık birikimiyle tarih kitabının kapanmış "
        "sayfaları arasındadır ve o sayfalara nelerin yazıldığı tam olarak bilinemez.\n\n"
        "**Bu parçaya göre aşağıdakilerden hangisi antik kentleri nitelemek için kullanılabilir?**"
    )
    q20["options"] = make_opts([
        "Tek boyutlu yalın bir görüntü",
        "Önemini kaybetmiş bir iz",
        "Değişimi yansıtan anlam katmanı",
        "Yok olmaya yüz tutmuş miras",
        "Geçmişin karanlık bir kitabı"
    ])
    q20["correctAnswer"] = "E"
    q20["suggestedSolution"] = (
        "Parçanın son cümlesinde antik kentlerin *'binlerce yıllık birikimiyle tarih kitabının kapanmış sayfaları arasında olduğu ve o sayfalara nelerin yazıldığının tam olarak bilinemeyeceği'* belirtilmiştir. "
        "Tarih kitabının okunamayan/bilinemeyen kapanmış sayfaları olması, antik kentlerin **'Geçmişin karanlık bir kitabı'** olarak nitelenebileceğini gösterir. Doğru cevap **E** seçeneğidir."
    )

    # Q22
    q22 = qmap["2021_ales1_turkce_22"]
    q22["questionText"] = (
        "Ay ve Mars yüzeyine gerçekleştirilmesi planlanan uzun süreli, mürettebatlı uzay seyahatleri için aşılması "
        "gereken çeşitli teknik zorluklar bulunuyor. Örneğin insanların ihtiyacı olan her şeyi Mars’a "
        "göndermek hem teknik hem de finansal açıdan mümkün görünmüyor. Bu nedenle araştırmacılar orada bulunan "
        "malzemelerle bina inşası ve basit araç gereçler üretilmesi gibi konulara pratik çözümler getirmeye "
        "çalışıyorlar. Uzun süreli, mürettebatlı görevler süresince kullanılacak çeşitli aletler ve barınaklar inşa etmek için "
        "güvenilir yapı malzemelerine ihtiyaç duyulması kaçınılmaz oluyor. Bu noktada yerel kaynakların etkin "
        "kullanımının, maliyetleri azaltmaya yardımcı olacağı düşünülüyor.\n\n"
        "**Bu parçadan aşağıdakilerin hangisine ulaşılabilir?**"
    )
    q22["options"] = make_opts([
        "İnsanın yakın gelecekte Dünya dışında bulunan farklı yaşam alanlarına yerleşerek bu alanlara kolaylıkla uyum sağlamasının mümkün olduğuna",
        "Günümüzdeki teknolojik olanaklarla Mars’a ancak kısa süreli seyahatlerin yapılabilmesi için gerekli alt yapı çalışmalarının tamamlandığına",
        "Yüksek maliyet ve teknolojik yetersizlikler aşıldığında Ay ve Mars dışında da insan yaşamına uygun yaşam alanları oluşturulabileceğine",
        "Mars’ta insan yaşamına uygun temel gereksinimlerin sağlanmasının yüksek maliyetler ve iş gücü gerektirdiği için çalışmaların yavaş ilerlediğine",
        "Mars’ta bulunan olanakları değerlendirerek görevli mürettebata uygun bir yaşam alanı oluşturabilmek için ek çalışmalar yapılması gerektiğine"
    ])
    q22["correctAnswer"] = "E"
    q22["suggestedSolution"] = (
        "Parçada araştırmacıların Mars'ta bulunan yerel malzemelerle bina inşası ve basit araç gereçler üretilmesi gibi "
        "konulara pratik çözümler getirmeye çalıştıkları ve güvenilir yapı malzemelerine ihtiyaç duyulduğu belirtilmektedir. "
        "Buradan **E** seçeneğine ulaşılır."
    )

    # Q29 - Q30 Group
    sc_29_30 = (
        "Hayal gücünün sınırları ne kadar zorlanırsa zorlansın fantastik edebiyatın nesne ve varlıkları en nihayetinde "
        "yaşadığımız dünyadandır. Tarih boyunca hemen her kültürden insan; pegasuslar, ejderhalar, uçan halılar, "
        "sihirli lambalar gibi dünyada olmayan sayısız şey hayal eder ve bunu yazı aracılığıyla bize aktarır. Ancak "
        "sonuçta hayal edilenler bu dünyada olmasa da hiç olmayan unsurlardan oluşmuş şeyler değildir. Çünkü "
        "hayal ettiklerimizin büyük bir kısmını, hatta tamamını, bu dünyada var olan şeylerle oluştururuz. Sadece onları bu "
        "dünyada olmayan bir düzen içinde bir araya getiririz. Atlara kanat takarken, uçan devasa sürüngenlere ateş "
        "püskürttürürken yaptığımız gibi. Dolayısıyla hayal gücümüz bu dünyada olmayanı bile bu dünyadan "
        "hareketle yaratır."
    )
    hdr_29_30 = "29 - 30. soruları aşağıdaki parçaya göre cevaplayınız."
    q29 = qmap["2021_ales1_turkce_29"]
    set_group(q29, "2021_ales1_turkce_29_30", hdr_29_30, 1, 2, sc_29_30)
    q29["questionText"] = "**Bu parçaya göre fantastik edebiyatta hayal edilen varlık ve nesnelerin bu dünyada var olanlarla sınırlı olmasının nedeni aşağıdakilerden hangisidir?**"
    q29["options"] = make_opts([
        "İfade ve anlatım imkânlarının kısıtlı olması",
        "Gerçeklik algısının değişkenlik göstermesi",
        "Dil ve düşünce ilişkisinin göz ardı edilmesi",
        "Hayallerin gerçeklerden beslenmesi",
        "Okur beklentilerinin önemsenmesi"
    ])
    q29["correctAnswer"] = "D"
    q29["suggestedSolution"] = (
        "Parçada *'hayal gücümüz bu dünyada olmayanı bile bu dünyadan hareketle yaratır'* denilerek fantastik unsurların "
        "bu dünyada var olanlarla sınırlı olmasının nedeninin **hayallerin gerçeklerden beslenmesi** (D) olduğu vurgulanmıştır."
    )

    q30 = qmap["2021_ales1_turkce_30"]
    set_group(q30, "2021_ales1_turkce_29_30", hdr_29_30, 2, 2, sc_29_30)
    q30["questionText"] = "**Bu parçada aşağıdakilerden hangisine değinilmemiştir?**"
    q30["options"] = make_opts([
        "Fantastik yazında, anlatımı etkili kılmak için tezat ve ironi gibi dilsel araçlardan yararlanıldığına",
        "Farklı toplumlardaki insanların yaşamlarında var olmayan canlı ve cansız varlıklar hayal ettiğine",
        "Fantastik yaratımlarda, aslında bu dünyaya ait unsurların sıra dışı bir şekilde bir araya getirildiğine",
        "Gerçekte var olmayan nesne ve varlıklara yer verilen yazınsal ürünlerin eski çağlardan beri var olduğuna",
        "Gerçeklikten bütünüyle bağımsız ve her yönüyle yeni bir şey hayal etmenin imkânsız olduğuna"
    ])
    q30["correctAnswer"] = "A"
    q30["suggestedSolution"] = (
        "Parçada B, C, D ve E seçeneklerindeki yargılara değinilmiş; ancak fantastik yazında tezat ve ironi gibi "
        "dilsel araçlardan yararlanıldığına (**A**) hiçbir şekilde değinilmemiştir."
    )

    # Q31 - Q32 Group
    sc_31_32 = (
        "Geleneksel toplumların mekâna bağlı eylem anlayışında eylemleri tasvir etmek için genelde beden ile zaman ve "
        "mekânı ilişkilendiren organik metaforlara başvurulur. Şöyle ki çatışma burun buruna, kavga göğüs göğüse "
        "yapılır; dostluk kol kola yürür ve değişim adım adım gerçekleşir. Günümüzde ise bu durum, insanın eylem "
        "kapasitesini daha önce erişilemeyen noktalara taşıyan teknolojik bilgi ve araçların devreye girmesiyle akıl "
        "almayacak bir biçimde değişti. Mekân artık işlendi, örgütlendi ve hepsinden de öte insan bedeninin doğal "
        "kısıtlamalarından sıyrıldı. Küresel enformasyon ağının gelişmesiyle önceki mekânlar üzerine bir üçüncü mekân "
        "yani insan dünyasının sibernetik mekânı inşa edildi. Bilgisayar terminallerinin birbirine bağlanmasıyla, burası "
        "ile orası arasındaki ayrım anlamsızlaştı. Bu yeni mekânın temel unsurları mekânsal boyutların ötesine "
        "geçti. İnsanları artık fiziksel engeller veya zamansal uzaklıklar ayıramaz hâle geldi."
    )
    hdr_31_32 = "31 - 32. soruları aşağıdaki parçaya göre cevaplayınız."
    q31 = qmap["2021_ales1_turkce_31"]
    set_group(q31, "2021_ales1_turkce_31_32", hdr_31_32, 1, 2, sc_31_32)
    q31["questionText"] = "**Bu parçada “sibernetik mekân” ile ilgili aşağıdakilerin hangisine değinilmiştir?**"
    q31["options"] = make_opts([
        "İnsanın beden algısını dönüştürdüğüne",
        "Mekânsal mesafe tanımını karmaşıklaştırdığına",
        "Zaman hakkındaki algıyı sürekli kıldığına",
        "Bilişim araçlarının kullanımını yaygınlaştırdığına",
        "Eylemin insan zihniyle ilişkisini ortadan kaldırdığına"
    ])
    q31["correctAnswer"] = "B"
    q31["suggestedSolution"] = (
        "Parçada sibernetik mekânla birlikte *'Bilgisayar terminallerinin birbirine bağlanmasıyla, burası ile orası arasındaki ayrım anlamsızlaştı. Bu yeni mekânın temel unsurları mekânsal boyutların ötesine geçti.'* "
        "denilerek mekânsal mesafe tanımını karmaşıklaştırdığına/dönüştürdüğüne (**B**) değinilmiştir."
    )

    q32 = qmap["2021_ales1_turkce_32"]
    set_group(q32, "2021_ales1_turkce_31_32", hdr_31_32, 2, 2, sc_31_32)
    q32["questionText"] = "**Bu parçada anlatılmak istenen aşağıdakilerden hangisidir?**"
    q32["options"] = make_opts([
        "Teknoloji vasıtasıyla yaşanan zaman-mekân ayrışması insanların imkânlarını genişleterek onları özgürleştirmiştir.",
        "Geçmiş zamanlardaki eylem biçimleri günümüzde teknolojinin gelişmesi ve eylem hızının artmasıyla çeşitlenmiştir.",
        "Zaman ve mekân olgularının yeniden inşası hem küresel enformasyondaki gelişmeler hem de geleneksel toplumların dönüşümüyle gerçekleşmiştir.",
        "Bilgi teknolojilerindeki dönüşümler ve teknolojinin sağladığı eylem hızı tüm dünyada etkili olan yeni bir küresel düzen inşa etmiştir.",
        "Zaman ve mekân arasındaki ilişki günümüzdeki enformatik dönüşümlerle insan zihninden çıkıp yaşam alanında somutlaşmıştır."
    ])
    q32["correctAnswer"] = "A"
    q32["suggestedSolution"] = (
        "Parçada teknolojinin devreye girmesiyle mekânın insan bedeninin doğal kısıtlamalarından sıyrıldığı ve "
        "insanları artık fiziksel engeller veya zamansal uzaklıkların ayıramaz hâle geldiği vurgulanmaktadır. "
        "Bu da **A** seçeneğindeki *'Teknoloji vasıtasıyla yaşanan zaman-mekân ayrışması insanların imkânlarını genişleterek onları özgürleştirmiştir.'* yargısını vermektedir."
    )

    # Q33 - Q35 Group (Walter Mischel)
    sc_33_35 = (
        "Walter Mischel, Trinidad’da kültürel farklılıklar ve kişilik üzerine bir araştırma yürüttü. Araştırmanın amacı "
        "ülkede yaşayan Afrika ve Hindistan kökenli etnik gruplar arasında yaygın kabul gören kişisel farklılıkları tespit "
        "etmekti. Hindistanlılara göre Afrikalılar yaptıklarının sonucunu düşünmeden hareket eden, yarını "
        "hesaplamadan elindeki parayı harcayan kişilerdi. Afrikalılar da Hindistanlıları cimri, fazla kaygılı ve daha "
        "iyi bir gelecek için çalışırken elinde olanın tadını çıkaramayan kişiler olarak tanımlıyordu. Mischel, benzer "
        "bir çalışmayı yaşları 7 ila 9 arasında değişen 35 Afrikalı ve 18 Hindistanlı çocukla da gerçekleştirdi. Deney "
        "günü Mischel, çocuklara birer çikolata uzattı ve bunu almayıp bir hafta beklerlerse daha büyük bir çikolata "
        "alabileceklerini söyledi. Afrikalıların çoğu o gün küçük çikolatayı kabul ederken Hindistanlıların çoğu bir hafta "
        "bekleyip büyük çikolatayı almayı tercih etti. Bu çalışma ayrıca iki grup içinden de yaşça büyük olan, "
        "ebeveynleriyle aynı evi paylaşan, ailesinde saygı gören, maddi manevi ihtiyaçları karşılanabilen ve kendini "
        "güvende hisseden çocukların, zevki erteleme konusunda daha başarılı olduğunu ortaya koydu. "
        "Araştırmalarının sonucunda Mischel, bir arada yaşayan toplulukların birbirlerine dair gözlemlerinin bilimsel "
        "çalışmalarla kanıtlanabilir gerçeklikler olduğunu saptadı ve çalışmasının sonucunda şunları söyledi: Ön yargılar "
        "gerçekten var olan bir durumu ortaya koysa da bu durumun kaynağını bulmaya çalışırken kolaya kaçtığı "
        "için sınıfta kalır. Bu da insanların <u>çok iyi gözlemciler ama berbat yorumcular oldukları</u> anlamına geliyor."
    )
    hdr_33_35 = "33 - 35. soruları aşağıdaki parçaya göre cevaplayınız."
    q33 = qmap["2021_ales1_turkce_33"]
    set_group(q33, "2021_ales1_turkce_33_35", hdr_33_35, 1, 3, sc_33_35)
    q33["questionText"] = "**Bu parçadan aşağıdakilerin hangisine ulaşılabilir?**"
    q33["options"] = make_opts([
        "Zevki erteleme çocuklukta ve aile içinde öğrenilen bir davranış kalıbıdır.",
        "Sıradan insanların gözlemlerini bilimsel bir temele oturtmak mümkündür.",
        "Etnik kimlikler toplumsal ön yargıların yaygınlaşmasında önemli rol oynar.",
        "Ebeveynleriyle aynı evi paylaşan çocuklar, kanaatkâr bireyler olarak yetişir.",
        "Güvenli olmayan bir çevrede büyüyen çocuklar, ön yargıları daha kolay içselleştirir."
    ])
    q33["correctAnswer"] = "B"
    q33["suggestedSolution"] = (
        "Parçada *'Araştırmalarının sonucunda Mischel, bir arada yaşayan toplulukların birbirlerine dair gözlemlerinin bilimsel çalışmalarla kanıtlanabilir gerçeklikler olduğunu saptadı'* "
        "ifadesinden doğrudan **B** seçeneğine (*'Sıradan insanların gözlemlerini bilimsel bir temele oturtmak mümkündür.'*) ulaşılır."
    )

    q34 = qmap["2021_ales1_turkce_34"]
    set_group(q34, "2021_ales1_turkce_33_35", hdr_33_35, 2, 3, sc_33_35)
    q34["questionText"] = "**Bu parçada altı çizili sözle insanlar hakkında anlatılmak istenen aşağıdakilerden hangisidir?**"
    q34["options"] = make_opts([
        "Olguları ayırt etmekte başarılı olsalar da sebeplerini açıklamakta başarısızdırlar.",
        "Başkalarının olumsuz yanlarını kolay fark eder ama kendilerini eleştirmekte zorlanırlar.",
        "Bireysel farklılıkları kolayca ortaya koysalar da toplumsal tutumları açıklayamazlar.",
        "Farklılıkları açıkça belirleyebilir fakat nasıl ortadan kaldırılmaları gerektiğini öngöremezler.",
        "Çevrelerindeki değişiklikleri algılamakta ve başkalarına aktarmakta zorlanırlar."
    ])
    q34["correctAnswer"] = "A"
    q34["suggestedSolution"] = (
        "Parçada *'Ön yargılar gerçekten var olan bir durumu ortaya koysa da bu durumun kaynağını bulmaya çalışırken kolaya kaçtığı için sınıfta kalır. Bu da insanların çok iyi gözlemciler ama berbat yorumcular oldukları anlamına geliyor.'* "
        "denmektedir. Yani insanlar var olan durumu (olguları) tespit etmekte başarılı (iyi gözlemci), ancak bunun kaynağını/sebeplerini açıklamakta başarısızdır (berbat yorumcu). Doğru cevap **A** seçeneğidir."
    )

    q35 = qmap["2021_ales1_turkce_35"]
    set_group(q35, "2021_ales1_turkce_33_35", hdr_33_35, 3, 3, sc_33_35)
    q35["questionText"] = "**Bu parçaya göre aşağıdakilerden hangisi deneye katılan çocukların tercihlerini etkileyen faktörlerden değildir?**"

    # Q36 - Q38 Group (Charlie Chaplin)
    sc_36_38 = (
        "Charlie Chaplin’e özgü güldürme yeteneğinin çıkış noktası, her birimizin yaptığı gibi, katı ama daima yeni "
        "olan, aynı zamanda belirsizlikler ve güçlüklerle dolu bir gündelik hayatın içine paldır küldür dalan bir çocuğun "
        "basitliğidir. Bu yüzden onun komedi gücünün sırrı bedeninde değil, bu bedenin maddi ve toplumsal "
        "dünyayla kurduğu ilişkide yatar. Chaplin’in yarattığı naif, çevik bedenli ama masum ruhlu Şarlo karakteri, "
        "davranışları belirlenmiş insanların ve şeylerin karmaşık ve kusursuzlaşmış evrenine girer. Şarlo’nun fiziksel "
        "esnekliği, jestlerini süratle uyarlama ve dönüştürme kapasitesi; naifliğinin kanıtı ve işareti olan aşırı "
        "beceriksizliğe insani bir doğallık katar. Şarlo, nesnelerle kavgaya girişir ve bunlar gündelik nesnelerdir: bir "
        "şemsiye, bir arkalıklı koltuk, bir motosiklet, bir muz kabuğu... Her daim şaşkın, şeylerin yabancılığı "
        "karşısında daima heyecanlı ve rutinleşmiş sıradan eylemlerde bile her zaman beceriksiz olan Şarlo, bu "
        "bayağı şeyler karşısındaki tutumumuzu gözümüzde sabitler. Böylece durumu şaşkınlık verici, dramatik ve "
        "neşeli hâle getirir. O, aşina olduğumuz dünyaya yabancı biri gibi girerek orada kendi yolunu neşeli hasarlarla "
        "açar. Tam da bu sırada aşina olduğumuz nesneler birdenbire aşina olmadığımız bir şekle bürünür ve bize "
        "aniden yabancılaşır. Aslında amaç bizi rahatsız etmek ve nesneler karşısındaki bizi, bize daha iyi göstermektir."
    )
    hdr_36_38 = "36 - 38. soruları aşağıdaki parçaya göre cevaplayınız."
    for idx, qnum in enumerate([36, 37, 38], 1):
        set_group(qmap[f"2021_ales1_turkce_{qnum:02d}"], "2021_ales1_turkce_36_38", hdr_36_38, idx, 3, sc_36_38)

    # Q39 - Q42 Group (Brene Brown / Toksik Olumluluk)
    sc_39_42 = (
        "Brene Brown’un “Empatik bir cevap, hiçbir zaman en azından ifadesiyle başlamaz.” cümlesi, olumsuz "
        "durumlarda etrafına pozitif dalgalar yayma mecburiyeti hissedenlerin sayısının hızla arttığı günümüzde daha "
        "fazla anlam kazanıyor. İşini kaybeden birinin duymak isteyeceği cümle “En azından daha çok kitap "
        "okuyabileceksin.” değildir. Çünkü kişi olumlanmaktan ziyade duygularının paylaşılmasını ister. Yaşananlara "
        "olumlu tarafından bakmak, elbette iyi ancak kendimizin veya karşımızdakinin yaşadığı olumsuz durumları yok "
        "sayıp sadece olumlu duyguları paylaşmak da empati yoksunu bireylere dönüşmemize yol açıyor. “Toksik "
        "olumluluk” adı verilen bu durum, olumsuz bir ruh hâlindeki kişinin doğal duygusal deneyimini reddetmesi "
        "anlamına geliyor. Toksik olumluluğa göre davranan kişiler; yalnızca kendi olumsuz duygularını bastırmakla "
        "kalmıyor, çevrelerinde sıkıntı içinde olan insanların da kendilerine benzemelerini istiyor. Bu kişilerin etrafa "
        "saçtığı “Her şeye olumlu tarafından bak.” türünden nasihatler, doğal bir duygu durumunu yapay bir şablonla "
        "değiştirmeyi amaçlıyor. Ayrıca bu öneriler, bakış açısını değiştirmekle acının yok olabileceğini ima ederek “Mutlu "
        "hissetmiyorsan sorumlusu sensin.” tenkidini de içeriyor. Bu sığ önerilerin özünde birer Truva atının saklı olduğu "
        "görülüyor. Çünkü kişiye gerçekleştiremeyeceği bu tür tavsiyelerde bulunmak; muhatabına içeriden saldırıyor "
        "ve kişide mutsuzluk, harekete geçememe, değersizlik hissi, olumlu tarafı görememe gibi durumların ortaya "
        "çıkmasına sebep oluyor. Aslında mutsuzlukla baş etmenin birçok yolunun olduğu biliniyor. Örneğin neden "
        "gözyaşı döken canlılar olduğumuzu araştıran bilim insanları, cevabın başkalarıyla daha güçlü bağlar "
        "kurmak isteğimiz olduğunu söylüyor. Yani sadece kendimiz için değil, acımızın çevremizdeki kişilerce "
        "görülmesi için de ağlıyoruz. Bu yüzden acı çekerken empati yoksunu boş cümleler duymak işe yaramıyor. "
        "Gerçek iyileşmeyi sağlayan; anlaşıldığımızı hissettiğimiz, duygularımızın kabul gördüğünü bildiğimiz "
        "ilişkiler içinde olmak."
    )
    hdr_39_42 = "39 - 42. soruları aşağıdaki parçaya göre cevaplayınız."
    for idx, qnum in enumerate([39, 40, 41, 42], 1):
        set_group(qmap[f"2021_ales1_turkce_{qnum:02d}"], "2021_ales1_turkce_39_42", hdr_39_42, idx, 4, sc_39_42)

    # Q43 - Q46 Group (Kütahya, Mersin, Niğde)
    sc_43_46 = qmap["2021_ales1_mantik_43"]["sharedContext"]
    hdr_43_46 = "43 - 46. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız."
    for idx, qnum in enumerate([43, 44, 45, 46], 1):
        set_group(qmap[f"2021_ales1_mantik_{qnum:02d}"], "2021_ales1_mantik_43_46", hdr_43_46, idx, 4, sc_43_46)

    # Q47 - Q50 Group (Kemal, Levent, Melek)
    sc_47_50 = qmap["2021_ales1_mantik_47"]["sharedContext"]
    hdr_47_50 = "47 - 50. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız."
    for idx, qnum in enumerate([47, 48, 49, 50], 1):
        set_group(qmap[f"2021_ales1_mantik_{qnum:02d}"], "2021_ales1_mantik_47_50", hdr_47_50, idx, 4, sc_47_50)

    # =========================================================================
    # 5. ADD UNDERLINES (<u>...</u>) TO TARGET PHRASES IN TURKISH QUESTIONS
    # =========================================================================
    for qid in ["2021_ales2_soz_31", "2021_ales2_soz_32"]:
        qmap[qid]["sharedContext"] = re.sub(
            r"ölesiye\s+hastadır\s+ancak\s+ölemezler\.",
            "<u>ölesiye hastadır ancak ölemezler</u>.",
            qmap[qid]["sharedContext"]
        )
    for qid in ["2021_ales2_soz_33", "2021_ales2_soz_34", "2021_ales2_soz_35"]:
        qmap[qid]["sharedContext"] = re.sub(
            r"Mağdurunu\s+kendi\s+kusurlu\s+ışığında\s+kör\s+eden",
            "<u>Mağdurunu kendi kusurlu ışığında kör eden</u>",
            qmap[qid]["sharedContext"]
        )
    qmap["2021_ales3_soz_20"]["questionText"] = re.sub(
        r"kumaşındaki\s+dokuma\s+hataları\s+giderilerek",
        "<u>kumaşındaki dokuma hataları giderilerek</u>",
        qmap["2021_ales3_soz_20"]["questionText"]
    )
    qmap["2021_ales3_soz_21"]["questionText"] = re.sub(
        r"Yüzyılların\s+yükselttiği\s+kuleye\s+bir\s+taş\s+daha\s+döşemek,\s+insanlığın\s+gelişmesinden\s+habersiz\s+olmak\s+demektir\.",
        "<u>Yüzyılların yükselttiği kuleye bir taş daha döşemek, insanlığın gelişmesinden habersiz olmak demektir.</u>",
        qmap["2021_ales3_soz_21"]["questionText"]
    )
    qmap["2021_ales3_soz_22"]["questionText"] = re.sub(
        r"Madam\s+Bovary,\s+herhangi\s+bir\s+Madam\s+Bovary['’]den\s+daha\s+sahicidir\.",
        "<u>Madam Bovary, herhangi bir Madam Bovary’den daha sahicidir.</u>",
        qmap["2021_ales3_soz_22"]["questionText"]
    )
    for qid in ["2021_ales3_soz_36", "2021_ales3_soz_37", "2021_ales3_soz_38"]:
        qmap[qid]["sharedContext"] = re.sub(
            r"ışığı\s+okurun\s+gözüne\s+çarpacak\s+eğimle",
            "<u>ışığı okurun gözüne çarpacak eğimle</u>",
            qmap[qid]["sharedContext"]
        )

    # =========================================================================
    # 6. FIX 2021-ALES/1 SAYISAL QUESTIONS
    # =========================================================================
    # Q19: wrap set options in $...$
    qmap["2021_ales1_mat_19"]["options"] = make_opts([
        "$\\{\\text{Berna, Ceren}\\}$",
        "$\\{\\text{Ceren, Deniz}\\}$",
        "$\\{\\text{Ahmet, Berna, Ceren}\\}$",
        "$\\{\\text{Berna, Ceren, Deniz}\\}$",
        "$\\{\\text{Ahmet, Berna, Ceren, Deniz}\\}$"
    ])

    # Ensure ALES1 Sayısal Group Questions have full sharedContext and group metadata
    ales1_mat_groups = [
        (23, 24, "2021_ales1_mat_23"),
        (25, 26, "2021_ales1_mat_25"),
        (27, 28, "2021_ales1_mat_27"),
        (29, 31, "2021_ales1_mat_29"),
        (32, 34, "2021_ales1_mat_32"),
        (35, 37, "2021_ales1_mat_35"),
        (38, 40, "2021_ales1_mat_38"),
        (41, 43, "2021_ales1_mat_41"),
    ]
    for start, end, ref_id in ales1_mat_groups:
        sc = qmap[ref_id]["sharedContext"]
        hdr = f"{start} - {end}. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız."
        total = end - start + 1
        for idx, qnum in enumerate(range(start, end + 1), 1):
            set_group(qmap[f"2021_ales1_mat_{qnum:02d}"], f"2021_ales1_mat_{start}_{end}", hdr, idx, total, sc)

    # Q34: show initial pie chart (ales1_q32_pie.svg), not the answer pie chart!
    set_svg(qmap["2021_ales1_mat_34"], "ales1_q32_pie.svg")

    # Q41: fix questionText ("?" column is 10th column, not 8th) and Option E = 17
    q41_1 = qmap["2021_ales1_mat_41"]
    q41_1["questionText"] = (
        "Verilen tabloda 1. satırın 3. sütununda $4$, 2. satırın 4. sütununda $3$, 3. satırın 5. sütununda $8$ ve 4. satırın 6. sütununda $0$ yer almaktadır.\n\n"
        "**Buna göre, “?” işareti ile dolu olan sütundaki sayıların toplamı kaçtır?**"
    )
    q41_1["options"] = make_opts(["21", "20", "19", "18", "17"])
    q41_1["correctAnswer"] = "E"
    q41_1["suggestedSolution"] = (
        "Her satırda soldan sağa doğru birer artan (9'dan sonra 0'a dönen) ardışık rakamlar yazılmaktadır. '?' işaretli sütun **10. sütundur**:\n\n"
        "• **1. satır:** 3. sütun $4$ ise 10. sütun $(4 + 7) \\bmod 10 = 1$'dir.\n"
        "• **2. satır:** 4. sütun $3$ ise 10. sütun $(3 + 6) \\bmod 10 = 9$'dur.\n"
        "• **3. satır:** 5. sütun $8$ ise 10. sütun $(8 + 5) \\bmod 10 = 3$'tür.\n"
        "• **4. satır:** 6. sütun $0$ ise 10. sütun $(0 + 4) \\bmod 10 = 4$'tür.\n\n"
        "O hâlde '?' işaretli sütundaki sayıların toplamı $1 + 9 + 3 + 4 = 17$ bulunur. Doğru cevap **E** seçeneğidir."
    )

    # Q47: restore official ALES1 Q47 matching geo_dikdortgen_oran_q47.svg
    q47_1 = qmap["2021_ales1_mat_47"]
    q47_1["questionText"] = (
        "$ABCD$ dikdörtgen\n"
        "* $|AE| = |EB|$\n"
        "* $\\frac{|DG|}{|GC|} = \\frac{|CF|}{|FB|} = \\frac{2}{3}$\n\n"
        "Şekilde $E, F$ ve $G$ noktaları $ABCD$ dikdörtgeninin kenarları üzerindedir.\n\n"
        "**Buna göre, $EFCG$ dörtgeninin alanının $ABCD$ dikdörtgeninin alanına oranı kaçtır?**"
    )
    q47_1["options"] = make_opts(["$\\frac{2}{5}$", "$\\frac{4}{5}$", "$\\frac{2}{3}$", "$\\frac{1}{3}$", "$\\frac{1}{2}$"])
    q47_1["correctAnswer"] = "A"
    q47_1["suggestedSolution"] = (
        "Dikdörtgenin kenar uzunluklarını oranlara uygun seçelim:\n"
        "$|DC| = |AB| = 10$ birim ve $|BC| = |AD| = 5$ birim olsun. Bu durumda:\n"
        "$$\\text{Alan}(ABCD) = 10 \\times 5 = 50\\text{ birimkare}$$\n"
        "• $|AE| = |EB| = 5$ birim,\n"
        "• $\\frac{|DG|}{|GC|} = \\frac{2}{3} \\implies |DG| = 4$ birim, $|GC| = 6$ birim,\n"
        "• $\\frac{|CF|}{|FB|} = \\frac{2}{3} \\implies |CF| = 2$ birim, $|FB| = 3$ birim.\n\n"
        "$[EC]$ köşegenini çizersek $EFCG$ dörtgeni, $EGC$ ve $ECF$ üçgenlerine ayrılır:\n"
        "• $\\text{Alan}(EGC) = \\frac{|GC| \\cdot |AD|}{2} = \\frac{6 \\cdot 5}{2} = 15$ birimkare,\n"
        "• $\\text{Alan}(ECF) = \\frac{|CF| \\cdot |EB|}{2} = \\frac{2 \\cdot 5}{2} = 5$ birimkare.\n\n"
        "Buradan $\\text{Alan}(EFCG) = 15 + 5 = 20$ birimkare olur ve istenen oran:\n"
        "$$\\frac{\\text{Alan}(EFCG)}{\\text{Alan}(ABCD)} = \\frac{20}{50} = \\frac{2}{5}$$\n"
        "bulunur. Doğru cevap **A** seçeneğidir."
    )
    set_svg(q47_1, "geo_dikdortgen_oran_q47.svg")

    # Q48: restore official ALES1 Q48 matching geo_cember_yarim_q48.svg
    q48_1 = qmap["2021_ales1_mat_48"]
    q48_1["questionText"] = (
        "* $D \\in [AC]$\n"
        "* $|AD| = 14\\text{ birim}$\n"
        "* $|DC| = 2\\text{ birim}$\n"
        "* $|AO| = 10\\text{ birim}$\n"
        "* $|OD| = x$\n\n"
        "$C$ noktası, $O$ merkezli yarım çemberin üzerindedir.\n\n"
        "**Buna göre, $x$ kaç birimdir?**"
    )
    q48_1["options"] = make_opts(["6", "8", "$6\\sqrt{2}$", "$8\\sqrt{2}$", "$6\\sqrt{3}$"])
    q48_1["correctAnswer"] = "C"
    q48_1["suggestedSolution"] = (
        "$O$ merkezli yarım çemberin yarıçapı $|AO| = |OC| = 10$ birimdir.\n"
        "$AOC$ üçgeninde $|AC| = |AD| + |DC| = 14 + 2 = 16$ birim ve $|AO| = |OC| = 10$ birim olduğundan $AOC$ ikizkenar üçgendir.\n"
        "$O$ merkezinden $[AC]$ kirişine dikme indirirsek ($OH \\perp AC$), kirişi iki eş parçaya böler:\n"
        "$$|AH| = |HC| = \\frac{16}{2} = 8\\text{ birim}$$\n"
        "$OHC$ dik üçgeninde Pisagor bağıntısından $|OH| = \\sqrt{10^2 - 8^2} = 6$ birimdir.\n"
        "Ayrıca $|HD| = |HC| - |DC| = 8 - 2 = 6$ birim olduğundan, $OHD$ ikizkenar dik üçgeninde:\n"
        "$$x = |OD| = \\sqrt{|OH|^2 + |HD|^2} = \\sqrt{6^2 + 6^2} = 6\\sqrt{2}\\text{ birim}$$\n"
        "bulunur. Doğru cevap **C** seçeneğidir."
    )
    set_svg(q48_1, "geo_cember_yarim_q48.svg")

    # =========================================================================
    # 7. FIX 2021-ALES/2 SAYISAL QUESTIONS
    # =========================================================================
    qmap["2021_ales2_mat_01"]["options"] = make_opts(["$\\frac{5}{3}$", "$\\frac{4}{3}$", "$\\frac{3}{2}$", "2", "3"])
    qmap["2021_ales2_mat_03"]["options"] = make_opts(["$\\sqrt{2}$", "$\\sqrt{3}$", "$\\sqrt{6}$", "$3\\sqrt{2}$", "$2\\sqrt{3}$"])
    qmap["2021_ales2_mat_09"]["options"] = make_opts(["$A + B + C$", "$AB + BA$", "$BC \\cdot AB$", "$AB + BC \\cdot AC$", "$A \\cdot B + C$"])
    qmap["2021_ales2_mat_09"]["suggestedSolution"] = (
        "İki basamaklı $AB, AC, BA, BC, CA, CB$ doğal sayılarından 2 tanesi tek, 4 tanesi çift sayı ise $A, B, C$ rakamlarından **biri tek, ikisi çift** rakamdır.\n\n"
        "İki rakam çift olduğundan $B$ ve $C$ rakamlarından en az biri kesinlikle çifttir. Dolayısıyla birler basamakları $C$ ve $B$ olan iki basamaklı $BC$ ve $AB$ sayılarından en az biri çift sayıdır.\n"
        "Çift bir tam sayı ile herhangi bir tam sayının çarpımı daima çift olduğundan **$BC \\cdot AB$** çarpımı her zaman çift sayıdır. Doğru cevap **C** seçeneğidir."
    )

    # ALES2 Q20 (Pie chart)
    q20_2 = qmap["2021_ales2_mat_20"]
    set_svg(q20_2, "ales2_q20_pie.svg")
    q20_2["options"] = make_opts([
        "Analiz: $160^\\circ$, Cebir: $80^\\circ$, Geometri: $120^\\circ$",
        "Analiz: $90^\\circ$, Cebir: $90^\\circ$, Geometri: $180^\\circ$",
        "Analiz: $210^\\circ$, Cebir: $60^\\circ$, Geometri: $90^\\circ$",
        "Analiz: $150^\\circ$, Cebir: $90^\\circ$, Geometri: $120^\\circ$",
        "Analiz: $120^\\circ$, Cebir: $120^\\circ$, Geometri: $120^\\circ$"
    ])
    q20_2["correctAnswer"] = "B"
    q20_2["suggestedSolution"] = (
        "• **Şekil 1 (Tüm Dersler):** Analiz $= 144^\\circ$, Geometri $= 144^\\circ$ ve Cebir $= 360^\\circ - 288^\\circ = 72^\\circ$'dir. Açılar $72^\\circ$ ile sadeleştirilirse toplam ders sayıları Analiz $= 4k$, Geometri $= 4k$, Cebir $= 2k$ (Toplam $10k$) alınabilir.\n"
        "• Geometri alanında açılan zorunlu ders sayısı seçmeli ders sayısına eşit olduğundan, toplam $4k$ Geometri dersinin $2k$'si **zorunlu**, $2k$'si **seçmeli** derstir.\n"
        "• **Şekil 2 (Zorunlu Dersler):** Geometri $= 120^\\circ$, Cebir $= 60^\\circ$, Analiz $= 180^\\circ$'dir. Zorunlu Geometri ($120^\\circ$) $= 2k$ ise, zorunlu Cebir ($60^\\circ$) $= 1k$ ve zorunlu Analiz ($180^\\circ$) $= 3k$ olur.\n"
        "• **Seçmeli Ders Sayıları:**\n"
        "  - Seçmeli Analiz $= 4k - 3k = 1k$\n"
        "  - Seçmeli Cebir $= 2k - 1k = 1k$\n"
        "  - Seçmeli Geometri $= 4k - 2k = 2k$\n"
        "Toplam $4k$ seçmeli ders daire grafiğinde ($360^\\circ$) gösterildiğinde: Analiz $= 90^\\circ$, Cebir $= 90^\\circ$, Geometri $= 180^\\circ$ olur. Doğru cevap **B** seçeneğidir."
    )

    # ALES2 Sayısal Group Questions (23..43)
    sc_23_24_2 = (
        "Bir yemek yarışmasında, yarışmacıların tamamı ile iki takım oluşturulmuştur. Her bir yarışmacının sadece bir takımda yer aldığı bu yarışmayla ilgili aşağıdakiler bilinmektedir:\n"
        "• 1. takımdaki kadın yarışmacıların sayısı, 1. takımdaki erkek yarışmacıların sayısından 8 fazladır.\n"
        "• 2. takımdaki kadın yarışmacıların sayısı, 2. takımdaki erkek yarışmacıların sayısının 3 katına eşittir.\n"
        "• Yarışmadaki kadın yarışmacıların toplam sayısı, erkek yarışmacıların toplam sayısının 2 katına eşittir."
    )
    set_group(qmap["2021_ales2_mat_23"], "2021_ales2_mat_23_24", "23 - 24. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", 1, 2, sc_23_24_2)
    qmap["2021_ales2_mat_23"]["questionText"] = "Her bir takımda bulunan toplam yarışmacı sayısının birbirine eşit olduğu biliniyor.\n\n**Buna göre, 2. takımdaki kadın yarışmacı sayısı kaçtır?**"
    set_group(qmap["2021_ales2_mat_24"], "2021_ales2_mat_23_24", "23 - 24. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", 2, 2, sc_23_24_2)
    qmap["2021_ales2_mat_24"]["questionText"] = "1. takımdaki erkek yarışmacı sayısının 15 olduğu biliniyor.\n\n**Buna göre, yarışmadaki toplam yarışmacı sayısı kaçtır?**"

    sc_25_26_2 = (
        "Bir okuldaki öğrencilere meslek tercihleri ile ilgili bir anket uygulanmıştır. A, B, C, D ve E olmak üzere beş farklı meslek adının yer aldığı bu ankete katılan her bir öğrenci; bu beş meslekten bir tanesini tercih ettiği meslek, başka bir tanesini de tercih etmediği meslek olarak işaretlemiştir. Anket sonuçlarına göre, bu beş meslekten her birini tercih eden ve tercih etmeyen öğrenci sayıları aşağıdaki sütun grafiğinde gösterilmiştir."
    )
    for idx, qnum in enumerate([25, 26], 1):
        q = qmap[f"2021_ales2_mat_{qnum:02d}"]
        set_group(q, "2021_ales2_mat_25_26", "25 - 26. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", idx, 2, sc_25_26_2)
        set_svg(q, "ales2_q25_barchart.svg")
    qmap["2021_ales2_mat_25"]["questionText"] = (
        "Bu ankete toplam 125 öğrenci katılmış ve A mesleğini 16, D mesleğini ise 24 öğrenci tercih etmiştir.\n\n"
        "**Buna göre, B mesleğini tercih etmeyen öğrenci sayısı kaçtır?**"
    )
    qmap["2021_ales2_mat_25"]["suggestedSolution"] = (
        "Sütun grafiğindeki kesikli kılavuz çizgilerine göre:\n"
        "• A ve B mesleklerini tercih eden öğrenci sayıları birbirine eşittir: $\\text{A}_{\\text{tercih}} = \\text{B}_{\\text{tercih}} = 16$.\n"
        "• C ve D mesleklerini tercih eden öğrenci sayıları birbirine eşittir: $\\text{C}_{\\text{tercih}} = \\text{D}_{\\text{tercih}} = 24$.\n"
        "• Toplam 125 öğrenci katıldığına göre E mesleğini tercih eden öğrenci sayısı:\n"
        "$$\\text{E}_{\\text{tercih}} = 125 - (16 + 16 + 24 + 24) = 125 - 80 = 45$$\n"
        "• Grafikte B mesleğini tercih etmeyenlerin sütunu ile E mesleğini tercih edenlerin sütunu aynı kılavuz çizgisinde (eşit boyda) olduğundan, B mesleğini tercih etmeyen öğrenci sayısı **45**'tir. Doğru cevap **C** seçeneğidir."
    )
    qmap["2021_ales2_mat_26"]["questionText"] = (
        "Ankete katılan öğrencilerden C mesleğini tercih eden öğrenci sayısı 30, tercih etmeyen öğrenci sayısı ise 25’tir.\n\n"
        "**A mesleğini tercih etmeyen öğrenci sayısı, E mesleğini tercih etmeyen öğrenci sayısından 35 fazla olduğuna göre, E mesleğini tercih etmeyen öğrenci sayısı kaçtır?**"
    )
    qmap["2021_ales2_mat_26"]["suggestedSolution"] = (
        "Grafikteki kesikli kılavuz çizgilerine göre:\n"
        "• 2. çizgi seviyesi $= \\text{C}_{\\text{etmeyen}} = \\text{A}_{\\text{eden}} = \\text{B}_{\\text{eden}} = 25$.\n"
        "• 3. çizgi seviyesi $= \\text{C}_{\\text{eden}} = \\text{D}_{\\text{eden}} = \\text{D}_{\\text{etmeyen}} = 30$.\n"
        "• 5. çizgi seviyesi $= \\text{B}_{\\text{etmeyen}} = \\text{E}_{\\text{eden}} = m$ diyelim.\n"
        "Her öğrenci bir tercih edilen, bir de tercih edilmeyen meslek işaretlediğinden toplam tercih edilen sayısı toplam tercih edilmeyen sayısına eşittir:\n"
        "$$25 + 25 + 30 + 30 + m = \\text{A}_{\\text{etmeyen}} + m + 25 + 30 + \\text{E}_{\\text{etmeyen}}$$\n"
        "$$110 = 55 + \\text{A}_{\\text{etmeyen}} + \\text{E}_{\\text{etmeyen}} \\implies \\text{A}_{\\text{etmeyen}} + \\text{E}_{\\text{etmeyen}} = 55$$\n"
        "Soruda $\\text{A}_{\\text{etmeyen}} - \\text{E}_{\\text{etmeyen}} = 35$ verildiğinden:\n"
        "$$2 \\cdot \\text{E}_{\\text{etmeyen}} = 55 - 35 = 20 \\implies \\text{E}_{\\text{etmeyen}} = 10$$\n"
        "bulunur. Doğru cevap **A** seçeneğidir."
    )

    sc_27_28_2 = (
        "Düzenekte bulunan beş tane daire ve altı tane karenin her birine bir tane sayı yazılacaktır. "
        "Dairelere 1’den 5’e kadar olan rakamlar her daireye farklı bir rakam gelecek şekilde yerleştirildikten sonra "
        "her bir kareye, bu kareye doğru parçası ile bağlı iki dairedeki sayıların farkının mutlak değeri yazılacaktır."
    )
    set_group(qmap["2021_ales2_mat_27"], "2021_ales2_mat_27_28", "27 - 28. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", 1, 2, sc_27_28_2)
    qmap["2021_ales2_mat_27"]["questionText"] = "**Yukarıdaki şekle göre, $a + b$ toplamı kaçtır?**"
    set_group(qmap["2021_ales2_mat_28"], "2021_ales2_mat_27_28", "27 - 28. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", 2, 2, sc_27_28_2)
    qmap["2021_ales2_mat_28"]["questionText"] = "**Yukarıdaki şekle göre, $x + y + z$ toplamı kaçtır?**"

    sc_29_31_2 = (
        "Başlangıçta sıcak su haznesindeki su miktarı, dem haznesindeki dem miktarının 2 katı olan bir çay makinesinde "
        "“açık çay”, “normal çay” ve “koyu çay” olmak üzere sadece üç seçenek bulunmaktadır. "
        "Bu makine, her bardağa sıcak su ve dem miktarının toplamı 100 mililitre olacak biçimde açık çay için 10, "
        "normal çay için 25, koyu çay için ise 40 mililitre dem ekleyip bardağın geri kalanını sıcak su ile doldurmaktadır."
    )
    for idx, qnum in enumerate([29, 30, 31], 1):
        set_group(qmap[f"2021_ales2_mat_{qnum:02d}"], "2021_ales2_mat_29_31", "29 - 31. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", idx, 3, sc_29_31_2)
    qmap["2021_ales2_mat_29"]["questionText"] = "Bu makine 2 bardak açık, 4 bardak normal ve 1 bardak koyu çayı tam olarak doldurduktan sonra sıcak su haznesinde 350 mililitre su kalmıştır.\n\n**Buna göre, başlangıçta makinenin sıcak su haznesinde kaç mililitre su bulunmaktadır?**"
    qmap["2021_ales2_mat_30"]["questionText"] = "Bu makine belirli sayıda bardağı tam olarak doldurduktan sonra haznelerde su ve dem kalmamıştır.\n\n**Buna göre, makinenin doldurduğu toplam bardak sayısı en az kaçtır?**"
    qmap["2021_ales2_mat_31"]["questionText"] = "Bu makine 4 bardak açık, 6 bardak normal ve birkaç bardak koyu çayı tam olarak doldurduktan sonra sıcak su haznesinde su kalmamış, dem haznesinde ise 5 mililitre dem kalmıştır.\n\n**Buna göre, makine kaç bardak koyu çay doldurmuştur?**"

    sc_32_34_2 = (
        "Beş arkadaşın; içinde belirli sayıda top bulunan bir kutudan sırayla top alarak oynayacakları oyunun kuralları aşağıda verilmiştir:\n"
        "• Oyuna Ali başlayacak, Ali’den sonra sırasıyla Buse, Can, Deniz ve Elif kutudan top alacaktır, Elif’ten sonra sıra tekrar Ali’ye geçecek ve oyun sırası aynı şekilde devam edecektir.\n"
        "• Her bir oyuncu sıra kendisine her geldiğinde kutudan 1, 2 veya 3 top alacaktır.\n"
        "• İlk oyuncudan sonra sırası gelen her bir oyuncu, kendisinden bir önceki oyuncunun aldığı top sayısından farklı sayıda top alacaktır.\n"
        "Sıradaki oyuncu verilen kurallara göre kutudan top alamadığında oyun bitecek ve kutudan en son top alan oyuncu oyunu kazanacaktır."
    )
    for idx, qnum in enumerate([32, 33, 34], 1):
        set_group(qmap[f"2021_ales2_mat_{qnum:02d}"], "2021_ales2_mat_32_34", "32 - 34. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", idx, 3, sc_32_34_2)
    qmap["2021_ales2_mat_32"]["questionText"] = "Başlangıçta kutuda 30 top vardır ve sıra kendisine her geldiğinde Ali 1, Can 3, Deniz ise 2 top almıştır.\n\n**Buna göre, Buse ve Elif oyun boyunca kutudan toplam kaç top almıştır?**"
    qmap["2021_ales2_mat_33"]["questionText"] = "Oyun boyunca, hem Buse hem de Can kendisinden bir önceki sıradaki oyuncudan 1 fazla, Elif ise kendisinden bir önceki sıradaki oyuncudan 2 fazla sayıda top almıştır.\n\n**Başlangıçta kutuda 23 top olduğuna göre, oyunu hangi oyuncu kazanır?**"
    qmap["2021_ales2_mat_34"]["questionText"] = "**Başlangıçta kutuda 9 top olduğuna göre, bu oyunun kazananı kaç farklı kişi olabilir?**"

    sc_35_37_2 = (
        "Kare, daire ve üçgen şeklinde üç tür cisim ile eşit kollu teraziler verilmiştir. "
        "Her türden yeterli sayıda cisim bulunmaktadır ve aynı tür cisimlerin ağırlıkları birbirine eşittir."
    )
    for idx, qnum in enumerate([35, 36, 37], 1):
        q = qmap[f"2021_ales2_mat_{qnum:02d}"]
        set_group(q, "2021_ales2_mat_35_37", "35 - 37. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", idx, 3, sc_35_37_2)
        set_svg(q, f"ales2_q{qnum}_scale.svg")
    qmap["2021_ales2_mat_35"]["questionText"] = (
        "Yukarıdaki eşit kollu terazide cisimler şekilde gösterilen sayılarda olup terazi dengededir.\n\n"
        "**Bir daire cismin ağırlığı 5 kilogram olduğuna göre, bir kare cisim ile bir üçgen cismin ağırlıkları toplamı kaç kilogramdır?**"
    )
    qmap["2021_ales2_mat_35"]["suggestedSolution"] = (
        "Terazinin sol kefesinde $1$ kare, $1$ daire ve $2$ üçgen; sağ kefesinde ise $1$ üçgen ve $4$ daire bulunmaktadır.\n"
        "Terazi dengede olduğuna göre:\n"
        "$$K + D + 2\\ddot{U} = \\ddot{U} + 4D \\implies K + \\ddot{U} = 3D$$\n"
        "Bir dairenin ağırlığı $D = 5$ kg olduğundan:\n"
        "$$K + \\ddot{U} = 3 \\times 5 = 15\\text{ kg}$$\n"
        "bulunur. Doğru cevap **A** seçeneğidir."
    )
    qmap["2021_ales2_mat_36"]["questionText"] = (
        "Yukarıdaki eşit kollu terazilerde cisimler şekilde gösterilen sayılarda olup 1. terazi dengede, 2. terazi ise dengede değildir.\n\n"
        "**Bir kare, bir daire ve bir üçgen cismin ağırlıkları sırasıyla $K, D$ ve $\\ddot{U}$ kilogram olduğuna göre, aşağıdaki sıralamalardan hangisi doğrudur?**"
    )
    qmap["2021_ales2_mat_36"]["options"] = make_opts([
        "$K < D < \\ddot{U}$",
        "$K < \\ddot{U} < D$",
        "$\\ddot{U} < K < D$",
        "$\\ddot{U} < D < K$",
        "$D < K < \\ddot{U}$"
    ])
    qmap["2021_ales2_mat_36"]["suggestedSolution"] = (
        "• **2. terazide** sağ kefe daha aşağıda (daha ağır) olduğundan:\n"
        "$$D + 2K + 2\\ddot{U} < 3\\ddot{U} + D \\implies 2K < \\ddot{U} \\implies K < \\ddot{U}$$\n"
        "• **1. terazide** denge olduğundan:\n"
        "$$D + 3K + \\ddot{U} = 2\\ddot{U} + 4D \\implies 3K - 3D = \\ddot{U}$$\n"
        "$\\ddot{U} > 0$ olduğundan $3(K - D) > 0 \\implies D < K$ olur.\n"
        "İki eşitsizlik birleştirildiğinde **$D < K < \\ddot{U}$** elde edilir. Doğru cevap **E** seçeneğidir."
    )
    qmap["2021_ales2_mat_37"]["questionText"] = (
        "Yukarıdaki eşit kollu terazilerde cisimler şekilde gösterilen sayılarda olup her iki terazi de dengededir.\n\n"
        "**Bir kare cismin ağırlığı 9 kilogram olduğuna göre, bir üçgen cismin ağırlığı kaç kilogramdır?**"
    )
    qmap["2021_ales2_mat_37"]["suggestedSolution"] = (
        "• **Birinci terazide** denge durumundan:\n"
        "$$\\ddot{U} + 4D = 3K$$\n"
        "• **İkinci terazide** denge durumundan:\n"
        "$$2\\ddot{U} + K + D = 2K + 2D \\implies 2\\ddot{U} = K + D \\implies D = 2\\ddot{U} - K$$\n"
        "Birinci denklemde $D$ yerine $2\\ddot{U} - K$ yazılırsa:\n"
        "$$\\ddot{U} + 4(2\\ddot{U} - K) = 3K \\implies 9\\ddot{U} = 7K$$\n"
        "$K = 9$ kg verildiğinden $9\\ddot{U} = 7 \\times 9 \\implies \\ddot{U} = 7$ kg bulunur. Doğru cevap **B** seçeneğidir."
    )

    sc_38_40_2 = (
        "Can tahtaya iki basamaklı bir doğal sayı yazdıktan sonra bu sayı\n"
        "• çift ise sayının 11 fazlasını\n"
        "• tek ise sayının rakamlarının yerlerini değiştirdikten sonra elde ettiği sayının 11 fazlasını\n"
        "hesaplayarak tahtaya hesapladığı bu sayıyı yazmıştır. Can tahtaya en son yazdığı her sayı için bu işlemi "
        "uygulamaya devam ederek üç basamaklı bir sayı elde ettiğinde bu sayıyı son sayı olarak yazmıştır.\n"
        "Örneğin Can’ın yazdığı ilk sayı 37 ise ikinci sayı 84, üçüncü sayı 95, dördüncü sayı 70 ve beşinci sayı 81’dir."
    )
    for idx, qnum in enumerate([38, 39, 40], 1):
        set_group(qmap[f"2021_ales2_mat_{qnum:02d}"], "2021_ales2_mat_38_40", "38 - 40. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", idx, 3, sc_38_40_2)
    qmap["2021_ales2_mat_38"]["questionText"] = "**Can’ın tahtaya yazdığı ilk sayı 17 olduğuna göre, altıncı sayı kaçtır?**"
    qmap["2021_ales2_mat_39"]["questionText"] = "**Can’ın tahtaya yazdığı yedinci sayı 99 olduğuna göre, ikinci sayı kaçtır?**"
    qmap["2021_ales2_mat_40"]["questionText"] = (
        "**Can’ın tahtaya yazdığı son sayı,**\n"
        "I. 100\n"
        "II. 101\n"
        "III. 102\n"
        "**sayılarından hangileri olabilir?**"
    )

    sc_41_43_2 = (
        "$3 \\times 4$ boyutlarındaki tablonun hücrelerine 1’den 12’ye kadar olan tam sayılar her bir hücrede farklı bir sayı olacak biçimde yazılacaktır. "
        "Sonra aşağıdaki kurallara göre tablonun boyama işlemi yapılacaktır:\n"
        "• Her bir sütunun ikinci satırındaki sayı, üçüncü satırındaki sayıdan büyük ise bu sütunun ikinci satırındaki hücre maviye boyanacaktır.\n"
        "• Her bir sütunun birinci satırındaki sayı hem ikinci hem de üçüncü satırındaki sayılardan büyük ise bu sütunun birinci satırındaki hücre maviye boyanacaktır.\n"
        "• Diğer durumlarda boyama işlemi yapılmayacaktır."
    )
    for idx, qnum in enumerate([41, 42, 43], 1):
        q = qmap[f"2021_ales2_mat_{qnum:02d}"]
        set_group(q, "2021_ales2_mat_41_43", "41 - 43. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", idx, 3, sc_41_43_2)
        set_svg(q, f"ales2_q{qnum}_table.svg")
    qmap["2021_ales2_mat_41"]["questionText"] = "Yukarıdaki tablonun boyama işlemi tamamlanmıştır.\n\n**Buna göre, $a + b + c + d$ toplamı kaçtır?**"
    qmap["2021_ales2_mat_41"]["suggestedSolution"] = (
        "Tabloda 1'den 12'ye kadar olan tam sayılardan $2, 3, 4, 7, 10, 12$ yazılmış olup geriye **$1, 5, 6, 8, 9, 11$** sayıları kalmıştır.\n"
        "• **3. sütun:** 1. satırdaki $c$ hücresi maviye boyandığına göre $c > 10$ ve $c > 3$ olmalıdır. Kalan sayılar içinde $10$'dan büyük tek sayı **$11$** olduğundan **$c = 11$**'dir.\n"
        "• **4. sütun:** 2. satırdaki $2$ hücresi boyanmamış ($2 < 4$), 1. satırdaki $d$ hücresi de boyanmamıştır ($d < 4$). Kalan sayılar içinde $4$'ten küçük tek sayı **$1$** olduğundan **$d = 1$**'dir.\n"
        "• **1. sütun:** 1. satır mavi ($> 7$ ve $> \\text{alt}$), 2. satırdaki $7$ ise beyazdır ($7 < \\text{alt}$). Demek ki 1. sütunun 3. satırı $7$'den büyüktür ve 1. satırı ondan da büyüktür. Kalan $\\{5, 6, 8, 9\\}$ sayılarından $7$'den büyük olanlar $8$ ve $9$'dur (3. satır $= 8$, 1. satır $= 9$).\n"
        "• **2. sütun:** Kalan son iki sayı **$5$ ve $6$**'dır ($a$ ve $b$). Hangi sırada yerleşirse yerleşsin $a + b = 5 + 6 = 11$'dir.\n\n"
        "Sonuç olarak $a + b + c + d = 11 + 11 + 1 = 23$ bulunur. Doğru cevap **B** seçeneğidir."
    )
    qmap["2021_ales2_mat_42"]["questionText"] = "Yukarıdaki tablonun boyama işlemi yapılmamıştır.\n\n**Buna göre, tablonun boyama işlemi tamamlandığında kaç tane hücre maviye boyanmış olur?**"
    qmap["2021_ales2_mat_43"]["questionText"] = "Yukarıdaki tablonun boyama işlemi tamamlanmıştır.\n\n**Buna göre, $x$ kaçtır?**"
    qmap["2021_ales2_mat_43"]["suggestedSolution"] = (
        "Tablodaki 1. ve 2. satırdaki tüm hücreler maviye boyanmıştır. Bu durum her sütunda **1. satır $>$ 2. satır $>$ 3. satır** sıralaması olduğunu gösterir:\n"
        "• **1. sütun:** $\\text{üst} > \\text{orta} > 9$. $10$ sayısı 4. sütunda kullanıldığından 1. sütunun üst ve orta hücrelerine **$12$ ve $11$** gelir.\n"
        "• **2. sütun:** $\\text{üst} > 7 > 2$. $7$'den büyük kalan tek sayı **$8$** olduğundan 2. sütunun 1. satırı **$8$**'dir.\n"
        "• **4. sütun:** $10 > 3 > \\text{alt}$. $2$ sayısı kullanıldığından $3$'ten küçük kalan tek sayı **$1$**'dir.\n"
        "• **3. sütun:** Kullanılmayan son üç sayı **$4, 5, 6$**'dır. $\\text{üst} > x > \\text{alt}$ sıralamasından $6 > 5 > 4$ olur ve **$x = 5$** bulunur. Doğru cevap **B** seçeneğidir."
    )

    qmap["2021_ales2_mat_45"]["options"] = make_opts(["3", "4", "6", "$4\\sqrt{3}$", "$6\\sqrt{3}$"])
    qmap["2021_ales2_mat_46"]["options"] = make_opts(["18", "24", "36", "$16\\sqrt{3}$", "$24\\sqrt{3}$"])

    # =========================================================================
    # 8. FIX 2021-ALES/3 SAYISAL QUESTIONS
    # =========================================================================
    qmap["2021_ales3_mat_01"]["options"] = make_opts(["$\\frac{4}{3}$", "$\\frac{3}{2}$", "$\\frac{5}{2}$", "2", "4"])
    qmap["2021_ales3_mat_03"]["options"] = make_opts(["1", "2", "3", "$2\\sqrt{2}$", "$2\\sqrt{3}$"])

    # Q05: 3AA + B4B = 1CC5
    q05_3 = qmap["2021_ales3_mat_05"]
    q05_3["questionText"] = (
        "$A, B$ ve $C$ sıfırdan farklı birer rakam olmak üzere\n\n"
        "$$\\begin{array}{r} 3AA \\\\ + \\quad B4B \\\\ \\hline 1CC5 \\end{array}$$\n\n"
        "**olduğuna göre, $A + B + C$ toplamı kaçtır?**"
    )
    q05_3["options"] = make_opts(["16", "17", "18", "19", "20"])
    q05_3["correctAnswer"] = "B"
    q05_3["suggestedSolution"] = (
        "Basamak çözümlemesi yapalım:\n"
        "• Birler basamağında $A + B$ toplamının birler basamağı $5$ ve toplam dört basamaklı ($1CC5$) olduğundan $A + B = 15$'tir (elde var $1$).\n"
        "• Onlar basamağında $A + 4 + 1 = A + 5$ toplamı $10 + C$ olmalıdır (elde $1$), buradan $C = A - 5$ bulunur.\n"
        "• Yüzler basamağında $3 + B + 1 = 10 + C \\implies B - C = 6$'dır.\n"
        "$C = A - 5$ yerine yazılırsa $B - (A - 5) = 6 \\implies B - A = 1$ olur.\n"
        "$A + B = 15$ ve $B - A = 1$ denklemlerinden **$B = 8$**, **$A = 7$** ve **$C = 7 - 5 = 2$** bulunur ($377 + 848 = 1225$).\n"
        "O hâlde $A + B + C = 7 + 8 + 2 = 17$ olur. Doğru cevap **B** seçeneğidir."
    )

    qmap["2021_ales3_mat_06"]["options"] = make_opts(["$a < b < c$", "$b < a < c$", "$b < c < a$", "$c < b < a$", "$c < a < b$"])
    qmap["2021_ales3_mat_07"]["options"] = make_opts(["2", "1", "$\\frac{1}{2}$", "$\\frac{1}{3}$", "$\\frac{1}{6}$"])

    # Q08
    q08_3 = qmap["2021_ales3_mat_08"]
    q08_3["questionText"] = (
        "$a, b$ ve $c$ birer tam sayı olmak üzere\n"
        "• $a - b$ ifadesinin çift sayı,\n"
        "• $a + c$ ifadesinin tek sayı\n"
        "olduğu biliniyor.\n\n"
        "**Buna göre,**\n"
        "I. $a \\cdot b \\cdot c$\n"
        "II. $a \\cdot c + b$\n"
        "III. $a + b + c$\n\n"
        "**ifadelerinden hangileri her zaman çift sayıdır?**"
    )
    q08_3["options"] = make_opts(["Yalnız I", "Yalnız II", "I ve II", "I ve III", "II ve III"])
    q08_3["correctAnswer"] = "A"
    q08_3["suggestedSolution"] = (
        "• $a - b$ çift sayı olduğundan $a$ ve $b$ aynı (ikisi de tek veya ikisi de çift) pariteye sahiptir.\n"
        "• $a + c$ tek sayı olduğundan $a$ ve $c$ zıt pariteye sahiptir.\n\n"
        "Dolayısıyla:\n"
        "1. **Durum:** $a$ Tek $\\implies b$ Tek, $c$ Çift.\n"
        "2. **Durum:** $a$ Çift $\\implies b$ Çift, $c$ Tek.\n\n"
        "Her iki durumda da $a, b, c$ tam sayılarından en az biri kesinlikle çifttir:\n"
        "• **I. $a \\cdot b \\cdot c$:** Çarpanlardan en az biri çift olduğu için **her zaman çifttir**.\n"
        "• **II. $a \\cdot c + b$:** 1. durumda $\\text{T} \\cdot \\text{Ç} + \\text{T} = \\text{Tek}$ olur.\n"
        "• **III. $a + b + c$:** 2. durumda $\\text{Ç} + \\text{Ç} + \\text{T} = \\text{Tek}$ olur.\n\n"
        "Yalnızca **I** her zaman çift sayıdır. Doğru cevap **A** seçeneğidir."
    )

    # Q09
    q09_3 = qmap["2021_ales3_mat_09"]
    q09_3["questionText"] = (
        "$a, b$ ve $c$ gerçel sayıları için\n\n"
        "$$\\frac{a}{b} < 0 < \\frac{b}{c} < a \\cdot b \\cdot c$$\n\n"
        "**olduğuna göre; $a, b$ ve $c$ sayılarının işaretleri sırasıyla aşağıdakilerden hangisidir?**"
    )
    q09_3["options"] = make_opts(["$-, +, +$", "$+, -, +$", "$+, -, -$", "$-, -, +$", "$-, +, -$"])
    q09_3["correctAnswer"] = "C"
    q09_3["suggestedSolution"] = (
        "Verilen eşitsizlikleri sırasıyla inceleyelim:\n"
        "1. $\\frac{b}{c} > 0$ olduğundan $b$ ile $c$ **aynı işaretlidir** (dolayısıyla $b \\cdot c > 0$'dır).\n"
        "2. $a \\cdot b \\cdot c > 0$ ve $b \\cdot c > 0$ olduğundan **$a > 0$ ($+$)** olmalıdır.\n"
        "3. $\\frac{a}{b} < 0$ ve $a > 0$ olduğundan **$b < 0$ ($-$)** olmalıdır.\n"
        "4. $b$ ile $c$ aynı işaretli olduğundan **$c < 0$ ($-$)** olur.\n\n"
        "O hâlde $a, b$ ve $c$'nin işaretleri sırasıyla **$+, -, -$**'dir. Doğru cevap **C** seçeneğidir."
    )

    # Q17 (Sevim's Cookbook TOC)
    q17_3 = qmap["2021_ales3_mat_17"]
    set_svg(q17_3, "ales3_q17_toc.svg")
    q17_3["suggestedSolution"] = (
        "Şekil 1'deki başlangıç sayfalarından her bölümün kaç sayfadan oluştuğunu bulalım:\n"
        "• **Çorbalar:** $10 - 1 = 9$ sayfa\n"
        "• **Salatalar:** $15 - 10 = 5$ sayfa\n"
        "• **Et yemekleri:** $28 - 15 = 13$ sayfa\n"
        "• **Sebze yemekleri:** $38 - 28 = 10$ sayfa\n\n"
        "Şekil 2'deki yeni sıralamaya göre başlangıç sayfalarını hesaplayalım:\n"
        "• **Salatalar:** $1$. sayfadan başlar ($5$ sayfa sürer).\n"
        "• **Çorbalar (?):** $1 + 5 = \\mathbf{6}$. sayfadan başlar ($9$ sayfa sürer).\n"
        "• **Sebze yemekleri (?):** $6 + 9 = \\mathbf{15}$. sayfadan başlar ($10$ sayfa sürer).\n"
        "• **Et yemekleri (?):** $15 + 10 = \\mathbf{25}$. sayfadan başlar ($13$ sayfa sürer, Tatlılar $25 + 13 = 38$. sayfada başlar).\n\n"
        "Buna göre '?' ile gösterilen yerlere gelecek sayıların toplamı:\n"
        "$$6 + 15 + 25 = 46$$\n"
        "bulunur. Doğru cevap **E** seçeneğidir."
    )

    # Q20 (Aslı's 1/7 down payment)
    q20_3 = qmap["2021_ales3_mat_20"]
    q20_3["questionText"] = (
        "Yeni bir oturma grubu alan Aslı; oturma grubunun fiyatının $\\frac{1}{7}$’sini peşin, kalan parayı da 4 eşit taksitle ödeyecektir.\n\n"
        "**Ödenecek her bir taksit tutarı 2700 TL olduğuna göre, oturma grubunun fiyatı kaç TL’dir?**"
    )
    q20_3["suggestedSolution"] = (
        "Oturma grubunun fiyatına $7x$ diyelim.\n"
        "• Peşin ödenen kısım: $7x \\cdot \\frac{1}{7} = x$\n"
        "• Kalan tutar: $7x - x = 6x$\n\n"
        "Kalan $6x$ tutarı 4 eşit taksitle ödendiğine ve her taksit $2700$ TL olduğuna göre:\n"
        "$$6x = 4 \\times 2700 = 10\\,800\\text{ TL} \\implies x = 1800\\text{ TL}$$\n"
        "Oturma grubunun toplam fiyatı:\n"
        "$$7x = 7 \\times 1800 = 12\\,600\\text{ TL}$$\n"
        "bulunur. Doğru cevap **D** seçeneğidir."
    )

    # Q21 (Berna's course schedule)
    q21_3 = qmap["2021_ales3_mat_21"]
    set_svg(q21_3, "ales3_q21_schedule.svg")
    q21_3["suggestedSolution"] = (
        "Tabloya göre günlere düşen ders sayıları:\n"
        "• **Pazartesi:** 1 İngilizce, 2 Matematik\n"
        "• **Salı:** 1 İngilizce, 2 Matematik\n"
        "• **Çarşamba:** 3 İngilizce, 1 Matematik\n"
        "• **Perşembe:** 2 İngilizce, 3 Matematik\n"
        "• **Cuma:** 2 İngilizce, 2 Matematik\n\n"
        "Berna'nın gitmediği **3 günde** toplam **6 İngilizce ve 6 Matematik** dersi vardır. "
        "3 günün toplamında 6 İngilizce ve 6 Matematik elde edebilmek için:\n"
        "• **Çarşamba** (3 İng, 1 Mat) + **Perşembe** (2 İng, 3 Mat) + **Pazartesi veya Salı** (1 İng, 2 Mat) $= (3+2+1)\\text{ İng} + (1+3+2)\\text{ Mat} = 6\\text{ İng}, 6\\text{ Mat}$ olmalıdır.\n\n"
        "Dolayısıyla Berna Çarşamba ve Perşembe günleri kesinlikle kursa gitmemiş, **Cuma** günü ise kursa **kesinlikle gitmiştir**. Doğru cevap **E** seçeneğidir."
    )

    # Q22 (Digital clock)
    q22_3 = qmap["2021_ales3_mat_22"]
    set_svg(q22_3, "ales3_q22_clock.svg")
    q22_3["questionText"] = (
        "$A, B, C$ ve $D$ doğal sayıları için $AB$ sayısı 24’ten küçük, $CD$ sayısı 60’tan küçük olmak üzere bir dijital saatte "
        "$\\boxed{A\\ B\\ .\\ C\\ D}$ gösterimi gün içerisinde bir anı göstermektedir.\n\n"
        "**Buna göre, $\\boxed{2\\ K\\ .\\ L\\ 4}$ ve $\\boxed{2\\ L\\ .\\ K\\ 8}$ ifadelerini bu dijital saatte gösterim yapan kaç farklı $(K, L)$ sıralı ikilisi vardır?**"
    )
    q22_3["suggestedSolution"] = (
        "İki gösterimin de geçerli bir dijital saat anını belirtmesi için:\n"
        "1. Saat kısmı olan iki basamaklı $2K$ ve $2L$ doğal sayıları $24$'ten küçük olmalıdır:\n"
        "$$2K < 24 \\implies K \\in \\{0, 1, 2, 3\\}$$\n"
        "$$2L < 24 \\implies L \\in \\{0, 1, 2, 3\\}$$\n"
        "2. Dakika kısmı olan $L4$ ve $K8$ sayıları da $60$'tan küçük olmalıdır ($K, L \\in \\{0, 1, 2, 3\\}$ için $L4 < 60$ ve $K8 < 60$ koşulu otomatik olarak sağlanır).\n\n"
        "$K$ için $4$ farklı değer ($0, 1, 2, 3$) ve $L$ için $4$ farklı değer ($0, 1, 2, 3$) bulunduğundan toplam:\n"
        "$$4 \\times 4 = 16$$\n"
        "farklı $(K, L)$ sıralı ikilisi vardır. Doğru cevap **B** seçeneğidir."
    )

    # ALES3 Sayısal Group Questions (23..43)
    sc_23_24_3 = (
        "Çoktan seçmeli bir sınavda adaylara 60 soru sorulmuş ve doğru cevaplanan her bir soru için adaylara 4 puan "
        "verilirken yanlış cevaplanan her bir soru için adayların puanları 1 puan azaltılmıştır. Boş bırakılan sorular için "
        "adayların puanlarında bir değişiklik yapılmamıştır."
    )
    set_group(qmap["2021_ales3_mat_23"], "2021_ales3_mat_23_24", "23 - 24. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", 1, 2, sc_23_24_3)
    qmap["2021_ales3_mat_23"]["questionText"] = "**Soruların hepsini cevaplayan bir aday 15 soruya yanlış cevap verdiğine göre, sınavdan kaç puan almıştır?**"
    set_group(qmap["2021_ales3_mat_24"], "2021_ales3_mat_23_24", "23 - 24. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", 2, 2, sc_23_24_3)
    qmap["2021_ales3_mat_24"]["questionText"] = (
        "Belirli sayıda soruyu boş bırakan bir adayın sınavda doğru cevap verdiği soru sayısı, yanlış cevap verdiği soru sayısının 5 katıdır.\n\n"
        "**Bu aday sınavdan 171 puan aldığına göre, kaç soruyu boş bırakmıştır?**"
    )

    # Q25 - Q26 (Teğet daireler oyunu)
    sc_25_26_3 = (
        "Üstte 5 dairenin ve altta 6 dairenin bulunduğu düzenekte, üstteki her bir daire altında bulunan iki daireye teğettir. "
        "Bu düzenekle oynanan bir oyunun kuralları aşağıdaki gibidir:\n"
        "• 1’den 11’e kadar olan tam sayılar bu dairelere her bir dairede farklı bir sayı olacak biçimde yazılıyor.\n"
        "• Üstteki bir dairede yazılı olan sayı, bu daireye teğet olan altındaki iki dairede yazılı olan sayıların her ikisinden de büyükse üstteki bu daire sarı renge boyanıyor.\n"
        "• Üstteki 5 daireden boyanması gereken dairelerin her biri sarı renge boyandığında oyun tamamlanıyor."
    )
    q25_3 = qmap["2021_ales3_mat_25"]
    set_group(q25_3, "2021_ales3_mat_25_26", "25 - 26. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", 1, 2, sc_25_26_3)
    set_svg(q25_3, "ales3_q25_chart.svg")
    q25_3["questionText"] = "**Dairelerin üzerinde yazan sayıların bir kısmının verildiği yukarıdaki düzenekte oyun tamamlandığına göre, $a + b + c$ toplamı kaçtır?**"
    q25_3["options"] = make_opts(["15", "18", "20", "21", "25"])
    q25_3["correctAnswer"] = "B"
    q25_3["suggestedSolution"] = (
        "Düzenekte $1, 2, 4, 6, 9, 11$ sayıları kullanılmış olup geriye **$3, 5, 7, 8, 10$** sayıları kalmıştır.\n"
        "• Üstte $4$ yazılı daire sarı boyalı olduğuna göre altındaki $1$ ve $a$'dan büyüktür: $a < 4 \\implies$ kalan sayılardan **$a = 3$** olur.\n"
        "• Üstte $6$ yazılı daire sarı boyalı olduğuna göre altındaki $c$ ve $2$'den büyüktür: $c < 6 \\implies$ kalan sayılardan **$c = 5$** olur.\n"
        "• Kalan üç sayı **$7, 8, 10$**'dur. Üstteki 2. ve 4. daireler sarı boyalı **olmadığına** göre, $10$ sayısı üstteki boş dairelere gelemez (çünkü $10$ nereye yazılırsa yazılsın altındaki iki sayıdan büyük olup sarıya boyanırdı!).\n"
        "• Dolayısıyla **$b = 10$** olmalı, üstteki iki boş daireye ise $7$ ve $8$ gelmelidir (soldaki boş daire $9$'dan küçük, sağdaki boş daire $b=10$'dan küçük olduğu için boyanmaz).\n\n"
        "O hâlde $a + b + c = 3 + 10 + 5 = 18$ bulunur. Doğru cevap **B** seçeneğidir."
    )

    q26_3 = qmap["2021_ales3_mat_26"]
    set_group(q26_3, "2021_ales3_mat_25_26", "25 - 26. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", 2, 2, sc_25_26_3)
    set_svg(q26_3, "ales3_q26_chart.svg")
    q26_3["questionText"] = "**Dairelerin üzerinde yazan sayıların bir kısmının verildiği yukarıdaki düzenekte oyun tamamlandığına göre, $x + y$ toplamı kaçtır?**"
    q26_3["options"] = make_opts(["3", "6", "7", "9", "12"])
    q26_3["correctAnswer"] = "D"
    q26_3["suggestedSolution"] = (
        "Üstteki 5 dairenin **tamamı** sarı renge boyanmıştır! Yani üstteki her daire, altındaki komşu iki daireden büyüktür.\n"
        "• Üstteki son dairede $3$ yazdığına göre, onun altındaki sağdaki iki daire $3$'ten küçük olmak zorundadır: bu iki daireye **$1$ ve $2$** gelir.\n"
        "• Üstteki 4. dairede $6$ yazdığına göre, onun sol altındaki **$y$** dairesi $6$'dan küçük olmalıdır ($y \\in \\{4, 5\\}$).\n"
        "• Kalan sayılar $\\{4, 5, 8, 10, 11\\}$ olup bunlardan üçü üstteki ilk 3 sarı daireye, ikisi ise $x$ ve $y$'ye gelecektir.\n"
        "• Üstteki ilk iki daire $9$'a teğet olduğu için ikisi de $9$'dan büyük olmalıdır ($10$ ve $11$). Üstteki 3. daire ise $x$ ve $y$'den büyük olacağından buraya $8$ gelir.\n"
        "• Geriye $x$ ve $y$ için **$4$ ve $5$** sayıları kalır.\n\n"
        "Buna göre $x + y = 4 + 5 = 9$ bulunur. Doğru cevap **D** seçeneğidir."
    )

    # Q27 - Q28 (2x2 kutu işlemi)
    sc_27_28_3 = (
        "Sıfırdan farklı $A, B, C$ ve $D$ rakamları için\n"
        "$$\\begin{array}{|c|c|} \\hline A & B \\\\ \\hline C & D \\\\ \\hline \\end{array}$$\n"
        "gösteriminin değeri, $AD$ iki basamaklı doğal sayı olmak üzere, **$AD + B \\cdot C$** sayısına eşittir.\n\n"
        "Örneğin,\n"
        "$$\\begin{array}{|c|c|} \\hline 4 & 5 \\\\ \\hline 5 & 7 \\\\ \\hline \\end{array}$$\n"
        "gösteriminin değeri $47 + 5 \\cdot 5 = 72$ sayısına eşittir."
    )
    q27_3 = qmap["2021_ales3_mat_27"]
    set_group(q27_3, "2021_ales3_mat_27_28", "27 - 28. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", 1, 2, sc_27_28_3)
    set_svg(q27_3, "ales3_q27_matrix.svg")
    q27_3["questionText"] = "**Yukarıdaki eşitliğe göre, $B$ kaçtır?**"
    q27_3["options"] = make_opts(["5", "6", "7", "8", "9"])
    q27_3["correctAnswer"] = "A"
    q27_3["suggestedSolution"] = (
        "Tanımlanan kurala göre eşitliğin her iki tarafındaki kutuların değerlerini yazalım:\n"
        "• Sol taraf: $53 + B \\cdot 1 = 53 + B$\n"
        "• Sağ taraf: $26 + 8 \\cdot 4 = 26 + 32 = 58$\n\n"
        "Eşitlikten:\n"
        "$$53 + B = 58 \\implies B = 5$$\n"
        "bulunur. Doğru cevap **A** seçeneğidir."
    )

    q28_3 = qmap["2021_ales3_mat_28"]
    set_group(q28_3, "2021_ales3_mat_27_28", "27 - 28. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", 2, 2, sc_27_28_3)
    set_svg(q28_3, "ales3_q28_matrix.svg")
    q28_3["questionText"] = "**Yukarıdaki gösterimin değeri 25 olduğuna göre, $B$’nin alabileceği farklı değerlerin toplamı kaçtır?**"
    q28_3["options"] = make_opts(["4", "5", "6", "7", "8"])
    q28_3["correctAnswer"] = "D"
    q28_3["suggestedSolution"] = (
        "Tanımlanan kurala göre gösterimin değeri ($A3$ iki basamaklı sayı olmak üzere):\n"
        "$$A3 + B \\cdot 2 = 25 \\implies (10A + 3) + 2B = 25 \\implies 10A + 2B = 22 \\implies 5A + B = 11$$\n"
        "$A$ ve $B$ sıfırdan farklı birer rakam olduğundan:\n"
        "• $A = 1 \\implies B = 6$\n"
        "• $A = 2 \\implies B = 1$\n\n"
        "$B$'nin alabileceği farklı değerler $6$ ve $1$ olup toplamları $6 + 1 = 7$'dir. Doğru cevap **D** seçeneğidir."
    )

    # Q29 - Q31 (Aysun iplik)
    sc_29_31_3 = (
        "Aysun, 1200 gram ipliğin tamamını kullanarak ya 1 tane kazak ya 4 tane aynı modelde atkı ya da 6 tane aynı "
        "modelde bere örebilmektedir. Sonra ördüğü kazak, atkı ve berelerin tanesini sırasıyla 110 TL, 30 TL ve 25 TL’ye satmaktadır."
    )
    for idx, qnum in enumerate([29, 30, 31], 1):
        set_group(qmap[f"2021_ales3_mat_{qnum:02d}"], "2021_ales3_mat_29_31", "29 - 31. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", idx, 3, sc_29_31_3)
    qmap["2021_ales3_mat_29"]["questionText"] = "**Buna göre, 1 tane atkı ve 1 tane bere örmek için kullanılan toplam iplik miktarı kaç gramdır?**"
    qmap["2021_ales3_mat_30"]["questionText"] = "Aysun, 3100 gram ipliğin tamamını kullanarak belirli sayıda atkı ve bere örüyor.\n\n**Aysun bu atkı ve berelerin tamamının satışından toplam 350 TL gelir elde ettiğine göre, sattığı bere sayısı kaçtır?**"
    qmap["2021_ales3_mat_31"]["questionText"] = (
        "Aysun, 3500 gram iplikle örebileceği en fazla sayıda kazak örüyor. Sonra, kalan iplikle örebileceği en fazla sayıda atkı örüyor. "
        "Sonra da kalan ipliğin tamamını kullanarak bere örüyor.\n\n"
        "**Örülen bu kazak, atkı ve berelerin tamamının satışından elde edilen gelir kaç TL’dir?**"
    )

    # Q32 - Q34 (Kürşat video tablosu)
    sc_32_34_3 = (
        "Çektiği yemek videolarını kendi profilinde paylaşan Kürşat; paylaştığı videonun görüntülenme sayısına, "
        "beğeni sayısına ve kendi profilindeki yeni takipçi sayısına göre puan kazanmaktadır.\n"
        "Her bir görüntülenme için 1 puan, her bir beğeni için 2 puan ve her bir yeni takipçi için 3 puan kazanan "
        "Kürşat’ın ocak, şubat ve mart aylarındaki paylaştığı videoların görüntülenme, beğeni ve profilindeki yeni "
        "takipçi sayılarından bazıları aşağıdaki tabloda verilmiştir."
    )
    for idx, qnum in enumerate([32, 33, 34], 1):
        q = qmap[f"2021_ales3_mat_{qnum:02d}"]
        set_group(q, "2021_ales3_mat_32_34", "32 - 34. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", idx, 3, sc_32_34_3)
        set_svg(q, "ales3_q32_table.svg")
    qmap["2021_ales3_mat_32"]["questionText"] = (
        "Şubat ayındaki beğeni sayısı; o ayki görüntülenme sayısının yarısı, o ayki yeni takipçi sayısının 2 katıdır.\n\n"
        "**Buna göre; şubat ayındaki görüntülenme, beğeni ve yeni takipçi sayılarının toplamı kaçtır?**"
    )
    qmap["2021_ales3_mat_33"]["questionText"] = (
        "Şubat ve mart aylarının her birinde, Kürşat’ın profilindeki yeni takipçi sayısı bir önceki aya göre % 20 artmıştır.\n\n"
        "**Buna göre; ocak, şubat ve mart aylarındaki yeni takipçi sayısından kazanılan puanların toplamı kaçtır?**"
    )
    qmap["2021_ales3_mat_34"]["questionText"] = (
        "Kürşat’ın şubat ayındaki beğeni sayısından kazandığı puan, ocak ve mart aylarındaki görüntülenme sayısından kazandığı puanların toplamına eşittir. "
        "Kürşat’ın ocak ayındaki yeni takipçi sayısından kazandığı puan ise şubat ayındaki görüntülenme sayısından kazandığı puana eşittir.\n\n"
        "**Buna göre, bu üç aydaki toplam görüntülenme sayısı kaçtır?**"
    )

    # Q35 - Q37 (Peynir süt oranları tablosu)
    sc_35_37_3 = (
        "Bir peynir üreticisi; inek, koyun ve keçi sütlerini belirli oranlarda karıştırarak beyaz peynir ve kaşar peyniri "
        "üretmektedir. Peynirlerin üretiminde kullanılan süt oranları aşağıdaki tabloda verilmiştir.\n"
        "• 1 kilogram beyaz peynir üretmek için 8 litre süt,\n"
        "• 1 kilogram kaşar peyniri üretmek için ise 10 litre süt kullanılmaktadır."
    )
    for idx, qnum in enumerate([35, 36, 37], 1):
        q = qmap[f"2021_ales3_mat_{qnum:02d}"]
        set_group(q, "2021_ales3_mat_35_37", "35 - 37. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", idx, 3, sc_35_37_3)
        set_svg(q, "ales3_q35_table.svg")
    qmap["2021_ales3_mat_35"]["questionText"] = "**İnek, koyun ve keçi sütlerinin litresini sırasıyla 2 TL, 3 TL ve 4 TL’den satın alan bu üreticinin 1 kilogram beyaz peynir üretmek için kullandığı sütün maliyeti kaç TL’dir?**"
    qmap["2021_ales3_mat_35"]["suggestedSolution"] = (
        "1 kg beyaz peynir için toplam **8 litre** süt kullanılmaktadır. Tablodaki yüzdelere göre:\n"
        "• **İnek sütü (% 50):** $8 \\times 0{,}50 = 4$ litre $\\implies 4 \\times 2\\text{ TL} = 8$ TL\n"
        "• **Koyun sütü (% 25):** $8 \\times 0{,}25 = 2$ litre $\\implies 2 \\times 3\\text{ TL} = 6$ TL\n"
        "• **Keçi sütü (% 25):** $8 \\times 0{,}25 = 2$ litre $\\implies 2 \\times 4\\text{ TL} = 8$ TL\n\n"
        "Toplam süt maliyeti $8 + 6 + 8 = 22$ TL bulunur. Doğru cevap **C** seçeneğidir."
    )
    qmap["2021_ales3_mat_36"]["questionText"] = (
        "Üretici; inek sütünün litresini 3 TL’den, koyun sütünün litresini 3,5 TL’den satın almıştır.\n\n"
        "**Üreticinin 1 kilogram kaşar peyniri üretmek için kullandığı sütün maliyeti 36 TL olduğuna göre, satın aldığı keçi sütünün litresi kaç TL’dir?**"
    )
    qmap["2021_ales3_mat_36"]["suggestedSolution"] = (
        "1 kg kaşar peyniri için toplam **10 litre** süt kullanılmaktadır. Tablodaki yüzdelere göre:\n"
        "• **İnek sütü (% 20):** $10 \\times 0{,}20 = 2$ litre $\\implies 2 \\times 3\\text{ TL} = 6$ TL\n"
        "• **Koyun sütü (% 40):** $10 \\times 0{,}40 = 4$ litre $\\implies 4 \\times 3{,}5\\text{ TL} = 14$ TL\n"
        "• **Keçi sütü (% 40):** $10 \\times 0{,}40 = 4$ litre $\\implies 4 \\times x$ TL\n\n"
        "Toplam maliyet $6 + 14 + 4x = 36 \\implies 4x = 16 \\implies x = 4$ TL bulunur. Doğru cevap **A** seçeneğidir."
    )
    qmap["2021_ales3_mat_37"]["questionText"] = (
        "Üretici toplam 350 litre süt kullanarak beyaz peynir ve kaşar peyniri üretiyor. Bu iki peynir türünün üretiminde de eşit miktarda inek sütü kullanıyor.\n\n"
        "**Buna göre, üretilen kaşar peyniri kaç kilogramdır?**"
    )
    qmap["2021_ales3_mat_37"]["suggestedSolution"] = (
        "Beyaz peynir için kullanılan toplam süt $B$ litre, kaşar peyniri için kullanılan toplam süt $K$ litre olsun ($B + K = 350$).\n"
        "İki peynirde eşit miktarda inek sütü kullanıldığına göre:\n"
        "$$B \\cdot \\frac{50}{100} = K \\cdot \\frac{20}{100} \\implies 5B = 2K$$\n"
        "$B = 2t$ ve $K = 5t$ dersek:\n"
        "$$2t + 5t = 350 \\implies 7t = 350 \\implies t = 50$$\n"
        "Kaşar peyniri için kullanılan toplam süt miktarı $K = 5 \\times 50 = 250$ litredir.\n"
        "1 kg kaşar peyniri için 10 litre süt kullanıldığından, üretilen kaşar peyniri:\n"
        "$$\\frac{250}{10} = 25\\text{ kilogram}$$\n"
        "bulunur. Doğru cevap **D** seçeneğidir."
    )

    # Q38 - Q40 (İç içe kareler düzeneği)
    sc_38_40_3 = (
        "Her bir köşesine birer doğal sayı yazılacak şekilde iç içe karelerden oluşan bir düzenek aşağıdaki kurallara göre hazırlanmaktadır:\n"
        "• Birinci adımda bir kare çizilir ve bu karenin köşelerine dört sayı yazılır.\n"
        "• Sonraki her adımda, en son çizilen karenin her bir kenarının orta noktalarını köşe olarak kabul eden yeni bir kare çizilir ve bu karenin köşelerine, orta noktası olduğu kenarın uçlarındaki sayıların farkı (mutlak değeri) yazılır.\n"
        "• Son çizilen karenin köşelerindeki sayıların hepsinin birbirine eşit olduğu ilk adımda, düzenek tamamlanmış olur."
    )
    for idx, qnum in enumerate([38, 39, 40], 1):
        q = qmap[f"2021_ales3_mat_{qnum:02d}"]
        set_group(q, "2021_ales3_mat_38_40", "38 - 40. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", idx, 3, sc_38_40_3)
        set_svg(q, f"ales3_q{qnum}_squares.svg")
    qmap["2021_ales3_mat_38"]["questionText"] = "**Birinci adımı şekildeki gibi verilen düzenek kaçıncı adımda tamamlanır?**"
    qmap["2021_ales3_mat_39"]["questionText"] = "**Ardışık 3 adımı verilen düzeneğin görünümünün bir kısmı şekildeki gibi olduğuna göre, $A + B$ toplamı kaçtır?**"
    qmap["2021_ales3_mat_39"]["suggestedSolution"] = (
        "En dış karenin üst kenarındaki $1$ ve $3$ sayılarının farkından orta karenin üst köşesi $|3 - 1| = 2$'dir.\n"
        "• İç karenin sağ üst köşesi $1$, sağ alt köşesi $1$ ve orta karenin alt köşesi $4$ olduğundan, orta karenin sağ köşesi hem $2$'ye hem $4$'e $1$ uzaklıkta olmalıdır $\\implies$ orta karenin sağ köşesi **$3$**'tür.\n"
        "• Sağ dış kenarda $|B - 3| = 3 \\implies B = 6$ (veya $B = 0$, ancak alt kenarda $|A - B| = 4$ ile birlikte kontrol edelim).\n"
        "• İç karenin sol alt köşesi $5$ olduğundan, orta karenin sol köşesi ile alt köşesi ($4$) arasındaki fark $5$'tir: orta karenin sol köşesi $4 + 5 = 9$'dur.\n"
        "• Sol dış kenarda $|A - 1| = 9 \\implies \\mathbf{A = 10}$ bulunur.\n"
        "• Alt dış kenarda $|10 - B| = 4 \\implies \\mathbf{B = 6}$ olur.\n\n"
        "O hâlde $A + B = 10 + 6 = 16$ bulunur. Doğru cevap **A** seçeneğidir."
    )
    qmap["2021_ales3_mat_40"]["questionText"] = (
        "Üçüncü adımda tamamlanan düzeneğin görünümünün bir kısmı şekilde verilmiştir.\n\n"
        "**Buna göre, $A$ kaçtır?**"
    )
    qmap["2021_ales3_mat_40"]["suggestedSolution"] = (
        "En dış karenin sol kenarının iki ucunda da $A$ yazdığından orta karenin sol köşesi $|A - A| = 0$'dır.\n"
        "Sağ dış kenarın uçlarında $2$ ve $4$ yazdığından orta karenin sağ köşesi $|4 - 2| = 2$'dir.\n"
        "3. adımdaki iç karenin dört köşesi de $1$'e eşittir. Orta karenin sol köşesi $0$ ve sağ köşesi $2$ olduğuna göre, iç karenin tüm köşelerinin $1$ çıkması için orta karenin **üst ve alt köşelerinin $1$** olması gerekir ($|1 - 0| = 1$ ve $|2 - 1| = 1$).\n"
        "Dolayısıyla hem $|A - 2| = 1$ hem de $|A - 4| = 1$ eşitliklerini sağlayan doğal sayı **$A = 3$**'tür. Doğru cevap **B** seçeneğidir."
    )

    # Q41 - Q43 (Bant ve kapsüller)
    sc_41_43_3 = (
        "Soldan sağa doğru hareket eden bir banttan ve bu bandın sonunda bulunan A, B ve C kapsüllerinden "
        "oluşan düzenekte bandın üzerine 1’den 5’e kadar rakamlarla numaralandırılmış 9 tane top konuluyor. "
        "Aşağıdaki kurallara göre sırası gelen top ilk uygun kapsüle gelince, kapsülün kapağı açılıp top içeri "
        "girdikten sonra kapak kapanıyor:\n"
        "• Her bir kapsüle en fazla 3 top girebilmektedir.\n"
        "• A kapsülüne sadece 1 ve 2 numaralı toplar girebilmektedir.\n"
        "• B kapsülüne sadece 1, 2, 3 ve 4 numaralı toplar girebilmektedir.\n"
        "• C kapsülüne bütün toplar girebilmektedir."
    )
    for idx, qnum in enumerate([41, 42, 43], 1):
        q = qmap[f"2021_ales3_mat_{qnum:02d}"]
        set_group(q, "2021_ales3_mat_41_43", "41 - 43. soruları aşağıdaki bilgilere göre birbirinden bağımsız olarak cevaplayınız.", idx, 3, sc_41_43_3)
        set_svg(q, f"ales3_q{qnum}_conveyor.svg")
    qmap["2021_ales3_mat_41"]["questionText"] = "**Başlangıçtaki görünümü şekildeki gibi olan düzenekte tüm toplar kapsüllere girdiğinde, C kapsülündeki topların üzerinde yazan rakamların toplamı kaçtır?**"
    qmap["2021_ales3_mat_42"]["questionText"] = (
        "Başlangıçtaki görünümü şekildeki gibi olan düzenekte topların üzerinde yazan rakamların bir kısmı verilmiştir. "
        "Bu düzenekteki tüm toplar kapsüllere girdiğinde, B kapsülündeki topların hiçbirinin numarasının 3 olmadığı görülmüştür.\n\n"
        "**Buna göre, $x$ kaçtır?**"
    )
    qmap["2021_ales3_mat_43"]["questionText"] = (
        "Düzenekteki toplar kapsüllere girdiğinde kapsüllerdeki görünüm şekildeki gibidir.\n\n"
        "**Buna göre, düzeneğin başlangıçtaki görünümü aşağıdakilerden hangisi olabilir?**"
    )

    # Q45, Q47, Q48
    qmap["2021_ales3_mat_45"]["options"] = make_opts(["$8\\sqrt{3}$", "$10\\sqrt{3}$", "$12\\sqrt{3}$", "$14\\sqrt{3}$", "$16\\sqrt{3}$"])
    qmap["2021_ales3_mat_45"]["suggestedSolution"] = (
        "$|AB| = |AC|$ olduğundan $ABC$ ikizkenar üçgendir. $A$ tepesinden $[BC]$ tabanına dikme ($AH \\perp BC$) indirirsek tabanı iki eş parçaya böler:\n"
        "$$|BH| = |HC| = \\frac{8 + 2}{2} = 5\\text{ birim}$$\n"
        "Buradan $|HD| = |BD| - |BH| = 8 - 5 = 3$ birimdir.\n"
        "$AHD$ dik üçgeninde $m(\\widehat{ADH}) = 60^\\circ$ olduğundan $30^\\circ - 60^\\circ - 90^\\circ$ üçgeni özelliğiyle:\n"
        "$$|AH| = |HD| \\cdot \\sqrt{3} = 3\\sqrt{3}\\text{ birim}$$\n"
        "Boyalı $ADB$ üçgeninin alanı:\n"
        "$$\\text{Alan}(ADB) = \\frac{|BD| \\cdot |AH|}{2} = \\frac{8 \\cdot 3\\sqrt{3}}{2} = 12\\sqrt{3}\\text{ birimkare}$$\n"
        "bulunur. Doğru cevap **C** seçeneğidir."
    )
    qmap["2021_ales3_mat_47"]["options"] = make_opts(["5", "10", "20", "$5\\sqrt{5}$", "$10\\sqrt{5}$"])
    qmap["2021_ales3_mat_48"]["questionText"] = qmap["2021_ales3_mat_48"]["questionText"].replace("\\widehat{OAD}", "\\widehat{OAC}")

    # =========================================================================
    # 9. SYNC ALL INLINE SVGS & CLEAN BULLET TOFU CHARACTERS (\uf0b7)
    # =========================================================================
    for q in questions:
        if q.get("hasImage") and q.get("imageUrl"):
            fn = os.path.basename(q["imageUrl"])
            svg_path = os.path.join("public/assets/questions/svg", fn)
            if os.path.exists(svg_path):
                q["svgContent"] = load_svg(fn)
        else:
            q["hasImage"] = False
            q["imageUrl"] = None
            q["svgContent"] = None

        for field in ["questionText", "sharedContext", "suggestedSolution", "quickTip", "groupHeader"]:
            val = q.get(field)
            if isinstance(val, str):
                q[field] = val.replace("\uf0b7", "•")

        for opt in q.get("options", []):
            if isinstance(opt.get("text"), str):
                opt["text"] = opt["text"].replace("\uf0b7", "•")

    # Save seed_questions.json
    with open("public/data/seed_questions.json", "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print("Saved 300 repaired questions to public/data/seed_questions.json!")

    # Update questions_manifest.json
    manifest = []
    for idx, q in enumerate(questions, 1):
        manifest.append({
            "id": q["id"],
            "number": q.get("number", idx),
            "subject": q.get("subject"),
            "category": q.get("category"),
            "orderIndex": q.get("orderIndex", idx),
            "isGroupQuestion": bool(q.get("isGroupQuestion", False)),
            "groupId": q.get("groupId", None)
        })
    with open("public/data/questions_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print("Saved updated manifest to public/data/questions_manifest.json!")

if __name__ == "__main__":
    main()
