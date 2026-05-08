from tools.date_calc import date_calculator
from tools.estimator import duration_estimator


print("Date calculator test:")
print(date_calculator("2026-05-06", 3, "week"))

print("\nDuration estimator test:")
print(duration_estimator("Backend API geliştirme", "high"))