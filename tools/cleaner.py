import streamlit as st
import pandas as pd
from io import BytesIO
from common import get_tier_collection


@st.cache_data
def load_file(raw_file):
    return pd.read_excel(raw_file)

def remove_duplicates(df, selected_columns):
    # removes duplicates from the raw file
    cleaned_df = df.drop_duplicates(subset=selected_columns)
    st.success(f'{df.shape[0] - cleaned_df.shape[0]} removed rows')
    return cleaned_df

def client_focus(df, selected_keywords):
    # creates a focus column based on number of clients mentioned in title and content
    for index, row in df.iterrows():
        in_title_score = 0
        in_content_score = 0
        title_text = str(row['Title']).lower()
        content_text = str(row['Content']).lower()

        for keyword in selected_keywords:
            # search in title column
            if keyword.lower() in title_text:
                in_title_score += 1
            
            # search in content column
            in_content_score += content_text.count(keyword)

        if in_title_score>=1 or in_content_score>=3:            
            df.loc[index, 'Focus'] = 'Main'
        else:
            df.loc[index, 'Focus'] = 'Mention'
    
    return df

def get_tier(df, collection):

    df['FQDN'] = ''
    df['TIER'] = 0

    for index, row in df.iterrows():
        url = row['Article Source']
        fqdn = url.split('/')[2]
        fqdn = fqdn.replace('www.', '')
        df.loc[index, 'FQDN'] = fqdn

        result = collection.find_one({'fqdn':fqdn})

        if result:
            df.loc[index, 'TIER'] = result['tier']
        
    return df



def cleaner():
    
    task_status = 0

    # st.title('🧹Cleaner')

    col11, col12 = st.columns([1,2])
    with col11:
        st.header('🗄️File Handler')
        with st.container(border=True):
            raw_file = st.file_uploader(
                label='Upload Raw File',
                type=['xls', 'xlsx'])

        if raw_file:
            df = load_file(raw_file)

            # get list of columns
            df_columns = df.columns.to_list()

            # get list of keywords
            list_keywords = (df['Keywords'].str.split(',').explode().reset_index(drop=True)).to_list()
            list_keywords = sorted(set(list_keywords))
            
            with col11:
                with st.container(border=True):
                    out_fname = st.text_input(
                        label='Output Filename')

            if out_fname:
                with col12:
                    st.header('🛠️Tools')
                    col1, col2, col3 = st.columns(3)
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
                    
                    with col3:
                        with st.container(border=True):
                            st.subheader('Tier')
                            cb_tier = st.checkbox(
                                label='Add TIER column'
                            )

                            if cb_tier:
                                task_status += 1
                                collection = get_tier_collection()
                            
                           


                    
                    # with col4:
                    #     with st.container(border=True):
                    #         st.subheader('Favorability')
                    
                    # cola, colb, colc, cold = st.columns(4)
                    # with cola:
                    #     with st.container(border=True):
                    #         st.subheader('Function5')
                    
                    # with colb:
                    #     with st.container(border=True):
                    #         st.subheader('Function6')
                    
                    # with colc:
                    #     with st.container(border=True):
                    #         st.subheader('Function7')
                    
                    # with cold:
                    #     with st.container(border=True):
                    #         st.subheader('Function8')

    

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
                        cleaned_df2 = client_focus(cleaned_df, selected_keywords)
                    except:
                        cleaned_df2 = cleaned_df

                    try:
                        cleaned_df3 = get_tier(cleaned_df2, collection)
                    except:
                        cleaned_df3 = cleaned_df2

                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        cleaned_df3.to_excel(writer, index=False, sheet_name='CleanedData')
                    processed_data = output.getvalue()
                
                    st.download_button(
                    label="📥 Download Cleaned Excel File",
                    data=processed_data,
                    file_name=f"{out_fname}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",)
    
