<div align="center">

# 🎓 Smart Curriculum & Academic Resource Curator AI Agent

**Yapay zeka destekli otonom müfredat analiz, ders notu sentezi ve akademik kaynak küratörlüğü sistemi**

<br/>

---

*PDF formatındaki ders müfredatlarını yapay zeka ile analiz eden, ders adını tespit ederek web taramasıyla içeriği zenginleştiren, konuları pedagojik olarak temelden ileriye sıralayan ve her alt konu için akademik kaynak/videolar bularak profesyonel ders notları sentezleyen tam yığın (full-stack) bir AI Agent uygulamasıdır.*

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

---

## 🔭 Genel Bakış

**Smart Curriculum & Academic Resource Curator AI Agent**, eğitimcilerin ve öğrencilerin ders müfredatlarını hızla analiz etmelerini sağlayan yapay zeka destekli bir otonom ajan sistemidir. Kullanıcılar PDF formatındaki müfredat belgelerini yükler; sistem dersin adını ve zorluk seviyesini otomatik tespit eder, internetten ek müfredat araması yapar ve konuları 8-12 alt başlığa (temelden ileriye doğru) ayırır. Son olarak her konu için akademik kaynaklar ve YouTube videoları bularak baştan sona profesyonel bir **Ders Çalışma Notu** sentezler.

### Neden Bu Proje?

| Problem | Çözüm |
|---------|-------|
| Müfredat analizi saatler sürer | AI ile saniyeler içinde otomatik analiz ve internet taraması |
| Kaynak bulma zahmetlidir | Otonom ajanlar ile paralel web ve YouTube taraması |
| Konu sıralaması ve seviye belirleme zordur | Pedagojik olarak temelden ileriye sıralama |
| Bilgiler dağınıktır | Tüm kaynakları sentezleyen kapsamlı ders notu üretimi |

---

## ✨ Temel Özellikler

### 🧠 Akıllı Ders Tespiti ve Yapılandırma
- PDF belgelerinden otomatik ders adı ve zorluk seviyesi tespiti
- Bulunan ders adı ile internette detaylı müfredat araştırması
- Müfredatın pedagojik olarak temelden ileriye doğru 8-12 alt konuya ayrılması

### 🤖 Otonom Çoklu Ajan Sistemi
- Her konu için seviyeye uygun (Temel/Orta/İleri) bağımsız kaynak araması
- **DuckDuckGo** API ile akademik makale taraması
- **YouTube** API ile eğitim videosu keşfi

### ✍️ Kapsamlı Ders Notu Sentezi
- Tüm alt konular için bulunan gerçek kaynakların analiz edilerek profesyonel ders notlarına dönüştürülmesi
- Token limiti aşmamak ve uydurma kaynak (hallucination) engellemek için bölüm bölüm LLM sentezi
- İndirilebilir tam metin (`.txt`) formatında çalışma rehberi ve kaynakça

### 🎨 Premium Arayüz
- **Dark Glassmorphism** tasarım konsepti
- Animasyonlu geçişler, ilerleme durum çubukları ve etkileşimli bölümler
- Tamamen responsive Streamlit arayüzü

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
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │      Ajan Beyni (Core)    │
         │      (ajan_beyni.py)      │
         │                           │
         │  1. Ders Adı ve Seviye    │
         │  2. Web'den Müfredat Ara  │
         │  3. Konuları Bölümlendir  │
         │  4. DDG & YouTube Arama   │
         │  5. Ders Notu Sentezle    │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │    Google Cloud Platform   │
         │      Vertex AI API         │
         │    (Gemini 2.5 Flash)      │
         └───────────────────────────┘
```

---

## 🛠 Teknoloji Yığını

| Katman | Teknoloji | Açıklama |
|--------|-----------|----------|
| **LLM** | Gemini 2.5 Flash (Vertex AI) | Güçlü dil modeli ile analiz ve sentez |
| **Orkestrasyon** | LangChain / Özel Ajan Akışı | Prompt yönetimi ve sıralı LLM çağrıları |
| **Bulut** | Google Cloud Platform | Model barındırma |
| **Arayüz** | Streamlit | Hızlı prototipleme ve interaktif web uygulaması |
| **PDF İşleme** | PyPDFLoader (LangChain) | PDF'ten metin çıkarma |
| **Arama Motorları** | DuckDuckGo API, YouTube Search API | Kaynak ve video keşfi |
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

> ⚠️ **Önemli:** `kimlik.json` dosyası `.gitignore` içinde tanımlıdır ve GitHub'a yüklenmez. Güvenliğiniz için asla bu dosyayı herkese açık alanlarda paylaşmayın.

### 5. Uygulamayı Başlatın

```bash
streamlit run app.py
```

Uygulama varsayılan olarak `http://localhost:8501` adresinde açılacaktır.

---

## 📋 Kullanım

### Adım 1 — Ders Müfredatını (PDF) Yükleyin
PDF formatındaki ders izlencenizi (syllabus) yükleyin. Sistem PDF metnini çıkararak hazırlık yapar.

### Adım 2 — Ders Adı Tespiti ve İnternet Araştırması
**"Müfredat Analizini Başlat"** butonuna tıkladığınızda, sistem AI ile dersin adını tespit eder ve internet üzerinde bu derse ait daha geniş müfredat bilgilerini arar.

### Adım 3 — Alt Konulara Ayırma
PDF ve web sonuçları birleştirilerek, ders pedagojik bir mantıkla (temelden ileri seviyeye doğru) 8-12 alt konuya otomatik olarak bölünür.

### Adım 4 — Kaynak Taraması
**"🌐 Kaynak Bul ve Ders Notu Yaz"** butonuna basıldığında, sistem her alt konu için seviyesine uygun akademik web kaynakları ve YouTube videoları tarar.

### Adım 5 — Kapsamlı Ders Notu Sentezi ve İndirme
Bulunan kaynaklar ışığında, model her konu için bölüm bölüm profesyonel bir ders çalışma notu sentezler. Sonunda tüm raporu `.txt` formatında bilgisayarınıza indirebilirsiniz.

---

## 📂 Proje Yapısı

```
Smart-Curriculum-and-Academic-Resource-Curator-AI-Agent/
│
├── app.py              # Ana uygulama — Streamlit arayüzü ve iş akışı yönetimi
├── ajan_beyni.py       # Ajan çekirdeği — Analiz, web taraması, sentezleme işlemleri
├── pdf_motoru.py       # PDF işleme motoru — metin çıkarma
├── config.py           # Yapılandırma — GCP kimlik bilgileri ve model parametreleri
├── theme.py            # UI tema motoru — CSS enjeksiyonu ve HTML bileşen render
├── requirements.txt    # Python bağımlılıkları
├── .gitignore          # Git hariç tutulan dosyalar
└── README.md           # Proje dokümantasyonu
```

---

## ⚙ Yapılandırma

### Ortam Değişkenleri

| Değişken | Varsayılan | Açıklama |
|----------|------------|----------|
| `GOOGLE_APPLICATION_CREDENTIALS` | `kimlik.json` | GCP servis hesabı anahtar dosyası yolu |

### Model Parametreleri (`config.py`)

| Parametre | Açıklama |
|-----------|----------|
| `PROJECT_ID` | Google Cloud proje kimliğiniz. Kendi projenizin ID'si ile güncelleyin. |
| `LOCATION` | Vertex AI bölgesi (örn. `us-central1`). |
| `MODEL_NAME` | Kullanılan LLM modeli (örn. `gemini-2.5-flash`). |

### Streamlit Cloud Dağıtımı

Projeyi Streamlit Cloud'a dağıtmak için, `kimlik.json` dosyası yerine **Streamlit Secrets** kullanılır:

1. Streamlit Cloud panosunda **Settings → Secrets** bölümüne gidin
2. Aşağıdaki yapıda GCP servis hesabı bilgilerinizi kendi güvenli anahtarlarınız ile ekleyin:

```toml
[gcp_service_account]
type = "service_account"
project_id = "YOUR_PROJECT_ID"
private_key_id = "..."
private_key = "..."
client_email = "..."
client_id = "..."
auth_uri = "..."
token_uri = "..."
```

---
