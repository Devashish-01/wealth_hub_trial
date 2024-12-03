import streamlit as st
import json
from datetime import date, timedelta , datetime
from dateutil.relativedelta import relativedelta


# Load Data
def load_data(file_path):
    """
    Load liabilities data from JSON file.
    Returns a default structure if the file doesn't exist or is corrupted.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"liabilities": {}}

# Save Data
def save_data(data, file_path):
    """
    Save the liabilities data to a JSON file.
    """
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def security_check():
    st.write("Enter CONFIRM to complete the transaction")
    x = st.text_input("CONFIRM")
    if(x == "CONFIRM"):
        return True
    return False

            
# Give list of emi 
def emi_list(start_date, deadline_months, interval_months, amount, lender_name, transaction_id):
    emis = []
    current_date = start_date
    end_date = start_date + relativedelta(months=deadline_months)
    count = int((end_date - start_date).days / (interval_months * 30))

    # Generate EMIs for the duration of the loan
    for i in range(count + 1):
        emis.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "amount": amount,
            "done": False,
            "lender_name": lender_name,
            "id": transaction_id,
            "remark": []
        })
        # Move to the next EMI date
        current_date = current_date + relativedelta(months=interval_months)

    return emis

def total_liability_till_today(principle , previous_emi_date , rate ):
    today_date = date.today()
    date_diff = today_date - previous_emi_date
    amount = principle * (rate/100) * (date_diff/30)/100
    return amount



def interest_accumulated(emi_list , d1 , interest_rate , current_principle): 
    d2 = date.today()
    months = (d2.year - d1.year) * 12 + (d2.month - d1.month) + d2.day / 30 - d1.day / 30
    interest_amount = (months * interest_rate * current_principle)/100
    return interest_amount , months

def change_emi_for_repayment (emi , next_emi_date , interest_made , interest_future , repayment_remark):
    current_date = date.today()
    for i in range(len(emi)) :
        if datetime.date.fromisoformat(emi[i]["date"]) == next_emi_date:
            emi[i]["amount"] = interest_future + interest_made
            emi[i]["remark"].append(f"""
            You had done one repayment on date: {date.today().strftime('%Y-%m-%d')}
            - **Interest added**: {interest_made : .2f}
            - **Repayment remark**: {repayment_remark}
            """)

        elif datetime.date.fromisoformat(emi[i]["date"]) > current_date:
            emi[i]["amount"] = interest_future
    return emi

import datetime

def previous_emi_date(emi_list):
    current_date = datetime.date.today()  # Get today's date
    previous_date = current_date  # Initialize previous_date to today's date
    
    for emi in emi_list:
        emi_date = datetime.date.fromisoformat(emi["date"])  # Correct usage
        if emi_date > current_date:
            break
        previous_date = emi_date
    
    return previous_date  # Return the previous EMI date


def remove_further_emi(emi):
    current_date = date.today()
    emi_updated = []
    for i in range(len(emi)):
        temp = datetime.date.fromisoformat(emi[i]["date"])
        if temp == current_date : 
            emi_updated.append(emi[i])
    return emi_updated

# Helper to find the next minimum available loan ID
def get_next_id(loans):
    existing_ids = [int(key) for key in loans.keys()] if loans else []
    return min(set(range(1, max(existing_ids, default=0) + 2)) - set(existing_ids))



