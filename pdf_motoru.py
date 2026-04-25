import os
from langchain_community.document_loaders import PyPDFLoader

def mufredat_metnini_cikar(dosya_yolu):
    """Verilen dosyayı doğrular, okur ve metni döndürür."""
    
    #Uzantı kontrolü (Sadece PDF)
    if not dosya_yolu.lower().endswith('.pdf'):
        raise ValueError("❌ Geçersiz Format: Lütfen sadece PDF formatında bir ders izlencesi yükleyin.")

    #Dosya gerçekten bilgisayarda var mı?
    if not os.path.exists(dosya_yolu):
        raise FileNotFoundError(f"❌ Dosya Bulunamadı: '{dosya_yolu}' sistemde yok.")

    try:
        loader = PyPDFLoader(dosya_yolu)
        sayfalar = loader.load()
        
        pdf_metni = "\n".join([sayfa.page_content for sayfa in sayfalar]).strip()
        
        #PDF resimden mi ibaret? (Metin çok kısaysa)
        if len(pdf_metni) < 50:
            raise ValueError("❌ Okunabilir Metin Yok: PDF içeriği okunamadı. Dosya taranmış bir resim olabilir.")
            
        return pdf_metni
        
    except Exception as e:
        # LangChain veya başka bir kütüphane hatasını yakalama
        raise Exception(f"PDF İşleme Hatası: {str(e)}")