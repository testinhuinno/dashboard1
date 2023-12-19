import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from operator import itemgetter

import json
from datetime import datetime
from gspread_dataframe import get_as_dataframe
from app.utils.constant import env
from app.utils.proc import load_meta, upto_date

def GET_DOCTOR_DATA():
    df_raw = get_as_dataframe(env.sh.worksheet('[CRM] RAW'))
    df_raw = df_raw[[i for i in df_raw.columns if 'Unn' not in i]]
    df_raw = df_raw.dropna(subset=[df_raw.columns[0]])
    return df_raw

def GET_REPOT_DATA():
    df_raw = get_as_dataframe(env.sh.worksheet('[REPORT] RAW'))
    df_raw = df_raw[[i for i in df_raw.columns if 'Unn' not in i]]
    df_raw = df_raw.dropna(subset=[df_raw.columns[0]])
    return df_raw

def GET_DOCTOR_CHART(df_doct:pd.DataFrame, the_period:str):
    '''the_period in ('monthly','weekly')'''

    if the_period == 'monthly':
        aa = df_doct.groupby(['names', 'prsc_month', 'prsc_period']).agg({'tid': 'count'}).reset_index()
        df_pivot = pd.pivot(aa, index=['names', 'prsc_month'], columns='prsc_period', values='tid').reset_index()
        y_val= [i for i in df_pivot.columns if '~' in i]
        fig = px.bar(
            df_pivot, x='prsc_month', y=y_val,#['1~3일', '4~7일', '8~14일'],
            template='plotly_white'
        )
        fig.update_xaxes(dtick='M1', tickformat='%Y\n%b')
        the_graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    elif the_period == 'weekly':
        aa = df_doct.groupby(['names', 'prsc_week', 'prsc_period']).agg({'tid': 'count'}).reset_index()
        df_pivot = pd.pivot(aa, index=['names', 'prsc_week'], columns='prsc_period', values='tid').reset_index()
        y_val = [i for i in df_pivot.columns if '~' in i]
        fig = px.bar(
            df_pivot, x='prsc_week', y=y_val,
            template='plotly_white'
        )
        fig.update_xaxes(type='category')

        # fig.update_xaxes(tickformat='%Y년\n%V주')
        the_graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return the_graph

def GET_XTICKS(the_period, val1, val2):
    val_lst = []
    if the_period == 'weekly':
        for i in [val1, val2]:
            year = i.split("-")[0]
            week = i.split("-")[1].split("W")[1]
            if year == '2022':
                for k in range(int(week), 53):
                    if len(str(k)) == 1:
                        k = '0' + str(k)
                    val = year + '-W' + str(k)
                    val_lst.append(val)
            elif year == '2023':
                for k in range(1, int(week)):
                    if len(str(k)) == 1:
                        k = '0' + str(k)
                    val = year + '-W' + str(k)
                    val_lst.append(val)
    elif the_period == 'monthly':
        for i in [val1, val2]:
            year = i.split("-")[0]
            month = i.split("-")[1]
            if year == '2022':
                for k in range(int(month), 13):
                    if len(str(k)) == 1:
                        k = '0' + str(k)
                    val = year + '-' + str(k)
                    val_lst.append(val)
            elif year == '2023':
                for k in range(1, int(month)):
                    if len(str(k)) == 1:
                        k = '0' + str(k)
                    val = year + '-' + str(k)
                    val_lst.append(val)
    return val_lst
def GET_INFO(the_name):
    df_raw = get_as_dataframe(env.sh.worksheet('[CRM] RAW'))
    df_raw = df_raw[[i for i in df_raw.columns if 'Unn' not in i]]
    df_raw = df_raw.dropna(subset=[df_raw.columns[0]])

    df_doct = df_raw[df_raw['names'] == str(the_name)]
    min_date = df_doct['prsc_date'].min()
    max_date = df_doct['prsc_date'].max()
    tot_dur = str(datetime.strptime(max_date, "%Y-%m-%d") - datetime.strptime(min_date, "%Y-%m-%d")).split(",")[0]
    duration = str(datetime.now() - datetime(
        int(max_date.split('-')[0]),
        int(max_date.split('-')[1]),
        int(max_date.split('-')[2]),
    )).split(',')[0]

    return min_date, max_date, tot_dur, duration

def GET_PRSC_CNT(the_name):
    df_raw = get_as_dataframe(env.sh.worksheet('[CRM] RAW'))
    df_raw = df_raw[[i for i in df_raw.columns if 'Unn' not in i]]
    df_raw = df_raw.dropna(subset=[df_raw.columns[0]])

    df_rank = df_raw.groupby(['names']).agg({'tid': 'nunique'}).reset_index().sort_values('tid',ascending=False).reset_index()
    df_rank['index'] = [i + 1 for i in range(df_rank.shape[0])]

    prsc_cnt = df_rank[df_rank['names'] == str(the_name)]['tid'].values[0]
    the_rank = df_rank[df_rank['names'] == str(the_name)]['index'].values[0]
    the_rank = str(the_rank)

    tot_rank = df_rank['index'].max()
    return prsc_cnt, the_rank, tot_rank

def GET_REPT_CNT(the_name):
    df_raw = get_as_dataframe(env.sh.worksheet('[REPORT] RAW'))
    df_raw = df_raw[[i for i in df_raw.columns if 'Unn' not in i]]
    df_raw = df_raw.dropna(subset=[df_raw.columns[0]])

    df_rank = df_raw.groupby(['names']).agg({'tid': 'nunique'}).reset_index().sort_values('tid',ascending=False).reset_index()
    df_rank['index'] = [i + 1 for i in range(df_rank.shape[0])]

    prsc_cnt = df_rank[df_rank['names'] == str(the_name)]['tid'].values[0]
    the_rank = df_rank[df_rank['names'] == str(the_name)]['index'].values[0]
    the_rank = str(the_rank)

    tot_rank = df_rank['index'].max()
    return prsc_cnt, the_rank, tot_rank

def GET_YEALRY_CNT(the_name):
    df_raw = get_as_dataframe(env.sh.worksheet('[CRM] RAW'))
    df_raw = df_raw[[i for i in df_raw.columns if 'Unn' not in i]]
    df_raw = df_raw.dropna(subset=[df_raw.columns[0]])
    df_raw = df_raw.astype(str)

    df_rank = df_raw.groupby(['names','prsc_year']).agg({'tid': 'nunique'}).reset_index()
    the_year = str(datetime.now()).split('-')[0]
    df_rank = df_rank[df_rank['prsc_year'] == the_year].sort_values('tid', ascending = False).reset_index()
    df_rank['index'] = [i + 1 for i in range(df_rank.shape[0])]
    tot_rank = df_rank['index'].max()

    try:
        prsc_cnt = df_rank[df_rank['names'] == str(the_name)]['tid'].values[0]
        the_rank = df_rank[df_rank['names'] == str(the_name)]['index'].values[0]
        the_rank = str(the_rank)
    except Exception as e:
        print("####", e)
        prsc_cnt = '0'
        the_rank = '-'

    return prsc_cnt, the_rank, tot_rank

def GET_QUARTER_CNT(the_name):
    df_raw = get_as_dataframe(env.sh.worksheet('[CRM] RAW'))
    df_raw = df_raw[[i for i in df_raw.columns if 'Unn' not in i]]
    df_raw = df_raw.dropna(subset=[df_raw.columns[0]])

    df_rank = df_raw.groupby(['names','prsc_quarter']).agg({'tid': 'nunique'}).reset_index()

    the_month = str(datetime.now()).split()[0][:7]
    the_year = the_month.split("-")[0]
    the_quarter = the_month.split("-")[1]
    if the_quarter<='03':
        val = 'Q1'
    elif the_quarter > '03' and the_quarter <='06':
        val = 'Q2'
    elif the_quarter > '07' and the_quarter <= '09':
        val = 'Q3'
    elif the_quarter > '09' and the_quarter <= '12':
        val = 'Q4'
    the_val = the_year + '-' + val


    df_rank = df_rank[df_rank['prsc_quarter'] == the_val].sort_values('tid', ascending = False).reset_index()
    df_rank['index'] = [i + 1 for i in range(df_rank.shape[0])]

    try:
        prsc_cnt = df_rank[df_rank['names'] == str(the_name)]['tid'].values[0]
        the_rank = df_rank[df_rank['names'] == str(the_name)]['index'].values[0]
        the_rank = str(the_rank)
    except Exception:
        prsc_cnt = '0'
        the_rank = '-'
    tot_rank = df_rank['index'].max()
    return prsc_cnt, the_rank, tot_rank

def GET_MONTHLY_CNT(the_name):
    df_raw = get_as_dataframe(env.sh.worksheet('[CRM] RAW'))
    df_raw = df_raw[[i for i in df_raw.columns if 'Unn' not in i]]
    df_raw = df_raw.dropna(subset=[df_raw.columns[0]])

    df_rank = df_raw.groupby(['names','prsc_month']).agg({'tid': 'nunique'}).reset_index()
    df_rank = df_rank[df_rank['prsc_month'] == str(datetime.now()).split()[0][:7]].sort_values('tid', ascending = False).reset_index()
    df_rank['index'] = [i + 1 for i in range(df_rank.shape[0])]

    try:
        prsc_cnt = df_rank[df_rank['names'] == str(the_name)]['tid'].values[0]
        the_rank = df_rank[df_rank['names'] == str(the_name)]['index'].values[0]
        the_rank = str(the_rank)
    except Exception:
        prsc_cnt = '0'
        the_rank = '-'
    tot_rank = df_rank['index'].max()
    return prsc_cnt, the_rank, tot_rank

def GET_WEEKLY_CNT(the_name):
    df_raw = get_as_dataframe(env.sh.worksheet('[CRM] RAW'))
    df_raw = df_raw[[i for i in df_raw.columns if 'Unn' not in i]]
    df_raw = df_raw.dropna(subset=[df_raw.columns[0]])

    df_rank = df_raw.groupby(['names','prsc_week']).agg({'tid': 'nunique'}).reset_index()
    params_yr = str(datetime.strptime(str(datetime.now()).split()[0], '%Y-%m-%d').isocalendar()[0])
    params_wk = str(datetime.strptime(str(datetime.now()).split()[0], '%Y-%m-%d').isocalendar()[1])
    if len(params_wk) == 1:
        params_wk = '0' + params_wk
    the_week = params_yr + '-W' + params_wk
    df_rank = df_rank[df_rank['prsc_week'] == the_week].sort_values('tid', ascending = False).reset_index()
    # df_rank = df_rank[df_rank['prsc_month'] == str(datetime.now()).split()[0][:7]].sort_values('tid',ascending=False).reset_index()
    df_rank['index'] = [i + 1 for i in range(df_rank.shape[0])]

    try:
        prsc_cnt = df_rank[df_rank['names'] == str(the_name)]['tid'].values[0]
        the_rank = df_rank[df_rank['names'] == str(the_name)]['index'].values[0]
        the_rank = str(the_rank)
    except Exception:
        prsc_cnt = '0'
        the_rank = '-'
    tot_rank = df_rank['index'].max()
    return prsc_cnt, the_rank, tot_rank

def GRAPH_MONTHLY(df_month, the_name):
    df_doct_month = df_month[df_month['names'] == str(the_name)]
    df_doct_month = df_doct_month.groupby('prsc_month').sum().reset_index()

    mon_lst = []
    for i in pd.date_range(df_doct_month.prsc_month.min() + '-01', str(datetime.now()).split()[0][:7] + '-02',
                           freq="MS"):
        val = '-'.join(str(i).split("-")[:2])
        mon_lst.append(val)
    df_join = pd.DataFrame(columns=['prsc_month'], data=mon_lst)
    df_doct_month = pd.merge(df_join, df_doct_month, on='prsc_month', how='left')

    fig = px.bar(
        df_doct_month,
        x='prsc_month', y=['1~3일', '4~7일', '8~14일'],
        template='plotly_white',
        height = 400
    )
    fig.update_xaxes(dtick='M1', tickformat='%Y\n%b')
    fig.update_layout(xaxis=dict(
        ticktext=GET_XTICKS(
            'monthly',
            df_doct_month.prsc_month.min(),
            df_month.prsc_month.max())
    ))
    the_graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return the_graph

def GRAPH_WEEKLY(the_name):
    the_sheet = '[CRM] DOCTORS WEEKLY'
    df_week = load_meta.GET_META_DATA_BY(the_sheet)
    df_doct_week = df_week[df_week['names'] == str(the_name)]

    week_lst = []
    for i in pd.date_range(df_doct_week.prsc_date.min(), str(datetime.now()).split()[0], freq='W'):
        params_yr = str(datetime.strptime(str(i).split()[0], '%Y-%m-%d').isocalendar()[0])
        params_wk = str(datetime.strptime(str(i).split()[0], '%Y-%m-%d').isocalendar()[1])
        if len(params_wk) == 1:
            params_wk = '0' + params_wk
        val = params_yr + '-W' + params_wk
        week_lst.append(val)

    df_doct_week = df_doct_week.groupby(['prsc_week', 'date_range']).sum().reset_index()
    df_join = pd.DataFrame(columns=['prsc_week'], data=week_lst)
    df_doct_week = pd.merge(df_join, df_doct_week, on='prsc_week', how='left')

    fig = px.bar(
        df_doct_week, x='prsc_week', y=['1~3일', '4~7일', '8~14일'], hover_name='date_range',
        template='plotly_white'
    )

    fig.update_xaxes(tickformat='%Y년\n%V주')

    the_graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return the_graph


def GRAPH_THE_MULTIPLE_PERIOD(df_tot):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig1 = (px.bar(df_tot.sort_values('period'), x='period', y='tid', color='type', color_discrete_sequence=["rgb(99, 110, 250)"]))

    fig2 = (
        px.line(df_tot.sort_values('period'), x='period', y='revenue', color='type', markers=True, color_discrete_sequence=["rgb(255, 0, 0)"]))
    fig2.update_traces(yaxis='y2')

    fig.add_traces(fig1.data + fig2.data)# + fig3.data)

    fig.update_layout(plot_bgcolor="white")
    fig.update_yaxes(title_text="<b>tid</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>revenue</b>", secondary_y=True)

    data_lst = [{
        "label": t.name,
        "method": "restyle",
        "args": [
            {"visible": [t2.name == t.name for t2 in fig.data]},
            {
                "xaxis.categoryarray": sorted([point for point in t['x']]),
                "xaxis.categoryorder": 'array'
            }
        ]} for t in fig.data][::-1]

    for trace in fig.data:
        trace.visible = False
    fig.data[-1].visible = True

    fig.update_layout(
        updatemenus=[
            {
                "buttons": list({i['label']: i for i in data_lst}.values()),#sorted(list({i['label']:i for i in data_lst}.values()), key = itemgetter('label'), reverse = True),
                'showactive': True,
                'x': 0.0,
                'xanchor': "left",
                'y': 1.2,
                'yanchor': "top"
            }
        ]
    )
    # fig.update_xaxes(categoryorder='array', categoryarray=sorted(set(sum([i['x'].tolist() for i in fig.data], []))))
    fig.update_layout(showlegend=False, font_size=10)
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.update_yaxes(matches=None)
    fig.for_each_xaxis(lambda yaxis: yaxis.update(showticklabels=True))

    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig


def GRAPH_WEEK_BUTTON(df_raw):
    df_month = df_raw.groupby(['names', 'prsc_week']).agg({'tid': 'nunique'}).reset_index()
    df_month['date_range'] = df_month['prsc_week'].apply(upto_date.GET_DATE_RANGE)
    df_month['date_range'] = [lst[0] + ' ~ ' + lst[-1] for lst in df_month['date_range']]

    fig = px.bar(df_month, x='prsc_week', y='tid',
                 color='names',hover_name='date_range',
                 template='plotly_white'
                 )
    fig.update_xaxes(categoryorder = 'array', categoryarray = sorted(df_month.prsc_week.unique().tolist()))
    fig.update_layout(
        updatemenus=[
            {
                "buttons": [
                    {
                        "label": t.name,
                        "method": "restyle",
                        "args": [
                            {"visible": [t2.name == t.name for t2 in fig.data]},
                        ],
                    }
                    for t in fig.data
                ]
            }
        ]
    )
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def GRAPH_QUARTER_BUTTON(df_raw):
    df_month = df_raw.groupby(['names', 'prsc_quarter']).agg({'tid': 'nunique'}).reset_index()
    fig = px.bar(df_month, x='prsc_quarter', y='tid', color='names')
    fig.update_xaxes(categoryorder='array', categoryarray=sorted(df_month.prsc_quarter.unique().tolist()))
    fig.update_layout(
        updatemenus=[
            {
                "buttons": [
                    {
                        "label": t.name,
                        "method": "restyle",
                        "args": [
                            {"visible": [t2.name == t.name for t2 in fig.data]},
                        ],
                    }
                    for t in fig.data
                ]
            }
        ]
    )
    fig.update_traces(width=0.5)

    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def GRAPH_RANK(df_raw, the_period):
    if the_period == 'prsc_week':
        df_raw['prsc_week'] = df_raw['prsc_week'] + ' ('+ df_raw['date_range'] + ')'
    df_month = df_raw.groupby(['names', str(the_period)]).agg({'tid': 'nunique'}).reset_index()
    df_month['rank'] = df_month.groupby(str(the_period))['tid'].rank(method='first', ascending=False)
    df_month = df_month.sort_values([str(the_period), 'tid'], ascending=[True, False])
    df_month = df_month[df_month['rank'] < 21]
    df_month[str(the_period)] = df_month[str(the_period)].astype(str)

    if 'year' in the_period:
        title = 'YEAR'
    elif 'quarter' in the_period:
        title = 'QUARTER'
    elif 'month' in the_period:
        title = 'MONTH'
    elif 'week' in the_period:
        title = 'WEEK'

    fig = px.bar(
        df_month, x='names', y='tid', color=str(the_period)
        , height=400, text = 'tid',template='plotly_white'
    )
    data_lst = [{
        "label": t.name,
        "method": "restyle",
        "args": [
            {"visible": [t2.name == t.name for t2 in fig.data]},

        ]} for t in fig.data][::-1]

    for trace in fig.data:
        trace.visible = False
    fig.data[-1].visible = True

    fig.update_xaxes(tickangle=25)
    fig.update_layout(title_text = title, title_x = 0, showlegend = False, font_size = 10)
    fig.update_layout(
        updatemenus=[
            {
                "buttons": list({i['label']: i for i in data_lst}.values()),#sorted(list({i['label']:i for i in data_lst}.values()), key = itemgetter('label'), reverse = True),
                'showactive':True,
                'x' : 0.0,
                'xanchor' : "left",
                'y' : 1.2,
                'yanchor' : "top"
            }
        ]
    )
    fig.update_layout(showlegend=False, font_size=10)
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.update_yaxes(matches=None)
    fig.for_each_xaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def GRAPH_RANK_REVENUE(df_raw, the_period):
    if the_period == 'rept_week':
        df_raw['rept_week'] = df_raw['rept_week'] + ' ('+ df_raw['rept_date_range'] + ')'

    df_month = df_raw.groupby(['names', str(the_period)]).agg({'cost': 'sum'}).reset_index()
    df_month['rank'] = df_month.groupby(str(the_period))['cost'].rank(method='first', ascending=False)
    df_month = df_month.sort_values([str(the_period), 'cost'], ascending=[True, False])
    df_month = df_month[df_month['rank'] < 21]
    df_month[str(the_period)] = df_month[str(the_period)].astype(str)

    if 'year' in the_period:
        title = 'YEAR'
    elif 'quarter' in the_period:
        title = 'QUARTER'
    elif 'month' in the_period:
        title = 'MONTH'
    elif 'week' in the_period:
        title = 'WEEK'

    fig = px.bar(
        df_month, x='names', y='cost', color=str(the_period), height=400, text = 'cost'
    )
    fig.update_xaxes(tickangle=25)
    fig.update_layout(title_text = title, title_x = 0, showlegend = False, font_size = 10)
    fig.update_layout(
        updatemenus=[
            {
                "buttons": [
                    {
                        "label": t.name,
                        "method": "restyle",
                        "args": [
                            {"visible": [t2.name == t.name for t2 in fig.data]},

                        ],
                    }
                    for t in fig.data
                ],
                'showactive':True,
                'x' : 0.0,
                'xanchor' : "left",
                'y' : 1.2,
                'yanchor' : "top"
            }
        ]
    )

    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

##########################################################################################
##########################################################################################
def GET_COUNT_BY_PERIOD(the_name):
    df_raw = get_as_dataframe(env.sh.worksheet('[CRM] RAW'))
    df_raw = df_raw[[i for i in df_raw.columns if 'Unn' not in i]]
    df_raw = df_raw.dropna(subset=[df_raw.columns[0]])
    df_raw = df_raw.astype(str)

    df_rept = get_as_dataframe(env.sh.worksheet('[REPORT] RAW'))
    df_rept = df_rept[[i for i in df_rept.columns if 'Unn' not in i]]
    df_rept = df_rept.dropna(subset=[df_rept.columns[0]])
    df_rept['rept_year'] = df_rept['rept_year'].astype(str)

    data_lst = []
    #### all
    df_rank = df_raw.groupby(['names']).agg({'tid': 'nunique','sid':'nunique'}).reset_index()
    df_rank = df_rank.sort_values('tid', ascending=False).reset_index()
    df_rank['index'] = [i + 1 for i in range(df_rank.shape[0])]
    tot_rank = df_rank['index'].max()
    try:
        prsc_cnt = df_rank[df_rank['names'] == str(the_name)]['tid'].values[0]
    except Exception:
        prsc_cnt = '0'
    try:
        the_rank = str(df_rank[df_rank['names'] == str(the_name)]['index'].values[0])
    except Exception:
        the_rank = '-'
    try:
        tot_dev = str(df_rank[df_rank['names'] == str(the_name)]['sid'].values[0])
    except Exception:
        tot_dev = '0'

    #### all rept
    df_rank = df_rept.groupby(['names']).agg({'tid':'nunique','cost': 'sum'}).reset_index()
    df_rank = df_rank.sort_values('cost', ascending=False).reset_index()
    df_rank['index'] = [i + 1 for i in range(df_rank.shape[0])]
    rept_rank_tot = df_rank['index'].max()
    revenue = "{:,}".format(df_rank[df_rank['names'] == str(the_name)]['cost'].max())

    try:
        rept_cnt = df_rank[df_rank['names'] == str(the_name)]['tid'].values[0]
        rept_rank = df_rank[df_rank['names'] == str(the_name)]['index'].values[0]
        rept_rank = str(the_rank)
    except Exception as e:
        # print("####", e)
        rept_cnt = '0'
        rept_rank = '-'
    # df_dev = df_raw.groupby([str(the_name)]).agg({'sid': 'nunique'}).reset_index()
    data_lst.append(
        ['전체 기간', prsc_cnt, the_rank, tot_rank, rept_cnt, rept_rank, rept_rank_tot, revenue, tot_dev])

    #### year
    df_rank = df_raw.groupby(['names','prsc_year']).agg({'tid':'nunique','sid': 'nunique'}).reset_index()
    the_year = str(datetime.now()).split('-')[0]
    df_rank = df_rank[df_rank['prsc_year'] == the_year].sort_values('tid', ascending = False).reset_index()
    df_rank['index'] = [i + 1 for i in range(df_rank.shape[0])]
    tot_rank = df_rank['index'].max()
    try:
        prsc_cnt = df_rank[df_rank['names'] == str(the_name)]['tid'].values[0]
    except Exception:
        prsc_cnt = '0'
    try:
        the_rank = str(df_rank[df_rank['names'] == str(the_name)]['index'].values[0])
    except Exception:
        the_rank = '-'
    try:
        tot_dev = str(df_rank[df_rank['names'] == str(the_name)]['sid'].values[0])
    except Exception:
        tot_dev = '0'

    #### year rept
    df_rank = df_rept.groupby(['names', 'rept_year']).agg({'tid':'nunique','cost': 'sum'}).reset_index()
    df_rank = df_rank[df_rank['rept_year'].str.contains(the_year)].sort_values('cost', ascending=False).reset_index()
    df_rank['index'] = [i + 1 for i in range(df_rank.shape[0])]
    rept_rank_tot = df_rank['index'].max()
    revenue = "{:,}".format(df_rank[df_rank['names'] == str(the_name)]['cost'].max())
    try:
        rept_cnt = df_rank[df_rank['names'] == str(the_name)]['tid'].values[0]
        rept_rank = df_rank[df_rank['names'] == str(the_name)]['index'].values[0]
        rept_rank = str(the_rank)
    except Exception as e:
        # print("####", e)
        rept_cnt = '0'
        rept_rank = '-'

    data_lst.append(['이번 년도', prsc_cnt, the_rank, tot_rank, rept_cnt, rept_rank, rept_rank_tot, revenue, tot_dev])

    #### quarter
    df_rank = df_raw.groupby(['names','prsc_quarter']).agg({'tid':'nunique','sid': 'nunique'}).reset_index()
    the_month = str(datetime.now()).split()[0][:7]
    the_year = the_month.split("-")[0]
    the_quarter = the_month.split("-")[1]
    if the_quarter<='03':
        val = 'Q1'
    elif the_quarter > '03' and the_quarter <='06':
        val = 'Q2'
    elif the_quarter > '07' and the_quarter <= '09':
        val = 'Q3'
    elif the_quarter > '09' and the_quarter <= '12':
        val = 'Q4'
    the_val = the_year + '-' + val
    df_rank = df_rank[df_rank['prsc_quarter'] == the_val].sort_values('tid', ascending = False).reset_index()
    df_rank['index'] = [i + 1 for i in range(df_rank.shape[0])]
    try:
        prsc_cnt = df_rank[df_rank['names'] == str(the_name)]['tid'].values[0]
    except Exception:
        prsc_cnt = '0'
    try:
        the_rank = str(df_rank[df_rank['names'] == str(the_name)]['index'].values[0])
    except Exception:
        the_rank = '-'
    try:
        tot_dev = str(df_rank[df_rank['names'] == str(the_name)]['sid'].values[0])
    except Exception:
        tot_dev = '0'
    tot_rank = df_rank['index'].max()

    #### quarter rept
    df_rank = df_rept.groupby(['names', 'rept_quarter']).agg({'tid':'nunique','cost': 'sum'}).reset_index()

    df_rank = df_rank[df_rank['rept_quarter'] == the_val].sort_values('cost', ascending=False).reset_index()
    df_rank['index'] = [i + 1 for i in range(df_rank.shape[0])]
    rept_rank_tot = df_rank['index'].max()
    revenue = "{:,}".format(df_rank[df_rank['names'] == str(the_name)]['cost'].max())
    try:
        rept_cnt = df_rank[df_rank['names'] == str(the_name)]['tid'].values[0]
        rept_rank = df_rank[df_rank['names'] == str(the_name)]['index'].values[0]
        rept_rank = str(the_rank)
    except Exception as e:
        print("####", e)
        rept_cnt = '0'
        rept_rank = '-'

    data_lst.append(
        ['이번 분기', prsc_cnt, the_rank, tot_rank, rept_cnt, rept_rank, rept_rank_tot, revenue, tot_dev])

    #### month
    df_rank = df_raw.groupby(['names','prsc_month']).agg({'tid':'nunique','sid': 'nunique'}).reset_index()
    the_month = str(datetime.now()).split()[0][:7]
    df_rank = df_rank[df_rank['prsc_month'] == str(the_month)].sort_values('tid', ascending = False).reset_index()
    df_rank['index'] = [i + 1 for i in range(df_rank.shape[0])]
    try:
        prsc_cnt = df_rank[df_rank['names'] == str(the_name)]['tid'].values[0]
    except Exception:
        prsc_cnt = '0'
    try:
        the_rank = str(df_rank[df_rank['names'] == str(the_name)]['index'].values[0])
    except Exception:
        the_rank = '-'
    try:
        tot_dev = str(df_rank[df_rank['names'] == str(the_name)]['sid'].values[0])
    except Exception:
        tot_dev = '0'
    tot_rank = df_rank['index'].max()

    #### month rept
    df_rank = df_rept.groupby(['names', 'rept_month']).agg({'tid':'nunique','cost': 'sum'}).reset_index()
    df_rank = df_rank[df_rank['rept_month'] == str(the_month)].sort_values('cost',ascending=False).reset_index()
    df_rank['index'] = [i + 1 for i in range(df_rank.shape[0])]
    rept_rank_tot = df_rank['index'].max()
    revenue = "{:,}".format(df_rank[df_rank['names'] == str(the_name)]['cost'].max())
    try:
        rept_cnt = df_rank[df_rank['names'] == str(the_name)]['tid'].values[0]
        rept_rank = df_rank[df_rank['names'] == str(the_name)]['index'].values[0]
        rept_rank = str(the_rank)
    except Exception as e:
        print("####", e)
        rept_cnt = '0'
        rept_rank = '-'


    data_lst.append(
        ['이번 월', prsc_cnt, the_rank, tot_rank, rept_cnt, rept_rank, rept_rank_tot, revenue, tot_dev])


    #### week
    df_rank = df_raw.groupby(['names','prsc_week']).agg({'tid':'nunique','sid': 'nunique'}).reset_index()
    params_yr = str(datetime.strptime(str(datetime.now()).split()[0], '%Y-%m-%d').isocalendar()[0])
    params_wk = str(datetime.strptime(str(datetime.now()).split()[0], '%Y-%m-%d').isocalendar()[1])
    if len(params_wk) == 1:
        params_wk = '0' + params_wk
    the_week = params_yr + '-W' + params_wk
    df_rank = df_rank[df_rank['prsc_week'] == the_week].sort_values('tid', ascending = False).reset_index()
    # df_rank = df_rank[df_rank['prsc_month'] == str(datetime.now()).split()[0][:7]].sort_values('tid',ascending=False).reset_index()
    df_rank['index'] = [i + 1 for i in range(df_rank.shape[0])]
    try:
        prsc_cnt = df_rank[df_rank['names'] == str(the_name)]['tid'].values[0]
    except Exception:
        prsc_cnt = '0'
    try:
        the_rank = str(df_rank[df_rank['names'] == str(the_name)]['index'].values[0])
    except Exception:
        the_rank = '-'
    try:
        tot_dev = str(df_rank[df_rank['names'] == str(the_name)]['sid'].values[0])
    except Exception:
        tot_dev = '0'

    tot_rank = df_rank['index'].max()

    #### week rept
    df_rank = df_rept.groupby(['names', 'rept_week']).agg({'tid':'nunique','cost': 'sum'}).reset_index()

    df_rank = df_rank[df_rank['rept_week'] == the_week].sort_values('cost', ascending=False).reset_index()
    # df_rank = df_rank[df_rank['prsc_month'] == str(datetime.now()).split()[0][:7]].sort_values('tid',ascending=False).reset_index()
    df_rank['index'] = [i + 1 for i in range(df_rank.shape[0])]
    rept_rank_tot = df_rank['index'].max()
    revenue = "{:,}".format(df_rank[df_rank['names'] == str(the_name)]['cost'].max())
    try:
        rept_cnt = df_rank[df_rank['names'] == str(the_name)]['tid'].values[0]
        rept_rank = df_rank[df_rank['names'] == str(the_name)]['index'].values[0]
        rept_rank = str(the_rank)
    except Exception as e:
        print("####", e)
        rept_cnt = '0'
        rept_rank = '-'

    data_lst.append(
        ['이번 주', prsc_cnt, the_rank, tot_rank, rept_cnt, rept_rank, rept_rank_tot, revenue, tot_dev])

    df_res = pd.DataFrame(
        columns = ['기간','처방수','prsc_rank','prsc_tot','분석수','rept_rank','rept_rank_tot','분석 매출','사용 기기수'],
        data = data_lst)
    df_res = df_res.astype(str)
    df_res['처방수'] = df_res['처방수'] + ' 건'
    df_res['prsc_tot'] = [str(i).split('.')[0] if str(i) != 'nan' else '0' for i in df_res['prsc_tot']]
    df_res['처방 순위'] = df_res['prsc_rank'] + '위 ('+df_res['prsc_tot'] + '명 중)'

    df_res['분석수'] = df_res['분석수'] + ' 건'
    df_res['rept_rank_tot'] = [str(i).split('.')[0] if str(i) != 'nan' else '0' for i in df_res['rept_rank_tot']]
    df_res['분석 순위'] = df_res['rept_rank'] + '위 (' + df_res['rept_rank_tot'] + '명 중)'
    # df_res['분석 매출'] = ["{:,}".format(i) for i in df_res['분석 매출']]
    return df_res[['기간','처방수','처방 순위','분석수','분석 순위','분석 매출','사용 기기수']]

def GET_REPORT_WEEKDAYS(df_report, the_period):
    if 'week' in the_period :
        df_gogo = df_report.groupby(['names', str(the_period),'rept_date_range','rept_day']).agg({'tid':'nunique'}).reset_index()
        df_gogo[str(the_period)] = df_gogo[str(the_period)] + ' ('+ df_gogo['rept_date_range'] + ')'
        df_gogo = df_gogo.drop(columns = ['rept_date_range'])
    else:
        df_gogo = df_report.groupby(['names', str(the_period),'rept_day']).agg({'tid':'nunique',}).reset_index()

    df_gogo['type'] = the_period.split("_")[1]
    df_gogo = df_gogo.rename(columns = {str(the_period):'period', 'rept_day':'weekday'})
    df_gogo['category'] = 'report'
    return df_gogo


def GET_PRSC_WEEKDAYS(df_prsc, the_period):
    if 'week' in the_period :
        df_gogo = df_prsc.groupby(['names', str(the_period),'date_range','prsc_day']).agg({'tid':'nunique'}).reset_index()
        df_gogo[str(the_period)] = df_gogo[str(the_period)] + ' ('+ df_gogo['date_range'] + ')'
        df_gogo = df_gogo.drop(columns = ['date_range'])
    else:
        df_gogo = df_prsc.groupby(['names', str(the_period),'prsc_day']).agg({'tid':'nunique'}).reset_index()

    df_gogo['type'] = the_period.split("_")[1]
    df_gogo = df_gogo.rename(columns = {str(the_period):'period', 'prsc_day':'weekday'})
    df_gogo['category'] = 'prescription'
    return df_gogo

def GET_UPLD_WEEKDAYS(df_upld, the_period):
    if 'week' in the_period :
        df_gogo = df_upld.groupby(['names', str(the_period),'upld_date_range','upld_day']).agg({'tid':'nunique'}).reset_index()
        df_gogo[str(the_period)] = df_gogo[str(the_period)] + ' ('+ df_gogo['upld_date_range'] + ')'
        df_gogo = df_gogo.drop(columns = ['upld_date_range'])
    else:
        df_gogo = df_upld.groupby(['names', str(the_period),'upld_day']).agg({'tid':'nunique',}).reset_index()
    df_gogo['type'] = the_period.split("_")[1]
    df_gogo = df_gogo.rename(columns = {str(the_period):'period', 'upld_day':'weekday'})
    df_gogo['category'] = 'upload'
    return df_gogo

def GET_DATA_ARCH(df_report, for_what):
    val_yr = for_what + '_year'
    val_qt = for_what + '_quarter'
    val_mt = for_what + '_month'
    val_wk = for_what + '_week'

    if for_what == 'rept':
        df_year = GET_REPORT_WEEKDAYS(df_report, str(val_yr))
        df_quarter = GET_REPORT_WEEKDAYS(df_report, str(val_qt))
        df_month = GET_REPORT_WEEKDAYS(df_report, str(val_mt))
        df_week = GET_REPORT_WEEKDAYS(df_report, str(val_wk))
    elif for_what == 'prsc':
        df_year = GET_PRSC_WEEKDAYS(df_report, str(val_yr))
        df_quarter = GET_PRSC_WEEKDAYS(df_report, str(val_qt))
        df_month = GET_PRSC_WEEKDAYS(df_report, str(val_mt))
        df_week = GET_PRSC_WEEKDAYS(df_report, str(val_wk))
    elif for_what == 'upld':
        df_year = GET_UPLD_WEEKDAYS(df_report, str(val_yr))
        df_quarter = GET_UPLD_WEEKDAYS(df_report, str(val_qt))
        df_month = GET_UPLD_WEEKDAYS(df_report, str(val_mt))
        df_week = GET_UPLD_WEEKDAYS(df_report, str(val_wk))

    df_rept_thus = pd.concat([df_year, df_quarter])
    df_rept_thus = pd.concat([df_rept_thus, df_month])
    df_rept_thus = pd.concat([df_rept_thus, df_week])
    return df_rept_thus

def GRAPH_SHOW_MULTI(df_therefore):
    fig = px.bar(
        df_therefore,
        x='period', y='tid',

        color='category',

        facet_row='type',
        facet_row_spacing=0.1,
        facet_col='weekday',
        category_orders={"weekday": ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']},
        barmode='group',
        template='plotly_white'
    )

    data_lst = [{
        "label": t.name,
        "method": "restyle",
        "args": [
            {"visible": [t2.name == t.name for t2 in fig.data]},

        ]} for t in fig.data]

    fig.update_layout(
        updatemenus=[
            {
                "buttons": sorted(list({i['label']: i for i in data_lst}.values()), key=itemgetter('label'),
                                  reverse=True),
                'showactive': True,
                'x': 0.0,
                'xanchor': "left",
                'y': 1.15,
                'yanchor': "top"
            }
        ]
    )
    fig.update_xaxes(
        categoryorder='array',
        categoryarray=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    )
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    # fig.for_each_yaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.update_yaxes(categoryorder='array', categoryarray=['prescription', 'upload', 'report'])
    fig.update_layout(font_size=10) #showlegend=False,
    fig.update_layout(legend=dict(yanchor="top", y=1.15, xanchor="right", x=0.4, orientation='h'))
    fig.update_layout(height=1000) #autosize=True,
    fig.update_xaxes(type='category')

    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig
