
# 🎯 AI Görev Planlayıcı (Otonom Ajan)

Bu proje, Sakarya Üniversitesi "Yapay Zeka" dersi kapsamında geliştirilmiş, Groq API (Llama-3.3-70b) tabanlı otonom bir görev planlama asistanıdır.

## 🛠️ Sistem Gereksinimleri ve Kurulum

Projeyi yerel makinenizde (localhost) çalıştırmak için aşağıdaki adımları sırasıyla uygulayınız:

### 1. Python Sanal Ortamını (Venv) Kurma

Projenin bağımlılıklarının bilgisayarınızdaki diğer projelerle çakışmaması için sanal ortam kullanılması önerilir. Terminalde proje dizinine giderek şu komutları çalıştırın:

```bash
python -m venv venv
```

##### Sanal ortamı aktif etmek için:

* **Windows:** `.\venv\Scripts\activate`
* **Mac/Linux:** `source venv/bin/activate`

### 2. Gerekli Kütüphanelerin Yüklenmesi

Sanal ortam aktifken (terminalde `(venv)` ibaresi varken), projenin ihtiyaç duyduğu tüm kütüphaneleri yükleyin:

```
pip install -r requirements.txt
```

### 3. API Anahtarının Ayarlanması (Çok Önemli!)

Uygulama arka planda Groq API kullanmaktadır. Projenin ana dizininde (bu README dosyası ile aynı yerde) `.env` adında gizli bir dosya oluşturun ve içine Groq üzerinden aldığınız API anahtarını şu formatta ekleyin:

```
GROQ_API_KEY=gsk_sizin_api_anahtariniz_buraya_gelecek
```

### 4. Uygulamayı Çalıştırma

Tüm kurulumlar tamamlandıktan sonra, Streamlit arayüzünü başlatmak için şu komutu çalıştırın:

`streamlit run ui/app.py`

Bu komut, varsayılan web tarayıcınızda `http://localhost:8501` adresinde uygulamayı otomatik olarak açacaktır.

## 📂 Kod Mimarisi ve Modüller

* `ui/app.py`: Çift sütunlu ve çoklu sohbet destekli kullanıcı arayüzü.
* `agent/agent.py`: ReAct (Reasoning + Acting) döngüsünü çalıştıran merkezi LLM ajanı.
* `agent/memory.py`: Ajanın çok turlu konuşmalarını ve araç (tool) sonuçlarını saklayan hafıza yönetimi.
* `tools/`: Ajanın otonom olarak kullanabildiği `date_calculator`, `task_breakdown` gibi Python fonksiyonları.
