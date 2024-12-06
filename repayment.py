import streamlit as st
import json
from utils import *
import pandas as pd
from datetime import date , datetime 

# Set page config as the first Streamlit command
# st.set_page_config(page_title="Portfolio Management", layout="wide")

DATA_FILE = "liabilities.json"

def delete_lender(liabilities, lender_name):
    """Delete an entire lender from the liabilities"""
    if lender_name in liabilities["liabilities"]:
        del liabilities["liabilities"][lender_name]
        save_data(liabilities, DATA_FILE)
        st.success(f"Lender {lender_name} has been completely removed.")
        return True
    return False

def delete_loan(liabilities, lender_name, loan_id):
    """Delete a specific loan from a lender"""
    if lender_name in liabilities["liabilities"]:
        lender = liabilities["liabilities"][lender_name]
        if loan_id in lender["loans"]:
            # Reduce total liabilities and active loan count
            lender["total_liabilities"] -= lender["loans"][loan_id]["main_principle"]
            lender["active_no_of_loan"] -= 1
            
            # Remove the loan
            del lender["loans"][loan_id]
            
            # Save changes
            save_data(liabilities, DATA_FILE)
            st.success(f"Loan {loan_id} for {lender_name} has been deleted.")
            return True
    return False

def main():
    st.title("Portfolio Management")
    st.write("View lender portfolios, manage repayments, and track liabilities.")

    # Load liabilities
    liabilities = load_data(DATA_FILE)

    # Check if there are any lenders
    if not liabilities["liabilities"]:
        st.warning("No lenders found. Please add a lender first.")
        return

    # Lender Selection
    lender_names = list(liabilities["liabilities"].keys())
    lender_name = st.selectbox("Select Lender", lender_names)

    if lender_name:
        lender = liabilities["liabilities"][lender_name]
        
        # Lender Summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Liabilities", f"₹{lender['total_liabilities']:,.2f}")
        with col2:
            st.metric("Active Loans", lender['active_no_of_loan'])
        with col3:
            st.metric("Lender Status", "Active" if lender['active'] else "Inactive")

        # Loan Management Section
        st.subheader("Loan Details")
        
        # Tabs for different views
        tab1, tab2 = st.tabs(["Loan Overview", "Loan Actions"])
        
        with tab1:
            # Loan Overview
            for loan_id, loan in lender["loans"].items():
                with st.expander(f"Loan {loan_id} Details"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Principal:** ₹{loan['main_principle']:,.2f}")
                        st.write(f"**Current Principal:** ₹{loan['current_principle']:,.2f}")
                        st.write(f"**Interest Rate:** {loan['interest_rate']}%")
                    with col2:
                        st.write(f"**Transaction Date:** {loan['transaction_date']}")
                        st.write(f"**Deadline:** {loan['deadline_months']} months")
                        st.write(f"**Status:** {'Active' if loan['active'] else 'Inactive'}")
                    
                    # EMI Schedule
                    st.subheader("Upcoming EMI Schedule")
                    emi_df = pd.DataFrame(loan['upcoming_emi_list'])
                    updated_emi_list = []
                    render_emi_section_tab("Due Today", emi_df, updated_emi_list)
                    if st.button("💾 Save Changes"):
                        updated_json = update_json_with_done(liabilities, updated_emi_list)
                        save_data(updated_json, DATA_FILE)
                        st.success("🎉 EMI statuses updated and saved to JSON!")

        with tab2:
            # Loan Actions
            st.subheader("Loan Management")
            
            # Repayment Form
            with st.form("repayment_form"):
                st.write("Loan Repayment")
                loan_id = st.selectbox("Select Loan", list(lender["loans"].keys()))
                amount = st.number_input("Repayment Amount", min_value=0.0)
                remark = st.text_input("Remark (optional)")
                confirm = st.form_submit_button("Submit Repayment")

                if confirm:
                    loan = lender["loans"][loan_id]
                    final_loan = loan["current_principle"]  + loan["Interest_accumulated_till_today"] 
                    #update loan["final_amount"] in all places
                    if amount == final_loan:
                        loan["current_principle"] = 0
                        loan["final_amount"] = 0
                        loan["interest_payment_interval_months"] = remove_further_emi(loan)

                    elif amount > loan["current_principle"]:
                        st.error("Repayment amount exceeds remaining balance.")
                    else:
                        # Update loan details
                        loan["current_principle"] -= amount
                        
                        # Add to repayment list
                        if "repayment_list" not in loan:
                            loan["repayment_list"] = {}
                        
                        repayment_id = len(loan["repayment_list"]) + 1
                        loan["repayment_list"][str(repayment_id)] = {
                            "date": str(date.today()),
                            "amount": amount,
                            "remark": remark
                        }

                        # Save changes
                        save_data(liabilities, DATA_FILE)
                        st.success("Repayment successful!")

            # Deletion Actions
            st.subheader("Danger Zone")
            col1, col2 = st.columns(2)
            
            with col1:
                # Delete Loan
                st.write("**Delete Specific Loan**")
                loan_to_delete = st.selectbox("Select Loan to Delete", list(lender["loans"].keys()))
                if st.button("Delete Selected Loan", type="primary"):
                    delete_loan(liabilities, lender_name, loan_to_delete)
                    st.experimental_rerun()

            with col2:
                # Delete Entire Lender
                st.write("**Delete Entire Lender**")
                if st.button("Delete Lender", type="primary"):
                    delete_lender(liabilities, lender_name)
                    st.experimental_rerun()

if __name__ == "__main__":
    main()