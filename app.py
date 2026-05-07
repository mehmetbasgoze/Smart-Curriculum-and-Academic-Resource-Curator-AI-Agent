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
        "ders_adi": None,
        "seviye": None,
        "alt_konular": [],
        "hazir": False,
        "raporlar": {},           
        "ders_notu": None,
        "arama_tamamlandi": False 
    }

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
            st.session_state.data["ders_adi"],
            st.session_state.data["seviye"],
            len(st.session_state.data["alt_konular"])
        )

    theme.sidebar_adim_listesi([
        ("1", "Ders müfredatını (PDF) yükleyin"),
        ("2", "Ders adı tespiti ve internet araştırması"),
        ("3", "Alt konulara ayırma (temelden ileriye)"),
        ("4", "Her konu için kaynak taraması"),
        ("5", "Kapsamlı Ders Notu sentezi ve indirme"),
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    theme.gradient_ayirici_goster()

    if st.button("🔄 Yeni Ders Yükle", use_container_width=True):
        st.session_state.data = {
            "ders_adi": None, "seviye": None, "alt_konular": [], 
            "hazir": False, "raporlar": {}, "ders_notu": None, 
            "arama_tamamlandi": False
        }
        st.rerun()

    theme.sidebar_alt_bilgi()

# ==========================================
# 4. ANA AKIŞ - ADIM 1: PDF YÜKLEME VE ANALİZ
# ==========================================
if not st.session_state.data["hazir"]:
    theme.hero_baslik_goster()
    col_pad1, col_main, col_pad2 = st.columns([1, 2.2, 1])

    with col_main:
        theme.hero_kart_goster()
        st.markdown("<br>", unsafe_allow_html=True)

        file = st.file_uploader(
            "Ders müfredatını içeren PDF dosyasını seçin",
            type=["pdf"],
            help="Sistem PDF'den ders adını tespit edip, internetten detaylı müfredat araştırması yapacaktır."
        )

        if file:
            dosya_kb = round(file.size / 1024, 1)
            theme.dosya_bilgi_satirlari_goster(file.name, dosya_kb)
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Müfredat Analizini Başlat", use_container_width=True):
                with st.status("Ders İçeriği Analiz Ediliyor...", expanded=True) as durum:
                    try:
                        # --- ADIM 1: PDF'yi Oku ---
                        st.write("📄 PDF metne dönüştürülüyor...")
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                            tmp.write(file.read())
                            tmp.flush()
                            gecici_yol = tmp.name
                        
                        pdf_metni = pdf_motoru.mufredat_metnini_cikar(gecici_yol)
                        
                        # --- ADIM 2: Ders Adını Tespit Et ---
                        st.write("🧠 Yapay zeka ders adını tespit ediyor...")
                        ders_adi, seviye = ajan_beyni.ders_adini_tespit_et(pdf_metni)
                        st.write(f"✅ Tespit edilen ders: **{ders_adi}** ({seviye})")
                        
                        # --- ADIM 3: İnternette Ders Müfredatı Ara ---
                        st.write(f"🔍 İnternette '{ders_adi}' dersi için müfredat içerikleri aranıyor...")
                        web_sonuclari = ajan_beyni.ders_icerigini_internetten_ara(ders_adi)
                        
                        if web_sonuclari:
                            st.write("✅ İnternetten ders içerikleri bulundu.")
                        else:
                            st.write("⚠️ Web sonuçları sınırlı, PDF içeriği ağırlıkla kullanılacak.")
                        
                        # --- ADIM 4: Alt Konulara Ayır ---
                        st.write("📋 Ders temelden ileriye doğru alt konulara ayrılıyor...")
                        alt_konular = ajan_beyni.alt_konulara_ayir(ders_adi, web_sonuclari, pdf_metni, seviye)
                        st.write(f"✅ **{len(alt_konular)}** alt konu belirlendi (temelden ileriye sıralı).")

                        st.session_state.data.update({
                            "ders_adi": ders_adi,
                            "seviye": seviye,
                            "alt_konular": alt_konular,
                            "hazir": True
                        })
                        durum.update(label=f"✅ Analiz Tamamlandı: {ders_adi}", state="complete", expanded=False)
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
                ("🎯", "Otomatik Ders Tespiti", "PDF'den ders adını AI ile tespit eder, internet araştırması yapar"),
                ("📋", "Pedagojik Alt Konu Sıralaması", "Dersi temelden ileriye 8-12 alt konuya ayırır"),
                ("📚", "Seviyeye Uygun Kaynaklar", "Her alt konu için seviyeye uygun makale ve videolar bulur"),
                ("✍️", "Kapsamlı Ders Notu", "Tüm kaynakları sentezleyerek profesyonel bir ders notu oluşturur"),
            ])

# ==========================================
# 5. ANA AKIŞ - ADIM 2: ARAŞTIRMA VE SENTEZ
# ==========================================
else:
    theme.sonuc_sayfasi_baslik_goster(st.session_state.data["ders_adi"])
    col_ozet, col_arastirma = st.columns([1, 2.2], gap="large")

    with col_ozet:
        theme.bolum_badge_goster("📊 Ders Yapısı")
        st.metric(label="📖 Ders", value=st.session_state.data["ders_adi"])
        st.metric(label="🎓 Seviye", value=st.session_state.data["seviye"])
        st.markdown("<br>", unsafe_allow_html=True)
        theme.konu_listesi_goster(st.session_state.data["alt_konular"])
        st.markdown("<br>", unsafe_allow_html=True)
        theme.gradient_ayirici_goster()

        baslat_butonu = st.button(
            "🌐 Kaynak Bul ve Ders Notu Yaz", 
            type="primary", 
            use_container_width=True, 
            disabled=st.session_state.data["arama_tamamlandi"]
        )

    with col_arastirma:
        
        if st.session_state.data["arama_tamamlandi"]:
            theme.bolum_badge_goster("🎓 Yapay Zeka Tarafından Sentezlenen Ders Notu")
            st.success("✅ Ders notunuz ve kaynakçanız hazırlandı. Aşağıdan inceleyebilir ve indirebilirsiniz.")
            
            # --- 1. DERS NOTU (ANA ÇIKTI) ---
            theme.sonuc_kart_ust_goster("✍️ Kapsamlı Ders Çalışma Notu")
            st.markdown(st.session_state.data["ders_notu"])
            theme.sonuc_kart_alt_kapat()

            # --- 2. REFERANS KAYNAKLAR (DETAYLAR) ---
            st.divider()
            theme.bolum_badge_goster("📚 Kullanılan Referanslar ve Kaynaklar")
            
            ders_adi = st.session_state.data['ders_adi']
            seviye = st.session_state.data['seviye']
            
            tam_rapor_txt = f"{'='*60}\n  {ders_adi} - {seviye} Seviyesi İçin Akademik Ders Notu\n{'='*60}\n\n"
            tam_rapor_txt += f"BÖLÜM 1: DERS NOTU\n{'-'*30}\n{st.session_state.data['ders_notu']}\n\n"
            tam_rapor_txt += f"BÖLÜM 2: KAYNAKÇA VE REFERANSLAR\n{'-'*30}\n\n"

            for i, konu in enumerate(st.session_state.data["alt_konular"]):
                icerik = st.session_state.data["raporlar"].get(konu, "İçerik bulunamadı.")
                
                # Seviye etiketi belirle
                oran = (i + 1) / len(st.session_state.data["alt_konular"])
                if oran <= 0.33:
                    seviye_etiketi = "🟢 Temel"
                elif oran <= 0.66:
                    seviye_etiketi = "🟡 Orta"
                else:
                    seviye_etiketi = "🔴 İleri"
                
                with st.expander(f"{seviye_etiketi} | {i+1}. {konu}"):
                    st.markdown(icerik)
                tam_rapor_txt += f"--- {i+1}. {konu} ({seviye_etiketi}) ---\n{icerik}\n\n"
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="📥 Tüm Ders Notunu ve Kaynakçayı İndir (.txt)",
                data=tam_rapor_txt,
                file_name=f"{ders_adi.replace(' ', '_')}_ders_notu.txt",
                mime="text/plain",
                use_container_width=True
            )

        elif baslat_butonu:
            theme.bolum_badge_goster("📚 Kaynaklar Taranıyor")
            
            ders_adi = st.session_state.data["ders_adi"]
            alt_konular = st.session_state.data["alt_konular"]
            toplam = len(alt_konular)

            # --- Adım 1: Her alt konu için kaynak bul ---
            for index, konu in enumerate(alt_konular):
                sira = index + 1
                
                # Seviye etiketi
                oran = sira / toplam
                if oran <= 0.33:
                    seviye_etiketi = "Temel"
                elif oran <= 0.66:
                    seviye_etiketi = "Orta"
                else:
                    seviye_etiketi = "İleri"
                
                with st.status(f"🔍 [{seviye_etiketi}] **{sira}/{toplam} - {konu}** için kaynaklar aranıyor...", expanded=True) as durum:
                    try:
                        rapor = ajan_beyni.konu_icin_kaynak_bul(ders_adi, konu, sira, toplam)
                        durum.update(label=f"✅ **{sira}/{toplam} - {konu}** tamamlandı", state="complete", expanded=False)
                    except Exception as e:
                        rapor = f"Kaynak bulunamadı: {str(e)}"
                        durum.update(label=f"⚠️ **{konu}** - kısmi sonuç", state="complete", expanded=False)

                    st.session_state.data["raporlar"][konu] = rapor

                if index < toplam - 1:
                    time.sleep(3)  # API rate limit koruması

            # --- Adım 2: Ders Notunu Bölüm Bölüm Sentezle ---
            not_status = st.status("✍️ Ders Notu bölüm bölüm oluşturuluyor...", expanded=True)
            
            try:
                def ilerleme_goster(bolum_no, toplam, konu):
                    not_status.write(f"📝 Bölüm {bolum_no}/{toplam}: **{konu}** yazılıyor...")
                
                not_metni = ajan_beyni.ders_notu_olustur(
                    st.session_state.data["ders_adi"],
                    st.session_state.data["raporlar"], 
                    st.session_state.data["seviye"],
                    progress_callback=ilerleme_goster
                )
                st.session_state.data["ders_notu"] = not_metni
                st.session_state.data["arama_tamamlandi"] = True
                not_status.update(label="✅ Ders Notu Sentezlendi (Tüm Bölümler)", state="complete", expanded=False)
            except Exception as e:
                st.session_state.data["ders_notu"] = f"Not oluşturulamadı: {str(e)}"
                st.session_state.data["arama_tamamlandi"] = True
                not_status.update(label="❌ Not oluşturma başarısız", state="error")
            
            st.rerun()

        else:
            theme.ajan_bekleme_ekrani_goster()