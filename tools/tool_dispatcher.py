from tools.date_calc import date_calculator
from tools.estimator import duration_estimator
from tools.task_break import task_breakdown
from tools.exporter import markdown_exporter


def run_tool(tool_name: str, arguments: dict) -> dict:
    """
    Tool adını ve parametrelerini alır, ilgili fonksiyonu çalıştırır.

    Args:
        tool_name: çalıştırılacak aracın adı
        arguments: araca gönderilecek parametreler

    Returns:
        ilgili aracın çıktısı
    """

    try:
        if tool_name == "date_calculator":
            return date_calculator(
                start_date=arguments["start_date"],
                amount=arguments["amount"],
                unit=arguments["unit"]
            )

        elif tool_name == "duration_estimator":
            return duration_estimator(
                task_name=arguments["task_name"],
                complexity=arguments.get("complexity", "medium")
            )

        elif tool_name == "task_breakdown":
            return task_breakdown(
                project_name=arguments["project_name"]
            )

        elif tool_name == "markdown_exporter":
            return markdown_exporter(
                project_name=arguments["project_name"],
                tasks=arguments["tasks"]
            )

        else:
            return {
                "success": False,
                "error": f"Bilinmeyen araç adı: {tool_name}"
            }

    except KeyError as error:
        return {
            "success": False,
            "error": f"Eksik parametre: {str(error)}"
        }

    except Exception as error:
        return {
            "success": False,
            "error": f"Araç çalıştırılırken hata oluştu: {str(error)}"
        }