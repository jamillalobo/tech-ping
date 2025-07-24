from typing import List, Dict, Any

def format_prompt_text(items: List[Dict[str, Any]], fields: List[str], empty_message: str) -> str:
    if not items:
        return empty_message
    
    formatted = []

    for item in items[:10]:
        parts = [item.get(field, "") for field in fields]
        formatted.append("\n".join(parts).strip())

    return "\n\n".join(formatted)

