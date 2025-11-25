import streamlit as st
from streamlit_option_menu import option_menu
from common import get_client, gradient_line
# from product_mgt import product_management
# from stock_mgt import stock_management
# from tracking_reports import tracking_reports
from users_management import user_management
from tools.cleaner import cleaner
from tools.basic_report import basic_report


def main_start(fname, rights):

    with st.sidebar:
        if rights=='admin':
            options_list=['Report Tools', 'Settings']
            icons_list=['wrench-adjustable', 'gear']
        elif rights=='sub-admin':
            options_list=[]
            icons_list=[]
        else:
            options_list=['Report Tools']
            icons_list=['wrench-adjustable']

        st.sidebar.header(f':red[Welcome :blue[*{fname.title()}*]] 👤')
        gradient_line()
        selected = option_menu(
            menu_title='MARSv1.0',
            menu_icon='list-columns',
            options=options_list,
            icons=icons_list
        )
        
        if selected=='Report Tools':
            sub_selected = option_menu(
                menu_title=None,
                options=['Cleaner', 'Report'],
                icons=['magic', 'file-earmark-spreadsheet-fill']
        )
        
        if selected=='Settings':
            sub_selected = option_menu(
                menu_title=None,
                options=['User Management'],
                icons=['people-fill']
        )
            

        btn_clearcache = st.button('**Clear Cache**', use_container_width=True)
    
    if sub_selected=='User Management':
        user_management()
    
    if sub_selected=='Cleaner':
        cleaner()
    
    if sub_selected=='Report':
        basic_report()


        
    
    
    
    

