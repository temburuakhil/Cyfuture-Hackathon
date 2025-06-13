import pandas as pd

def reconcile_invoices(book_df, gstr_df):
    result = []

    for _, book in book_df.iterrows():
        invoice_no = book["invoice_no"]
        match = gstr_df[gstr_df["Invoice No"] == invoice_no]

        if match.empty:
            result.append({**book, "match_status": "❌ Missing in GSTR-2A", "mismatch_reason": "Not found"})
        else:
            gstr = match.iloc[0]
            reasons = []
            if pd.to_datetime(book["invoice_date"]) != pd.to_datetime(gstr["Invoice Date"]):
                reasons.append("Date mismatch")
            if book["total_amount"] != gstr["Total Value"]:
                reasons.append("Amount mismatch")

            status = "✅ Matched" if not reasons else "⚠️ Mismatched"
            result.append({**book, "match_status": status, "mismatch_reason": ", ".join(reasons) or "-"})

    return pd.DataFrame(result)
