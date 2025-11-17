import pandas as pd


def share_of_voice(data_frame, category):
    '''
    data_frame ==>> dataframe from which the pivot table will be created\n
    category ==>> category used to filer the pivot table
    '''

    data_frame_set = []

    # filter the data_frame by the given category
    filtered_df = data_frame.query('Category in @category')

    count_sov = pd.pivot_table(
        data=filtered_df,
        values='Ad Value',
        index=['Raw Date'],
        columns=['Bucket'],
        aggfunc='count',
        fill_value=0,).reset_index()
    
    count_sov = count_sov.rename(columns={'Raw Datew':'Date'})
    data_frame_set.append(count_sov)

    sum_sov = pd.pivot_table(
        data=filtered_df,
        values='Ad Value',
        index=['Raw Date'],
        columns=['Bucket'],
        aggfunc='sum',
        fill_value=0,).reset_index()
    
    sum_sov = sum_sov.rename(columns={'Raw Datew':'Date'})
    data_frame_set.append(sum_sov)

    company_sov = pd.pivot_table(
        data=filtered_df,
        values='Ad Value',
        index=['Bucket'],
        aggfunc=['count', 'sum'],
        fill_value=0,).reset_index()
    
    company_sov.columns = company_sov.columns.get_level_values(0)
    company_sov = company_sov.sort_values(by='sum', ascending=False)
    company_sov = company_sov.rename(columns={'Bucket':'Compamy', 'count':'Count', 'sum':'Value'})
    
    data_frame_set.append(company_sov)

    return data_frame_set