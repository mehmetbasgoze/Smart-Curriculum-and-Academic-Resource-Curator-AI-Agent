import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_vertexai import ChatVertexAI

# 1. Kimlik ve Proje Ayarları (O okyanusu aştığımız kısım)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "kimlik.json"
PROJECT_ID = "smart-syllabus-agent"
LOCATION = "us-central1"

print("1. Adım: Müfredat PDF'i okunuyor...")
# 2. PDF'i Okuma
try:
    loader = PyPDFLoader("mufredat.pdf")
    sayfalar = loader.load()
    # Tüm sayfaların metnini birleştiriyoruz
    pdf_metni = "\n".join([sayfa.page_content for sayfa in sayfalar])
    print("-> PDF başarıyla okundu.\n")
except Exception as e:
    print("PDF okunurken hata oluştu:", e)
    exit()

print("2. Adım: Ajan, müfredatı analiz ediyor (Vertex AI devrede)...")
# 3. Modeli Başlatma
llm = ChatVertexAI(
    model_name="gemini-2.5-flash",
    project=PROJECT_ID,
    location=LOCATION,
    temperature=0.3 # Analitik ve net cevaplar için yaratıcılığı düşük tutuyoruz
)

# 4. Ajanın Talimatı (Prompt Engineering)
# Modele tam olarak ne yapması gerektiğini ve hangi veriyi kullanacağını söylüyoruz.
prompt = f"""
Sen uzman bir akademik asistan ve eğitim küratörüsün.
Aşağıda sana bir dersin müfredatını (izlencesini) veriyorum. 
Bu metni dikkatlice analiz et ve aşağıdaki bilgileri çıkar:
1. Bu dersin temel amacı nedir? (Tek cümleyle)
2. Öğrencilerin bu dersten edineceği en önemli 3 öğrenim kazanımını (hedefini) maddeler halinde listele.

İşte Müfredat Metni:
---------------------
{pdf_metni}
---------------------
"""

# 5. Ajanı Çalıştırma
try:
    cevap = llm.invoke(prompt)
    print("\nBAŞARILI! Ajanın Analiz Raporu:")
    print("=" * 50)
    print(cevap.content)
    print("=" * 50)
except Exception as e:
    print("Vertex AI'a bağlanırken hata:", e)