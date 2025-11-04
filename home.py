import streamlit as st
from streamlit_option_menu import option_menu
from common import get_client
# from product_mgt import product_management
# from stock_mgt import stock_management
# from tracking_reports import tracking_reports
from users_management import user_management


def main(username, rights):

    with st.sidebar:
        if rights=='admin':
            options_list=['Product Management', 'Stock Management', 'Tracking & Reports', 'Search & Filters', 'User Management']
            icons_list=['box2-fill', 'bag-fill', 'body-text', 'search', 'people-fill']
        elif rights=='sub-admin':
            options_list=['Entry', 'Archive', 'Summary', 'Client Management']
            icons_list=['pencil-square', 'archive', 'journals', 'gear']
        else:
            options_list=['Archive', 'Summary']
            icons_list=['archive', 'journals']

        st.sidebar.header(f':red[Welcome :blue[*{username.title()}*]] 👤')
        selected = option_menu(
            menu_title='Warehouse Inventory',
            menu_icon='list-columns',
            options=options_list,
            icons=icons_list
        )
        btn_clearcache = st.button('**Clear Cache**', use_container_width=True)
    
    # client_list = []
    # if selected=='Product Management':
    #     product_management()
            
    # elif selected=='Stock Management':
    #     stock_management()
        
    # elif selected=='Tracking & Reports':
    #     tracking_reports()
    
    if selected=='User Management':
        user_management()


        
    
    
    
    

