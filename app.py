import streamlit as st
import tempfile
import os
import theme
import pdf_motoru
import ajan_beyni
import time

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
        "raporlar": {},           
        "haftalik_plan": None,    
        "arama_tamamlandi": False 
    }

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
        ("4", "2 Haftalık Programınızı indirin"),
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    theme.gradient_ayirici_goster()

    if st.button("🔄 Yeni Müfredat Yükle", use_container_width=True):
        st.session_state.data = {"seviye": None, "konular": [], "hazir": False, "raporlar": {}, "haftalik_plan": None, "arama_tamamlandi": False}
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

            if st.button("Analizi Başlat", use_container_width=True):
                with st.status("Müfredat İşleniyor...", expanded=True) as durum:
                    try:
                        st.write("📄 PDF metne dönüştürülüyor...")
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                            tmp.write(file.read())
                            tmp.flush()
                            gecici_yol = tmp.name
                        
                        metin = pdf_motoru.mufredat_metnini_cikar(gecici_yol)
                        st.write("🧠 Yapay zeka seviye ve hedefleri belirliyor (Bellek kontrol ediliyor)...")
                        
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
                        if 'gecici_yol' in locals() and os.path.exists(gecici_yol):
                            os.remove(gecici_yol)
        else:
            st.markdown("<br>", unsafe_allow_html=True)
            theme.ozellik_listesi_goster([
                ("🎯", "Konu Çıkarımı", "En kritik araştırma konularını belirler"),
                ("📚", "Çok Yönlü Kaynaklar", "Makaleler ve YouTube eğitim videoları"),
                ("🗓️", "Akademik Plan", "Kaynaklara göre 2 haftalık program çıkarır"), 
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
        
        # EĞER ARAMA BİTTİYSE STATİK EKRANI VE İNDİRME BUTONUNU GÖSTER
        if st.session_state.data["arama_tamamlandi"]:
            theme.bolum_badge_goster("📚 Akademik Okuma ve İzleme Rehberiniz")
            st.success("✅ Tüm otonom araştırmalar ve çalışma programı tamamlandı. Raporunuzu aşağıdan indirebilirsiniz.")
            
            tam_rapor_txt = f"{'='*60}\n  {st.session_state.data['seviye']} Seviye - Akademik Rehber\n{'='*60}\n\n"
            
            for konu in st.session_state.data["konular"]:
                icerik = st.session_state.data["raporlar"].get(konu, "İçerik bulunamadı.")
                theme.sonuc_kart_ust_goster(konu)
                st.markdown(icerik)
                theme.sonuc_kart_alt_kapat()
                tam_rapor_txt += f"--- {konu} ---\n{icerik}\n\n{'─'*40}\n\n"
            
            # DÜZELTME: Ekranda 2 Haftalık Programı gösterme bloku eklendi
            st.divider()
            theme.sonuc_kart_ust_goster("🗓️ 2 Haftalık Akademik Gelişim Planı")
            st.markdown(st.session_state.data["haftalik_plan"])
            theme.sonuc_kart_alt_kapat()
            
            # DÜZELTME: TXT dosyasına programın eklenmesi
            tam_rapor_txt += f"{'='*60}\n  2 HAFTALIK ÇALIŞMA PROGRAMI\n{'='*60}\n\n"
            tam_rapor_txt += str(st.session_state.data["haftalik_plan"]) + "\n"
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="📥 Tüm Rehberi ve Programı İndir (.txt)",
                data=tam_rapor_txt,
                file_name="akademik_rehber_ve_program.txt",
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

            # 1. Kaynakları Bul
            for index, konu in enumerate(st.session_state.data["konular"]):
                with st.status(f"🔍 **{konu}** için makale ve video araştırılıyor...", expanded=True) as durum:
                    try:
                        rapor = ajan_calistirici.invoke({"input": f"Lütfen şu konu için 2 akademik makale ve 1 adet YouTube eğitim videosu bul: {konu}"})["output"]
                        durum.update(label=f"✅ **{konu}** tamamlandı", state="complete", expanded=False)

                        if isinstance(rapor, list):
                            temiz_metin = "".join([p.get('text', '') if isinstance(p, dict) else str(p) for p in rapor])
                        else:
                            temiz_metin = rapor
                            
                        st.session_state.data["raporlar"][konu] = temiz_metin
                        theme.sonuc_kart_ust_goster(konu)
                        st.markdown(temiz_metin)
                        theme.sonuc_kart_alt_kapat()

                    except Exception as e:
                        durum.update(label=f"❌ **{konu}** araması başarısız", state="error")
                        st.session_state.data["raporlar"][konu] = f"❌ Hata: {str(e)}"

                # Eğer bu son konu değilse diğerine geçmeden önce 5 saniye bekle
                if index < len(st.session_state.data["konular"]) - 1:
                    time.sleep(5)

            # Road Map
            with st.status("🗓️ Kaynaklar sentezleniyor ve 2 Haftalık Program oluşturuluyor...", expanded=True) as durum:
                try:
                    plan = ajan_beyni.haftalik_plan_olustur(st.session_state.data["raporlar"], st.session_state.data["seviye"])
                    st.session_state.data["haftalik_plan"] = plan
                    durum.update(label="✅ Program Hazırlandı", state="complete", expanded=False)
                except Exception as e:
                    st.session_state.data["haftalik_plan"] = f"Program oluşturulamadı: {str(e)}"
                    durum.update(label="❌ Program oluşturma başarısız", state="error")

            st.session_state.data["arama_tamamlandi"] = True
            st.rerun()

        else:
            theme.ajan_bekleme_ekrani_goster()