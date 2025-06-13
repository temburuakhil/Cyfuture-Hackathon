def generate_summary(df):
    total = len(df)
    matched = (df["match_status"] == "✅ Matched").sum()
    mismatched = (df["match_status"] == "⚠️ Mismatched").sum()
    missing = (df["match_status"] == "❌ Missing in GSTR-2A").sum()

    return {
        "Total Invoices": total,
        "Matched": matched,
        "Mismatched": mismatched,
        "Missing": missing,
        "Accuracy (%)": round((matched / total) * 100, 2)
    }
