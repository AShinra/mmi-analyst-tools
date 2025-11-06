import streamlit as st
import pandas as pd
from io import BytesIO

def remove_duplicates(df, selected_columns):
    # removes duplicates from the raw file
    cleaned_df = df.drop_duplicates(subset=selected_columns)
    st.success(f'{df.shape[0] - cleaned_df.shape[0]} removed rows')
    return cleaned_df

def client_focus(df, selected_keywords):
    # creates a focus column based on number of clients mentioned in title and content
    for index, row in df.iterrows():
        title_score = 0
        content_score = 0
        for keyword in selected_keywords:
            # search in title column
            if keyword.lower() in row['Title'].lower():
                title_score += 1
            
            # search in content column
            content_text = row['Content'].lower()
            content_score = content_text.count(keyword)

        if title_score>=1 or content_score>=3:
            # st.write(f'title score {title_score}, content score {content_score} - Main')
            # row['Focus'] = 'Main'
            df.loc[index, 'Focus'] = 'Main'
        elif title_score<1 and content_score<3:
            # st.write(f'title score {title_score}, content score {content_score} - Mention')
            df.loc[index, 'Focus'] = 'Mention'
    
    return df


def cleaner():
    task_status = 0

    st.title('File Cleaner')

    col11, col12 = st.columns(2)
    with col11:
        with st.container(border=True):
            raw_file = raw_file = st.file_uploader(
                label='Upload Raw File',
                type=['xls', 'xlsx'])

    if raw_file:
        df = pd.read_excel(raw_file)

        # get list of columns
        df_columns = df.columns.to_list()

        # get list of keywords
        list_keywords = (df['Keywords'].str.split(',').explode().reset_index(drop=True)).to_list()
        list_keywords = list(dict.fromkeys(list_keywords))
        
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
        
            with col2:
                with st.container(border=True):
                    st.subheader('Focus')
                    cb_focus = st.checkbox(
                        label='Client Based',
                        help='Creates a column that contains focus on client')
                    
                    if cb_focus:
                        selected_keywords = st.multiselect(
                            label='Select keyword or Client name',
                            options=list_keywords,
                            help='Select keyword to focus')

                    if cb_focus and len(selected_keywords) > 0:
                        task_status += 1

    
    if task_status > 0:
        with st.container():
            btn_process = st.button(  
                label='Process',
                width='stretch')
                    
            if btn_process:
                with st.spinner(text='Processing File',show_time=True):
                    try:
                        cleaned_df = remove_duplicates(df, selected_columns)
                    except:
                        cleaned_df = df
                    
                    try:
                        cleaned_df = client_focus(df, selected_keywords)
                    except:
                        cleaned_df = df

                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        cleaned_df.to_excel(writer, index=False, sheet_name='CleanedData')
                    processed_data = output.getvalue()
                
                    st.download_button(
                    label="📥 Download Cleaned Excel File",
                    data=processed_data,
                    file_name=f"{out_fname}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",)
    
