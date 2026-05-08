def task_breakdown(project_name: str) -> dict:
    """
    Projeyi temel geliştirme adımlarına böler.
    """

    project = project_name.lower()

    common_tasks = [
        "Gereksinim analizi",
        "Teknoloji araştırması",
        "UI/UX tasarımı",
        "Backend geliştirme",
        "Frontend geliştirme",
        "API entegrasyonu",
        "Test ve hata ayıklama",
        "Dokümantasyon",
        "Demo hazırlığı"
    ]

    if "mobil" in project:
        common_tasks.insert(3, "Mobil arayüz geliştirme")

    if "yapay zeka" in project or "ai" in project:
        common_tasks.insert(4, "LLM entegrasyonu")
        common_tasks.insert(5, "Prompt mühendisliği")

    return {
        "project_name": project_name,
        "task_count": len(common_tasks),
        "tasks": common_tasks
    }