import streamlit as st
import calendar
from datetime import date, datetime
import pandas as pd
from common import gradient_line
from tools.pivot import pivot_sheet, tonality_sheets, daily_statistics, media_statistics, share_of_voice

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
                                        options=['Single', 'Multiple'])

                                with colb12:
                                    competitor_sheet_option = st.radio(
                                        label='Competitor Sheet',
                                        options=['Single', 'Multiple'])
                                    
                                st.subheader('Additional Sheets')
                                cb_tonality_sheets = st.checkbox(label='Tonality Sheets')
                            
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
                                label='Create Report')

                            if btn_create_br:
                                # gather main sheet data
                                if main_category_select:
                                    st.write('Main')
                                    main_data_frame_set = pivot_sheet(
                                        data_frame=df,
                                        category=main_category_select)
                                    
                                    if main_sheet_option=='Single':
                                        st.dataframe(pd.concat(main_data_frame_set))
                                    elif main_sheet_option=='Multiple':
                                        for data_frame_set in main_data_frame_set:
                                            st.dataframe(data_frame_set)
                                
                                # gather competitor sheet data
                                if competitor_category_select:
                                    st.write('Competitor')
                                    competitor_data_frame_set = pivot_sheet(
                                        data_frame=df,
                                        category=competitor_category_select)
                                    
                                    if competitor_sheet_option=='Single':
                                        st.dataframe(pd.concat(competitor_data_frame_set))
                                    elif competitor_sheet_option=='Multiple':
                                        for data_frame_set in competitor_data_frame_set:
                                            st.dataframe(data_frame_set)
                                
                                # gather industry sheet data
                                if industry_category_select:
                                    st.write('Industry')
                                    industry_data_frame_set = pivot_sheet(
                                        data_frame=df,
                                        category=industry_category_select)
                                    
                                    st.dataframe(pd.concat(industry_data_frame_set))
                                
                                if cb_tonality_sheets:
                                    st.write('Tonality Sheets')
                                    tone_data_frame_set = tonality_sheets(
                                        data_frame=df,
                                        category=main_category_select)
                                    
                                    for tone, data_frame_set in tone_data_frame_set.items():
                                        st.write(tone)
                                        st.dataframe(data_frame_set)

                                if daily_stats:
                                    st.write('Daily Statistics')
                                    daily_stats_dict = daily_statistics(
                                        data_frame=df,
                                        category=main_category_select)
                                    
                                    for k, v in daily_stats_dict.items():
                                        st.write(k)
                                        st.dataframe(v)

                                if media_stats:
                                    st.write('Media Statistics')
                                    media_statistics(
                                        data_frame=df,
                                        category=main_category_select)
                                
                                if share_voice:
                                    st.write('Share of Voice')
                                    share_of_voice(
                                        data_frame=df,
                                        category=main_category_select + competitor_category_select)
                                    
                                    
