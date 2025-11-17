import pandas as pd

def media_statistics(data_frame, category):
    '''
    data_frame ==>> dataframe from which the pivot table will be created\n
    category ==>> category used to filer the pivot table
    '''

    data_frame_set = {}

    # filter the data_frame by the given category
    filtered_df = data_frame.query('Category in @category')

    media_type = pd.pivot_table(
        data=filtered_df,
        values='Ad Value',
        index=['Media Type'],
        aggfunc=['count', 'sum'],
        fill_value=0,).reset_index()
    
    media_type.columns = media_type.columns.get_level_values(0)
    media_type = media_type.sort_values(by='sum', ascending=False)
    media_type = media_type.rename(columns={'count':'Count', 'sum':'Value'})
    
    data_frame_set['Media Statistics'] = media_type

    pub_name = pd.pivot_table(
        data=filtered_df,
        values='Ad Value',
        index=['Publication'],
        aggfunc=['count', 'sum'],
        fill_value=0,).reset_index()
    
    pub_name.columns = pub_name.columns.get_level_values(0)
    pub_name = pub_name.sort_values(by='sum', ascending=False)
    
    data_frame_set['Publications'] = pub_name.head(10)

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

        data_frame_set[media] = pub_type.head(10)
    
    return data_frame_set