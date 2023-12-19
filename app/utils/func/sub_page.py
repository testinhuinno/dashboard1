import json
import plotly
import plotly.express as px
import pandas as pd

#### NO TEST
def BAR_NO_TEST_MONTH(df_no_tid):
    index = pd.date_range(df_no_tid.upld_date.min(), df_no_tid.upld_date.max(), freq='1D')
    df_index = pd.DataFrame(columns=['upld_date'], data=index)
    df_index['upld_date'] = df_index['upld_date'].astype('str')

    df_no_date = pd.merge(
        df_index,
        df_no_tid.groupby(['upld_date','hosp_name']).agg({'tid': 'nunique'}).reset_index(),
        on='upld_date',
        how='left'
    )
    df_no_date['tid'] = df_no_date['tid'].fillna(0)
    df_no_date['month'] = [i[:7] for i in df_no_date['upld_date']]
    df_no_date = df_no_date.dropna(subset=['hosp_name']).groupby(['month']).agg(
        {'tid': 'sum', 'hosp_name': 'unique'}).reset_index()

    fig = px.bar(
        df_no_date,
        x='month',
        y='tid',
        text='tid',
        hover_name='hosp_name',
        color='tid',
        height=400,
        template='plotly_white'
    )
    fig.update_layout(margin=dict(t=30, l=20, r=20, b=30))

    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def PIE_NO_TEST_MONTH(df_no_tid):
    fig = px.sunburst(
        df_no_tid.groupby(['hosp_cate','hosp_name']).agg({'tid':'nunique'}).reset_index(),
        path=['hosp_cate', 'hosp_name'],
        values='tid',
        color='tid',
        width=500,
        height=500,
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

######## WEEKLY HOSPITAL ########
def GET_DF_HOSPITAL(df_thus):
    df_check = df_thus.groupby(['hosp_cate', 'hosp_name', 'prsc_week_range']).agg({'tid': 'nunique'}).reset_index()
    df_check['week'] = [i.split()[0] for i in df_check['prsc_week_range']]
    # df_check['week'] = [i.split('-')[1].split()[0] for i in df_check['prsc_week_range']]

    # df_check['year'] = [i.split('-')[0] for i in df_check['prsc_week_range']]
    df_check['hospital'] = df_check['hosp_cate'] + ' - ' + df_check['hosp_name']
    return df_check

def GET_SCATTER_DOCTOR(df_check):
    # print("@@@@@", df_check.hosp_cate.unique())
    if '상급종합병원' == df_check.hosp_cate.unique()[0]:
        the_height = 500
    elif '종합병원' == df_check.hosp_cate.unique()[0]:
        the_height = 800
    else:
        the_height = 800

    fig = px.scatter(
        df_check,
        x='week',
        y='hospital',
        size='tid',
        color='tid',
        height=the_height,
        hover_name = 'prsc_week_range',
        template='plotly_white',
        category_orders={
            'week_range': sorted(df_check.week.unique().tolist()),
            # 'hosp_cate': ['상급종합병원', '종합병원', '병원', '의원']
        }
    )
    fig.for_each_yaxis(lambda y: y.update(showticklabels=True, matches=None))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.update_layout(
        legend=dict(
            x=0.5,
            y=1.1,  # 범례를 그래프 위에 위치
            xanchor='center',
            yanchor='top',
            orientation='h'  # 가로 방향으로 범례 배치
        )
    )
    fig.update_xaxes(dtick='M1', tickformat='%b\n%Y')
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig
def WEEKLY_GANTT_HOSPITAL(df_gantt):
    # Plotly Timeline 생성
    fig = px.timeline(
        df_gantt,
        x_start='Start',
        x_end='End',
        y='hospital',
        color='tid',
        text='tid',
        height=800,
        template='plotly_white'
    )
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.for_each_yaxis(lambda y: y.update(showticklabels=True, matches=None))
    fig.update_layout(hovermode='y')
    fig.update_layout(hovermode='x')

    fig.update_xaxes(showspikes=True, spikecolor="grey", spikesnap="cursor", spikemode="across", spikethickness=1)
    fig.update_yaxes(showspikes=True, spikecolor="grey", spikesnap="cursor", spikemode="across", spikethickness=1)
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig