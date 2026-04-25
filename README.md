<div align="center">

# 🎓 Smart Curriculum & Academic Resource Curator AI Agent

**Yapay zeka destekli otonom müfredat analiz ve akademik kaynak küratörlüğü sistemi**

<br/>

---

*PDF formatındaki ders müfredatlarını yapay zeka ile analiz eden, akademik seviye belirleyen ve otonom araştırma ajanları aracılığıyla ilgili akademik makaleler ile YouTube eğitim videolarını otomatik olarak küratörleyen tam yığın (full-stack) bir AI Agent uygulamasıdır.*

</div>

<br/>

---

## 📖 İçindekiler

- [Genel Bakış](#-genel-bakış)
- [Temel Özellikler](#-temel-özellikler)
- [Sistem Mimarisi](#-sistem-mimarisi)
- [Teknoloji Yığını](#-teknoloji-yığını)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Proje Yapısı](#-proje-yapısı)
- [Yapılandırma](#-yapılandırma)
- [Katkıda Bulunma](#-katkıda-bulunma)

---

## 🔭 Genel Bakış

**Smart Curriculum & Academic Resource Curator AI Agent**, eğitimcilerin ve öğrencilerin ders müfredatlarını hızla analiz etmelerini sağlayan yapay zeka destekli bir otonom ajan sistemidir. Kullanıcılar PDF formatındaki müfredat belgelerini yükler; sistem müfredatın zorluk seviyesini belirler, kritik araştırma konularını çıkarır ve her konu için izole otonom ajanlar aracılığıyla hem akademik makaleler hem de YouTube eğitim videoları bulur.

### Neden Bu Proje?

| Problem | Çözüm |
|---------|-------|
| Müfredat analizi saatler sürer | AI ile saniyeler içinde otomatik analiz |
| Kaynak bulma zahmetlidir | Otonom ajanlar ile paralel web taraması |
| Seviye belirleme özneldir | NLP tabanlı objektif zorluk tespiti |
| Çoklu platform tarama gerekir | DuckDuckGo + YouTube entegre tarama |

---

## ✨ Temel Özellikler

### 🧠 Akıllı Müfredat Analizi
- PDF belgelerinden otomatik metin çıkarma (OCR değil, metin tabanlı)
- Gemini 2.5 Flash ile zorluk seviyesi tespiti (Giriş / Orta / İleri Seviye)
- En kritik 3 araştırma konusunun otomatik belirlenmesi

### 🤖 Otonom Çoklu Ajan Sistemi
- Her konu için bağımsız çalışan izole ajanlar
- **DuckDuckGo** entegrasyonu ile akademik makale taraması
- **YouTube** entegrasyonu ile eğitim videosu keşfi
- Her konu için 2 akademik makale + 1 YouTube videosu önerisi

### ⚡ Sıfır Maliyetli Bellek Sistemi (Caching)
- `@st.cache_data` ile akıllı önbellekleme
- Aynı müfredat için tekrar API çağrısı yapılmaz
- API kredi tasarrufu sağlar

### 📥 Dışa Aktarma
- Tüm araştırma sonuçlarını **Markdown (.md)** formatında indirme
- Konulara göre yapılandırılmış, paylaşıma hazır akademik rehber çıktısı

### 🎨 Premium Arayüz
- **Dark Glassmorphism** tasarım konsepti
- Plus Jakarta Sans tipografisi
- Animasyonlu geçişler ve mikro-etkileşimler
- Tamamen responsive (mobil uyumlu) Streamlit arayüzü

---

## 🏗 Sistem Mimarisi

```
┌──────────────────────────────────────────────────────────┐
│                    KULLANICI ARAYÜZÜ                     │
│              Streamlit + Dark Glassmorphism               │
│                      (app.py + theme.py)                 │
└──────────────────────┬───────────────────────────────────┘
                       │
         ┌─────────────▼─────────────┐
         │      PDF İşleme Motoru    │
         │       (pdf_motoru.py)     │
         │    PyPDFLoader + Metin    │
         │    Çıkarma & Doğrulama    │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │      Ajan Beyni (Core)    │
         │      (ajan_beyni.py)      │
         │                           │
         │  ┌─────────────────────┐  │
         │  │  Analiz Modülü      │  │
         │  │  Gemini 2.5 Flash   │  │
         │  │  Seviye & Konu      │  │
         │  │  Çıkarımı           │  │
         │  └─────────────────────┘  │
         │                           │
         │  ┌─────────────────────┐  │
         │  │  Araştırma Ajanları │  │
         │  │  (Tool-Calling)     │  │
         │  │                     │  │
         │  │  🔍 DuckDuckGo     │  │
         │  │  🎥 YouTube Search  │  │
         │  └─────────────────────┘  │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │    Google Cloud Platform   │
         │      Vertex AI API         │
         │    (config.py + kimlik)    │
         └───────────────────────────┘
```

### Akış Diyagramı

```
PDF Yükleme → Metin Çıkarma → LLM Analizi → Seviye + Konular
                                                    │
                                    ┌───────────────┼───────────────┐
                                    ▼               ▼               ▼
                              Ajan: Konu 1    Ajan: Konu 2    Ajan: Konu 3
                              (DuckDuckGo)    (DuckDuckGo)    (DuckDuckGo)
                              (YouTube)       (YouTube)       (YouTube)
                                    │               │               │
                                    └───────────────┼───────────────┘
                                                    ▼
                                          Akademik Rehber (.md)
```

---

## 🛠 Teknoloji Yığını

| Katman | Teknoloji | Açıklama |
|--------|-----------|----------|
| **LLM** | Gemini 2.5 Flash | Google'ın hızlı ve güçlü dil modeli |
| **Orkestrasyon** | LangChain | Ajan oluşturma, araç çağırma ve prompt yönetimi |
| **Bulut** | Google Cloud Vertex AI | Model barındırma ve API erişimi |
| **Arayüz** | Streamlit | Hızlı prototipleme ve interaktif web uygulaması |
| **PDF İşleme** | PyPDFLoader (LangChain) | PDF'ten metin çıkarma |
| **Web Arama** | DuckDuckGo Search | Akademik makale taraması |
| **Video Arama** | YouTube Search Tool | Eğitim videosu keşfi |
| **Dil** | Python 3.10+ | Ana geliştirme dili |

---

## 🚀 Kurulum

### Ön Koşullar

- **Python 3.10** veya üzeri
- **Google Cloud Platform** hesabı ve aktif bir proje
- Vertex AI API'nin etkinleştirilmiş olması
- Servis hesabı anahtarı (`kimlik.json`)

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/mehmetbasgoze/Smart-Curriculum-and-Academic-Resource-Curator-AI-Agent.git
cd Smart-Curriculum-and-Academic-Resource-Curator-AI-Agent
```

### 2. Sanal Ortam Oluşturun

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 4. Google Cloud Kimlik Bilgilerini Yapılandırın

Google Cloud Console'dan bir **Servis Hesabı** oluşturun ve JSON anahtarını indirin. İndirilen dosyayı proje kök dizinine `kimlik.json` adıyla yerleştirin:

```
Smart-Curriculum-and-Academic-Resource-Curator-AI-Agent/
├── kimlik.json   ← Buraya koyun
├── app.py
├── ...
```

> ⚠️ **Önemli:** `kimlik.json` dosyası `.gitignore` içinde tanımlıdır ve GitHub'a yüklenmez. Asla bu dosyayı paylaşmayın.

### 5. Uygulamayı Başlatın

```bash
streamlit run app.py
```

Uygulama varsayılan olarak `http://localhost:8501` adresinde açılacaktır.

---

## 📋 Kullanım

### Adım 1 — Müfredat Yükleme
PDF formatındaki ders izlencenizi (syllabus) sürükleyip bırakın veya dosya seçici ile yükleyin.

### Adım 2 — AI Analizi Başlatma
**"🚀 Analizi Başlat"** butonuna tıklayın. Sistem:
- PDF'ten metni çıkarır
- Gemini 2.5 Flash ile zorluk seviyesini belirler
- En kritik 3 araştırma konusunu saptar

### Adım 3 — Otonom Araştırma
**"🌐 Otonom Araştırmayı Başlat"** butonuna tıklayın. Her konu için bağımsız bir ajan çalışır ve:
- DuckDuckGo üzerinden 2 akademik makale bulur
- YouTube üzerinden 1 eğitim videosu önerir
- Kaynakların neden bu seviyeye uygun olduğunu açıklar

### Adım 4 — Sonuçları İndirme
Tüm araştırma sonuçlarını yapılandırılmış bir **Markdown dosyası** olarak bilgisayarınıza indirin.

---

## 📂 Proje Yapısı

```
Smart-Curriculum-and-Academic-Resource-Curator-AI-Agent/
│
├── app.py              # Ana uygulama — Streamlit arayüzü ve iş akışı yönetimi
├── ajan_beyni.py       # Ajan çekirdeği — LLM analiz + otonom araştırma ajanı oluşturma
├── pdf_motoru.py       # PDF işleme motoru — metin çıkarma ve doğrulama
├── config.py           # Yapılandırma — GCP kimlik bilgileri ve model parametreleri
├── theme.py            # UI tema motoru — CSS enjeksiyonu ve HTML bileşen render
│
├── test/               # Geliştirme ve test betikleri
│   ├── test_pdf.py         # PDF okuma testi
│   ├── test_llm.py         # Vertex AI bağlantı testi
│   ├── pdf_analiz.py       # PDF + LLM entegrasyon testi
│   └── ajan_internette.py  # Otonom ajan internet tarama testi
│
├── requirements.txt    # Python bağımlılıkları
├── .gitignore          # Git hariç tutulan dosyalar
└── README.md           # Proje dokümantasyonu
```

### Modül Detayları

| Modül | Sorumluluk |
|-------|------------|
| `app.py` | Streamlit sayfa yapılandırması, oturum yönetimi, dosya yükleme, analiz tetikleme, araştırma akışı ve sonuç indirme |
| `ajan_beyni.py` | `mufredati_analiz_et()` — Seviye ve konu çıkarımı; `arama_ajani_olustur()` — Tool-calling ajan fabrikası |
| `pdf_motoru.py` | `mufredat_metnini_cikar()` — PDF doğrulama, metin çıkarma ve boş içerik kontrolü |
| `config.py` | GCP kimlik yönetimi (yerel/bulut), proje sabitleri (PROJECT_ID, LOCATION, MODEL_NAME) |
| `theme.py` | Premium CSS tasarımı, glassmorphism bileşenler, animasyonlar ve tüm HTML render fonksiyonları |

---

## ⚙ Yapılandırma

### Ortam Değişkenleri

| Değişken | Varsayılan | Açıklama |
|----------|------------|----------|
| `GOOGLE_APPLICATION_CREDENTIALS` | `kimlik.json` | GCP servis hesabı anahtar dosyası yolu |

### Model Parametreleri (`config.py`)

| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| `PROJECT_ID` | `smart-syllabus-agent` | Google Cloud proje kimliği |
| `LOCATION` | `us-central1` | Vertex AI bölgesi |
| `MODEL_NAME` | `gemini-2.5-flash` | Kullanılan LLM modeli |

### Ajan Parametreleri (`ajan_beyni.py`)

| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| `temperature` | `0.2` | Model yaratıcılık seviyesi (düşük = daha analitik) |
| `max_iterations` | `5` | Ajanın maksimum düşünme adımı |
| `max_execution_time` | `45 sn` | Ajan için maksimum çalışma süresi |
| `max_results` | `3` | DuckDuckGo arama sonuç limiti |

### Streamlit Cloud Dağıtımı

Projeyi Streamlit Cloud'a dağıtmak için, `kimlik.json` dosyası yerine **Streamlit Secrets** kullanılır:

1. Streamlit Cloud panosunda **Settings → Secrets** bölümüne gidin
2. Aşağıdaki yapıda GCP servis hesabı bilgilerini ekleyin:

```toml
[gcp_service_account]
type = "service_account"
project_id = "smart-syllabus-agent"
private_key_id = "..."
private_key = "..."
client_email = "..."
client_id = "..."
auth_uri = "..."
token_uri = "..."
```

---

## 🤝 Katkıda Bulunma

Katkılarınızı memnuniyetle karşılıyoruz! Aşağıdaki adımları izleyin:

1. Bu depoyu **fork** edin
2. Yeni bir dal (branch) oluşturun: `git checkout -b feature/yeni-ozellik`
3. Değişikliklerinizi commit edin: `git commit -m "feat: yeni özellik eklendi"`
4. Dalınıza push yapın: `git push origin feature/yeni-ozellik`
5. Bir **Pull Request** açın

---


