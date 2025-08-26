import sqlite3

def check_database():
    conn = sqlite3.connect('kazanc.db')
    cursor = conn.cursor()
    
    # Tabloları listele
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablolar = cursor.fetchall()
    print("Tablolar:", tablolar)
    
    # Bölümleri listele
    cursor.execute("SELECT * FROM bolumler")
    bolumler = cursor.fetchall()
    print(f"\nToplam {len(bolumler)} bölüm bulundu:")
    for bolum in bolumler:
        print(f"- {bolum[1]}: {bolum[2]}₺")
    
    conn.close()

if __name__ == "__main__":
    check_database()