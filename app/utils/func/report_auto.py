import json
import plotly
import plotly.express as px
import pandas as pd
from app.utils.proc import proc
from datetime import datetime, timedelta

######### PROC #########
def GET_QUARTER(i):
    year = i.split('-')[0]
    month = i.split('-')[1]
    try:
        if int(month)<=3:
            val = 'Q1'
        elif int(month) > 3 and int(month) <=6:
            val = 'Q2'
        elif int(month) > 6 and int(month) <= 9:
            val = 'Q3'
        elif int(month) > 9 and int(month) <= 12:
            val = 'Q4'
        return year+'-'+val
    except Exception:
        return np.nan
def GET_WEEK_PARAMS(df_hosp):
    #### 오늘 날짜로 최근 WEEK 확인하기
    this_week = sorted(df_hosp[df_hosp['period_type'] == 'WEEK']['period'].unique())[-1]
    date_first = sorted(df_hosp[df_hosp['period_type'] == 'WEEK']['period'].unique())[-1].split("(")[1].split()[0]
    date_last = \
    sorted(df_hosp[df_hosp['period_type'] == 'WEEK']['period'].unique())[-1].split("(")[1].split()[2].split(")")[0]
    week_lst = [str(i).split()[0] for i in pd.date_range(date_first, date_last)]
    date_today = str(datetime.today()).split()[0]

    if date_today in week_lst:
        # this_week = sorted(df_hosp[df_hosp['period_type']=='WEEK']['period'].unique())[-2]
        this_week = sorted(df_hosp[df_hosp['period_type'] == 'WEEK']['period'].unique())[-1]
        week_last = sorted(df_hosp[df_hosp['period_type'] == 'WEEK']['period'].unique())[-2]
        week_prev = sorted(df_hosp[df_hosp['period_type'] == 'WEEK']['period'].unique())[-3]
        pass
    else:
        this_week = sorted(df_hosp[df_hosp['period_type'] == 'WEEK']['period'].unique())[-2]
        date_first = sorted(df_hosp[df_hosp['period_type'] == 'WEEK']['period'].unique())[-1].split("(")[1].split()[0]
        date_last = \
        sorted(df_hosp[df_hosp['period_type'] == 'WEEK']['period'].unique())[-1].split("(")[1].split()[2].split(")")[0]
        week_lst = [str(i).split()[0] for i in pd.date_range(date_first, date_last)]
        week_last = sorted(df_hosp[df_hosp['period_type'] == 'WEEK']['period'].unique())[-3]
        week_last = sorted(df_hosp[df_hosp['period_type'] == 'WEEK']['period'].unique())[-4]

    return this_week, week_last, week_prev

def GET_STATUS_NUMBER(df_summary, this_week):
    df = df_summary[df_summary['period'] == str(this_week)].groupby(['period']).agg({
        'hosp_cate': 'nunique',
        'hosp_name': 'nunique',
        'doctors': 'nunique',
        'tid': 'sum',
        'upld_id': 'sum',
        'rept_id': 'sum',
    }).sort_values('tid', ascending=False).reset_index()
    return df

def GRAPH_HOSPITAL_TID(df_summary, this_week):
    fig = px.bar(
        df_summary[df_summary['period'] == str(this_week)].groupby(['period', 'hosp_cate', 'hosp_name']).agg(
            {'tid': 'sum'}).sort_values('tid', ascending=False).reset_index(),
        x='hosp_name',
        y='tid',
        text='tid',
        color='hosp_cate',
        category_orders={
            'hosp_cate': ['상급종합병원', '종합병원', '병원', '의원']
        },
        color_discrete_sequence=["#636EFA", "#EF553B", "#00CC96", "#19D3F3"],
        height=400,
        template='plotly_white'
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.update_layout(
        legend=dict(x=0.5, y=1.1, xanchor='center', yanchor='top'),
        legend_orientation='h'
    )
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def GRAPH_DOCTORS_TID(df_summary, this_week):

    df = df_summary[df_summary['period']==str(this_week)].groupby(['period','hosp_cate','hosp_name','doct_name']).agg({'tid':'sum'}).sort_values(['hosp_name','tid'],ascending = [True,False]).reset_index()

    fig = px.treemap(
        df,
        path=[
            px.Constant("TOTAL (" + str(df.tid.sum()).replace(".0", "") + ")"),
            'hosp_cate', 'hosp_name', 'doct_name',  'tid'
        ],
        values='tid',
        color='tid',
        height=700,
        # color_continuous_midpoint = 0.1
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig