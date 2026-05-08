from tools.task_break import task_breakdown
from tools.estimator import duration_estimator
from tools.exporter import markdown_exporter


def generate_project_plan(project_name: str) -> dict:
    """
    Projeyi analiz eder,
    görevleri oluşturur,
    süre tahmini yapar,
    markdown plan üretir.
    """

    # 1. Görevleri oluştur
    breakdown_result = task_breakdown(project_name)

    if not breakdown_result.get("tasks"):
        return {
            "success": False,
            "error": "Görevler oluşturulamadı."
        }

    tasks = breakdown_result["tasks"]

    # 2. Her görev için süre tahmini yap
    detailed_tasks = []

    for task in tasks:
        estimation = duration_estimator(task)

        detailed_tasks.append({
            "task": task,
            "estimated_min_days": estimation["min"],
            "estimated_max_days": estimation["max"]
        })

    # 3. Markdown çıktısı oluştur
    markdown_tasks = []

    for item in detailed_tasks:
        markdown_tasks.append(
            f"{item['task']} "
            f"({item['estimated_min_days']}-{item['estimated_max_days']} gün)"
        )

    markdown_result = markdown_exporter(
        project_name,
        markdown_tasks
    )

    return {
        "success": True,
        "project_name": project_name,
        "tasks": detailed_tasks,
        "markdown": markdown_result["markdown"]
    }