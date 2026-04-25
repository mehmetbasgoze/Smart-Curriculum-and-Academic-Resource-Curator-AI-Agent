from langchain_community.document_loaders import PyPDFLoader 

dosya_yolu = "mufredat.pdf"

print(f"Ajanın gözleri açılıyor: {dosya_yolu} dosyası okunuyor...\n")

try:
    # PyPDFLoader ile PDF dosyasını LangChain'in işleyebileceği sayfalara bölüyoruz
    loader = PyPDFLoader(dosya_yolu)
    sayfalar = loader.load()

    print(f"BAŞARILI! Toplam {len(sayfalar)} sayfa bulundu.")
    
    # Modelin okuyacağı metnin içeriğini test etmek için ilk sayfanın bir kısmını yazdıralım
    print("\n--- İlk Sayfadan Örnek Metin (İlk 300 Karakter) ---")
    print(sayfalar[0].page_content[:300])

except FileNotFoundError:
    print(f"HATA: '{dosya_yolu}' adında bir dosya klasörde bulunamadı.")
except Exception as e:
    print("Beklenmeyen bir hata oluştu:", e)