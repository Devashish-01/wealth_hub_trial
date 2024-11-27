import streamlit as st
import json
import os
from utils import load_data

DATA_FILE = "liabilities.json"

def main():
    st.title("Dashboard")
    st.write("An overview of your financial liabilities and metrics.")

    # Load data
    liabilities = load_data(DATA_FILE)

    # Metrics
    total_liabilities = sum([lender["total_liabilities"] for lender in liabilities["liabilities"].values()])
    active_loans = sum([lender["active_no_of_loan"] for lender in liabilities["liabilities"].values()])
    upcoming_emis = sum([len(lender["emi_list"]) for lender in liabilities["liabilities"].values()])

    # Display Metrics
    st.metric("Total Liabilities", f"${total_liabilities:,.2f}")
    st.metric("Active Loans", active_loans)
    st.metric("Upcoming EMIs", upcoming_emis)

    # Show liabilities summary
    st.header("Liabilities Overview")
    for lender_name, details in liabilities["liabilities"].items():
        st.subheader(lender_name)
        st.write(f"Total Liabilities: ${details['total_liabilities']:.2f}")
        st.write(f"Active Loans: {details['active_no_of_loan']}")
        st.write("Loans:")
        st.json(details["loans"])
