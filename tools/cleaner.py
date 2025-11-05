import streamlit as st
import pandas as pd
from io import BytesIO


def cleaner():
    task_status = 0

    st.title('File Cleaner')

    col11, col12 = st.columns(2)
    with col11:
        with st.container(border=True):
            raw_file = st.file_uploader(
                label='Upload Raw File',
                type=['xls', 'xlsx']
            )

    if raw_file:
        df = pd.read_excel(raw_file)
        df_columns = df.columns.to_list()
        
        with col11:
            with st.container(border=True):
                out_fname = st.text_input(
                    label='Output Filename')

        col1, col2, col3, col4 = st.columns(4)
        if out_fname:
            with col1:
                with st.container(border=True):
                    st.subheader('Duplicates')
                    cb_cleaner = st.checkbox(
                        label='Remove Duplicates',
                        help='Only the first occurrence will be retained')
                    
                    if cb_cleaner:
                        selected_columns = st.multiselect(
                            label='Select Columns',
                            options=df_columns,
                            help='Select columns for basis of duplication')
                    
                    if cb_cleaner and len(selected_columns)>0:
                        task_status += 1
    
    if task_status > 0:
        with col1:
            with st.container():
                btn_process = st.button(  
                    label='Process',
                    width='stretch')
                        
                if btn_process:
                    with st.spinner(text='Processing File',show_time=True):
                        cleaned_df = df.drop_duplicates(subset=selected_columns)
                        st.write(cleaned_df.shape[0])

                        output = BytesIO()
                        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                            cleaned_df.to_excel(writer, index=False, sheet_name='CleanedData')
                        processed_data = output.getvalue()
                    
                        st.download_button(
                        label="📥 Download Cleaned Excel File",
                        data=processed_data,
                        file_name="cleaned_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
