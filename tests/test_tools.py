from tools.date_calc import date_calculator
from tools.estimator import duration_estimator
from tools.task_break import task_breakdown
from tools.tool_definitions import TOOL_DEFINITIONS


print("Date calculator test:")
print(date_calculator("2026-05-06", 3, "week"))

print("\nDuration estimator test:")
print(duration_estimator("Backend API geliştirme", "high"))

print("\nTask breakdown test:")
print(task_breakdown("Yapay zeka destekli mobil uygulama"))

print("\nTool definitions test:")
for tool in TOOL_DEFINITIONS:
    print(f"- {tool['name']}: {tool['description']}")