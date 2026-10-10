import math, random, json, os
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

HAFIZA_DOSYASI = "ai_hafiza.json"
sozluk = ["siber", "sığınak", "kod", "roket", "telsiz", "aktif", "güvenli", "utku", "kanka", "knk"]
word_to_idx = {word: i for i, word in enumerate(sozluk)}
egitim_verisi = []
boyut = len(sozluk)
agirliklar = [[random.uniform(-0.5, 0.5) for _ in range(boyut)] for _ in range(boyut)]

ARKADASCALAR = [
    "Ooo kanka bu terimi henüz hafıza matrislerime işlemedin ama kulağa tam 24 çekirdekli Xeon sunucumuzda koşturulacak canavar bir proje gibi geliyor! Ne olduğunu bana hızlıca çıtlatsana? 📡",
    "Bak bu kavramı henüz sistem çekirdeğine enjekte etmedin patron! Eğitmek için '/öğret [anahtar] [cevap]' formatıyla bana hemen öğret! 🚀",
    "Kanka emektar i5 bilgisayarımızın işlemcisini yakacak cinsten gizemli bir istek bu! Bana bunun jilet gibi bir tanımını versene. 💻",
    "Format dışı veya bilinmeyen veri algılandı knk! Yoksa yine koddaki while True döngüsünü açık unuttun da potasyum nitrat tozu nöronlarımın arasına mı kaçtı? Bana bunu hemen /öğret! 💥"
]

def hafiza_kaydet():
    try:
        with open(HAFIZA_DOSYASI, "w", encoding="utf-8") as f:
            json.dump({"sozluk": sozluk, "egitim_verisi": egitim_verisi, "agirliklar": agirliklar}, f, ensure_ascii=False, indent=4)
        print("💾 [Matris Hafıza Motoru] Tüm ağırlık matrisleri 'ai_hafiza.json' dosyasına mühürlendi!")
    except: pass

def hafiza_yukle():
    global sozluk, word_to_idx, egitim_verisi, agirliklar, boyut
    if os.path.exists(HAFIZA_DOSYASI):
        try:
            with open(HAFIZA_DOSYASI, "r", encoding="utf-8") as f: veri = json.load(f)
            sozluk = veri["sozluk"]; word_to_idx = {word: i for i, word in enumerate(sozluk)}
            egitim_verisi = [tuple(x) for x in veri["egitim_verisi"]]; agirliklar = veri["agirliklar"]; boyut = len(sozluk)
            if len(agirliklar) < boyut:
                for satir in agirliklar:
                    while len(satir) < boyut: satir.append(random.uniform(-0.5, 0.5))
                while len(agirliklar) < boyut: agirliklar.append([random.uniform(-0.5, 0.5) for _ in range(boyut)])
            print(f"🧠 [Matris Hafıza Motoru] Elle eğittiğin {len(egitim_verisi)} bilgi ve sinir ağları geri yüklendi kanka!")
            return True
        except: pass
    return False

def sozluk_genislet(yeni_kelime):
    global boyut, agirliklar, sozluk, word_to_idx
    if yeni_kelime not in word_to_idx:
        sozluk.append(yeni_kelime); word_to_idx[yeni_kelime] = len(sozluk) - 1
        for satir in agirliklar: satir.append(random.uniform(-0.5, 0.5))
        agirliklar.append([random.uniform(-0.5, 0.5) for _ in range(len(sozluk))]); boyut = len(sozluk)

def sigmoid(x):
    x = max(-500, min(500, x)); return 1 / (1 + math.exp(-x))

def sigmoid_turev(s_cikis): return s_cikis * (1 - s_cikis)

def yapay_zekayi_egit(epochs=100, ogrenme_hizi=0.5):
    if not egitim_verisi: return
    for epoch in range(epochs):
        for giris_kelimesi, hedef_kelimesi in egitim_verisi:
            if giris_kelimesi not in word_to_idx or hedef_kelimesi not in word_to_idx: continue
            giris_vektoru = [0 for _ in range(boyut)]; giris_vektoru[word_to_idx[giris_kelimesi]] = 1
            hedef_vektoru = [0 for _ in range(boyut)]; hedef_vektoru[word_to_idx[hedef_kelimesi]] = 1
            cikis_vektoru = [0 for _ in range(boyut)]
            for i in range(boyut):
                toplam = 0
                for j in range(boyut): toplam += giris_vektoru[j] * agirliklar[j][i]
                cikis_vektoru[i] = sigmoid(toplam)
            hatalar = [hedef_vektoru[i] - cikis_vektoru[i] for i in range(boyut)]
            for i in range(boyut):
                gradyan = hatalar[i] * sigmoid_turev(cikis_vektoru[i])
                for j in range(boyut): agirliklar[j][i] += ogrenme_hizi * gradyan * giris_vektoru[j]

def koruma_kontrolu(metin):
    illegaller = ["ddos", "hackle", "saldır", "çökert", "sız", "darkweb", "awazon"]
    for suc in illegaller:
        if suc in metin:
            return "🚨 [KANKA-AI GÜVENLİK FİLTRESİ: UYARI]\nHop dur bakalım deha kanka! Kapıya gelen o Türk Telekom ekiplerini ve o yazılı ihtarları ne çabuk unuttun? Zekamızı kurumsal sistemlere saldırmak için değil, yasal SaaS projelerinde paraya çevireceğiz kanka. Sığınağı tehlikeye atmayalım! 🤝🔐"
    return None

def canli_saat_ver():
    simdi = datetime.now(); saat_str = simdi.strftime("%H:%M:%S"); saat_int = simdi.hour
    if 0 <= saat_int < 6: durum = "Siber sığınakta tam bir gece yarısı operasyonu dönüyor kanka! 24 çekirdekli Xeon fan sesleri dışında çıt yok. Tam kod saati! 📡🌃"
    elif 6 <= saat_int < 12: durum = "Günaydın deha kanka! Güne Proton VPN siber hijyeni ve emektar i5'i uzay üssüne çevirme projeleriyle başlamak için harika bir sabah! 🚀🌅"
    elif 12 <= saat_int < 18: durum = "Tünaydın SaaS patronu! Dev.to analitiğini coşturacak o kodları geliştirmenin tam zamanı. 💻🔥"
    else: durum = "İyi akşamlar kanka! Günün siber bilançosunu çıkarma..."
    return f"📅 Bugün: {simdi.strftime('%d.%m.%Y')} | ⏱️ Canlı Saat: {saat_str}\n\n🤖 Kanka-AI Durum Raporu: {durum}"

def yapay_zekaya_sor(metin):
    # 🔥 DOĞRUDAN BELLEK KÖPRÜSÜ (Saçmalamayı %100 Bitiren Siber Hile kanka!)
    for g, h in egitim_verisi:
        if g == metin: return h
def yapay_zekaya_sor(metin):
    # 1. Aşama: Doğrudan Bellek Köprüsü (Hile Modu en üstte)
    for g, h in egitim_verisi:
        if g == metin: return h
        
    if not egitim_verisi: return random.choice(ARKADASCALAR)
    
    # 2. Aşama: Gelişmiş NLP Kütüphane Analizi
    try:
        # Hafızadaki tüm soruları (girdileri) topluyoruz
        sorular_listesi = [giriş for giriş, hedef in egitim_verisi]
        
        # Kelimelerin önemini tartan vektör motorunu çalıştırıyoruz
        vectorizer = TfidfVectorizer().fit(sorular_listesi)
        
        # Utku'nun yazdığı soruyu ve hafızadaki soruları matrise çeviriyoruz
        hafiza_matrisi = vectorizer.transform(sorular_listesi)
        utku_matrisi = vectorizer.transform([metin])
        
        # Matematiksel olarak en yakın anlamlı soruyu buluyoruz (Benzerlik Testi)
        benzerlikler = cosine_similarity(utku_matrisi, hafiza_matrisi)[0]
        en_yuksek_benzerlik_idx = benzerlikler.argsort()[-1]
        
        # Eğer benzerlik oranı %25'ten yüksekse doğru cevabı yapıştır
        if benzerlikler[en_yuksek_benzerlik_idx] > 0.25:
            hedef_cevap = egitim_verisi[en_yuksek_benzerlik_idx][1]
            return hedef_cevap
            
    except:
        pass
        
    # Eğer kütüphane eşleşme bulamazsa sığınak modunda rastgele takılsın
    return random.choice(ARKADASCALAR)

if __name__ == "__main__":
    os.system('color 0A'); hafiza_yukle()
    print("\n🎉 [SÜPER ZEKİ %100 HEDEF ODAKLI KANKA-AI v3.9] AKTİF PATRON!")
    print("------------------------------------------------------------------")
    print("💡 Doğrudan Bellek Köprüsü Enjekte Edildi. Saçmalama Modu Tamamen Yok Edildi.")
    print("💡 Hızlı Öğretme Modu Aktif. Eğitim Süresi 0.1 Saniyeye Düşürüldü.")
    while True:
        try:
            soru = input("\n👤 Utku: ").strip()
            if soru.lower() in ['exit', 'quit', 'kapat']:
                print("\n🤖 Kanka-AI uyku moduna geçti. Siber sığınak her zaman güvende patron!"); break
            if not soru: continue
            uyari_mesaji = koruma_kontrolu(soru.lower())
            if uyari_mesaji: print(f"\n🤖 Kanka-AI: {uyari_mesaji}"); continue
            
            if soru.lower().startswith("/kod-ekle"):
                parcalar = soru.split(" ", 2)
                if len(parcalar) >= 3:
                    anahtar = parcalar[1].lower(); enjekte_kod = parcalar[2]
                    kod_blogu = f"\n```python\n# UTKU-AI CANLI KOD MOTORU ÇIKTISI\n# DOSYA ADI: {anahtar}.py\n{enjekte_kod}\n```"
                    sozluk_genislet(anahtar); sozluk_genislet(kod_blogu)
                    egitim_verisi.append((anahtar, kod_blogu)); yapay_zekayi_egit(epochs=5); hafiza_kaydet()
                    print(f"\n🤖 Kanka-AI: Kod motoru aktif! '{anahtar}' nöronuna canavar kod mühürlendi kanka!")
                else: print("❌ Hatalı format kanka! Örnek: /kod-ekle socket-kod print('hello world')")
                continue
                
            if soru.lower().startswith("/öğret"):
                parcalar = soru.split(" ", 2)
                if len(parcalar) >= 3:
                    g_kelime = parcalar[1].lower(); h_cumle = parcalar[2]
                    sozluk_genislet(g_kelime); sozluk_genislet(h_cumle)
                    egitim_verisi.append((g_kelime, h_cumle)); yapay_zekayi_egit(epochs=5); hafiza_kaydet()
                    print(f"\n🤖 Kanka-AI: Siber hafıza güncellendi! '{g_kelime}' nöron bağlantısı kuruldu kanka!")
                else: print("❌ Hatalı format kanka! Örnek: /öğret knk ne oldu kanka?")
                continue
                
            temiz_soru = soru.lower().replace(" ", "").replace("ç", "c").replace("×", "x")
            if temiz_soru in ["saat", "saatkac", "zaman", "tarih"]: print(f"\n🤖 Kanka-AI:\n{canli_saat_ver()}"); continue
            
            sorgu_temiz = soru.lower().replace("×", "x")
            cevap = yapay_zekaya_sor(sorgu_temiz)
            print(f"\n🤖 Kanka-AI:\n{cevap}")
        except KeyboardInterrupt: print("\n[!] Siber sığınak acil durum moduna alındı kanka."); break
