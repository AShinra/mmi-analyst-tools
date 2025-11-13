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
    bucket_list = list(set(bucket_list))

    data_frame_set = []

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
        
        data_frame_set.append(pivottable)
    
    return data_frame_set


def tonality_sheets(data_frame, category):
    '''
    data_frame ==>> dataframe from which the pivot table will be created\n
    category ==>> category used to filer the pivot table
    '''

    # filter the data_frame by the given category
    filtered_df = data_frame.query('Category in @category')

    # create a bucket list from Bucket column
    bucket_list = filtered_df['Bucket'].to_list()
    # remove duplicates
    bucket_list = list(set(bucket_list))

    # get tone list from filtered df
    tonality_list = list(set(filtered_df['Tonality'].to_list()))
   
    tone_data_frame_set = {}

    for tonality in tonality_list:
        data_frame_set = []
        tonality_df = filtered_df.query('Tonality==@tonality')

        for bucket in bucket_list:
            bucket_df = tonality_df.query('Bucket==@bucket')

            # create pivot table based from the bucket
            pivottable = pd.pivot_table(
                data=bucket_df,
                values='Article ID',
                index=['Bucket', 'Raw Date', 'Media Type', 'Article Class', 'Publication', 'Title', 'Section', 'Tonality', 'Length', 'Ad Value', 'AVE'],
                aggfunc='count',
                margins=True,
                margins_name=f'{bucket} Total',
                fill_value=0,).reset_index()
            
            data_frame_set.append(pivottable)
        
        tone_data_frame_set[tonality] = pd.concat(data_frame_set)
    
    return tone_data_frame_set


def daily_statistics(data_frame, category):
    '''
    data_frame ==>> dataframe from which the pivot table will be created\n
    category ==>> category used to filer the pivot table
    '''

    daily_stats_dict = {}

    # filter the data_frame by the given category
    filtered_df = data_frame.query('Category in @category')
    filtered_df['Ad Value'] = filtered_df['Ad Value'].str.replace(',', '')
    filtered_df['Ad Value'] = filtered_df['Ad Value'].astype(float)
    
    count_daily_statistics = pd.pivot_table(
        data=filtered_df,
        values='Ad Value',
        index=['Raw Date'],
        columns=['Media Type'],
        aggfunc='count',        
        fill_value=0,).reset_index()
    
    daily_stats_dict['Count'] = count_daily_statistics
    
    sum_daily_statistics = pd.pivot_table(
        data=filtered_df,
        values='Ad Value',
        index=['Raw Date'],
        columns=['Media Type'],
        aggfunc='sum',        
        fill_value=0,).reset_index()
    
    daily_stats_dict['Sum'] = sum_daily_statistics
        
    return daily_stats_dict


def media_statistics(data_frame, category):
    '''
    data_frame ==>> dataframe from which the pivot table will be created\n
    category ==>> category used to filer the pivot table
    '''

    # filter the data_frame by the given category
    filtered_df = data_frame.query('Category in @category')
    filtered_df['Ad Value'] = filtered_df['Ad Value'].str.replace(',', '')
    filtered_df['Ad Value'] = filtered_df['Ad Value'].astype(float)

    media_type = pd.pivot_table(
        data=filtered_df,
        values='Ad Value',
        index=['Media Type'],
        aggfunc=['count', 'sum'],
        fill_value=0,).reset_index()
    
    media_type.columns = media_type.columns.get_level_values(0)
    media_type = media_type.sort_values(by='sum', ascending=False)
    media_type = media_type.rename(columns={'count':'Count', 'sum':'Value'})
    
    st.dataframe(media_type)

    pub_name = pd.pivot_table(
        data=filtered_df,
        values='Ad Value',
        index=['Publication'],
        aggfunc=['count', 'sum'],
        fill_value=0,).reset_index()
    
    pub_name.columns = pub_name.columns.get_level_values(0)
    pub_name = pub_name.sort_values(by='sum', ascending=False)
    pub_name = pub_name.rename(columns={'count':'Count', 'sum':'Value'})
    
    st.dataframe(pub_name.head(10))

    media_types = list(set(filtered_df['Media Type'].to_list()))
    for media in media_types:
        
        _filtered = filtered_df.query('`Media Type`==@media')

        pub_type = pd.pivot_table(
            data=_filtered,
            values='Ad Value',
            index=['Publication'],
            aggfunc=['count', 'sum'],
            fill_value=0,).reset_index()
        
        pub_type.columns = pub_type.columns.get_level_values(0)
        pub_type = pub_type.sort_values(by='sum', ascending=False)
        pub_type = pub_type.rename(columns={'count':'Count', 'sum':'Value'})

        st.write(media)
        st.dataframe(pub_type.head(10))
    

def share_of_voice(data_frame, category):
    '''
    data_frame ==>> dataframe from which the pivot table will be created\n
    category ==>> category used to filer the pivot table
    '''

    # filter the data_frame by the given category
    filtered_df = data_frame.query('Category in @category')
    filtered_df['Ad Value'] = filtered_df['Ad Value'].str.replace(',', '')
    filtered_df['Ad Value'] = filtered_df['Ad Value'].astype(float)

    count_sov = pd.pivot_table(
        data=filtered_df,
        values='Ad Value',
        index=['Raw Date'],
        columns=['Bucket'],
        aggfunc='count',
        fill_value=0,).reset_index()
    
    st.dataframe(count_sov)

    sum_sov = pd.pivot_table(
        data=filtered_df,
        values='Ad Value',
        index=['Raw Date'],
        columns=['Bucket'],
        aggfunc='sum',
        fill_value=0,).reset_index()
    
    st.dataframe(sum_sov)

    company_sov = pd.pivot_table(
        data=filtered_df,
        values='Ad Value',
        index=['Bucket'],
        aggfunc=['count', 'sum'],
        fill_value=0,).reset_index()
    
    company_sov.columns = company_sov.columns.get_level_values(0)
    company_sov = company_sov.sort_values(by='sum', ascending=False)
    company_sov = company_sov.rename(columns={'count':'Count', 'sum':'Value'})
    
    st.dataframe(company_sov)


        



            
        
            

        

