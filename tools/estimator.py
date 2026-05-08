def duration_estimator(task_name: str, complexity: str = "medium") -> dict:
    """
    Görev adına ve karmaşıklık seviyesine göre süre tahmini üretir.
    complexity: low, medium, high
    """

    task = task_name.lower()
    base_days = 2

    if "analiz" in task or "requirement" in task:
        base_days = 2
    elif "tasarım" in task or "ui" in task or "arayüz" in task:
        base_days = 3
    elif "backend" in task or "api" in task:
        base_days = 4
    elif "frontend" in task or "streamlit" in task:
        base_days = 3
    elif "test" in task:
        base_days = 2
    elif "rapor" in task or "dokümantasyon" in task:
        base_days = 2
    elif "entegrasyon" in task:
        base_days = 3

    if complexity == "low":
        min_days = max(1, base_days - 1)
        max_days = base_days
    elif complexity == "high":
        min_days = base_days
        max_days = base_days + 3
    else:
        min_days = base_days
        max_days = base_days + 1

    return {
        "task_name": task_name,
        "complexity": complexity,
        "min": min_days,
        "max": max_days,
        "unit": "gün"
    }