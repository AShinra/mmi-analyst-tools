import streamlit as st
from streamlit_option_menu import option_menu
from common import get_client
# from product_mgt import product_management
# from stock_mgt import stock_management
# from tracking_reports import tracking_reports
from users_management import user_management


def main(fname, rights):

    with st.sidebar:
        if rights=='admin':
            options_list=['User Management']
            icons_list=['people-fill']
        elif rights=='sub-admin':
            options_list=[]
            icons_list=[]
        else:
            options_list=['Report Tools']
            icons_list=['wrench-adjustable']

        st.sidebar.header(f':red[Welcome :blue[*{fname.title()}*]] 👤')
        selected = option_menu(
            menu_title='MARS V1.0',
            menu_icon='list-columns',
            options=options_list,
            icons=icons_list
        )
        btn_clearcache = st.button('**Clear Cache**', use_container_width=True)
    
    # client_list = []
    if selected=='User Management':
        user_management()


        
    
    
    
    

