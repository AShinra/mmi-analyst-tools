import streamlit as st
import calendar
from datetime import date, datetime


def basic_report():
    
    col11, col12 = st.columns([1,2])
    with col11:
        st.header('🗄️File Handler')
        with st.container(border=True):
            raw_file = st.file_uploader(
                label='Upload Cleaned File',
                type=['xls', 'xlsx'])
            
            if raw_file:
                with col11:
                    with st.container(border=True):
                        out_fname = st.text_input(label='Output Filename')
                
                if out_fname:
                    with col12:
                        st.header('⚙️Parameters')
                        cola1, cola2, cola3, cola4 = st.columns(4)
                        with cola1:
                            with st.container(border=True):
                                date_selector = st.radio(
                                    label='Date Selector',
                                    options=['Date', 'Date Range'],
                                    horizontal=True)

                                if date_selector=='Date':
                                    cold1, cold2 = st.columns(2)
                                    with cold1:
                                        month_select = st.selectbox(
                                            label='Month',
                                            options=list(calendar.month_name)[1:])
                                    with cold2:
                                        now_year = date.today().year
                                        year_select = st.selectbox(
                                            label='Year',
                                            options=[year for year in range(now_year, now_year - 6, -1)]
                                        )
                                        
                                else:
                                    start_date = datetime.now().date()
                                    end_date = datetime.now().date()
                                    
                                    date_range = st.date_input(
                                        label="Select date range",
                                        value=(start_date, end_date),
                                        min_value=date(2000, 1, 1),
                                        max_value=date.today())
                                    
                        with cola2:
                            with st.container(border=True):
                                main_category_select = st.multiselect(
                                    label='Main Category',
                                    options=[]
                                )
                        
                        with cola3:
                            with st.container(border=True):
                                competitor_category_select = st.multiselect(
                                    label='Comeptitor Category',
                                    options=[]
                                )
                        
                        with cola4:
                            with st.container(border=True):
                                industry_category_select = st.multiselect(
                                    label='Industry Category',
                                    options=[]
                                )
                        
                        colb1, colb2, colb3, col44 = st.columns(4)
                        with colb1:
                            with st.container(border=True):
                                main_sheet_option = st.radio(
                                    label='Main Sheet',
                                    options=['Single', 'Mulitple'],
                                    horizontal=True
                                )

                        with colb2:
                            with st.container(border=True):
                                competitor_sheet_option = st.radio(
                                    label='Competitor Sheet',
                                    options=['Single', 'Mulitple'],
                                    horizontal=True
                                )
                        

