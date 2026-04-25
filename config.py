import os
import streamlit as st
import json
import tempfile

# 1. BULUT İÇİN AĞ TIKANIKLIĞI 
# Streamlit Cloud üzerinde Vertex AI'ın gRPC protokolünde donmasını engelle
os.environ["GRPC_DNS_RESOLVER"] = "native"

KIMLIK_DOSYASI = "kimlik.json"

# 2. AKILLI KİMLİK YÖNETİMİ
if os.path.exists(KIMLIK_DOSYASI):
    # Yerel bilgisayarındaysan (Localhost) doğrudan dosyayı kullan
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KIMLIK_DOSYASI
else:
    # Bulut sunucusundaysan Streamlit Secrets'ı devreye sok
    try:
        # Secrets'tan JSON verisini al
        secret_dict = dict(st.secrets["gcp_service_account"])
        
        # Olası bir TOML ayrıştırma hatasına karşı Private Key'deki "\n" metinlerini gerçek alt satıra çevir
        if "\\n" in secret_dict["private_key"]:
            secret_dict["private_key"] = secret_dict["private_key"].replace("\\n", "\n")
            
        # İşletim sisteminin en güvenli/yazılabilir "Geçici (Temp)" klasörüne kimliği kaydet
        temp_path = os.path.join(tempfile.gettempdir(), "gcp_temp_key.json")
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(secret_dict, f)
            
        # Google sistemlerine bu güvenli yolu göster
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_path
        
    except Exception as e:
        # Eğer bir hata olursa sonsuza kadar bekleme, anında sistemi durdur ve ekrana hata bas
        st.error(f"🚨 Kimlik Doğrulama Hatası: Streamlit Secrets okunamadı. Detay: {e}")
        st.stop()

# --- PROJE SABİTLERİ ---
PROJECT_ID = "smart-syllabus-agent"
LOCATION = "us-central1"
MODEL_NAME = "gemini-2.5-flash"