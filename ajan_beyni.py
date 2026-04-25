from langchain_google_vertexai import ChatVertexAI
from langchain_community.tools import DuckDuckGoSearchResults, YouTubeSearchTool
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
import config  

def llm_olustur(temperature=0.2):
    return ChatVertexAI(
        model=config.MODEL_NAME,
        project=config.PROJECT_ID,
        location=config.LOCATION,
        temperature=temperature 
    )

def mufredati_analiz_et(pdf_metni):
    llm = llm_olustur()
    analiz_prompt = f"""
    Aşağıdaki müfredatı analiz et.
    1. Zorluk seviyesini (Giriş / Orta / İleri Seviye) belirle.
    2. En kritik 3 araştırma konusunu seç.
    Cevabını KESİNLİKLE şu formatta ver (aralarına | koy): 
    Zorluk Seviyesi | Konu1, Konu2, Konu3
    Müfredat: {pdf_metni}
    """
    
    try:
        response = llm.invoke(analiz_prompt)
        content = response.content
        
        #Gelen yanıt liste mi yoksa metin mi kontrol et ve temizle
        if isinstance(content, list):
            analiz_sonuc = "".join([p.get('text', '') if isinstance(p, dict) else str(p) for p in content]).strip()
        else:
            analiz_sonuc = str(content).strip()
        
        if "|" not in analiz_sonuc:
            raise ValueError("Yapay zeka beklenen formatta (Zorluk | Konular) yanıt veremedi.")
            
        zorluk_seviyesi, aranacak_konular_str = analiz_sonuc.split("|", 1)
        konular_listesi = [k.strip() for k in aranacak_konular_str.split(",") if k.strip()]
        
        return zorluk_seviyesi.strip(), konular_listesi
        
    except Exception as e:
        raise Exception(f"Analiz Modülü Çöktü: {str(e)}")

def arama_ajani_olustur(zorluk_seviyesi):
    llm = llm_olustur()
    
    #Ajanın araç çantasına DuckDuckGo'nun yanına YouTube'u da ekledik
    arama_araci = DuckDuckGoSearchResults(max_results=3)
    youtube_araci = YouTubeSearchTool()
    
    tools = [arama_araci, youtube_araci]
    
    ajan_prompt = ChatPromptTemplate.from_messages([
        ("system", f"""Sen akademik bir asistansın. Zorluk: {zorluk_seviyesi}. 
        Görevin:
        1. Sana verilen TEK BİR konu için arama yap.
        2. Akademik makaleler için internet arama aracını, eğitici videolar için KESİNLİKLE YouTube aracını kullan.
        3. İlk bulduğun 2 makaleyi ve en ilgili 1 YouTube videosunu seç. Mükemmeli aramak için sürekli döngüye girme.
        4. Çıktını KESİNLİKLE aşağıdaki formatta ver:
        
        **📚 Akademik Makaleler:**
        **[Makale Başlığı]**
        - **Özet:** (Kısa özet)
        - **Link:** (Kaynak linki)
        - **Neden Bu Kaynak:** (Bu kaynağın {zorluk_seviyesi} seviyesine neden uygun olduğunu açıkla)
        
        **🎥 Önerilen Eğitim Videosu:**
        - **Video Linki:** (YouTube Linki)
        - **Neden Bu Video:** (Videonun {zorluk_seviyesi} seviyesindeki bir öğrenciye nasıl fayda sağlayacağını açıkla)
        """),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    ajan = create_tool_calling_agent(llm, tools, ajan_prompt)
    
    return AgentExecutor(
        agent=ajan, 
        tools=tools, 
        verbose=False, 
        # Ajan iki farklı platformda arama yapacağı için düşünme payını (3'ten 5'e) ve süreyi artırdık
        max_iterations=5, 
        max_execution_time=45,
        handle_parsing_errors=True
    )

def calisma_programi_olustur(raporlar_dict, zorluk_seviyesi):
    """Bulunan tüm kaynakları okuyup mantıklı bir çalışma yol haritası çıkarır."""
    llm = llm_olustur()
    
    # Tüm kaynakları tek bir metin bloğunda birleştiriyoruz
    derlenmis_kaynaklar = ""
    for konu, icerik in raporlar_dict.items():
        derlenmis_kaynaklar += f"\n--- {konu} ---\n{icerik}\n"
        
    danisman_prompt = f"""Sen uzman bir akademik mentör ve eğitim planlayıcısısın. 
    Öğrencinin seviyesi: {zorluk_seviyesi}.
    
    Aşağıda, öğrencinin çalışması gereken konular ve bu konular için yapay zeka tarafından özel olarak bulunmuş akademik makaleler ve eğitici YouTube videoları bulunmaktadır.
    
    Görevin: Bu kaynakları mantıklı bir pedagojik sıraya koyarak, adım adım bir "Çalışma Programı (Road Map)" oluşturmak.
    - Hangi gün/adımda hangi makalenin okunması gerektiğini,
    - Hangi videonun konuyu pekiştirmek için makaleden önce veya sonra izlenmesi gerektiğini planla.
    - {zorluk_seviyesi} seviyesindeki bir öğrencinin bilişsel yükünü hesaba katarak programı hazırla.
    
    Bulunan Kaynaklar:
    {derlenmis_kaynaklar}
    
    Çıktını sadece programı içerecek şekilde, Markdown formatında, şık ve motive edici bir dille ver. Ekstra giriş veya çıkış cümleleri kullanma.
    """
    
    try:
        response = llm.invoke(danisman_prompt)
        content = response.content
        
        # Liste veya metin kontrolü
        if isinstance(content, list):
            return "".join([p.get('text', '') if isinstance(p, dict) else str(p) for p in content]).strip()
        return str(content).strip()
    except Exception as e:
        return f"Yol haritası oluşturulurken hata meydana geldi: {str(e)}"