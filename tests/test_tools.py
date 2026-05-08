from tools.date_calc import date_calculator
from tools.estimator import duration_estimator
from tools.task_break import task_breakdown
from tools.tool_definitions import TOOL_DEFINITIONS
from tools.exporter import markdown_exporter
from tools.tool_dispatcher import run_tool


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

print("\nTool dispatcher test:")

dispatcher_result = run_tool("date_calculator", {
    "start_date": "2026-05-06",
    "amount": 2,
    "unit": "week"
})

print(dispatcher_result)

unknown_tool_result = run_tool("unknown_tool", {})
print(unknown_tool_result)

print("\nEdge case testleri:")

print(run_tool("date_calculator", {
    "start_date": "2026-05-06",
    "amount": -2,
    "unit": "week"
}))

print(run_tool("date_calculator", {
    "start_date": "2026-05-06",
    "amount": 2,
    "unit": "hafta"
}))

print(run_tool("duration_estimator", {
    "task_name": "Backend geliştirme",
    "complexity": "zor"
}))

print(run_tool("markdown_exporter", {
    "project_name": "Test Projesi",
    "tasks": "liste değil"
}))