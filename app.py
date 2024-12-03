import streamlit as st
from streamlit_option_menu import option_menu

# Load pages
from data_input import main as data_input_page
from repayment import main as repayment_page
from dashboard import main as dashboard_page

# App Layout
# st.set_page_config(page_title="Liabilities Manager", layout="wide")
# st.set_page_config(page_title="Liabilities Manager", layout="wide", page_icon="🎈" ,
#     initial_sidebar_state="expanded",
#     menu_items={
#         'Get Help': 'https://www.extremelycoolapp.com/help',
#         'Report a bug': "https://www.extremelycoolapp.com/bug",
#         'About': "# This is a header. This is an *extremely* cool app!"
#     }
# )
# Sidebar Menu
with st.sidebar:
    selected = option_menu(
        "Menu",
        ["Dashboard", "Liabilities", "Portfolio"],
        icons=["house", "list-task", "pie-chart"],
        menu_icon="cast",
        default_index=0
    )

# Render the selected page
if selected == "Dashboard":
    dashboard_page()
elif selected == "Liabilities":
    data_input_page()
elif selected == "Portfolio":
    repayment_page()
