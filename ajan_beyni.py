from langchain_google_vertexai import ChatVertexAI
from ddgs import DDGS
from youtube_search import YoutubeSearch
import config  
import time

# ==========================================
# 1. LLM FABRİKASI
# ==========================================
def llm_olustur(temperature=0.3):
    return ChatVertexAI(
        model=config.MODEL_NAME,
        project=config.PROJECT_ID,
        location=config.LOCATION,
        temperature=temperature,
        max_retries=2,
        timeout=60 
    )

# ==========================================
# 2. YARDIMCI: LLM YANIT ÇÖZÜCÜ
# ==========================================
def _llm_yanit_al(response):
    """LLM yanıtını temiz string olarak döndürür."""
    content = response.content
    if isinstance(content, list):
        return "".join([p.get('text', '') if isinstance(p, dict) else str(p) for p in content]).strip()
    return str(content).strip()

# ==========================================
# 3. YARDIMCI: WEB ARAMA (DDGS DOĞRUDAN API)
# ==========================================
def web_ara(sorgu, max_sonuc=5):
    """DuckDuckGo ile doğrudan web araması yapar. Agent kullanmaz."""
    try:
        ddgs = DDGS()
        sonuclar = list(ddgs.text(sorgu, max_results=max_sonuc))
        return sonuclar  # [{"title": ..., "body": ..., "href": ...}, ...]
    except Exception as e:
        return []

def youtube_ara(sorgu, max_sonuc=3):
    """YouTube'da video araması yapar."""
    try:
        sonuclar = YoutubeSearch(sorgu, max_results=max_sonuc).to_dict()
        return sonuclar
    except Exception:
        return []

# ==========================================
# 4. ADIM 1: PDF'DEN DERS ADINI TESPİT ET
# ==========================================
def ders_adini_tespit_et(pdf_metni):
    """PDF metninden ana ders adını AI ile tespit eder."""
    llm = llm_olustur(temperature=0.1)
    
    prompt = f"""Aşağıdaki belgeyi analiz et. Bu bir üniversite ders müfredatı veya ders içeriği belgesidir.

    GÖREVİN:
    1. Belgede birden fazla ders listeleniyorsa (ör: bölüm müfredatı), en ağırlıklı/ana dersi seç.
    2. Eğer belge tek bir derse aitse, o dersin adını belirle.
    3. Dersin akademik zorluk seviyesini belirle (Lisans / Yüksek Lisans / Doktora).
    
    CEVABINI KESİNLİKLE ŞU FORMATTA VER (aralarına | koy):
    Ders Adı | Seviye
    
    Örnek: Makine Öğrenmesi | Yüksek Lisans
    
    Sadece bu formatı ver, başka hiçbir şey yazma.
    
    Belge Metni:
    {pdf_metni[:3000]}
    """
    
    try:
        response = llm.invoke(prompt)
        sonuc = _llm_yanit_al(response)
        
        if "|" not in sonuc:
            raise ValueError("AI beklenen formatta yanıt veremedi.")
        
        ders_adi, seviye = sonuc.split("|", 1)
        return ders_adi.strip(), seviye.strip()
        
    except Exception as e:
        raise Exception(f"Ders adı tespit hatası: {str(e)}")

# ==========================================
# 5. ADIM 2: İNTERNETTE DERS MÜFREDATİ ARA
# ==========================================
def ders_icerigini_internetten_ara(ders_adi):
    """Ders adını kullanarak internette o dersin detaylı müfredatını arar."""
    
    sorgular = [
        f"{ders_adi} ders içeriği haftalık konular syllabus",
        f"{ders_adi} course syllabus topics weekly",
        f"{ders_adi} müfredat konu başlıkları üniversite",
    ]
    
    tum_sonuclar = []
    for sorgu in sorgular:
        sonuclar = web_ara(sorgu, max_sonuc=4)
        tum_sonuclar.extend(sonuclar)
        time.sleep(1)  # Rate limit koruması
    
    # Sonuçları metin olarak birleştir
    icerik_metni = ""
    for i, s in enumerate(tum_sonuclar):
        icerik_metni += f"\n--- Kaynak {i+1}: {s.get('title', '')} ---\n"
        icerik_metni += f"{s.get('body', '')}\n"
        icerik_metni += f"URL: {s.get('href', '')}\n"
    
    return icerik_metni

# ==========================================
# 6. ADIM 3: ALT KONULARA AYIR (TEMELDEN İLERİYE)
# ==========================================
def alt_konulara_ayir(ders_adi, web_sonuclari, pdf_metni, seviye):
    """Ders adı, web sonuçları ve PDF metnini kullanarak dersi alt konulara ayırır."""
    llm = llm_olustur(temperature=0.2)
    
    prompt = f"""Sen bir üniversite profesörüsün. "{ders_adi}" dersinin müfredatını oluşturacaksın.

    ELINDE OLAN VERİLER:
    1. Öğrencinin yüklediği PDF'den çıkan metin:
    {pdf_metni[:2000]}
    
    2. İnternetten bulunan bu derse ait müfredat/içerik bilgileri:
    {web_sonuclari[:3000]}
    
    GÖREVİN:
    Bu verileri analiz ederek "{ders_adi}" dersini 8 ile 12 arasında alt konuya böl.
    
    KRİTİK KURALLAR:
    1. Alt konular KRONOLOJİK ve PEDAGOJİK sırayla olmalı: TEMEL kavramlardan başla, İLERİ konulara doğru ilerle.
    2. Her alt konu sadece bir anahtar kelime DEĞİL, açıklayıcı bir başlık olmalı (ör: "Doğrusal Regresyon ve En Küçük Kareler Yöntemi").
    3. Sıralama mantıksal olmalı: Bir konuyu anlamak için önceki konunun bilinmesi gerekir.
    4. Akademik seviye: {seviye}
    
    CEVABINI KESİNLİKLE ŞU FORMATTA VER (her satıra bir konu, başına numara koy):
    1. [Temel Konu Başlığı]
    2. [Bir Sonraki Konu]
    3. [...]
    ...
    
    Sadece numaralı listeyi ver, başka açıklama yazma.
    """
    
    try:
        response = llm.invoke(prompt)
        sonuc = _llm_yanit_al(response)
        
        # Numaralı listeyi parse et
        konular = []
        for satir in sonuc.split('\n'):
            satir = satir.strip()
            if satir and satir[0].isdigit():
                # "1. Konu başlığı" formatından konuyu çıkar
                konu = satir.split('.', 1)[-1].strip()
                if konu:
                    konular.append(konu)
        
        if len(konular) < 3:
            raise ValueError("Yeterli sayıda alt konu oluşturulamadı.")
        
        return konular
        
    except Exception as e:
        raise Exception(f"Alt konu analiz hatası: {str(e)}")

# ==========================================
# 7. ADIM 4: HER ALT KONU İÇİN KAYNAK BUL
# ==========================================
def konu_icin_kaynak_bul(ders_adi, alt_konu, sira_no, toplam_konu):
    """Tek bir alt konu için seviyeye uygun akademik kaynaklar ve videolar bulur."""
    
    # Konunun seviyesini sıra numarasına göre belirle
    oran = sira_no / toplam_konu
    if oran <= 0.33:
        seviye_etiketi = "Temel (Giriş)"
        seviye_anahtar = "giriş temel tutorial başlangıç"
    elif oran <= 0.66:
        seviye_etiketi = "Orta"
        seviye_anahtar = "orta seviye uygulama"
    else:
        seviye_etiketi = "İleri"
        seviye_anahtar = "ileri düzey advanced"
    
    # --- WEB KAYNAKLARI ---
    web_sorgu = f"{ders_adi} {alt_konu} {seviye_anahtar} ders notu"
    web_sonuclar = web_ara(web_sorgu, max_sonuc=4)
    
    time.sleep(1)
    
    # --- YOUTUBE VİDEOLARI ---
    video_sorgu = f"{ders_adi} {alt_konu} ders anlatım"
    videolar = youtube_ara(video_sorgu, max_sonuc=2)
    
    # --- LLM İLE KAYNAK ÖZETİ OLUŞTUR ---
    llm = llm_olustur(temperature=0.2)
    
    # Web sonuçlarını formatlı metin yap
    web_metin = ""
    for i, s in enumerate(web_sonuclar):
        web_metin += f"  {i+1}. {s.get('title', 'Başlık yok')}\n"
        web_metin += f"     Özet: {s.get('body', '')}\n"
        web_metin += f"     Link: {s.get('href', '')}\n\n"
    
    video_metin = ""
    for v in videolar:
        video_url = f"https://www.youtube.com{v.get('url_suffix', '')}"
        video_metin += f"  - {v.get('title', 'Video')} ({v.get('duration', '?')}) - {v.get('channel', '?')}\n"
        video_metin += f"    Link: {video_url}\n\n"
    
    prompt = f""""{ders_adi}" dersi kapsamında "{alt_konu}" konusu için kaynak raporu hazırla.
    Bu konu dersin {sira_no}. alt konusu (toplam {toplam_konu} konu). Seviye: {seviye_etiketi}.
    
    BULUNAN WEB KAYNAKLARI:
    {web_metin if web_metin else "Web araması sonuç döndürmedi."}
    
    BULUNAN VİDEOLAR:
    {video_metin if video_metin else "Video araması sonuç döndürmedi."}
    
    GÖREVİN: Yukarıdaki kaynakları değerlendirerek şu formatta bir özet yaz:
    
    **📚 Önerilen Kaynaklar ({seviye_etiketi}):**
    (Her kaynak için: başlık, kısa açıklama, link ve neden bu seviyeye uygun olduğu)
    
    **🎥 Önerilen Videolar:**
    (Video başlığı, süre, kanal ve neden izlenmeli)
    
    **📝 Konu Özeti:**
    (Bu alt konunun kapsamını ve öğrenme hedeflerini 2-3 cümleyle özetle)
    
    Kaynakların gerçek linklerini kullan, link uydurma.
    """
    
    try:
        response = llm.invoke(prompt)
        return _llm_yanit_al(response)
    except Exception as e:
        # Fallback: Ham sonuçları formatla
        fallback = f"**📚 Bulunan Kaynaklar ({seviye_etiketi}):**\n{web_metin}\n\n**🎥 Bulunan Videolar:**\n{video_metin}"
        return fallback

# ==========================================
# 8. ADIM 5: DERS NOTU SENTEZLE (BÖLÜM BÖLÜM)
# ==========================================
def _tek_bolum_notu_olustur(ders_adi, konu, konu_icerigi, bolum_no, toplam_bolum, seviye):
    """Tek bir alt konu için ders notu bölümü oluşturur."""
    llm = llm_olustur(temperature=0.4)
    
    # Konunun seviyesini belirle
    oran = bolum_no / toplam_bolum
    if oran <= 0.33:
        konu_seviyesi = "Temel"
    elif oran <= 0.66:
        konu_seviyesi = "Orta"
    else:
        konu_seviyesi = "İleri"
    
    prompt = f"""Sen uzman bir üniversite profesörüsün. 
    Ders: "{ders_adi}" | Akademik Seviye: {seviye}
    
    Aşağıda bu dersin {bolum_no}. alt konusu ({toplam_bolum} alt konu içinden) ve bu konu için bulunan kaynaklar var.
    Konu Seviyesi: {konu_seviyesi}
    
    ALT KONU: {konu}
    
    BULUNAN KAYNAKLAR VE BİLGİLER:
    {str(konu_icerigi)[:3000]}
    
    GÖREVİN: Yukarıdaki bilgileri kullanarak bu TEK ALT KONU için bir DERS NOTU BÖLÜMÜ yaz.
    
    KURALLAR:
    1. Konuyu {konu_seviyesi} seviyeye uygun derinlikte AÇIKLA: tanımlar yap, teorik altyapıyı özetle, önemli kavramları detaylandır.
    2. Eğer varsa formüller, pratik örnekler veya analojiler kullan.
    3. Kaynaklardaki GERÇEK linkleri kullan, KESİNLİKLE link UYDURMA. Eğer uygun bir gerçek link yoksa, link verme.
    4. Okuma önerilerini "📖 Okuma Önerisi:" ve video önerilerini "🎬 İzleme Önerisi:" şeklinde metin içine yerleştir.
    5. Ciddi, profesyonel ve eğitici bir dil kullan.
    6. Markdown formatında yaz.
    7. Bölüm başlığını "### Bölüm {bolum_no}: {konu}" olarak başlat.
    
    KRİTİK: Sadece BULUNAN KAYNAKLARDA yer alan gerçek linkleri öner. Hiçbir link uydurma.
    """
    
    max_deneme = 3
    for deneme in range(max_deneme):
        try:
            response = llm.invoke(prompt)
            return _llm_yanit_al(response)
        except Exception as e:
            hata_mesaji = str(e)
            if "429" in hata_mesaji and deneme < max_deneme - 1:
                time.sleep(15)
                continue
            return f"### Bölüm {bolum_no}: {konu}\n\n*Bu bölüm için not oluşturulamadı: {hata_mesaji}*"


def ders_notu_olustur(ders_adi, raporlar_dict, seviye, progress_callback=None):
    """Tüm alt konular için BÖLÜM BÖLÜM ders notu üretir ve birleştirir.
    
    Her alt konu için ayrı bir LLM çağrısı yapılır. Bu sayede:
    - Token limiti aşılmaz
    - Her bölüm kendi gerçek kaynaklarını kullanır
    - Uydurma link riski minimize edilir
    """
    
    konular = list(raporlar_dict.keys())
    toplam = len(konular)
    
    # Başlık
    tam_not = f"# {ders_adi}: Kapsamlı Ders Notları\n\n"
    tam_not += f"**Ders:** {ders_adi}  \n"
    tam_not += f"**Seviye:** {seviye}  \n"
    tam_not += f"**Toplam Bölüm:** {toplam}  \n\n"
    tam_not += "---\n\n"
    
    for i, konu in enumerate(konular):
        bolum_no = i + 1
        icerik = raporlar_dict[konu]
        
        if progress_callback:
            progress_callback(bolum_no, toplam, konu)
        
        bolum_notu = _tek_bolum_notu_olustur(
            ders_adi, konu, icerik, bolum_no, toplam, seviye
        )
        tam_not += bolum_notu + "\n\n---\n\n"
        
        # API rate limit koruması - her bölüm arasında bekle
        if bolum_no < toplam:
            time.sleep(5)
    
    return tam_not