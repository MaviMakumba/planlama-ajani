from tools.date_calc import date_calculator
from tools.estimator import duration_estimator
from tools.task_break import task_breakdown
from tools.exporter import markdown_exporter

from tools.validator import (
    validate_required_fields,
    validate_enum,
    validate_positive_number
)


def run_tool(tool_name: str, arguments: dict) -> dict:
    """
    Tool adını ve parametrelerini alır, ilgili fonksiyonu güvenli şekilde çalıştırır.
    """

    try:
        if not isinstance(arguments, dict):
            return {
                "success": False,
                "error": "arguments dict formatında olmalıdır."
            }

        if tool_name == "date_calculator":
            required_check = validate_required_fields(
                arguments,
                ["start_date", "amount", "unit"]
            )
            if not required_check["success"]:
                return required_check

            amount_check = validate_positive_number(arguments["amount"], "amount")
            if not amount_check["success"]:
                return amount_check

            unit_check = validate_enum(
                arguments["unit"],
                ["day", "week", "month"],
                "unit"
            )
            if not unit_check["success"]:
                return unit_check

            return date_calculator(
                start_date=arguments["start_date"],
                amount=arguments["amount"],
                unit=arguments["unit"]
            )

        if tool_name == "duration_estimator":
            required_check = validate_required_fields(arguments, ["task_name"])
            if not required_check["success"]:
                return required_check

            complexity = arguments.get("complexity", "medium")

            complexity_check = validate_enum(
                complexity,
                ["low", "medium", "high"],
                "complexity"
            )
            if not complexity_check["success"]:
                return complexity_check

            return duration_estimator(
                task_name=arguments["task_name"],
                complexity=complexity
            )

        if tool_name == "task_breakdown":
            required_check = validate_required_fields(arguments, ["project_name"])
            if not required_check["success"]:
                return required_check

            return task_breakdown(
                project_name=arguments["project_name"]
            )

        if tool_name == "markdown_exporter":
            required_check = validate_required_fields(
                arguments,
                ["project_name", "tasks"]
            )
            if not required_check["success"]:
                return required_check

            if not isinstance(arguments["tasks"], list):
                return {
                    "success": False,
                    "error": "tasks liste formatında olmalıdır."
                }

            return markdown_exporter(
                project_name=arguments["project_name"],
                tasks=arguments["tasks"]
            )

        return {
            "success": False,
            "error": f"Bilinmeyen araç adı: {tool_name}"
        }

    except Exception as error:
        return {
            "success": False,
            "error": f"Araç çalıştırılırken hata oluştu: {str(error)}"
        }