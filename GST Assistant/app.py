import streamlit as st
import pandas as pd
from utils.reconciler import reconcile_invoices
from utils.reporter import generate_summary
from utils.parser import load_invoice_data
from utils.categorizer import categorize_invoice
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="GST Reconciliation Assistant", layout="wide")

st.title("📊 GST Reconciliation Assistant")

invoice_file = st.file_uploader("Upload Invoice JSON", type=["json"])
gstr2a_file = st.file_uploader("Upload GSTR-2A Excel", type=["xlsx"])

if invoice_file and gstr2a_file:
    invoice_data = load_invoice_data(invoice_file)
    gstr2a_df = pd.read_excel(gstr2a_file)

    for invoice in invoice_data:
        result = categorize_invoice(invoice)
        invoice["category"] = result["category"]
        invoice["reason"] = result["reason"]

    invoice_df = pd.DataFrame(invoice_data)
    st.subheader("📄 Categorized Invoices")
    st.dataframe(invoice_df)

    match_result = reconcile_invoices(invoice_df, gstr2a_df)
    st.subheader("🔍 GST Reconciliation Result")
    st.dataframe(match_result)

    summary = generate_summary(match_result)
    st.subheader("📋 Reconciliation Summary")
    st.json(summary)

    st.download_button("Download Result CSV", match_result.to_csv(index=False), "reconciliation_result.csv")
