import sqlite3

def test_readonly():
    try:
        conn = sqlite3.connect('kazanc.db')
        
        # Test ekleme
        conn.execute("INSERT INTO bolumler (bolum_adi, aylik_maas_tr, aylik_maas_araligi_tr, yorum) VALUES (?, ?, ?, ?)",
                    ('TEST BOLUM', 999, '999₺', 'Test'))
        conn.commit()
        print("✅ Yazma işlemi BAŞARILI!")
        
        # Test silme
        conn.execute("DELETE FROM bolumler WHERE bolum_adi = 'TEST BOLUM'")
        conn.commit()
        print("✅ Silme işlemi BAŞARILI!")
        
        conn.close()
        print("🎉 Veritabanı tamamen YAZILABILIR!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    test_readonly()