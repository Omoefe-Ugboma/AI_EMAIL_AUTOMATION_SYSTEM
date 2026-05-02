import re

def anonymize_text(text: str):
    text = re.sub(r'\S+@\S+', '[EMAIL]', text)
    return text