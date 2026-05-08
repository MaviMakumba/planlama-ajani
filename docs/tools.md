TOOL SİSTEMİ DOKÜMANTASYONU

Bu doküman, AI destekli görev planlama ajanında kullanılan araçların (tools) çalışma mantığını, parametre yapılarını ve örnek kullanımlarını açıklamak amacıyla hazırlanmıştır.

==================================================
GENEL MİMARİ
==================================================

Sistem aşağıdaki akış mantığıyla çalışmaktadır:

Kullanıcı İsteği
↓
LLM / Agent
↓
Tool Dispatcher
↓
Tool Validation
↓
İlgili Tool Çalıştırma
↓
Sonuç Üretimi
↓
Markdown / JSON Çıktısı

Tool sistemi, LLM’in güvenilir olmayan hesaplama işlemlerini kontrol altına almak ve daha stabil görev planlama çıktıları üretmek amacıyla geliştirilmiştir.

==================================================
KULLANILAN ARAÇLAR
==================================================

1. DATE_CALCULATOR

Amaç:
Belirtilen başlangıç tarihine gün, hafta veya ay ekleyerek hedef tarihi hesaplar.

Parametreler:
- start_date → Başlangıç tarihi (YYYY-MM-DD)
- amount → Eklenecek miktar
- unit → day / week / month

Örnek Kullanım:

run_tool("date_calculator", {
    "start_date": "2026-05-06",
    "amount": 3,
    "unit": "week"
})

Örnek Çıktı:

{
    "success": True,
    "result_date": "2026-05-27"
}

--------------------------------------------------

2. DURATION_ESTIMATOR

Amaç:
Görev adına ve karmaşıklık seviyesine göre tahmini süre aralığı üretir.

Parametreler:
- task_name → Görev adı
- complexity → low / medium / high

Örnek Kullanım:

run_tool("duration_estimator", {
    "task_name": "Backend API geliştirme",
    "complexity": "high"
})

Örnek Çıktı:

{
    "min": 4,
    "max": 7,
    "unit": "gün"
}

--------------------------------------------------

3. TASK_BREAKDOWN

Amaç:
Verilen proje adını yazılım geliştirme sürecine uygun alt görevlere böler.

Parametreler:
- project_name → Proje adı

Örnek Kullanım:

run_tool("task_breakdown", {
    "project_name": "Yapay zeka destekli mobil uygulama"
})

Örnek Çıktı:

{
    "task_count": 12,
    "tasks": [...]
}

--------------------------------------------------

4. MARKDOWN_EXPORTER

Amaç:
Görev listesini Markdown tablo formatına dönüştürür.

Parametreler:
- project_name → Proje adı
- tasks → Görev listesi

Örnek Kullanım:

run_tool("markdown_exporter", {
    "project_name": "AI Projesi",
    "tasks": [
        "Backend geliştirme",
        "Frontend geliştirme"
    ]
})

==================================================
TOOL DISPATCHER
==================================================

Amaç:
Tool adını ve parametreleri alarak ilgili aracı çalıştırır.

Dispatcher katmanı sayesinde LLM doğrudan Python fonksiyonlarını değil, merkezi bir tool sistemi üzerinden işlem yapar.

Örnek:

run_tool(tool_name, arguments)

==================================================
VALIDATION SİSTEMİ
==================================================

Validation katmanı aşağıdaki durumları kontrol eder:

- Eksik parametre
- Yanlış veri tipi
- Geçersiz enum değeri
- Negatif sayısal değer
- Yanlış liste formatı

Örnek Hata Çıktısı:

{
    "success": False,
    "error": "amount pozitif bir değer olmalıdır."
}

==================================================
PLANNING PIPELINE
==================================================

Amaç:
Birden fazla tool’u sıralı şekilde çalıştırarak tam proje planı üretir.

Çalışma Akışı:

task_breakdown
↓
duration_estimator
↓
markdown_exporter

Üretilen Çıktılar:
- Görev listesi
- Süre tahminleri
- Markdown tablo
- JSON plan çıktısı
- Proje özeti

==================================================
DEMO SENARYOLARI
==================================================

Sistem içerisinde demo ve test süreçleri için hazır proje senaryoları bulunmaktadır.

Örnek Senaryolar:
- Yapay zeka destekli mobil uygulama
- E-ticaret sitesi geliştirme
- Üniversite bitirme projesi

==================================================
TEST SİSTEMİ
==================================================

Tüm tool’lar aşağıdaki komut ile test edilmektedir:

python3 -m tests.test_tools

Test sistemi aşağıdaki alanları kapsamaktadır:

- Normal kullanım testleri
- Tool chaining testleri
- Validation testleri
- Edge case testleri

==================================================
NOTLAR
==================================================

- Tool sistemi modüler yapıdadır.
- Yeni araçlar dispatcher ve tool_definitions içerisine eklenerek sisteme dahil edilebilir.
- Sistem Streamlit tabanlı UI ve LLM agent entegrasyonuna hazırdır.
- Araç sistemi Python tabanlı geliştirilmiştir.
- Tüm tool çıktıları JSON formatında standartlaştırılmıştır.