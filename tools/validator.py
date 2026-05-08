def validate_required_fields(arguments: dict, required_fields: list) -> dict:
    """
    Gerekli parametreler var mı kontrol eder.
    """

    missing_fields = []

    for field in required_fields:
        if field not in arguments or arguments[field] in [None, ""]:
            missing_fields.append(field)

    if missing_fields:
        return {
            "success": False,
            "error": f"Eksik parametreler: {', '.join(missing_fields)}"
        }

    return {
        "success": True
    }


def validate_enum(value: str, allowed_values: list, field_name: str) -> dict:
    """
    Parametre değeri izin verilen değerlerden biri mi kontrol eder.
    """

    if value not in allowed_values:
        return {
            "success": False,
            "error": f"{field_name} alanı şu değerlerden biri olmalıdır: {', '.join(allowed_values)}"
        }

    return {
        "success": True
    }


def validate_positive_number(value, field_name: str) -> dict:
    """
    Sayısal değerin pozitif olup olmadığını kontrol eder.
    """

    if not isinstance(value, (int, float)):
        return {
            "success": False,
            "error": f"{field_name} sayısal bir değer olmalıdır."
        }

    if value <= 0:
        return {
            "success": False,
            "error": f"{field_name} pozitif bir değer olmalıdır."
        }

    return {
        "success": True
    }