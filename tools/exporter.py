def markdown_exporter(project_name: str, tasks: list) -> dict:
    """
    Görev listesini Markdown formatında tabloya dönüştürür.

    Args:
        project_name: Proje adı
        tasks: Görev listesi

    Returns:
        Markdown tablo çıktısı
    """

    if not tasks:
        return {
            "success": False,
            "error": "Görev listesi boş olamaz."
        }

    markdown = f"# {project_name} - Proje Planı\n\n"
    markdown += "| No | Görev |\n"
    markdown += "|---|---|\n"

    for index, task in enumerate(tasks, start=1):
        markdown += f"| {index} | {task} |\n"

    return {
        "success": True,
        "project_name": project_name,
        "markdown": markdown
    }