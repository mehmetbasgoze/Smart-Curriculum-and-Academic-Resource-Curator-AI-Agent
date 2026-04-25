import streamlit as st
import tempfile
import os
import theme
import pdf_motoru
import ajan_beyni

# ==========================================
# 1. SAYFA KURULUMU VE TEMA
# ==========================================
st.set_page_config(
    page_title="Akıllı Müfredat Küratörü",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)
theme.css_uygula()

# ==========================================
# 2. OTURUM VE BELLEK YÖNETİMİ
# ==========================================
if 'data' not in st.session_state:
    st.session_state.data = {
        "seviye": None,
        "konular": [],
        "hazir": False,
        "raporlar": {},           # SENIOR EKLENTİ: Ajanın bulduğu sonuçları hafızada tutar
        "arama_tamamlandi": False # SENIOR EKLENTİ: İndirme butonunu göstermek için tetikleyici
    }

# YENİ ÖZELLİK 1: BELLEK (CACHING) 
# Aynı metin gelirse LLM'i tekrar çalıştırma
@st.cache_data(show_spinner=False)
def ai_analiz_getir(metin):
    return ajan_beyni.mufredati_analiz_et(metin)

# ==========================================
# 3. YAN MENÜ (SIDEBAR)
# ==========================================
with st.sidebar:
    theme.sidebar_logo_goster()

    theme.sidebar_bolum_baslik("SİSTEM DURUMU")
    st.markdown('<div class="sidebar-chip">● Sistem Aktif</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.data["hazir"]:
        theme.sidebar_analiz_durumu_goster(
            st.session_state.data["seviye"],
            len(st.session_state.data["konular"])
        )

    theme.sidebar_adim_listesi([
        ("1", "PDF müfredatınızı yükleyin"),
        ("2", "Analizi başlatın"),
        ("3", "Otonom araştırmayı çalıştırın"),
        ("4", "Akademik kaynakları indirin"),
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    theme.gradient_ayirici_goster()

    # Sıfırlama Butonu: Belleği de temizler
    if st.button("🔄 Yeni Müfredat Yükle", use_container_width=True):
        st.session_state.data = {"seviye": None, "konular": [], "hazir": False, "raporlar": {}, "arama_tamamlandi": False}
        st.rerun()

    theme.sidebar_alt_bilgi()

# ==========================================
# 4. ANA AKIŞ - ADIM 1: YÜKLEME VE ANALİZ
# ==========================================
if not st.session_state.data["hazir"]:

    theme.hero_baslik_goster()

    col_pad1, col_main, col_pad2 = st.columns([1, 2.2, 1])

    with col_main:
        theme.hero_kart_goster()
        st.markdown("<br>", unsafe_allow_html=True)

        file = st.file_uploader(
            "PDF dosyanızı sürükleyin veya tıklayarak seçin",
            type=["pdf"],
            help="Yalnızca PDF formatı desteklenmektedir."
        )

        if file:
            dosya_kb = round(file.size / 1024, 1)
            theme.dosya_bilgi_satirlari_goster(file.name, dosya_kb)
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🚀 Analizi Başlat", use_container_width=True):
                with st.status("Müfredat İşleniyor...", expanded=True) as durum:
                    try:
                        st.write("📄 PDF metne dönüştürülüyor...")
                        
                        # --- SENIOR FIX BAŞLANGICI ---
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                            tmp.write(file.read())
                            tmp.flush() # Veriyi RAM'den fiziksel diske zorla yaz!
                            gecici_yol = tmp.name
                        
                        # Dosya tamamen kaydedilip kapatıldıktan sonra motora gönder
                        metin = pdf_motoru.mufredat_metnini_cikar(gecici_yol)
                        # --- SENIOR FIX BİTİŞİ ---

                        st.write("🧠 Yapay zeka seviye ve hedefleri belirliyor (Bellek kontrol ediliyor)...")
                        
                        # Bellek fonksiyonunu çağırıyoruz
                        seviye, konular = ai_analiz_getir(metin)

                        st.session_state.data.update({
                            "seviye": seviye,
                            "konular": konular,
                            "hazir": True
                        })
                        durum.update(label="✅ Analiz Tamamlandı!", state="complete", expanded=False)
                        st.rerun()

                    except Exception as e:
                        durum.update(label="❌ Hata Oluştu", state="error", expanded=True)
                        st.error(str(e))
                    finally:
                        # İşlem bitince sunucuda yer kaplamaması için geçici dosyayı siliyoruz
                        if 'gecici_yol' in locals() and os.path.exists(gecici_yol):
                            os.remove(gecici_yol)
        else:
            st.markdown("<br>", unsafe_allow_html=True)
            theme.ozellik_listesi_goster([
                ("⚡", "Sıfır Maliyetli Bellek", "Aynı analizler için API kredisi harcamaz"),
                ("🎯", "Konu Çıkarımı", "En kritik araştırma konularını belirler"),
                ("📚", "Çok Yönlü Kaynaklar", "Makaleler ve YouTube eğitim videoları"),
                ("💾", "Dışa Aktarma", "Rehberi metin dosyası (.txt) olarak indirme imkanı"),
            ])

# ==========================================
# 5. ANA AKIŞ - ADIM 2: ARAŞTIRMA VE SONUÇ
# ==========================================
else:
    theme.sonuc_sayfasi_baslik_goster()

    col_ozet, col_arastirma = st.columns([1, 2.2], gap="large")

    with col_ozet:
        theme.bolum_badge_goster("📊 Analiz Raporu")
        st.metric(label="🎓 Akademik Seviye", value=st.session_state.data["seviye"])
        st.markdown("<br>", unsafe_allow_html=True)
        theme.konu_listesi_goster(st.session_state.data["konular"])
        st.markdown("<br>", unsafe_allow_html=True)
        theme.gradient_ayirici_goster()

        baslat_butonu = st.button("🌐 Otonom Araştırmayı Başlat", type="primary", use_container_width=True, disabled=st.session_state.data["arama_tamamlandi"])

        st.markdown("""
        <div style="margin-top: 0.8rem; font-size: 0.8rem; color: #a1a1aa; text-align: center;">
            Her konu için seçilen ajanlar üzerinden<br>akademik makale ve video taraması başlatılacaktır.
        </div>
        """, unsafe_allow_html=True)

    with col_arastirma:
        
        # YENİ ÖZELLİK 2: EĞER ARAMA BİTTİYSE STATİK EKRANI VE İNDİRME BUTONUNU GÖSTER
        if st.session_state.data["arama_tamamlandi"]:
            theme.bolum_badge_goster("📚 Akademik Okuma ve İzleme Rehberiniz")
            st.success("✅ Tüm otonom araştırmalar tamamlandı. Raporunuzu aşağıdan bilgisayarınıza indirebilirsiniz.")
            
            # Metin dosyasının içeriğini hazırlıyoruz
            tam_rapor_txt = f"{'='*60}\n  {st.session_state.data['seviye']} Seviye - Akademik Rehber\n{'='*60}\n\n"
            
            for konu in st.session_state.data["konular"]:
                icerik = st.session_state.data["raporlar"].get(konu, "İçerik bulunamadı.")
                
                # Ekrana bas
                theme.sonuc_kart_ust_goster(konu)
                st.markdown(icerik)
                theme.sonuc_kart_alt_kapat()
                
                # İndirilecek dosyaya ekle
                tam_rapor_txt += f"--- {konu} ---\n{icerik}\n\n{'─'*40}\n\n"
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Sihirli İndirme Butonu
            st.download_button(
                label="📥 Tüm Rehberi İndir (.txt)",
                data=tam_rapor_txt,
                file_name="akademik_rehber.txt",
                mime="text/plain",
                use_container_width=True
            )

        # EĞER BUTONA BASILDIYSA AJANLARI ÇALIŞTIR
        elif baslat_butonu:
            theme.bolum_badge_goster("📚 Akademik Okuma ve İzleme Rehberiniz")
            st.markdown("""
            <p style="color: #64748B; font-size: 0.88rem; margin-bottom: 1.2rem;">
                Yapay zeka ajan her konu için bağımsız araştırma yapıyor.
                Sonuçlar tamamlandıkça aşağıda görünecektir.
            </p>
            """, unsafe_allow_html=True)

            ajan_calistirici = ajan_beyni.arama_ajani_olustur(st.session_state.data["seviye"])

            for konu in st.session_state.data["konular"]:
                with st.status(f"🔍 **{konu}** için makale ve video araştırılıyor...", expanded=True) as durum:
                    try:
                        rapor = ajan_calistirici.invoke({
                            "input": f"Lütfen şu konu için 2 akademik makale ve 1 adet YouTube eğitim videosu bul: {konu}"
                        })["output"]

                        durum.update(label=f"✅ **{konu}** tamamlandı", state="complete", expanded=False)

                        # Listeden string'e güvenli dönüşüm
                        if isinstance(rapor, list):
                            temiz_metin = "".join([p.get('text', '') if isinstance(p, dict) else str(p) for p in rapor])
                        else:
                            temiz_metin = rapor
                            
                        # YENİ: Çıktıyı gelecekte indirmek üzere hafızaya kaydet
                        st.session_state.data["raporlar"][konu] = temiz_metin

                        theme.sonuc_kart_ust_goster(konu)
                        st.markdown(temiz_metin)
                        theme.sonuc_kart_alt_kapat()

                    except Exception as e:
                        durum.update(label=f"❌ **{konu}** araması başarısız", state="error")
                        st.warning(f"Ajan bu konuda zorlandı. Hata: {str(e)}")
                        st.session_state.data["raporlar"][konu] = f"❌ Hata: {str(e)}"
            
            # Tüm aramalar bittiğinde indirme butonunu göstermek için sayfayı yenile
            st.session_state.data["arama_tamamlandi"] = True
            st.rerun()

        # BEKLEME EKRANI
        else:
            theme.ajan_bekleme_ekrani_goster()