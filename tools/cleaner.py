import streamlit as st
import pandas as pd



def cleaner():
    st.title('File Cleaner')

    raw_file = st.file_uploader(
        label='Input File',
        label_visibility='hidden',
        type=['xls', 'xlsx']
    )

    if raw_file:
        df = pd.read_excel(raw_file)
        st.dataframe(df)    
    
