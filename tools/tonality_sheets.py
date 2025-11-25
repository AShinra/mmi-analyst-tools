import pandas as pd


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
    bucket_list = sorted(list(set(bucket_list)))

    # get tone list from filtered df
    if 'Tonality_Custom' in filtered_df.columns:
        tonality_list = list(set(filtered_df['Tonality_Custom'].to_list()))
    else:
        tonality_list = list(set(filtered_df['Tonality'].to_list()))
   
    tone_data_frame_set = {}

    for tonality in tonality_list:
        data_frame_set = []

        _index = ['Bucket', 'Raw Date', 'Media Type', 'Article Class', 'Publication', 'Title', 'Section', 'Focus', 'Tonality', 'Length', 'Ad Value', 'AVE']

        if "Tonality_Custom" in filtered_df.columns:
            tonality_df = filtered_df.query('Tonality_Custom==@tonality')
            _index[8] = 'Tonality_Custom'
        else:
            tonality_df = filtered_df.query('Tonality==@tonality')
        
        if "Focus_Custom" in filtered_df.columns:
            _index[7] = 'Focus_Custom'

        for bucket in bucket_list:
            bucket_df = tonality_df.query('Bucket==@bucket')
            if not bucket_df.empty:

                # create pivot table based from the bucket
                pivottable = pd.pivot_table(
                    data=bucket_df,
                    values='Article ID',
                    index=_index,
                    aggfunc='count',
                    margins=True,
                    margins_name=f'{bucket} Total',
                    fill_value=0,).reset_index()
                
                data_frame_set.append(pivottable)
        
        tone_data_frame_set[tonality] = pd.concat(data_frame_set)
    
    return tone_data_frame_set