import json
import plotly
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
from datetime import datetime, timedelta


def ACTIVE_SID(df_thug):
    df = df_thug[(df_thug['type'] == 'prsc')]
    df = df[df['period']!='ALL']

    df['tid_pct_change'] = round(df.groupby(['period_type', 'type'])['tid'].pct_change() * 100, 2)
    df['hover_name'] = df['period'].astype(str) + ' (' + df['tid_pct_change'].astype(str) + '% )'

    df_non = df[df['period_type'] != 'week']
    df_week = df[df['period_type'] == 'week']
    df_week['period'] = [i.split(" (")[1].split()[0] for i in df_week['period']]

    df_graph = pd.concat([df_non, df_week])

    fig = px.bar(
        df_graph,
        x='period',
        y='sid',
        text='sid',
        color='sid',
        hover_name='hover_name',
        facet_col='period_type',
        facet_col_wrap=2,
        facet_row_spacing=0.1,
        category_orders={
            'period_type': ['year', 'quarter', 'month', 'week'],
            'type': ['prsc', 'upld', 'rept']
        },
        height=600,
        template='plotly_white',
    )
    fig.update_layout(
        legend=dict(x=0.5, y=1.1, xanchor='center', yanchor='top'),
        legend_orientation='h'
    )
    fig.update_layout(margin=dict(t=30, l=0, r=0, b=0))
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.for_each_yaxis(lambda y: y.update(showticklabels=True, matches=None))

    fig.update_xaxes(dtick='M1', tickformat='%b\n%Y')
    fig.for_each_annotation(lambda a: a.update(text='<b>' + a.text.split("=")[1] + '</b>', textangle=-360))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def PRSC_BY_HOSPITAL(df_thug2):
    df = df_thug2[df_thug2['type'] == 'prsc'].groupby(['period_type', 'period', 'hosp_cate']).agg(
        {'tid': 'sum'}).reset_index()
    df = df[df['period'] != 'ALL']

    df['tid_pct_change'] = round(df.groupby(['period_type', 'hosp_cate'])['tid'].pct_change() * 100,2)
    df['hover_name'] = df['period'].astype(str) + ' (' + df['tid_pct_change'].astype(str) + '% )'

    df_non = df[df['period_type'] != 'week']
    df_week = df[df['period_type'] == 'week']
    df_week['period'] = [i.split(" (")[1].split()[0] for i in df_week['period']]

    df_graph = pd.concat([df_non, df_week])

    fig = px.bar(
        df_graph,
        x='period',
        y='tid',
        hover_name='hover_name',
        text='tid',
        facet_row='hosp_cate',
        facet_row_spacing=0.1,
        facet_col='period_type',
        color='hosp_cate',
        category_orders={
            'period_type': ['year', 'quarter', 'month', 'week'],
            'hosp_cate': ['상급종합병원', '종합병원', '병원', '의원']
        },
        height=900,
        template='plotly_white',
    )
    fig.update_layout(
        legend=dict(x=0.5, y=1.1, xanchor='center', yanchor='top'),
        legend_orientation='h'
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.for_each_yaxis(lambda y: y.update(showticklabels=True, matches=None))
    fig.update_xaxes(dtick='M1', tickformat='%b\n%Y')
    fig.for_each_annotation(lambda a: a.update(text='<b>' + a.text.split("=")[1] + '</b>', textangle=-360))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def MEMO_OPS_COUNT(df_thug):
    ##### LEAD TIME
    df = df_thug.groupby(['period_type', 'period', 'type']).agg({'tid': 'sum'}).reset_index()
    df = df[df['period'] != 'ALL']
    df['tid_pct_change'] = round(df.groupby(['period_type','type'])['tid'].pct_change() * 100,2)
    df['hover_name'] = df['period'].astype(str) + ' (' + df['tid_pct_change'].astype(str) + '% )'

    df_non = df[df['period_type'] != 'week']
    df_week = df[df['period_type'] == 'week']
    df_week['period'] = [i.split(" (")[1].split()[0] for i in df_week['period']]

    df_graph = pd.concat([df_non, df_week])
    # df_graph = df_graph.sort_values(['period_type','period'])


    fig = px.bar(
        df_graph,
        x='period',
        y='tid',
        text='tid',
        hover_name='hover_name',
        facet_row='type',
        facet_row_spacing=0.1,
        facet_col='period_type',
        color='type',
        category_orders={
            'period_type': ['year', 'quarter', 'month', 'week'],
            'type': ['prsc', 'upld', 'rept']
        },
        height=900,
        template='plotly_white',
    )
    fig.update_layout(
        legend=dict(x=0.5, y=1.1, xanchor='center', yanchor='top'),
        legend_orientation='h'
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.for_each_yaxis(lambda y: y.update(showticklabels=True, matches=None))

    fig.update_xaxes(dtick='M1', tickformat='%b\n%Y')
    fig.for_each_annotation(lambda a: a.update(text='<b>' + a.text.split("=")[1] + '</b>', textangle=-360))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig
    #
    # df = df_thug.groupby(['period_type', 'period', 'type']).agg({'tid_cnt': 'sum'}).reset_index()
    # df_non = df[df['period_type'] != 'week']
    # df_week = df[df['period_type'] == 'week']
    # df_week['period'] = [i.split(" (")[1].split()[0] for i in df_week['period']]
    # # df_week['period'] = [i.split()[0]+' ('+'/'.join(i.split('-')[2:4]).split()[0] +')' for i in df_week['period']]
    #
    # df_graph = pd.concat([df_non, df_week])
    #
    # fig = px.bar(
    #     df_graph,
    #     x='period',
    #     y='tid_cnt',
    #     text='tid_cnt',
    #     hover_name='period',
    #     facet_row='type',
    #     facet_row_spacing=0.1,
    #     facet_col='period_type',
    #     color='type',
    #     category_orders={
    #         'period_type': ['year', 'quarter', 'month', 'week'],
    #         'type': ['prsc', 'upld', 'rept']
    #     },
    #     height=900,
    #     template='plotly_white',
    #     # animation_frame = 'type',
    #     # animation_group = 'hosp_cate',
    # )
    # fig.update_layout(
    #     legend=dict(x=0.5, y=1.1, xanchor='center', yanchor='top'),
    #     legend_orientation='h'
    # )
    # fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    # fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    # fig.for_each_yaxis(lambda y: y.update(showticklabels=True, matches=None))
    #
    # fig.update_xaxes(dtick='M1', tickformat='%b\n%Y')
    # fig.for_each_annotation(lambda a: a.update(text='<b>' + a.text.split("=")[1] + '</b>', textangle=-360))
    # fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # return fig

def LEADTIME_STATUS(df_thug):
    ##### LEAD TIME
    df = df_thug.groupby(['period_type', 'period', 'type']).agg({'leadtime_days': 'mean'}).reset_index()
    df = df[df['period'] != 'ALL']
    df_non = df[df['period_type'] != 'week']
    df_week = df[df['period_type'] == 'week']
    df_week['period'] = [i.split(" (")[1].split()[0] for i in df_week['period']]
    # df_week['period'] = [i.split()[0]+' ('+'/'.join(i.split('-')[2:4]).split()[0] +')' for i in df_week['period']]

    df_graph = pd.concat([df_non, df_week])
    df_graph = df_graph.sort_values(['period'])

    fig = px.line(
        df_graph,
        x='period',
        y='leadtime_days',
        hover_name='period',
        facet_row='type',
        facet_row_spacing=0.1,
        facet_col='period_type',
        color='type',
        category_orders={
            'period_type': ['year', 'quarter', 'month', 'week'],
            'type': ['prsc', 'upld', 'rept']
        },
        markers=True,
        height=900,
        template='plotly_white',
    )
    fig.update_layout(
        legend=dict(x=0.5, y=1.1, xanchor='center', yanchor='top'),
        legend_orientation='h'
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.for_each_yaxis(lambda y: y.update(showticklabels=True, matches=None))
    fig.update_xaxes(dtick='M1', tickformat='%b\n%Y')
    fig.for_each_annotation(lambda a: a.update(text='<b>' + a.text.split("=")[1] + '</b>', textangle=-360))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

    #
    # ##### LEAD TIME
    # df = df_thug.groupby(['period_type', 'period', 'type']).agg({'leadtime_day': 'mean'}).reset_index()
    # df_non = df[df['period_type'] != 'week']
    # df_week = df[df['period_type'] == 'week']
    # df_week['period'] = [i.split(" (")[1].split()[0] for i in df_week['period']]
    # # df_week['period'] = [i.split()[0]+' ('+'/'.join(i.split('-')[2:4]).split()[0] +')' for i in df_week['period']]
    #
    # df_graph = pd.concat([df_non, df_week])
    #
    # fig = px.line(
    #     df_graph,
    #     x='period',
    #     y='leadtime_day',
    #     hover_name='period',
    #     facet_row='type',
    #     facet_row_spacing=0.1,
    #     facet_col='period_type',
    #     color='type',
    #     category_orders={
    #         'period_type': ['year', 'quarter', 'month', 'week'],
    #         'type': ['prsc', 'upld', 'rept']
    #     },
    #     markers=True,
    #     height=900,
    #     template='plotly_white',
    # )
    # fig.update_layout(
    #     legend=dict(x=0.5, y=1.1, xanchor='center', yanchor='top'),
    #     legend_orientation='h'
    # )
    # fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    # fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    # fig.for_each_yaxis(lambda y: y.update(showticklabels=True, matches=None))
    # fig.update_xaxes(dtick='M1', tickformat='%b\n%Y')
    # fig.for_each_annotation(lambda a: a.update(text='<b>' + a.text.split("=")[1] + '</b>', textangle=-360))
    # fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # return fig