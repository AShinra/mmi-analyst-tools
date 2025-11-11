import pandas as pd
import streamlit as st



def client_single(df, main_category):

    filtered_df = df.query('Category in @main_category')

    pivot = pd.pivot_table(
        data=filtered_df,
        values='Article ID',
        index=['Bucket', 'Raw Date', 'Media Type', 'Article Class', 'Publication', 'Title', 'Section', 'Length', 'Ad Value', 'AVE'],
        aggfunc='count',
        fill_value=0,).reset_index()

    st.dataframe(pivot)



def client_multiple(df, main_category):
    with st.spinner(
        text='Processing',
        show_time=True):

        filtered_df = df.query('Category in @main_category')
        bucket_list = filtered_df['Bucket'].to_list()
        bucket_list = list(set(bucket_list))

        for bucket in bucket_list:

            filtered_df = df.query('Bucket==@bucket')
                        
            pivot = pd.pivot_table(
                data=filtered_df,
                values='Article ID',
                index=['Bucket', 'Raw Date', 'Media Type', 'Article Class', 'Publication', 'Title', 'Section', 'Length', 'Ad Value', 'AVE'],
                aggfunc='count',
                fill_value=0,).reset_index()

            st.dataframe(pivot, hide_index=True)