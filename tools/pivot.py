import pandas as pd
import streamlit as st

def pivot_sheet(data_frame, category):
    '''
    data_frame ==>> dataframe from which the pivot table will be created\n
    category ==>> category used to filer the pivot table
    '''

    # filter the data_frame by the given category
    filtered_df = data_frame.query('Category in @category')

    # create a bucket list from Bucket column
    bucket_list = filtered_df['Bucket'].to_list()
    # remove duplicates
    bucket_list = sorted(list(set(bucket_list)))

    data_frame_set = {}

    for bucket in bucket_list:
        bucket_df = filtered_df.query('Bucket==@bucket')

        # create pivot table based from the bucket
        pivottable = pd.pivot_table(
            data=bucket_df,
            values='Article ID',
            index=['Bucket', 'Raw Date', 'Media Type', 'Article Class', 'Publication', 'Title', 'Section', 'Length', 'Ad Value', 'AVE'],
            aggfunc='count',
            margins=True,
            margins_name=f'{bucket} Total',
            fill_value=0,).reset_index()
        
        data_frame_set[bucket] = pivottable
    
    return data_frame_set