import json
import plotly
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from app.utils.proc import proc

def DF_SUMMARY(df_revenue, the_period):
    df_revenue['doct'] = df_revenue['hosp_name'] + ' - ' + df_revenue['doct_name']
    df_summ_rev = df_revenue[df_revenue['period_type'] == str(the_period)].groupby('period').agg({'tid':'sum','hosp_name':'nunique','doct':'nunique',}).reset_index()
    df_summ_rev['tid_pct'] = round(df_summ_rev['tid'].pct_change() * 100,2)
    df_summ_rev['hosp_pct'] = round(df_summ_rev['hosp_name'].pct_change() * 100,2)
    df_summ_rev['doct_pct'] = round(df_summ_rev['doct'].pct_change() * 100,2)
    return df_summ_rev


def GRAPH_FIRST_IN(df_first_in_thus, the_period):
    # period_type = 'month'
    the_df = df_first_in_thus[df_first_in_thus['period_type'] == str(the_period)].sort_values(['period','rank'])

    fig = px.scatter(
        the_df,
        x='period',
        y='rank',
        size='tid',
        hover_name='hosp_name',
        # text = 'hosp_name',
        color='hosp_cate',
        title=str(the_df.hosp_name.nunique()),
        height = 400,
        category_orders={
            'hosp_cate': ['상급종합병원', '종합병원', '의원', '병원'],
            'period': sorted(the_df.period.unique())
        },
        color_discrete_sequence=["#636EFA", "#EF553B", "#19D3F3", "#00CC96"],
        template='plotly_white'
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.for_each_trace(lambda t: t.update(textfont_color=t.marker.color, textposition='top center'))

    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.for_each_trace(lambda t: t.update(textfont_color=t.marker.color, textposition='top center'))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig



def GRAPH_ANIMATED(df_hosp, the_period):
    df_rev = df_hosp[df_hosp['period_type'] == str(the_period)].groupby(['period', 'hosp_cate', 'hosp_name']).agg(
        {'tid': 'sum'}).reset_index()
    if the_period == 'WEEK':
        df_rev['period'] = [i.split("(")[1].split()[0] for i in df_rev['period']]

    df_proc_thus = pd.DataFrame()
    for per in df_rev['period'].unique().tolist():
        df_proc = df_rev[['hosp_cate', 'hosp_name']].drop_duplicates()
        df_proc['period'] = per
        df_proc_thus = pd.concat([df_proc_thus, df_proc])

    df_thus_thus = pd.merge(df_proc_thus, df_rev, on=['period', 'hosp_cate', 'hosp_name'], how='left')
    df_thus_thus = df_thus_thus.sort_values(['period','tid'], ascending=[True, False])
    fig = px.bar(
        df_thus_thus,
        x='hosp_name',
        y='tid',
        text='tid',
        color = 'tid',
        facet_row='hosp_cate',
        facet_row_spacing=0.1,
        height=800,
        template='plotly_white',
        animation_frame='period',
        # color='hosp_cate',
        category_orders={'hosp_cate': ['상급종합병원', '종합병원', '의원', '병원']},
        color_discrete_sequence=["#636EFA", "#EF553B", "#19D3F3", "#00CC96"],
        range_y = [0, df_thus_thus.tid.max()],
    )

    for i, d in enumerate(fig.data):
        fig.data[i].textfont.color = ['white' if tid < df_thus_thus.tid.mean() else 'black' for tid in d.y]
    fig.for_each_annotation(lambda a: a.update(text= '<b>'+a.text.split("=")[1] +'</b>', textangle=-360))
    fig.update_layout(
        legend=dict(x=0.5, y=1.1, xanchor='center', yanchor='top'),
        legend_orientation='h'
    )
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.for_each_yaxis(lambda y: y.update(showticklabels=True, matches=None))
    # fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    # fig.update_yaxes(matches=None)
    # fig.for_each_xaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def GRAPH_PIE(df_summary, the_period):
    df_rev = df_summary[df_summary['period_type'] == str(the_period)].groupby(['period', 'hosp_cate', 'hosp_name','prsc_period']).agg(
            {'tid': 'sum'}).reset_index()
    if the_period == 'WEEK':
        df_rev['period'] = [i.split("(")[1].split()[0] for i in df_rev['period']]

    df_proc_thus = pd.DataFrame()
    for per in df_rev['period'].unique().tolist():
        df_proc = df_rev[['hosp_cate', 'hosp_name']].drop_duplicates()
        df_proc['period'] = per
        df_proc_thus = pd.concat([df_proc_thus, df_proc])

    df_thus_thus = pd.merge(df_proc_thus, df_rev, on=['period', 'hosp_cate', 'hosp_name'], how='left')
    df_thus_thus = df_thus_thus.sort_values(['period','tid'], ascending=[True, False])

    fig = px.bar_polar(
        df_thus_thus,
        theta='hosp_name',
        r='tid',
        height=1000,
        color='prsc_period',
        template='plotly_white',
        animation_frame='period',
        animation_group='hosp_cate',
        start_angle=60,
        category_orders={

            'hosp_cate': ['상급종합병원', '종합병원', '병원', '의원']
        }
        # color = 'prsc_period',
    )
    fig.update_layout(
        legend=dict(x=0.5, y=1.1, xanchor='center', yanchor='top'),
        legend_orientation='h'
    )
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.for_each_yaxis(lambda y: y.update(showticklabels=True, matches=None))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def GRAPH_PRSC(df_hosp, the_period):
    df_hosp = df_hosp[df_hosp['period_type'] == str(the_period)].groupby(['period']).agg(
        {'tid': 'sum'}).reset_index()
    if the_period == 'WEEK':
        df_hosp['period'] = [i.split("(")[1].split()[0] for i in df_hosp['period']]
    fig = px.bar(
        df_hosp,
        x='period',
        y='tid',
        text='tid',
        color='tid',
        height=400,
        template='plotly_white'
    )
    fig.update_xaxes(dtick='M1', tickformat='%b\n%Y')
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.update_layout(
        legend=dict(x=0.5, y=1.2, xanchor='center', yanchor='top'),
        legend_orientation='h',
        font_size=12
    )
    for i, d in enumerate(fig.data):
        fig.data[i].textfont.color = ['white' if tid < df_hosp.tid.mean() else 'black' for tid in d.y]
    fig.update_layout(xaxis=dict(rangeslider_visible=True))

    # fig.update_layout(
    #     updatemenus=[
    #         {
    #             'type': 'buttons',
    #             'direction': 'right',
    #             'x': 0.1,
    #             'y': 1.2,
    #             'showactive': True,
    #             'buttons': [
    #                 {
    #                     'label': 'Hide Numbers',
    #                     'method': 'update',
    #                     'args': [{'text': [None] * len(fig.data)}],  # 텍스트 숨김
    #                 },
    #                 {
    #                     'label': 'Show Numbers',
    #                     'method': 'update',
    #                     # 각 트레이스의 텍스트를 복원
    #                     'args': [{'text': [trace['text'] for trace in fig.data]}]
    #                 }
    #             ]
    #         }
    #     ]
    # )

    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig


def GRAPH_REPT_REV(df_revenue, the_period):
    df_rev = df_revenue[df_revenue['period_type'] == str(the_period)].groupby(['period']).agg(
     {'tid': 'sum', 'revenue': 'sum'}).reset_index()
    if the_period == 'WEEK':
     df_rev['period'] = [i.split("(")[1].split()[0] for i in df_rev['period']]

     fig = make_subplots(specs=[[{"secondary_y": True}]])
     fig22 = (px.bar(df_rev, x='period', y='tid'))  # , color = 'tid'
     fig11 = (px.line(df_rev, x='period', y='revenue', markers=True))

    else:

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig22 = (px.bar(df_rev, x='period', y='tid', text = 'tid')) #, color = 'tid'
        fig11 = (px.line(df_rev, x='period', y='revenue', text = 'revenue', markers=True))


    fig11.update_traces(opacity=.8)

    fig11.update_traces(line_color='red', line_width=1)
    fig11.update_traces(textposition='top center')
    for i, d in enumerate(fig11.data):
        fig11.data[i].text = [proc.human_format(x) for x in d.y]

    fig11.update_traces(yaxis='y2')

    fig.add_traces(fig11.data + fig22.data)

    fig.update_layout(plot_bgcolor="white")
    # fig.update_yaxes(title_text="<b>tid (bar)</b>", secondary_y=False)
    # fig.update_yaxes(title_text="<b>revenue (line)</b>", secondary_y=True)

    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.update_yaxes(matches=None)
    fig.for_each_xaxis(lambda yaxis: yaxis.update(showticklabels=True))

    fig.update_layout(height=400)
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.update_xaxes(dtick='M1', tickformat='%b\n%Y')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')


    # fig.update_layout(
    #     updatemenus=[
    #         {
    #             'type': 'buttons',
    #             'direction': 'right',
    #             'x': 0.1,
    #             'y': 1.2,
    #             'showactive': True,
    #             'buttons': [
    #                 {
    #                     'label': 'Hide Numbers',
    #                     'method': 'update',
    #                     'args': [{'text': [None] * len(fig.data)}],  # 텍스트 숨김
    #                 },
    #                 {
    #                     'label': 'Show Numbers',
    #                     'method': 'update',
    #                     # 각 트레이스의 텍스트를 복원
    #                     'args': [{'text': [trace['text'] for trace in fig.data]}]
    #                 }
    #             ]
    #         }
    #     ]
    # )

    fig.update_layout(xaxis=dict(rangeslider_visible=True))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def SCATTER_WEEKLY_HOSP_CHANGE(df_hosp,recent_week, prev_week):
    df_check_hosp = pd.concat([
        df_hosp[df_hosp['period'] == recent_week].groupby(['period', 'hosp_cate', 'hosp_name']).agg(
            {'tid': 'sum'}).sort_values('tid', ascending=False).reset_index(),
        df_hosp[df_hosp['period'] == prev_week].groupby(['period', 'hosp_cate', 'hosp_name']).agg(
            {'tid': 'sum'}).sort_values('tid', ascending=False).reset_index()
    ])
    df_check_hosp = df_check_hosp.sort_values(['hosp_name', 'period'])
    df_check_hosp['tid_pct'] = round(df_check_hosp.groupby('hosp_name')['tid'].pct_change() * 100, 2)
    fig = px.scatter(
        df_check_hosp,
        x='hosp_name',
        y='tid_pct',
        size='tid',
        color='tid',
        hover_name='tid',
        height=400,
        template='plotly_white'
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.for_each_annotation(lambda a: a.update(text=a.text, textangle=-360))
    # fig.update_xaxes(dtick='M1', tickformat='%b\n%Y')

    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def SCATTER_WEEKLY_DOCT_CHANGE(df_hosp,recent_week, prev_week):
    df_check_hosp = pd.concat([
        df_hosp[df_hosp['period']==recent_week].groupby(['period','hosp_cate','hosp_name','doct_name']).agg({'tid':'sum'}).sort_values('tid', ascending = False).reset_index(),
        df_hosp[df_hosp['period']==prev_week].groupby(['period','hosp_cate','hosp_name','doct_name']).agg({'tid':'sum'}).sort_values('tid', ascending = False).reset_index()
    ])
    df_check_hosp = df_check_hosp.sort_values(['hosp_name','doct_name','period'])
    df_check_hosp['tid_pct'] = round(df_check_hosp.groupby(['hosp_name','doct_name'])['tid'].pct_change()*100,2)
    df_check_hosp['doctors'] = df_check_hosp['hosp_name'] + ' - ' + df_check_hosp['doct_name']
    fig = px.scatter(
        df_check_hosp,
        x='doctors',
        y='tid_pct',
        size='tid',
        color='tid',
        hover_name='tid',
        height=400,
        template='plotly_white'
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.for_each_annotation(lambda a: a.update(text=a.text, textangle=-360))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig


######### PROC #########
def GET_QUARTER(i):
    year = i.split('-')[0]
    month = i.split('-')[1]
    try:
        if int(month) <= 3:
            val = 'Q1'
        elif int(month) > 3 and int(month) <= 6:
            val = 'Q2'
        elif int(month) > 6 and int(month) <= 9:
            val = 'Q3'
        elif int(month) > 9 and int(month) <= 12:
            val = 'Q4'
        return year + '-' + val
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
            sorted(df_hosp[df_hosp['period_type'] == 'WEEK']['period'].unique())[-1].split("(")[1].split()[2].split(
                ")")[0]
        week_lst = [str(i).split()[0] for i in pd.date_range(date_first, date_last)]
        week_last = sorted(df_hosp[df_hosp['period_type'] == 'WEEK']['period'].unique())[-3]
        week_prev = sorted(df_hosp[df_hosp['period_type'] == 'WEEK']['period'].unique())[-4]

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


def GRAPH_DOCTORS_TID(df_summary, the_period):
    df = df_summary[df_summary['period'] == str(the_period)].groupby(
        ['period_type','period', 'hosp_cate', 'hosp_name', 'doct_name']
    ).agg({'tid': 'sum'}).sort_values(['hosp_name', 'tid'],ascending=[True,False]).reset_index()

    proc00 = df.groupby(['period']).agg({'tid': 'sum'}).reset_index()
    proc00['period_label'] = proc00['period'] + ' (' + proc00['tid'].astype(str) + ')'

    proc11 = df.groupby(['period', 'hosp_cate']).agg({'tid': 'sum'}).reset_index()
    proc11['hosp_cate_label'] = proc11['hosp_cate'] + ' (' + proc11['tid'].astype(str) + ')'

    proc22 = df.groupby(['period', 'hosp_name']).agg({'tid': 'sum'}).reset_index()
    proc22['hosp_name_label'] = proc22['hosp_name'] + ' (' + proc22['tid'].astype(str) + ')'

    proc33 = df.groupby(['period', 'hosp_name', 'doct_name']).agg({'tid': 'sum'}).reset_index()
    proc33['doct_name_label'] = proc33['doct_name'] + ' (' + proc33['tid'].astype(str) + ')'

    the_df_hosp33 = pd.merge(df, proc00[['period', 'period_label']], on=['period'], how='left')
    the_df_hosp33 = pd.merge(the_df_hosp33, proc11[['period', 'hosp_cate', 'hosp_cate_label']],
                             on=['period', 'hosp_cate'], how='left')
    the_df_hosp33 = pd.merge(the_df_hosp33, proc22[['period', 'hosp_name', 'hosp_name_label']],
                             on=['period', 'hosp_name'], how='left')
    the_df_hosp33 = pd.merge(the_df_hosp33, proc33[['period', 'hosp_name', 'doct_name', 'doct_name_label']],
                             on=['period', 'hosp_name', 'doct_name', ], how='left')
    the_df_hosp33 = the_df_hosp33[
        ['period_label', 'hosp_cate_label', 'hosp_name_label', 'doct_name_label', 'tid', ]]
    the_df_hosp33.columns = [i.replace("_label", "") for i in the_df_hosp33.columns]

    # ### 버튼
    # periods = the_df_hosp33['period'].unique()
    #
    # buttons = []
    # for period in periods:
    #     # 해당 기간의 데이터 필터링
    #     df_filtered = the_df_hosp33[the_df_hosp33['period'] == period]
    #
    #     # 버튼 추가
    #     buttons.append(dict(
    #         method='restyle',
    #         label=period,
    #         args=[{
    #             'transforms': [{
    #                 'type': 'filter',
    #                 'target': the_df_hosp33['period'],
    #                 'operation': '=',
    #                 'value': period
    #             }]
    #         }]
    #     ))


    fig = px.treemap(
        the_df_hosp33,
        path=[
            px.Constant("TOTAL (" + str(the_df_hosp33.tid.sum()).replace(".0", "") + ")"),
            'hosp_cate', 'hosp_name', 'doct_name', 'tid'
        ],
        values='tid',
        color='tid',
        height=700,
        # color_continuous_midpoint = 0.1
    )
    # # 드롭다운 메뉴 추가
    # fig.update_layout(
    #     updatemenus=[{
    #         'buttons': buttons,
    #         'direction': 'down',
    #         'showactive': True,
    #     }]
    # )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

