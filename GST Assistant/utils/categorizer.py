from utils.gemini_api import ask_gemini

def categorize_invoice(invoice):
    prompt = f"""
    Categorize this invoice into [B2B, B2C, Export, SEZ, Reverse Charge].

    Invoice:
    {invoice}

    Return JSON format:
    {{ "category": "<Category>", "reason": "<Short Reason>" }}
    """
    response = ask_gemini(prompt)
    try:
        return eval(response)
    except:
        return {"category": "Uncategorized", "reason": "Parsing error"}
