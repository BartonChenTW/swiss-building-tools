"""Utility functions for swiss-address-tools."""


def li2str(li, sep=','):
    """
    Convert list to string with separator.
    
    Args:
        li (list): Input list
        sep (str): Separator string
    
    Returns:
        str: Joined string
    """
    return sep.join([str(item) for item in li])


def get_df_by_key(df_data, label, by='EGID', col_sum=[], col_avg=[], col_join=[], col_first=[], col_unique=[], col_max=[]):
    '''get a 'groupby' dataframe by key columns (e.g. EGID) with different groupby function:

    input
    --
    df_data: input dataframe
    label: name to add in column "{label}_count" (e.g. 'dist_heat', 'PV')
    by: groupby column (e.g. EGID)
    col_sum: the columns to get sumup values by groupby
    col_avg: the columns to get average values by groupby
    col_join: the columns to get join string (e.g. 'id1', 'id2', 'id3')
    col_first: the columns to get the first value (drop duplicated value)    
    col_unique: the columns to get unique values (set)
    col_max: the columns to get max values by groupby
    '''

    # create data frame and set up index
    df_return = pd.DataFrame()

    # count by key
    df_data = df_data.copy()
    df_data['count'] = 1    # make a column to 1 to avoid mis-count NaN for the 1st column
    df_count = df_data.groupby(by=by).count()
    df_return[f'count.{label}'] = df_count['count']

    # add sum up
    df_sum = df_data.groupby(by=by).sum(numeric_only=True)
    for col in col_sum:
        df_return[f'sum.{col}'] = df_sum[col]

    # add average 
    df_avg = df_data.groupby(by=by).mean(numeric_only=True)
    for col in col_avg:
        df_return[f'avg.{col}'] = df_avg[col]

    # add max
    df_max = df_data.groupby(by=by).max(numeric_only=True)
    for col in col_max:
        df_return[f'max.{col}'] = df_max[col]

    # add join strings 
    for col in col_join:

        df_join = df_data.groupby(by=by)[col].apply(lambda x: ', '.join(map(str, x))).to_frame()
        df_return[f'join.{col}'] = df_join[col]

        # df_return[f'join.{col}'] = ''

        # for indx_return in df_return.index:
        #     li_values = df_data[df_data[by] == indx_return][col].tolist()
        #     df_return.at[indx_return, f'join.{col}'] = '; '.join(map(str, li_values))

    # get data in first row 
    df_first = df_data.drop_duplicates(by)
    df_first.set_index(by, inplace=True)
    for col in col_first:
        df_return[f'1st.{col}'] = df_first[col]

    # add unique values
    for col in col_unique:
        df_unique = df_data.groupby(by=by)[col].apply(lambda x: ', '.join(map(str, x.unique()))).to_frame()
        df_return[f'unique.{col}'] = df_unique[col]
        
    return df_return