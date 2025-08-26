# Gerekli Flask modülünü ve datetime kütüphanesini içe aktarır.
from flask import Flask, render_template, request, jsonify
import datetime

# Flask uygulamasını başlatır.
app = Flask(__name__)

# Kapsamlı ve statik bir meslek veri seti.
# Bu veriler, kullanıcı tarafından sağlanan en güncel maaş beklentileri ile birleştirilmiştir.
bolum_verileri = {
    "Acil Tıp Teknisyeni": {
        "ortalama_maas_aylik": 25450,
        "aylik_maas_araligi": "22.000 TL - 40.000 TL",
        "yorum": "Acil durumlarda ilk yardım ve hasta taşıma hizmeti verirler."
    },
    "Aktüerya Bilimleri": {
        "ortalama_maas_aylik": 30000,
        "aylik_maas_araligi": "25.000 TL - 45.000 TL",
        "yorum": "Sigortacılık ve finans sektöründe risk analisti olarak çalışırlar."
    },
    "Aşçı": {
        "ortalama_maas_aylik": 35800,
        "aylik_maas_araligi": "30.000 TL - 60.000 TL",
        "yorum": "Restoran ve otellerde yemek hazırlarlar."
    },
    "Avukat": {
        "ortalama_maas_aylik": 43500,
        "aylik_maas_araligi": "40.000 TL - 80.000 TL",
        "yorum": "Hukuk fakültesi mezunlarının icra ettiği bir meslektir."
    },
    "Bilgisayar Mühendisliği": {
        "ortalama_maas_aylik": 37600,
        "aylik_maas_araligi": "25.000 TL - 80.000 TL",
        "yorum": "Yazılım mühendisliğine benzer, geniş bir yelpazede iş imkanı sunar."
    },
    "Bilişim Sistemleri Mühendisliği": {
        "ortalama_maas_aylik": 43148,
        "aylik_maas_araligi": "28.000 TL - 60.000 TL",
        "yorum": "İşletme ve teknoloji arasında köprü kurarlar."
    },
    "Çevre Mühendisliği": {
        "ortalama_maas_aylik": 22000,
        "aylik_maas_araligi": "18.000 TL - 30.000 TL",
        "yorum": "Çevresel danışmanlık, atık yönetimi ve enerji sektörlerinde çalışabilirler."
    },
    "Diğer": {
        "ortalama_maas_aylik": 20000,
        "aylik_maas_araligi": "18.000 TL - 30.000 TL",
        "yorum": "Farklı bölümleri içerir, maaşlar çok çeşitli olabilir."
    },
    "Diş Hekimliği": {
        "ortalama_maas_aylik": 45400,
        "aylik_maas_araligi": "30.000 TL - 60.000 TL",
        "yorum": "Kendi kliniğini açma potansiyeli yüksek bir meslek."
    },
    "Dil ve Konuşma Terapisti": {
        "ortalama_maas_aylik": 36600,
        "aylik_maas_araligi": "30.000 TL - 50.000 TL",
        "yorum": "Konuşma ve dil bozukluklarının tedavisiyle ilgilenirler."
    },
    "Ebelik": {
        "ortalama_maas_aylik": 24000,
        "aylik_maas_araligi": "20.000 TL - 35.000 TL",
        "yorum": "Gebelik ve doğum süreçlerinde kadınlara destek olurlar."
    },
    "Eczacılık": {
        "ortalama_maas_aylik": 39500,
        "aylik_maas_araligi": "25.000 TL - 45.000 TL",
        "yorum": "Serbest eczane veya ilaç sektöründe maaşlar farklılık gösterir."
    },
    "Eğitim Bilimleri": {
        "ortalama_maas_aylik": 25000,
        "aylik_maas_araligi": "22.000 TL - 35.000 TL",
        "yorum": "Genellikle sabit bir maaş yapısına sahip. Özel sektörde farklılıklar görülebilir."
    },
    "Elektrik Elektronik Mühendisliği": {
        "ortalama_maas_aylik": 43000,
        "aylik_maas_araligi": "25.000 TL - 50.000 TL",
        "yorum": "Teknoloji şirketlerinde ve AR-GE pozisyonlarında yüksek maaş potansiyeli."
    },
    "Elektronik ve Haberleşme Mühendisliği": {
        "ortalama_maas_aylik": 37850,
        "aylik_maas_araligi": "30.000 TL - 55.000 TL",
        "yorum": "Telekomünikasyon ve teknoloji sektörlerinde iş imkanı sunar."
    },
    "Endüstri Mühendisliği": {
        "ortalama_maas_aylik": 38300,
        "aylik_maas_araligi": "22.000 TL - 40.000 TL",
        "yorum": "Üretim, lojistik ve süreç optimizasyonu alanlarında çalışabilirler."
    },
    "Fizik": {
        "ortalama_maas_aylik": 45650,
        "aylik_maas_araligi": "20.000 TL - 40.000 TL",
        "yorum": "Akademik kariyer veya teknoloji firmalarında Ar-Ge pozisyonları mevcuttur."
    },
    "Fizyoterapi ve Rehabilitasyon": {
        "ortalama_maas_aylik": 27900,
        "aylik_maas_araligi": "20.000 TL - 35.000 TL",
        "yorum": "Özel kliniklerde veya hastanelerde iş imkanı mevcuttur."
    },
    "Gastronomi ve Mutfak Sanatları": {
        "ortalama_maas_aylik": 19000,
        "aylik_maas_araligi": "16.000 TL - 30.000 TL",
        "yorum": "Restoranın statüsüne ve deneyime göre maaşlar değişiklik gösterir."
    },
    "Gemi İnşaatı ve Gemi Makineleri Mühendisliği": {
        "ortalama_maas_aylik": 56300,
        "aylik_maas_araligi": "25.000 TL - 50.000 TL",
        "yorum": "Denizcilik sektöründe uzmanlaşmış bir alandır."
    },
    "Gemi ve Deniz Teknolojisi Mühendisliği": {
        "ortalama_maas_aylik": 30000,
        "aylik_maas_araligi": "25.000 TL - 50.000 TL",
        "yorum": "Denizcilik, savunma sanayii ve enerji alanlarında çalışabilirler."
    },
    "Gıda Mühendisliği": {
        "ortalama_maas_aylik": 43250,
        "aylik_maas_araligi": "20.000 TL - 35.000 TL",
        "yorum": "Gıda üretimi, kalite kontrol ve Ar-Ge alanlarında iş imkanı vardır."
    },
    "Grafik Tasarım": {
        "ortalama_maas_aylik": 17000,
        "aylik_maas_araligi": "15.000 TL - 25.000 TL",
        "yorum": "Serbest çalışma ve projeli işler yaygındır."
    },
    "Halkla İlişkiler": {
        "ortalama_maas_aylik": 19000,
        "aylik_maas_araligi": "17.000 TL - 30.000 TL",
        "yorum": "Şirketlerin iletişim ve pazarlama departmanlarında çalışabilirler."
    },
    "Hemşire": {
        "ortalama_maas_aylik": 31300,
        "aylik_maas_araligi": "25.000 TL - 45.000 TL",
        "yorum": "Hastanelerde ve sağlık merkezlerinde hasta bakımıyla ilgilenirler."
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
    "İletişim": {
        "ortalama_maas_aylik": 23000,
        "aylik_maas_araligi": "18.000 TL - 40.000 TL",
        "yorum": "Geniş bir iş alanı olmasına rağmen, maaş potansiyeli kişisel yetenek ve network'e bağlıdır."
    },
    "İnşaat Mühendisliği": {
        "ortalama_maas_aylik": 27000,
        "aylik_maas_araligi": "20.000 TL - 45.000 TL",
        "yorum": "Proje bazlı işler ve saha tecrübesine göre maaşlar değişiklik gösterir."
    },
    "İşletme": {
        "ortalama_maas_aylik": 18000,
        "aylik_maas_araligi": "15.000 TL - 30.000 TL",
        "yorum": "Pozisyona ve şirkete göre geniş bir maaş aralığına sahiptir."
    },
    "İşletme Mühendisliği": {
        "ortalama_maas_aylik": 33700,
        "aylik_maas_araligi": "30.000 TL - 55.000 TL",
        "yorum": "İşletme süreçlerinin verimliliğini artırmaya odaklanır."
    },
    "Jeoloji Mühendisliği": {
        "ortalama_maas_aylik": 25000,
        "aylik_maas_araligi": "20.000 TL - 40.000 TL",
        "yorum": "Madencilik, petrol ve doğalgaz arama alanlarında çalışabilirler."
    },
    "Kimya Mühendisliği": {
        "ortalama_maas_aylik": 35750,
        "aylik_maas_araligi": "20.000 TL - 35.000 TL",
        "yorum": "İlaç, gıda ve kimya sektörlerinde iş bulma imkanı vardır."
    },
    "Kontrol ve Otomasyon Mühendisliği": {
        "ortalama_maas_aylik": 41800,
        "aylik_maas_araligi": "25.000 TL - 45.000 TL",
        "yorum": "Sanayi otomasyonu, robotik ve akıllı sistemler alanlarında çalışırlar."
    },
    "Lojistik Yönetimi": {
        "ortalama_maas_aylik": 25000,
        "aylik_maas_araligi": "20.000 TL - 40.000 TL",
        "yorum": "Üretim ve e-ticaret şirketlerinde operasyonel pozisyonlar bulunur."
    },
    "Makine Mühendisliği": {
        "ortalama_maas_aylik": 36550,
        "aylik_maas_araligi": "22.000 TL - 45.000 TL",
        "yorum": "Sanayi ve üretim sektöründe yoğunlukla tercih edilen bir alandır."
    },
    "Mali Müşavirlik": {
        "ortalama_maas_aylik": 26000,
        "aylik_maas_araligi": "20.000 TL - 40.000 TL",
        "yorum": "Tecrübe ve portföye göre maaşlar artış gösterir."
    },
    "Matematik Mühendisliği": {
        "ortalama_maas_aylik": 65300,
        "aylik_maas_araligi": "25.000 TL - 50.000 TL",
        "yorum": "Finans, teknoloji ve sigortacılık gibi alanlarda geniş iş imkanları bulunur."
    },
    "Metalurji ve Malzeme Mühendisliği": {
        "ortalama_maas_aylik": 40400,
        "aylik_maas_araligi": "22.000 TL - 40.000 TL",
        "yorum": "Otomotiv, havacılık ve savunma sanayi gibi alanlarda çalışırlar."
    },
    "Mimar": {
        "ortalama_maas_aylik": 45550,
        "aylik_maas_araligi": "30.000 TL - 60.000 TL",
        "yorum": "Mimarlık fakültesi mezunlarının icra ettiği bir meslektir."
    },
    "Moleküler Biyoloji ve Genetik": {
        "ortalama_maas_aylik": 28000,
        "aylik_maas_araligi": "22.000 TL - 45.000 TL",
        "yorum": "Biyoteknoloji ve ilaç sektörlerinde araştırma pozisyonları bulunur."
    },
    "Otomotiv Mühendisliği": {
        "ortalama_maas_aylik": 41600,
        "aylik_maas_araligi": "25.000 TL - 45.000 TL",
        "yorum": "Otomotiv sektöründe tasarım, üretim ve Ar-Ge pozisyonları bulunur."
    },
    "Petrol ve Doğalgaz Mühendisliği": {
        "ortalama_maas_aylik": 56500,
        "aylik_maas_araligi": "60.000 TL - 100.000 TL",
        "yorum": "Enerji sektöründe yüksek maaş potansiyeli sunan bir alandır."
    },
    "Pilotaj": {
        "ortalama_maas_aylik": 85000,
        "aylik_maas_araligi": "70.000 TL - 150.000 TL+",
        "yorum": "Yüksek eğitim maliyeti ve zorlu süreçlere karşılık çok yüksek maaş imkanı."
    },
    "Psikolog": {
        "ortalama_maas_aylik": 32100,
        "aylik_maas_araligi": "18.000 TL - 40.000 TL",
        "yorum": "Klinik tecrübe ve uzmanlaşmaya göre maaşlar artabilir."
    },
    "Reklamcılık": {
        "ortalama_maas_aylik": 21000,
        "aylik_maas_araligi": "18.000 TL - 30.000 TL",
        "yorum": "Ajanslar veya şirketlerin pazarlama departmanlarında çalışabilirler."
    },
    "Sanat ve Tasarım": {
        "ortalama_maas_aylik": 20000,
        "aylik_maas_araligi": "15.000 TL - 30.000 TL",
        "yorum": "Freelance ve proje bazlı işler yaygındır. İstikrarsızlık maaş potansiyelini etkileyebilir."
    },
    "Sanat Tarihi": {
        "ortalama_maas_aylik": 18000,
        "aylik_maas_araligi": "15.000 TL - 25.000 TL",
        "yorum": "Müzeler, galeriler ve kültürel kurumlar gibi yerlerde çalışabilirler."
    },
    "Sınıf Öğretmeni": {
        "ortalama_maas_aylik": 33200,
        "aylik_maas_araligi": "30.000 TL - 50.000 TL",
        "yorum": "İlkokul öğrencilerine eğitim verirler."
    },
    "Şehir ve Bölge Planlama": {
        "ortalama_maas_aylik": 20000,
        "aylik_maas_araligi": "18.000 TL - 30.000 TL",
        "yorum": "Kamu kurumları ve özel danışmanlık firmalarında iş bulabilirler."
    },
    "Tıp": {
        "ortalama_maas_aylik": 60000,
        "aylik_maas_araligi": "50.000 TL - 100.000 TL+",
        "yorum": "Uzun ve zorlu bir eğitim süreci sonrası yüksek maaş potansiyeli. Kamu ve özel sektör maaşları farklılık gösterir."
    },
    "Turizm İşletmeciliği": {
        "ortalama_maas_aylik": 18000,
        "aylik_maas_araligi": "16.000 TL - 25.000 TL",
        "yorum": "Otel ve seyahat acentelerinde yönetici pozisyonları mevcuttur."
    },
    "Uçak Bakım Mühendisliği": {
        "ortalama_maas_aylik": 60450,
        "aylik_maas_araligi": "30.000 TL - 50.000 TL",
        "yorum": "Havacılık sektörünün vazgeçilmez bir parçasıdır."
    },
    "Uçak Mühendisliği": {
        "ortalama_maas_aylik": 57000,
        "aylik_maas_araligi": "30.000 TL - 60.000 TL",
        "yorum": "Havacılık ve savunma sanayinde yüksek talep gören bir meslektir."
    },
    "Yazılım Mühendisliği": {
        "ortalama_maas_aylik": 39300,
        "aylik_maas_araligi": "20.000 TL - 70.000 TL",
        "yorum": "Yüksek talep gören bir alan ancak rekabet de çok yoğun. Mezuniyet sonrası ilk 6 ay kritik öneme sahip."
    },
    "Yönetim Bilişim Sistemleri": {
        "ortalama_maas_aylik": 26000,
        "aylik_maas_araligi": "20.000 TL - 40.000 TL",
        "yorum": "İşletme ve teknolojiyi birleştiren bir alandır."
    },
    "Yönetim Danışmanlığı": {
        "ortalama_maas_aylik": 40000,
        "aylik_maas_araligi": "30.000 TL - 70.000 TL",
        "yorum": "Büyük şirketlere stratejik konularda danışmanlık yaparlar."
    }
}


@app.route("/")
def index():
    """
    Ana sayfayı işler. Sadece HTML şablonunu gönderir.
    """
    bolum_list = sorted(list(bolum_verileri.keys()))
    return render_template("index.html", bolum_list=bolum_list)

@app.route("/calculate", methods=["POST"])
def calculate():
    """
    Hesaplama işlemini yapar ve sonucu JSON olarak döndürür.
    Sayfa yeniden yüklenmez.
    """
    try:
        data = request.get_json()
        bolum = data.get("bolum")
        mezuniyet_tarihi_str = data.get("mezuniyet")

        if not bolum or not mezuniyet_tarihi_str:
            return jsonify({"error": "Lütfen tüm alanları doldurun."}), 400

        mezuniyet_tarihi = datetime.datetime.strptime(mezuniyet_tarihi_str, "%Y-%m-%d").date()
        bugun = datetime.date.today()

        if mezuniyet_tarihi > bugun:
            return jsonify({"error": "Mezuniyet tarihi gelecekte olamaz."}), 400

        gecen_gun_sayisi = (bugun - mezuniyet_tarihi).days
        
        if bolum in bolum_verileri:
            bolum_data = bolum_verileri[bolum]
            aylik_maas = bolum_data["ortalama_maas_aylik"]
            gunluk_maas = aylik_maas / 30.0
            toplam_kayip = gunluk_maas * gecen_gun_sayisi
            
            sonuc = {
                "bolum": bolum,
                "gecen_gun_sayisi": gecen_gun_sayisi,
                "aylik_maas": aylik_maas,
                "toplam_kayip": toplam_kayip,
                "maas_araligi": bolum_data["aylik_maas_araligi"],
                "yorum": bolum_data["yorum"]
            }
            return jsonify(sonuc)
        else:
            return jsonify({"error": "Geçersiz bölüm seçimi."}), 400

    except Exception as e:
        return jsonify({"error": f"Bir hata oluştu: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

