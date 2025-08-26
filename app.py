# Gerekli Flask modülünü ve datetime kütüphanesini içe aktarır.
from flask import Flask, render_template, request
import datetime

# Flask uygulamasını başlatır.
app = Flask(__name__)

# Kapsamlı ve statik bir meslek veri seti.
# Gerçek bir veritabanı simülasyonu olarak kullanılıyor.
# Her bölüm için daha detaylı veriler (en düşük, ortalama, en yüksek maaş) içerir.
# Bu veriler, TÜİK veya sektör raporları gibi kaynaklardan alınmış varsayılmıştır.
bolum_verileri = {
    "Yazılım Mühendisliği": {
        "ortalama_maas_aylik": 45000,
        "aylik_maas_araligi": "35.000 TL - 70.000 TL",
        "yorum": "Yüksek talep gören bir alan ancak rekabet de çok yoğun. Mezuniyet sonrası ilk 6 ay kritik öneme sahip."
    },
    "Tıp": {
        "ortalama_maas_aylik": 60000,
        "aylik_maas_araligi": "50.000 TL - 100.000 TL+",
        "yorum": "Uzun ve zorlu bir eğitim süreci sonrası yüksek maaş potansiyeli. Kamu ve özel sektör maaşları farklılık gösterir."
    },
    "Hukuk": {
        "ortalama_maas_aylik": 40000,
        "aylik_maas_araligi": "25.000 TL - 80.000 TL",
        "yorum": "Önemli tecrübe ve uzmanlık gerektiren bir alan. İlk yıllar düşük maaşla başlayabilir, ancak potansiyel çok yüksek."
    },
    "İktisat ve İşletme": {
        "ortalama_maas_aylik": 30000,
        "aylik_maas_araligi": "20.000 TL - 50.000 TL",
        "yorum": "Geniş bir iş yelpazesi sunar. Maaşlar sektöre ve pozisyona göre büyük ölçüde değişir."
    },
    "Eğitim Bilimleri": {
        "ortalama_maas_aylik": 25000,
        "aylik_maas_araligi": "22.000 TL - 35.000 TL",
        "yorum": "Genellikle sabit bir maaş yapısına sahip. Özel sektörde farklılıklar görülebilir."
    },
    "İletişim": {
        "ortalama_maas_aylik": 23000,
        "aylik_maas_araligi": "18.000 TL - 40.000 TL",
        "yorum": "Geniş bir iş alanı olmasına rağmen, maaş potansiyeli kişisel yetenek ve network'e bağlıdır."
    },
    "Sanat ve Tasarım": {
        "ortalama_maas_aylik": 20000,
        "aylik_maas_araligi": "15.000 TL - 30.000 TL",
        "yorum": "Freelance ve proje bazlı işler yaygındır. İstikrarsızlık maaş potansiyelini etkileyebilir."
    },
    "Diğer": {
        "ortalama_maas_aylik": 20000,
        "aylik_maas_araligi": "18.000 TL - 30.000 TL",
        "yorum": "Farklı bölümleri içerir, maaşlar çok çeşitli olabilir."
    }
}


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Ana sayfayı işler. GET isteğiyle sayfayı gösterir, POST isteğiyle hesaplama yapar.
    """
    sonuc = None
    hata = None
    
    # POST isteği geldiğinde hesaplama işlemini yapar.
    if request.method == "POST":
        bolum = request.form.get("bolum")
        mezuniyet_tarihi_str = request.form.get("mezuniyet")
        
        # Tarih formatını kontrol eder.
        try:
            mezuniyet_tarihi = datetime.datetime.strptime(mezuniyet_tarihi_str, "%Y-%m-%d").date()
        except ValueError:
            hata = "Lütfen geçerli bir tarih formatı girin (örn: YYYY-AA-GG)."
            return render_template("index.html", bolum_list=list(bolum_verileri.keys()), sonuc=sonuc, error=hata)
        
        bugun = datetime.date.today()
        
        # Mezuniyet tarihinin gelecekte olup olmadığını kontrol eder.
        if mezuniyet_tarihi > bugun:
            hata = "Mezuniyet tarihi gelecekte olamaz."
            return render_template("index.html", bolum_list=list(bolum_verileri.keys()), sonuc=sonuc, error=hata)

        # Geçen gün sayısını hesaplar.
        gecen_gun_sayisi = (bugun - mezuniyet_tarihi).days
        
        # Seçilen bölüme ait verileri alır.
        if bolum in bolum_verileri:
            bolum_data = bolum_verileri[bolum]
            aylik_maas = bolum_data["ortalama_maas_aylik"]
            gunluk_maas = aylik_maas / 30.0
            
            # Toplam kazanç kaybını hesaplar.
            toplam_kayip = gunluk_maas * gecen_gun_sayisi
            
            # Elde edilen sonuçları bir sözlükte toplar.
            sonuc = {
                "bolum": bolum,
                "gecen_gun_sayisi": gecen_gun_sayisi,
                "aylik_maas": aylik_maas,
                "toplam_kayip": toplam_kayip,
                "maas_araligi": bolum_data["aylik_maas_araligi"],
                "yorum": bolum_data["yorum"]
            }
        else:
            hata = "Geçersiz bölüm seçimi."
    
    # render_template fonksiyonu ile sonuçları ve bölüm listesini HTML şablonuna gönderir.
    return render_template("index.html", bolum_list=list(bolum_verileri.keys()), sonuc=sonuc, error=hata)

if __name__ == "__main__":
    # Uygulamayı hata ayıklama modu açıkken çalıştırır.
    app.run(debug=True)
