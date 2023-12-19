import pandas as pd
from datetime import datetime
from app.utils.proc import load


def GET_UNTIL_TODAY(period: str, col: str):
    df_raw = load.LOAD_MEMO_DATA()

    dict_val = {
        'prsc_date': 'prscription',
        'upld_date': 'upload',
        'rept_date': 'report',
    }
    dict_id = {
        'prsc_date': 'tid',
        'upld_date': 'upld_id',
        'rept_date': 'rept_id',
    }

    if period == 'year':
        the_period = str(datetime.now()).split('-')[0] + '-01-01'
    elif period == 'month':
        the_period = '-'.join(str(datetime.now()).split('-')[:2]) + '-01'
    elif period == 'all':
        the_period = df_raw.prsc_date.min()

    df_this_month_prsc = df_raw[df_raw[str(col)] >= the_period].agg({
        dict_id[str(col)]: 'nunique',
        'hosp_name': 'nunique',
        'doct_name': 'nunique',

    }).reset_index().rename(columns={0: 'count'})
    df_this_month_prsc['period'] = period
    df_this_month_prsc['type'] = col.split('_')[0]

    return df_this_month_prsc


def GET_UNTIL_TODAY_DATA(period: str) -> pd.DataFrame:
    '''
        period = period of ('year','month','all')
    '''

    df_proc = pd.concat(
        [GET_UNTIL_TODAY(str(period), 'prsc_date'), GET_UNTIL_TODAY(str(period), 'upld_date')])
    df_thus = pd.concat([df_proc, GET_UNTIL_TODAY(str(period), 'rept_date')])

    return df_thus


def GET_UNTIL_PIVOT() -> pd.DataFrame:
    '''
        period = period of ('year','month','all')
    '''

    df_merge = pd.concat([GET_UNTIL_TODAY_DATA('all'), GET_UNTIL_TODAY_DATA('year')])
    df_merge = pd.concat([df_merge, GET_UNTIL_TODAY_DATA('month')])

    df_pivot = pd.pivot(df_merge, index=['period'], columns=['type', 'index'], values=['count'])
    df_pivot.columns = ['prsc_cnt', 'prsc_hosp_cnt', 'prsc_doct_cnt', 'upld_cnt', 'upld_hosp_cnt', 'upld_doct_cnt',
                        'rept_cnt', 'rept_hosp_cnt', 'rept_doct_cnt', ]
    df_pivot = df_pivot.reset_index().sort_values(['prsc_cnt'], ascending=False).reset_index().drop(columns=['index'])
    df_pivot

    return df_pivot

def GET_DATE_RANGE(week_format):
    '''
        - takes a format of week (e.g., '2023-W37')
        - returns a list of date range of the week number in the year
    '''
    return sorted([str(datetime.strptime(week_format + str(i), '%G-W%V-%u')).split()[0] for i in range(-7,0)])