import streamlit as st
import json
from utils import *
from datetime import date
import os
# Load existing data or initialize empty
st.set_page_config(page_title="liability management" , page_icon="🎈" , layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

DATA_FILE = "liabilities.json"

def load_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            st.warning("Data file is corrupted. Resetting to default structure.")
            return {"liabilities": {}}
    else:
        return {"liabilities": {}}

liabilities_data = load_data(DATA_FILE)

# Save data function
def save_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
        

# liabilities_data = load_data(DATA_FILE)

def main():
    st.title("Liabilities Management")
    st.write("Add new liabilities or manage existing ones.")

    # Add Liability Form
    with st.expander("Add Liability"):
        
        name = st.text_input("Name", placeholder="Enter liability name")
        principle = st.number_input("Principle", min_value=0.0, step=1.0)
        interest_rate = st.number_input("Interest Rate per month (%)",step=1.,format="%.2f")
        deadline_months = st.number_input("Deadline (Months)", min_value=0.0, step=1.0)
        interest_payment_interval = st.number_input("interest payment interval (months.dates)",step=1.,format="%.2f")
        active = st.checkbox("Active", value=True)
        transaction_date = st.date_input("Transaction Date (year - month - date)")
        remark = st.text_input("Remark", placeholder="Add any remarks")

        # Add loan button
        if st.button("Add Loan"):
            if name:
                if name not in liabilities_data["liabilities"]:
                    liabilities_data["liabilities"][name] = {
                        "active": True,
                        "active_no_of_loan": 0,
                        "loans": {},
                        "total_liabilities": 0,
                        "emi_list": {}
                    }
                liability = liabilities_data["liabilities"][name]

                # Generate next loan ID
                next_id = get_next_id(liability["loans"])

                interest_amount = (principle * (interest_rate*interest_payment_interval))/100

                emi_list_ = emi_list(transaction_date, deadline_months, interest_payment_interval, interest_amount, name, next_id)
                
                #interest accumulated till now ,paid emi excluded
                interest_accumulated_ = interest_accumulated(emi_list_ ,   transaction_date   ,interest_rate , principle)
                
                # Add the loan to the liabilities data
                liability["loans"][next_id] = {
                    "active": active,
                    "transaction_date": str(transaction_date),  # Convert to string
                    "date_of_data_entry": str(date.today()),  # Convert to string
                    "main_principle": principle,
                    "current_principle": principle,
                    "interest_rate": interest_rate,
                    "interest_payment_interval_months": interest_payment_interval,
                    "deadline_months": deadline_months,
                    "Interest_accumulated_till_today" : interest_accumulated_ ,
                    "remark": remark,
                    "upcoming_emi_list": emi_list_,
                    "repayment_list": {}
                }
                liability["active_no_of_loan"] += 1
                liability["total_liabilities"] += principle

                # Save data to file
                save_data(DATA_FILE, liabilities_data)

                st.success(f"Loan added successfully to '{name}' with ID {next_id}!")
            else:
                st.error("Name is required to add a loan.")

# Display liabilities
    st.header("Current Liabilities")
    if liabilities_data["liabilities"]:
        for liability_name, details in liabilities_data["liabilities"].items():
            st.subheader(f"Name: {liability_name}")
            st.write(f"Active: {details['active']}")
            st.write(f"Number of Active Loans: {details['active_no_of_loan']}")
            st.write(f"Total Liabilities: {details['total_liabilities']}")
            st.write("Loans:")
            if details["loans"]:
                for loan_id, loan_details in details["loans"].items():
                    st.write(f"- Loan ID {loan_id}:")
                    st.write(loan_details)
            else:
                st.write("No loans added yet.")
    else:
        st.write("No liabilities found.")
