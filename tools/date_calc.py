from datetime import datetime
from dateutil.relativedelta import relativedelta


def date_calculator(start_date: str, amount: int, unit: str) -> dict:
    """
    start_date üzerine gün/hafta/ay ekler.
    start_date formatı: YYYY-MM-DD
    unit: day, week, month
    """

    try:
        date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()

        if unit == "day":
            result = date_obj + relativedelta(days=amount)
        elif unit == "week":
            result = date_obj + relativedelta(weeks=amount)
        elif unit == "month":
            result = date_obj + relativedelta(months=amount)
        else:
            return {
                "success": False,
                "error": "unit sadece day, week veya month olabilir."
            }

        return {
            "success": True,
            "start_date": start_date,
            "amount": amount,
            "unit": unit,
            "result_date": result.isoformat()
        }

    except ValueError:
        return {
            "success": False,
            "error": "Tarih formatı YYYY-MM-DD olmalıdır."
        }