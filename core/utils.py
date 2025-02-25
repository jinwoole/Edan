import re
import uuid

def generate_unique_id():
    return str(uuid.uuid4())

def count_tokens(text):
    return len(text.split()) * 1.5

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text

def truncate_text(text, max_length=100):
    if len(text) <= max_length:
        return text
    return text[:max_length] + '...'