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

#remove all emis having due_date > current_date
def remove_further_emi(loan):
    emi = loan["interest_payment_interval_months"]

    current_date = date.today()
    emi_updated = []
    for i in range(len(emi)):
        temp = datetime.date.fromisoformat(emi[i]["date"])
        if temp <  current_date : 
            emi_updated.append(emi[i])
    return emi_updated

# Helper to find the next minimum available loan ID
def get_next_id(loans):
    existing_ids = [int(key) for key in loans.keys()] if loans else []
    return min(set(range(1, max(existing_ids, default=0) + 2)) - set(existing_ids))

# Extract Upcoming EMI List of speific lender
def upcoming_emi_list(liabilities):
    emi_list = []
    today = date.today()  # Current date
    
    # Iterate through lenders
    for lender, lender_data in liabilities.items():
        # Iterate through loans
        for loan_id, loan_data in lender_data["loans"].items():
            # Iterate through the upcoming EMI list
            for emi in loan_data["upcoming_emi_list"]:
                emi_date = datetime.date.fromisoformat(emi["date"])
                # Check if EMI date is in the future and the EMI is not done
                if today < emi_date and not emi["done"]:
                    emi_list.append(emi)
    sorted_emi_list = sorted(emi_list, key=lambda x: datetime.date.fromisoformat(x["date"]))
    return sorted_emi_list

# Extract Upcoming EMI List
def upcoming_emi_list(liabilities):
    emi_list = []
    today = date.today()  # Current date
    
    # Iterate through lenders
    for lender, lender_data in liabilities.items():
        # Iterate through loans
        for loan_id, loan_data in lender_data["loans"].items():
            # Iterate through the upcoming EMI list
            for emi in loan_data["upcoming_emi_list"]:
                emi_date = datetime.date.fromisoformat(emi["date"])
                # Check if EMI date is in the future and the EMI is not done
                if today < emi_date and not emi["done"]:
                    emi_list.append(emi)
    sorted_emi_list = sorted(emi_list, key=lambda x: datetime.date.fromisoformat(x["date"]))
    return sorted_emi_list


# Extract Upcoming EMI List
def get_upcoming_emi(liabilities):
    emi_list = []
    today = date.today()  # Current date
    
    # Iterate through lenders
    for lender, lender_data in liabilities.items():
        # Iterate through loans
        for loan_id, loan_data in lender_data["loans"].items():
            # Iterate through the upcoming EMI list
            for emi in loan_data["upcoming_emi_list"]:
                emi_date = datetime.date.fromisoformat(emi["date"])
                # Check if EMI date is in the future and the EMI is not done
                if today < emi_date and not emi["done"]:
                    emi_list.append(emi)
    sorted_emi_list = sorted(emi_list, key=lambda x: datetime.date.fromisoformat(x["date"]))
    return sorted_emi_list

def get_complete_emi(liabilities):
    emi_list = []
    today = date.today()  # Current date
    
    # Iterate through lenders
    for lender, lender_data in liabilities.items():
        # Iterate through loans
        for loan_id, loan_data in lender_data["loans"].items():
            # Iterate through the upcoming EMI list
            for emi in loan_data["upcoming_emi_list"]:
                # Check if EMI date is in the future and the EMI is not done
                if emi["done"]:
                    emi_list.append(emi)
    sorted_emi_list = sorted(emi_list, key=lambda x: datetime.date.fromisoformat(x["date"]))
    return sorted_emi_list

def emi_not_paid(liabilities):
    emi_list = []
    today = date.today()  # Current date
    
    # Iterate through lenders
    for lender, lender_data in liabilities.items():
        # Iterate through loans
        for loan_id, loan_data in lender_data["loans"].items():
            # Iterate through the upcoming EMI list
            for emi in loan_data["upcoming_emi_list"]:
                emi_date = datetime.date.fromisoformat(emi["date"])
                # Check if EMI date is in the future and the EMI is not done
                if today > emi_date and not emi["done"]:
                    emi_list.append(emi)
    sorted_emi_list = sorted(emi_list, key=lambda x: datetime.date.fromisoformat(x["date"]))
    return sorted_emi_list

def emi_today(liabilities):
    emi_list = []
    today = date.today()  # Current date
    
    # Iterate through lenders
    for lender, lender_data in liabilities.items():
        # Iterate through loans
        for loan_id, loan_data in lender_data["loans"].items():
            # Iterate through the upcoming EMI list
            for emi in loan_data["upcoming_emi_list"]:
                emi_date = datetime.date.fromisoformat(emi["date"])
                # Check if EMI date is in the future and the EMI is not done
                if today == emi_date and not emi["done"]:
                    emi_list.append(emi)
    sorted_emi_list = sorted(emi_list, key=lambda x: datetime.date.fromisoformat(x["date"]))
    return sorted_emi_list



# Extract EMI data from JSON
def extract_emi_data(json_data):
    emi_list = []
    for lender, lender_data in json_data["liabilities"].items():
        for loan_id, loan_data in lender_data["loans"].items():
            for emi in loan_data["upcoming_emi_list"]:
                emi["lender_name"] = lender  # Add lender name for context
                emi["loan_id"] = loan_id    # Add loan ID for context
                emi_list.append(emi)
    return emi_list

def update_json_with_done(json_data, updated_emi_list):
    for emi in updated_emi_list:
        lender_name = emi["lender_name"]
        loan_id = str(emi["id"])  # Convert loan_id to string as JSON keys are strings
        date = emi["date"]
        
        # Navigate to the correct EMI entry
        if (
            lender_name in json_data["liabilities"] and
            loan_id in json_data["liabilities"][lender_name]["loans"]
        ):
            upcoming_emi_list = json_data["liabilities"][lender_name]["loans"][loan_id]["upcoming_emi_list"]
            
            # Update the 'done' status for matching EMIs
            for loan_emi in upcoming_emi_list:
                if loan_emi["date"] == date and loan_emi["id"] == emi["id"]:
                    loan_emi["done"] = emi["done"]
    
    return json_data


def render_emi_section_tab(title, emi_df, updated_emi_list):
    """
    Renders an EMI section within a tab with checkboxes for updating 'done' status.

    Args:
        title (str): Title of the section.
        emi_df (pd.DataFrame): DataFrame containing EMI details.
        updated_emi_list (list): List to collect updated EMI rows.
    """
    st.subheader(title)

    if emi_df.empty:
        st.info(f"No EMIs in the '{title}' category.")
    else:
        # Display scrollable data for large datasets
        # st.dataframe(emi_df, height=400)

        # Display checkboxes for each row to mark 'done'
        st.write("**Mark EMIs as Paid:**")
        for index, row in emi_df.iterrows():
            new_done = st.checkbox(
                f"{row['lender_name']} | {row['date']} | ₹{row['amount']}",
                value=row["done"],
                key=f"{title}_{index}"
            )
            row["done"] = new_done
            updated_emi_list.append(row.to_dict())

