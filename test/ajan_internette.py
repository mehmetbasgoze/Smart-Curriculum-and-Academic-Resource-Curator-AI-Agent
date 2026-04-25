import os
from langchain_google_vertexai import ChatVertexAI
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

# 1. Bulut Kimliğimiz
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "kimlik.json"

# 2. Ajanın Kullanacağı "Araç" (Tool) - İnternet Arama Motoru
arama_araci = DuckDuckGoSearchResults()
tools = [arama_araci]

# 3. Modelimiz (Ajanın Beyni)
llm = ChatVertexAI(
    model="gemini-2.5-flash",
    project="smart-syllabus-agent",
    location="us-central1",
    temperature=0.3
)

# 4. Ajanın Karakteri ve Talimatı (Prompt Engineering)
prompt = ChatPromptTemplate.from_messages([
    ("system", "Sen uzman bir akademik asistansın. Görevin, verilen eğitim hedeflerine uygun en güncel kaynakları internette arayıp bulmaktır. Bulduğun kaynakların linklerini ve kısa özetlerini vermelisin. Gerekirse arama aracını birden fazla kez kullanabilirsin."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 5. Ajanı İnşa Etme (Beyin + Gözler + Eller)
ajan = create_tool_calling_agent(llm, tools, prompt)

# verbose=True sayesinde ajanın arka planda internette nasıl arama yaptığını adım adım göreceğiz
ajan_calistirici = AgentExecutor(agent=ajan, tools=tools, verbose=True)

print("Ajan internete çıkıyor, araştırma yapıyor. Lütfen bekleyin...\n")

# Bir önceki adımda PDF'ten çıkardığımız kazanımlardan birini hedef olarak veriyoruz
hedef_kazanim = "Yapay zekanın sağlık ve eğitim sektörlerindeki uygulama alanları"
soru = f"Şu konu hakkında eğitim alan bir öğrenci için internetten güncel 2 kaynak (makale veya blog) bul ve linkleriyle listele: '{hedef_kazanim}'"

try:
    cevap = ajan_calistirici.invoke({"input": soru})
    # Yeni hali (Sadece temiz metni ve linkleri gösterir):
    print("\nBAŞARILI! Ajanın Kaynak Küratörlüğü Raporu:")
    print("=" * 60)
    rapor = cevap["output"]
    if isinstance(rapor, list):
        # Eğer liste gelirse içindeki text kısımlarını birleştiriyoruz
        temiz_rapor = "".join([parca.get('text', '') if isinstance(parca, dict) else str(parca) for parca in rapor])
        print(temiz_rapor)
    else:
        print(rapor)
    print("=" * 60)
except Exception as e:
    print("Hata detayı:", e)