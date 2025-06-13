import json

def load_invoice_data(json_file):
    content = json_file.read()
    data = json.loads(content)
    return [data] if isinstance(data, dict) else data
