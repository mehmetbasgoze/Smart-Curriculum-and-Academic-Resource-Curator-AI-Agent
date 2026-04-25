import streamlit as st

# ==========================================
# 1. CSS ENJEKSIYONU
# ==========================================
def css_uygula():
    """
    Premium, Senior Frontend Developer düzeyinde UI kodları.
    Minimalist, 'Dark Glassmorphism' konsepti, yüksek kaliteli tipografi ve
    Anthropic / Vercel tarzı profesyonel AI arayüz estetiğine sahiptir.
    """
    st.markdown("""
    <style>
        /* =========================================
           0. FONT IMPORT (Plus Jakarta Sans - Premium Typo)
           ========================================= */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

        /* =========================================
           1. GLOBAL RESET & ARKA PLAN
           ========================================= */
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        .stApp {
            background-color: #09090b; /* Zinc 950 */
            /* İki köşeden hafif ve çok yumuşak glow efekti */
            background-image: 
                radial-gradient(circle at 15% 0%, rgba(99, 102, 241, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 85% 100%, rgba(139, 92, 246, 0.08) 0%, transparent 40%);
            background-attachment: fixed;
            color: #fafafa;
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 4rem;
            max-width: 1100px;
        }

        /* =========================================
           2. SIDEBAR TASARIMI
           ========================================= */
        [data-testid="stSidebar"] {
            background-color: #09090b !important;
            border-right: 1px solid rgba(255, 255, 255, 0.06);
        }

        [data-testid="stSidebar"] > div:first-child {
            background: transparent;
            padding-top: 2rem;
        }

        /* Sidebar üst ince şerit */
        [data-testid="stSidebar"]::before {
            content: '';
            display: block;
            height: 2px;
            background: linear-gradient(90deg, #6366f1, #8b5cf6, #d946ef);
            opacity: 0.8;
            margin-bottom: 1rem;
        }

        /* =========================================
           3. BUTON TASARIMLARI
           ========================================= */
        /* Ana Eylem Butonları (Primary) */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            font-size: 0.95rem;
            letter-spacing: 0.3px;
            transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
            box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.25);
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            width: 100%;
        }

        div.stButton > button:first-child:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
            background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
        }

        div.stButton > button:first-child:active {
            transform: translateY(0px);
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
        }

        /* Sidebar içindeki butonlar (Secondary - Hayalet Buton) */
        [data-testid="stSidebar"] div.stButton > button:first-child {
            background: transparent;
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #e4e4e7;
            box-shadow: none;
        }

        [data-testid="stSidebar"] div.stButton > button:first-child:hover {
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.3);
            color: #ffffff;
            transform: none;
        }

        /* =========================================
           4. FILE UPLOADER TASARIMI
           ========================================= */
        [data-testid="stFileUploader"] {
            background: rgba(24, 24, 27, 0.4);
            border: 1px dashed rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: #6366f1;
            background: rgba(99, 102, 241, 0.03);
        }

        [data-testid="stFileUploader"] label {
            color: #a1a1aa !important; /* Zinc 400 */
            font-size: 0.95rem;
            font-weight: 500;
        }
        
        /* Uploader internal details (icons, standard internal text) */
        [data-testid="stFileUploadDropzone"] {
            color: #a1a1aa !important;
        }

        /* =========================================
           5. INFO / ALERT STATUS KUTULARI
           ========================================= */
        .stInfo, [data-testid="stAlert"] {
            background: rgba(39, 39, 42, 0.5) !important; /* Zinc 800 */
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 10px !important;
            color: #e4e4e7 !important;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        .stSuccess { border-left: 3px solid #10b981 !important; }
        .stWarning { border-left: 3px solid #f59e0b !important; }
        .stError   { border-left: 3px solid #ef4444 !important; }
        .stInfo    { border-left: 3px solid #6366f1 !important; }

        /* =========================================
           6. METRİK KUTUSU
           ========================================= */
        [data-testid="stMetric"] {
            background: rgba(24, 24, 27, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1.2rem 1.4rem;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(8px);
        }

        [data-testid="stMetric"]:hover {
            border-color: rgba(99, 102, 241, 0.4);
            transform: translateY(-2px);
            box-shadow: 0 10px 30px -10px rgba(99, 102, 241, 0.15);
        }

        [data-testid="stMetricLabel"] {
            color: #a1a1aa !important;
            font-size: 0.8rem !important;
            font-weight: 500 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }

        [data-testid="stMetricValue"] {
            color: #fafafa !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px !important;
        }

        /* =========================================
           7. STATUS / EXPANDER (İşlem Yükleniyor v.b.)
           ========================================= */
        .streamlit-expanderHeader,
        [data-testid="stExpander"] summary {
            font-weight: 500 !important;
            color: #e4e4e7 !important;
            background: rgba(24, 24, 27, 0.7) !important;
            border-radius: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            padding: 0.8rem 1.2rem !important;
            transition: all 0.2s ease;
        }

        [data-testid="stExpander"] summary:hover {
            background: rgba(39, 39, 42, 0.9) !important;
            border-color: rgba(255, 255, 255, 0.15) !important;
        }

        [data-testid="stExpander"] {
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-radius: 10px !important;
            background: rgba(24, 24, 27, 0.4) !important;
            backdrop-filter: blur(10px);
        }

        /* =========================================
           8. DIVIDER / AYIRICI
           ========================================= */
        hr {
            border: none !important;
            border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
            margin: 2rem 0 !important;
        }

        /* =========================================
           9. MİNİMALİST TİPOGRAFİ
           ========================================= */
        h1, h2, h3, h4, h5, h6 {
            color: #fafafa !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            letter-spacing: -0.02em !important;
        }

        p, li { color: #a1a1aa; line-height: 1.6; }

        .stMarkdown h1 { font-size: 2.5rem !important; font-weight: 800 !important; }
        .stMarkdown h2 { font-size: 1.8rem !important; font-weight: 700 !important; }
        .stMarkdown h3 { font-size: 1.3rem !important; font-weight: 600 !important; }
        .stMarkdown h4 { font-size: 1.1rem !important; font-weight: 600 !important; color: #f4f4f5 !important; }

        /* =========================================
           10. SCROLLBAR TASARIMI (ZARİF)
           ========================================= */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.4); }

        /* =========================================
           11. ANİMASYONLAR
           ========================================= */
        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(15px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        
        .animate-fade-up {
            animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        /* =========================================
           12. ÖZEL HTML BİLEŞEN SINIFLARI (GLASSMORPHISM)
           ========================================= */

        /* Hero Kartı */
        .glass-card {
            background: rgba(24, 24, 27, 0.5); /* Zinc 900, 50% ops */
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 2.5rem 2rem;
            text-align: center;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        }

        /* Konu / Özellik Kartı */
        .item-card {
            background: rgba(24, 24, 27, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 1rem 1.25rem;
            margin-bottom: 0.75rem;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .item-card:hover {
            background: rgba(39, 39, 42, 0.5);
            border-color: rgba(99, 102, 241, 0.3);
            transform: translateX(4px);
        }

        .item-icon {
            font-size: 1.25rem;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            flex-shrink: 0;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .item-title {
            color: #fafafa;
            font-weight: 500;
            font-size: 0.95rem;
        }
        
        .item-desc {
            color: #a1a1aa;
            font-size: 0.8rem;
            margin-top: 0.2rem;
        }

        /* Modern Badge */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: rgba(99, 102, 241, 0.1);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 6px;
            padding: 0.25rem 0.6rem;
            font-size: 0.75rem;
            font-weight: 600;
            color: #818cf8; /* Soft Indigo */
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 1rem;
        }

        /* İnce Çizgi Ayırıcı */
        .divider {
            height: 1px;
            background: linear-gradient(90deg, 
                transparent 0%, 
                rgba(255,255,255,0.1) 50%, 
                transparent 100%);
            margin: 1.5rem 0;
        }

        /* Sonuç Rapor Kartı */
        .report-card {
            background: rgba(24, 24, 27, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.25rem;
            backdrop-filter: blur(12px);
        }
        
        .report-header {
            display: flex; 
            align-items: center; 
            gap: 0.6rem; 
            margin-bottom: 1rem;
            padding-bottom: 0.8rem; 
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* Sidebar Bilgi Hapları */
        .chip {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            border-radius: 20px;
            padding: 0.25rem 0.75rem;
            font-size: 0.75rem;
            font-weight: 500;
            color: #34d399; /* Emerald 400 */
            display: inline-flex;
            align-items: center;
        }

        /* Adım / Kılavuz Listesi */
        .step-item {
            display: flex; 
            align-items: flex-start; 
            gap: 0.75rem; 
            margin-bottom: 0.8rem; 
        }
        .step-number {
            width: 20px; 
            height: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
            display: flex; 
            align-items: center; 
            justify-content: center;
            font-size: 0.7rem; 
            font-weight: 600; 
            color: #d4d4d8; 
            flex-shrink: 0;
            margin-top: 0.1rem;
        }
        .step-text { 
            color: #a1a1aa; 
            font-size: 0.85rem; 
            font-weight: 400; 
            line-height: 1.4;
        }

        /* Dosya istatistikleri (Yüklemeden Sonra) */
        .stat-bar {
            display: flex; 
            gap: 0.5rem; 
            flex-wrap: wrap; 
            margin-top: 1rem;
        }
        .stat-pill {
            background: rgba(39, 39, 42, 0.6);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 6px;
            padding: 0.3rem 0.6rem;
            font-size: 0.75rem;
            color: #d4d4d8;
        }

        /* Linear Gradient Text Class */
        .text-gradient {
            background: linear-gradient(135deg, #a5b4fc 0%, #d8b4fe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

    </style>
    """, unsafe_allow_html=True)


# ==========================================
# 2. BİLEŞENLER / COMPONENTS (HTML RENDERER)
# ==========================================

def sidebar_logo_goster():
    """Sidebar üst kısmı (Logo)"""
    st.markdown("""
    <div style="padding: 0rem 0 1rem 0; text-align: center;">
        <div style="font-size: 2.2rem; margin-bottom: 0.2rem;">✨</div>
        <div style="font-size: 1.1rem; font-weight: 700; color: #fafafa; letter-spacing: -0.02em;">
            Müfredat Küratörü
        </div>
        <div style="font-size: 0.8rem; color: #71717a; margin-top: 0.1rem;">
            Otonom Araştırma Asistanı
        </div>
    </div>
    <div class="divider"></div>
    """, unsafe_allow_html=True)


def sidebar_bolum_baslik(metin: str):
    """Sidebar bölüm başlığı"""
    st.markdown(
        f'<div style="font-size: 0.7rem; font-weight: 600; color: #71717a; '
        f'text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">'
        f'{metin}</div>',
        unsafe_allow_html=True
    )


def sidebar_analiz_durumu_goster(seviye: str, konu_sayisi: int):
    """Sidebar Analiz Durumu Kartı"""
    sidebar_bolum_baslik("Analiz Özeti")
    st.markdown(f"""
    <div style="background: rgba(24,24,27,0.5); border: 1px solid rgba(255,255,255,0.06);
                border-radius: 8px; padding: 1rem; margin-bottom: 1.25rem;">
        <div style="font-size: 0.75rem; color: #a1a1aa; margin-bottom: 0.2rem;">Akademik Seviye</div>
        <div style="font-size: 1.05rem; font-weight: 600; color: #fafafa;">{seviye}</div>
        <div style="height: 1px; background: rgba(255,255,255,0.05); margin: 0.75rem 0;"></div>
        <div style="font-size: 0.75rem; color: #a1a1aa; margin-bottom: 0.2rem;">Hedef Konular</div>
        <div style="font-size: 1.05rem; font-weight: 600; color: #fafafa;">{konu_sayisi} Konu Saptandı</div>
    </div>
    """, unsafe_allow_html=True)


def sidebar_adim_listesi(adimlar: list):
    """Sidebar kullanım adımları — her adım ayrı render edilir."""
    sidebar_bolum_baslik("Nasıl Çalışır?")
    for num, metin in adimlar:
        st.markdown(f"""
        <div class="step-item">
            <div class="step-number">{num}</div>
            <div class="step-text">{metin}</div>
        </div>
        """, unsafe_allow_html=True)


def sidebar_alt_bilgi():
    """Sidebar alt bilgi"""
    st.markdown("""
    <div style="position: fixed; bottom: 1.5rem; font-size: 0.7rem; color: #52525b; text-align: center;">
        Powered by AI <br/> Gemini 2.5 Flash
    </div>
    """, unsafe_allow_html=True)


def hero_baslik_goster():
    """Ana sayfa kahraman (hero) başlığı"""
    st.markdown("""
    <div class="animate-fade-up" style="text-align: center; padding: 3rem 0 2.5rem 0;">
        <div class="badge" style="margin-bottom: 1.25rem; font-size: 0.7rem;">
            <span>Yapay Zeka Destekli</span>
        </div>
        <h1 style="font-size: 3.5rem; font-weight: 800; margin: 0; line-height: 1.1; letter-spacing: -0.03em;">
            Akıllı Müfredat <br/>
            <span class="text-gradient">Analitik Motoru</span>
        </h1>
        <p style="color: #a1a1aa; font-size: 1.1rem; margin-top: 1.25rem; font-weight: 400; max-width: 600px; margin-left: auto; margin-right: auto;">
            Syllabus belgenizi saniyeler içinde analiz edin, akademik seviyeyi belirleyin ve otonom araştırma ajanlarıyla anında literatür taraması yapın.
        </p>
    </div>
    """, unsafe_allow_html=True)


def hero_kart_goster():
    """Yükleme alanı bilgilendirme kartı"""
    st.markdown("""
    <div class="glass-card animate-fade-up" style="margin-bottom: 1rem;">
        <div style="font-size: 2rem; margin-bottom: 1rem; color: #f4f4f5;">📄</div>
        <div style="font-size: 1.25rem; font-weight: 600; color: #fafafa; margin-bottom: 0.5rem; letter-spacing: -0.02em;">
            Müfredat Belgenizi Yükleyin
        </div>
        <div style="font-size: 0.9rem; color: #a1a1aa; line-height: 1.5; max-width: 450px; margin: 0 auto;">
            PDF formatındaki ders izlencenizi bırakın. Sistem otomatik olarak metni ayıklayıp, NLP analizi başlatacaktır.
        </div>
    </div>
    """, unsafe_allow_html=True)


def dosya_bilgi_satirlari_goster(dosya_adi: str, dosya_kb: float):
    """Dosya istatistikleri ve onay"""
    st.markdown(f"""
    <div class="stat-bar animate-fade-up">
        <div class="stat-pill">📎 {dosya_adi}</div>
        <div class="stat-pill">💾 {dosya_kb} KB</div>
        <div class="stat-pill" style="border-color: rgba(16,185,129,0.3); color: #34d399;">✓ Sistem Onayı</div>
    </div>
    """, unsafe_allow_html=True)


def ozellik_listesi_goster(ozellikler: list):
    """Giriş sayfasındaki kartvizit tarzı özellikler — her kart ayrı render edilir."""
    for ikon, baslik, aciklama in ozellikler:
        st.markdown(f"""
        <div class="item-card">
            <div class="item-icon">{ikon}</div>
            <div>
                <div class="item-title">{baslik}</div>
                <div class="item-desc">{aciklama}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def sonuc_sayfasi_baslik_goster():
    """Analiz sonuçları ana sayfa başlık"""
    st.markdown("""
    <div class="animate-fade-up" style="padding: 1rem 0 2rem 0;">
        <div class="badge">Analiz Tamamlandı</div>
        <h1 style="font-size: 2.25rem; font-weight: 800; color: #fafafa; margin: 0;">
            Araştırma Başlatmaya Hazır
        </h1>
        <p style="color: #a1a1aa; margin-top: 0.5rem; font-size: 0.95rem;">
            Yapay zeka motoru müfredat verilerini optimize etti. Her konu için izole ajanları çalıştırabilirsiniz.
        </p>
    </div>
    """, unsafe_allow_html=True)


def bolum_badge_goster(etiket: str):
    """İçerik üstü mini badge"""
    st.markdown(f'<div class="badge">{etiket}</div>', unsafe_allow_html=True)


def konu_listesi_goster(konular: list):
    """Konuların listesi — her kart ayrı render edilir."""
    st.markdown(
        '<div style="font-size: 0.75rem; font-weight: 600; color: #a1a1aa; '
        'text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">'
        'Tespit Edilen Çekirdek Konular</div>',
        unsafe_allow_html=True
    )

    ikonlar = ["⚡", "🔍", "📐", "🔬", "💡"]
    for i, konu in enumerate(konular):
        ikon = ikonlar[i % len(ikonlar)]
        st.markdown(f"""
        <div class="item-card" style="padding: 0.75rem 1rem;">
            <div class="item-icon" style="width: 28px; height: 28px; font-size: 0.9rem;">{ikon}</div>
            <div class="item-title">{konu}</div>
        </div>
        """, unsafe_allow_html=True)


def gradient_ayirici_goster():
    """Genel ayırıcı"""
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


def ajan_bekleme_ekrani_goster():
    """Ajan çalıştırma öncesi boş ekran / placeholder"""
    st.markdown("""
    <div class="animate-fade-up" style="display: flex; align-items: center; justify-content: center; min-height: 400px; border-radius: 16px; border: 1px dashed rgba(255,255,255,0.08); background: rgba(24,24,27,0.2);">
        <div style="text-align: center; max-width: 380px; padding: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem; color: #52525b;">🤖</div>
            <div style="font-size: 1.15rem; font-weight: 600; color: #e4e4e7; margin-bottom: 0.5rem;">
                Ajanlar Standby Konumunda
            </div>
            <div style="color: #a1a1aa; font-size: 0.9rem; line-height: 1.6;">
                Sistemi tetiklemek için sol paneldeki ana butonu kullanın. Otonom tarama saniyeler içinde başlayacaktır.
            </div>
            <div style="margin-top: 1.5rem; display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap;">
                <span class="stat-pill">DuckDuckGo Search Info</span>
                <span class="stat-pill">Gemini Core</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def sonuc_kart_ust_goster(konu: str):
    """Araştırma sonucu çıktı kartı üst kısım"""
    st.markdown(f"""
    <div class="report-card animate-fade-up">
        <div class="report-header">
            <span style="font-size: 1.2rem;">📑</span>
            <span style="font-size: 1rem; font-weight: 600; color: #fafafa;">{konu}</span>
        </div>
    """, unsafe_allow_html=True)


def sonuc_kart_alt_kapat():
    """Araştırma sonucu çıktı kartı alt kısım"""
    st.markdown("</div>", unsafe_allow_html=True)