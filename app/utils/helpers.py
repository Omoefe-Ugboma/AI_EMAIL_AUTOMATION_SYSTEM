VALID_CATEGORIES = ["complaint", "request", "inquiry", "feedback", "general"]

def normalize_category(category: str) -> str:
    category = category.lower().strip()
    return category if category in VALID_CATEGORIES else "general"