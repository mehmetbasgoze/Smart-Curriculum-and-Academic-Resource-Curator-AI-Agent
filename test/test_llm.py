import os
from langchain_google_vertexai import ChatVertexAI

# Servis hesabımızı (kimlik.json) kullanmaya devam ediyoruz
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "kimlik.json"

# İŞTE BÜYÜK DEĞİŞİKLİK: Görselde yazan asıl Proje ID'miz!
PROJECT_ID = "smart-syllabus-agent"
LOCATION = "us-central1"

print("Projeye bağlanılıyor...\n")

try:
    llm = ChatVertexAI(
        model_name="gemini-2.5-flash",
        project=PROJECT_ID,
        location=LOCATION,
        temperature=0.3
    )

    cevap = llm.invoke("Bana bir yapay zeka ajanının (AI Agent) geleneksel bir yazılımdan temel farkını tek cümleyle açıkla.")
    
    print("BAŞARILI! Vertex AI (Gemini) Cevabı:")
    print("-" * 30)
    print(cevap.content) 

except Exception as e:
    print("Hata detayı:", e)