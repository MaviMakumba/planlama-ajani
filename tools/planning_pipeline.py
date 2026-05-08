from tools.task_break import task_breakdown
from tools.estimator import duration_estimator
from tools.exporter import markdown_exporter


def generate_project_plan(project_name: str) -> dict:
    """
    Projeyi analiz eder, alt görevlere böler, her görev için süre tahmini yapar
    ve hem JSON hem Markdown formatında plan üretir.
    """

    if not project_name or not project_name.strip():
        return {
            "success": False,
            "error": "Proje adı boş olamaz."
        }

    breakdown_result = task_breakdown(project_name)

    if not breakdown_result.get("tasks"):
        return {
            "success": False,
            "error": "Görevler oluşturulamadı."
        }

    tasks = breakdown_result["tasks"]
    detailed_tasks = []

    total_min_days = 0
    total_max_days = 0

    for index, task in enumerate(tasks, start=1):
        estimation = duration_estimator(task)

        min_days = estimation["min"]
        max_days = estimation["max"]

        total_min_days += min_days
        total_max_days += max_days

        detailed_tasks.append({
            "id": index,
            "task": task,
            "estimated_min_days": min_days,
            "estimated_max_days": max_days,
            "unit": "gün"
        })

    markdown_tasks = [
        f"{item['task']} ({item['estimated_min_days']}-{item['estimated_max_days']} gün)"
        for item in detailed_tasks
    ]

    markdown_result = markdown_exporter(project_name, markdown_tasks)

    summary = (
        f"{project_name} projesi için toplam {len(detailed_tasks)} görev oluşturuldu. "
        f"Tahmini toplam süre {total_min_days}-{total_max_days} gün aralığındadır."
    )

    return {
        "success": True,
        "project_name": project_name,
        "task_count": len(detailed_tasks),
        "estimated_total_min_days": total_min_days,
        "estimated_total_max_days": total_max_days,
        "summary": summary,
        "tasks": detailed_tasks,
        "markdown": markdown_result["markdown"]
    }