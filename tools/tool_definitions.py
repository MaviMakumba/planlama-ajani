TOOL_DEFINITIONS = [
    {
        "name": "date_calculator",
        "description": "Başlangıç tarihine gün, hafta veya ay ekleyerek hedef tarihi hesaplar.",
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Başlangıç tarihi. Format: YYYY-MM-DD"
                },
                "amount": {
                    "type": "integer",
                    "description": "Eklenecek miktar. Örneğin 3"
                },
                "unit": {
                    "type": "string",
                    "enum": ["day", "week", "month"],
                    "description": "Eklenecek zaman birimi"
                }
            },
            "required": ["start_date", "amount", "unit"]
        }
    },
    {
        "name": "duration_estimator",
        "description": "Görev adına ve karmaşıklık seviyesine göre tahmini süre aralığı üretir.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_name": {
                    "type": "string",
                    "description": "Süresi tahmin edilecek görev adı"
                },
                "complexity": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "Görevin karmaşıklık seviyesi"
                }
            },
            "required": ["task_name"]
        }
    },
    {
        "name": "task_breakdown",
        "description": "Verilen proje adını yazılım geliştirme sürecine uygun alt görevlere böler.",
        "parameters": {
            "type": "object",
            "properties": {
                "project_name": {
                    "type": "string",
                    "description": "Alt görevlere bölünecek proje adı"
                }
            },
            "required": ["project_name"]
        }
    },
        {
        "name": "markdown_exporter",
        "description": "Oluşturulan görev listesini okunabilir Markdown tablo formatına dönüştürür.",
        "parameters": {
            "type": "object",
            "properties": {
                "project_name": {
                    "type": "string",
                    "description": "Markdown çıktısında kullanılacak proje adı"
                },
                "tasks": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Markdown tabloya dönüştürülecek görev listesi"
                }
            },
            "required": ["project_name", "tasks"]
        }
    }
]