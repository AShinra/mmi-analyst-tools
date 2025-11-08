import streamlit as st
import calendar
from datetime import date, datetime
import pandas as pd
from common import gradient_line

st.cache_data()
def get_categories(df):
    return sorted(list(set(df['Category'].to_list())))

def basic_report():
    
    col11, col12 = st.columns([1,2])
    with col11:
        st.header('🗄️File Handler')
        gradient_line()
        with st.container(border=True):
            raw_file = st.file_uploader(
                label='Upload Cleaned File',
                type=['xls', 'xlsx'])
                        
            if raw_file:

                df = pd.read_excel(raw_file)            
                initial_categories = get_categories(df)

                with col11:
                    with st.container(border=True):
                        out_fname = st.text_input(label='Output Filename')
                
                if out_fname:
                    with col12:
                        st.header('⚙️Parameters')
                        gradient_line()
                        cola1, cola2 = st.columns([2,3], border=True)
                        with cola1:
                            st.subheader('Report Information')
                            
                            with st.container(border=True):
                                report_client = st.text_input(
                                    label='Client Name')
                        
                            with st.container(border=True):
                                date_selector = st.radio(
                                    label='Date Selector',
                                    options=['Date', 'Date Range'])

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
                                            options=[year for year in range(now_year, now_year - 6, -1)])
                                        
                                else:
                                    start_date = datetime.now().date()
                                    end_date = datetime.now().date()
                                    
                                    date_range = st.date_input(
                                        label="Select date range",
                                        value=(start_date, end_date),
                                        min_value=date(2000, 1, 1),
                                        max_value=date.today())
                                    
                        with cola2:
                            st.subheader('Category Select')
                            cola21, cola22, cola23 = st.columns(3, border=True)
                            with cola21:
                                main_category_select = st.multiselect(
                                    label='Main Category',
                                    options=initial_categories)

                                if main_category_select != []:
                                    for category in main_category_select:
                                        initial_categories.remove(category)
                        
                            with cola22:
                                competitor_category_select = st.multiselect(
                                    label='Competitor Category',
                                    options=initial_categories)

                                if competitor_category_select != []:
                                    for category in competitor_category_select:
                                        initial_categories.remove(category)
                        
                            with cola23:
                                industry_category_select = st.multiselect(
                                    label='Industry Category',
                                    options=initial_categories)
                        
                            colb1, colb2 = st.columns([2, 1], border=True)
                            with colb1:
                                st.subheader('Sheet Layout')
                                colb11, colb12 = st.columns(2, border=True)
                                with colb11:
                                    main_sheet_option = st.radio(
                                        label='Main Sheet',
                                        options=['Single', 'Mulitple'])

                                with colb12:
                                    competitor_sheet_option = st.radio(
                                        label='Competitor Sheet',
                                        options=['Single', 'Mulitple'])
                            
                            with colb2:
                                st.subheader('Chart Select')
                                with st.container(border=True):
                                    daily_stats = st.checkbox(
                                        label='Daily Statistics')
                                    media_stats = st.checkbox(
                                        label='Media Statistics')
                                    share_voice = st.checkbox(
                                        label='Share of Voice')
                                
                        
                        if report_client and (main_category_select or competitor_category_select):
                            btn_create_br = st.button(
                                label='Create Report'
                            )
