from tools.date_calc import date_calculator
from tools.estimator import duration_estimator
from tools.task_break import task_breakdown
from tools.tool_definitions import TOOL_DEFINITIONS
from tools.exporter import markdown_exporter


print("Date calculator test:")
print(date_calculator("2026-05-06", 3, "week"))

print("\nDuration estimator test:")
print(duration_estimator("Backend API geliştirme", "high"))

print("\nTask breakdown test:")
print(task_breakdown("Yapay zeka destekli mobil uygulama"))

print("\nTool definitions test:")
for tool in TOOL_DEFINITIONS:
    print(f"- {tool['name']}: {tool['description']}")
    print("\nMarkdown exporter test:")
breakdown_result = task_breakdown("Yapay zeka destekli mobil uygulama")
export_result = markdown_exporter(
    breakdown_result["project_name"],
    breakdown_result["tasks"]
)

print(export_result["markdown"])