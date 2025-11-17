import pandas as pd

def daily_statistics(data_frame, category):
    '''
    data_frame ==>> dataframe from which the pivot table will be created\n
    category ==>> category used to filer the pivot table
    '''

    daily_stats_dict = {}

    # filter the data_frame by the given category
    filtered_df = data_frame.query('Category in @category')
    
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