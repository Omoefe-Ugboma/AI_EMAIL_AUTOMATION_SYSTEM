def route_email(category: str):
    mapping = {
        "finance": "Routed to Finance Department",
        "admissions": "Routed to Admissions Office",
        "academic": "Routed to Academic Office",
        "complaint": "Escalated to Support Team",
        "request": "Handled Automatically",
        "inquiry": "Handled Automatically",
        "general": "Handled Automatically"
    }

    return mapping.get(category, "Unhandled")