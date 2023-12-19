import json
import plotly
import plotly.express as px
import pandas as pd
from app.utils.proc import proc
import plotly.graph_objects as go



def GET_HEAT_MAP(df_thus):
    aaaa = pd.pivot(
        df_thus.groupby(['hosp_name', 'doct_name', 'prsc_day', 'prsc_hour']).agg(
            {'tid': 'nunique'}).reset_index(),
        index='prsc_day',
        columns='prsc_hour',
        values='tid'
    )
    #### 성정훈 수요일에 없음 --> 0으로 치환 필요
    bbbb = aaaa.T[ [i for i in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] if i in df_thus.prsc_day.unique()] ]
    df_pivot = bbbb.T

    fig = px.imshow(df_pivot, height=400, width=1000, template='plotly_white', text_auto=".f")

    fig.update_layout(yaxis_title=None, xaxis_title=None)
    fig.update_layout(margin=dict(t=30, l=20, r=20, b=30))

    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def GET_DOCT_DATA_BY_PERIOD(df_doct_tid, df_hosp):
    df_doct_tid = df_doct_tid[df_doct_tid['period_type'] != 'ALL']

    df_full_week = df_hosp[['period']][df_hosp['period_type'] == 'WEEK'].drop_duplicates().reset_index().drop(
        columns=['index']).sort_values('period')
    df_full_week = df_full_week[
        df_full_week['period'] >= df_doct_tid[df_doct_tid['period_type'] == 'WEEK']['period'].min()]
    df_doct_tid = pd.merge(df_doct_tid, df_full_week, on='period', how='outer')
    df_doct_tid['period_type'] = df_doct_tid['period_type'].fillna('WEEK')

    df_full_month = df_hosp[['period']][df_hosp['period_type'] == 'MONTH'].drop_duplicates().reset_index().drop(
        columns=['index']).sort_values('period')
    df_full_month = df_full_month[
        df_full_month['period'] >= df_doct_tid[df_doct_tid['period_type'] == 'MONTH']['period'].min()]
    df_doct_tid = pd.merge(df_doct_tid, df_full_month, on='period', how='outer')
    df_doct_tid['period_type'] = df_doct_tid['period_type'].fillna('MONTH')

    df_full_quarter = df_hosp[['period']][df_hosp['period_type'] == 'QUARTER'].drop_duplicates().reset_index().drop(
        columns=['index']).sort_values('period')
    df_full_quarter = df_full_quarter[
        df_full_quarter['period'] >= df_doct_tid[df_doct_tid['period_type'] == 'QUARTER']['period'].min()]
    df_doct_tid = pd.merge(df_doct_tid, df_full_quarter, on='period', how='outer')
    df_doct_tid['period_type'] = df_doct_tid['period_type'].fillna('QUARTER')

    df_doct_tid['tid'] = df_doct_tid['tid'].fillna(0)
    df_doct_tid = df_doct_tid.sort_values(['period_type', 'period'])
    return df_doct_tid

def BAR_DOCT_PRSC(df_doct_tid):
    fig = px.line(
        df_doct_tid,
        x='period',
        y='tid',
        text='tid',
        color='period_type',
        facet_row='period_type',
        height=700,
        template='plotly_white',
        category_orders={'period_type': ['YEAR', 'QUARTER', 'MONTH', 'WEEK']}
    )
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1], textangle= -360))
    fig.update_traces(textposition='top center')
    fig.update_layout(showlegend=False, font_size=10)
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.update_yaxes(matches=None)
    fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))

    # 각 period_type별 최대 tid 값 계산
    max_y_values = df_doct_tid.groupby('period_type')['tid'].max()

    # 각 서브플롯의 y축 범위 조정
    for i, d in enumerate(fig.data):
        period_type = d.name
        max_tid = max_y_values.get(period_type, 0)
        fig.layout[f'yaxis{-((i + 1) - 5)}'].update(range=[0, max_tid * 1.3])

    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def BAR_HOSP_PRSC_BY_DOCT(df_doct_tid):
    fig = px.line(
        df_doct_tid,
        x='period',
        y='tid',
        text='tid',
        color='doct_name',
        facet_row='period_type',
        height=700,
        template='plotly_white',
        category_orders={'period_type': ['YEAR', 'QUARTER', 'MONTH', 'WEEK']}
    )
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1], textangle= -360))
    fig.update_traces(textposition='top center')
    fig.update_layout(showlegend=False, font_size=10)
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.update_yaxes(matches=None)
    fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))

    # # 각 period_type별 최대 tid 값 계산
    # max_y_values = df_doct_tid.groupby('period_type')['tid'].max()
    #
    # # 각 서브플롯의 y축 범위 조정
    # for i, d in enumerate(fig.data):
    #     period_type = d.name
    #     max_tid = max_y_values.get(period_type, 0)
    #     fig.layout[f'yaxis{-((i + 1) - 5)}'].update(range=[0, max_tid * 1.3])

    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig
def PIE_DOCT_PRSC(df_prod_doct):
    fig = px.pie(
        df_prod_doct,
        values='tid',
        names='product',
        facet_col='prod_type',
        hole=0.3,
        height=500
    )
    fig.update_layout(margin=dict(t=30, l=0, r=0, b=0))
    fig.update_layout(showlegend=False, font_size=14)
    fig.update_traces(textposition='inside')

    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    # text_positions = [0.105, 0.375, 0.625, 0.895]
    text_positions = [0.23,0.77]

    # 각 파이 차트에 텍스트 추가
    for i, text in enumerate([
        str(df_prod_doct['tid'][df_prod_doct['prod_type'] == 'prsc_period'].sum()).replace(".0", ""),
        # str(df_prod_doct['tid'][df_prod_doct['prod_type'] == 'prod_type'].sum()).replace(".0", ""),
        str(df_prod_doct['tid'][df_prod_doct['prod_type'] == 'prsc_days'].sum()).replace(".0", ""),
        # str(df_prod_doct['tid'][df_prod_doct['prod_type'] == 'prod_detail'].sum()).replace(".0", "")
        ]):
        fig.add_annotation(
            x=text_positions[i % len(text_positions)], y=0.5,
            text=str(text),
            showarrow=False,
            xref="paper", yref="paper",
            font_size=20,
            font_color="black"
        )

    fig.update_traces(textinfo='label+percent+value')
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def GET_DOCTOR_DATA(df_hosp):
    df_all = df_hosp[df_hosp['period_type'] == 'ALL'].groupby(['hosp_cate', 'hosp_name', 'doct_name']).agg({'tid': 'sum', 'first_date': 'min', 'recent_date': 'max', 'total_prsc_days': 'max','no_prsc_days': 'min'}).reset_index().sort_values(['tid'], ascending=False)
    df_all['rank'] = df_all['tid'].rank(ascending=False)
    df_all = df_all.reset_index().drop(columns='index')
    df_all = df_all[['rank','hosp_cate','hosp_name','doct_name','tid','first_date','total_prsc_days','recent_date','no_prsc_days']]
    return df_all

def GET_HOSPITAL_DATA(df_hosp):
    df_all = df_hosp[df_hosp['period_type'] == 'ALL'].groupby(['hosp_cate', 'hosp_name']).agg(
        {'tid': 'sum', 'first_date': 'min', 'recent_date': 'max', 'total_prsc_days': 'max',
         'no_prsc_days': 'min'}).reset_index().sort_values(['tid'], ascending=False)
    df_all['rank'] = df_all['tid'].rank(ascending=False)
    df_all = df_all.reset_index().drop(columns='index')
    df_all = df_all[['rank','hosp_cate','hosp_name','tid','first_date','total_prsc_days','recent_date','no_prsc_days']]
    return df_all
def DATA_LABELING(the_df_hosp):
    proc00 = the_df_hosp.groupby(['period']).agg({'tid': 'sum'}).reset_index()
    proc00['period_label'] = proc00['period'] + ' (' + proc00['tid'].astype(str) + ')'

    proc11 = the_df_hosp.groupby(['period', 'hosp_cate']).agg({'tid': 'sum'}).reset_index()
    proc11['hosp_cate_label'] = proc11['hosp_cate'] + ' (' + proc11['tid'].astype(str) + ')'

    proc22 = the_df_hosp.groupby(['period', 'hosp_name']).agg({'tid': 'sum'}).reset_index()
    proc22['hosp_name_label'] = proc22['hosp_name'] + ' (' + proc22['tid'].astype(str) + ')'

    proc33 = the_df_hosp.groupby(['period', 'hosp_name', 'doct_name']).agg({'tid': 'sum'}).reset_index()
    proc33['doct_name_label'] = proc33['doct_name'] + ' (' + proc33['tid'].astype(str) + ')'

    the_df_hosp33 = pd.merge(the_df_hosp, proc00[['period', 'period_label']], on=['period'], how='left')
    the_df_hosp33 = pd.merge(the_df_hosp33, proc11[['period', 'hosp_cate', 'hosp_cate_label']],
                             on=['period', 'hosp_cate'], how='left')
    the_df_hosp33 = pd.merge(the_df_hosp33, proc22[['period', 'hosp_name', 'hosp_name_label']],
                             on=['period', 'hosp_name'], how='left')
    the_df_hosp33 = pd.merge(the_df_hosp33, proc33[['period', 'hosp_name', 'doct_name', 'doct_name_label']],
                             on=['period', 'hosp_name', 'doct_name', ], how='left')
    the_df_hosp33 = the_df_hosp33[
        ['period_label', 'hosp_cate_label', 'hosp_name_label', 'doct_name_label', 'prsc_period', 'tid', ]]
    the_df_hosp33.columns = [i.replace("_label", "") for i in the_df_hosp33.columns]
    return the_df_hosp33
def PIVOT_DATA(cc):

    cc_tot = cc.groupby(['period', 'hosp_cate', 'hosp_name', 'doct_name']).agg({'tid': 'sum'}).reset_index().rename(
        columns={'tid': 'tid_tot'})
    cc_thus = pd.merge(cc, cc_tot, on=['period', 'hosp_cate', 'hosp_name', 'doct_name'], how='left')

    df_pivot = pd.pivot_table(cc_thus, index=['period','hosp_cate', 'hosp_name', 'doct_name', 'tid_tot'],
                              columns=['prsc_period'], values='tid').reset_index().sort_values(
        ['tid_tot'], ascending=[False]).fillna('')
    # df_pivot['rank'] = [i for i in range(1, df_pivot.shape[0]+1)]
    df_pivot['rank'] = df_pivot.groupby(['period'])['tid_tot'].rank(method='dense', ascending=False)
    df_pivot = df_pivot.sort_values(['period', 'rank'], ascending=[False, True])

    df_pivot = df_pivot[['rank'] + [i for i in df_pivot.columns[:-1]]]
    df_pivot['rank'] = [str(i).replace(".0","") for i in df_pivot['rank']]
    df_pivot['tid_tot'] = [str(i).replace(".0", "") for i in df_pivot['tid_tot']]
    # df_pivot['1~2일'] = df_pivot['1~2일'].apply(proc.custom_format)
    # df_pivot['3~7일'] = df_pivot['3~7일'].apply(proc.custom_format)
    # df_pivot['8~14일'] = df_pivot['8~14일'].apply(proc.custom_format)
    df_pivot = df_pivot.reset_index().drop(columns = 'index')
    ####

    return df_pivot

def PIVOT_DATA_HOSP(cc):

    cc_tot = cc.groupby(['period', 'hosp_cate', 'hosp_name']).agg({'tid': 'sum'}).reset_index().rename(
        columns={'tid': 'tid_tot'})
    cc_thus = pd.merge(cc, cc_tot, on=['period', 'hosp_cate', 'hosp_name'], how='left')

    df_pivot = pd.pivot_table(cc_thus, index=['period','hosp_cate', 'hosp_name', 'tid_tot'],
                              columns=['prsc_period'], values='tid').reset_index().sort_values(
        ['tid_tot'], ascending=[False]).fillna('')
    df_pivot = df_pivot.sort_values(['period', 'rank'], ascending=[False, True])
    # df_pivot['rank'] = [i for i in range(1, df_pivot.shape[0]+1)]
    df_pivot = df_pivot[['rank'] + [i for i in df_pivot.columns[:-1]]]
    df_pivot['rank'] = [str(i).replace(".0", "") for i in df_pivot['rank']]
    df_pivot['tid_tot'] = [str(i).replace(".0", "") for i in df_pivot['tid_tot']]
    df_pivot['1~2일'] = df_pivot['1~2일'].apply(proc.custom_format)
    df_pivot['3~7일'] = df_pivot['3~7일'].apply(proc.custom_format)
    df_pivot['8~14일'] = df_pivot['8~14일'].apply(proc.custom_format)
    df_pivot = df_pivot.reset_index().drop(columns='index')
    ####

    return df_pivot


def GRAPH_BAR_TID_OVER_TIME(the_df_hosp):
    the_df_hosp['period'] = the_df_hosp['period'].astype(str)
    if '-W' in the_df_hosp.period.iloc[0]:
        the_df_hosp['year'] = [i.split("-")[1].split("(")[1] for i in the_df_hosp['period']]
        the_df_hosp['week'] = [i.split("-")[1].split(" (")[0] for i in the_df_hosp['period']]
        # the_df_hosp['tid'] = the_df_hosp['tid'].apply(proc.custom_format)
        fig = px.bar(
            the_df_hosp,
            x='week',
            y='tid',
            hover_name='period',
            facet_row='year',
            facet_row_spacing=0.1,
            template='plotly_white',
            color='hosp_cate',
            height=600,
            category_orders={
                'week': sorted(the_df_hosp.week.unique().tolist()),
                'hosp_cate': ['상급종합병원', '종합병원', '병원', '의원']
            },
            color_discrete_sequence=["#636EFA", "#EF553B", "#00CC96", "#19D3F3"]
        )
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1], textangle=-360))

        tot_tid_sums = the_df_hosp.groupby(['year', 'week'])['tid'].sum().reset_index()

        for i, annotation in enumerate(fig.layout.annotations):
            year = annotation.text.split('=')[-1]  # 연도 추출

            year_data = tot_tid_sums[tot_tid_sums['year'] == str(year)]

            for _, row in year_data.iterrows():
                fig.add_annotation(
                    x=row['week'],
                    y=row['tid'],
                    text=str(row['tid']).replace(".0",""),
                    xref='x' + str(i + 1),
                    yref='y' + str(i + 1),
                    showarrow=False,
                    font=dict(size=12),
                )
        fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True, matches=None))

    else:
        fig = px.bar(
            the_df_hosp,
            x='period',
            y='tid',
            hover_name='period',

            template='plotly_white',
            color='hosp_cate',
            height=400,
            category_orders={
                'period': sorted(the_df_hosp.period.unique().tolist()),
                'hosp_cate': ['상급종합병원', '종합병원', '병원', '의원']
            },
            color_discrete_sequence=["#636EFA", "#EF553B", "#00CC96", "#19D3F3"]
        )
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1], textangle=-360))

        tot_tid_sums = the_df_hosp.groupby(['period'])['tid'].sum().reset_index()

        fig.add_trace(go.Scatter(
            x=tot_tid_sums.period,
            y=tot_tid_sums['tid'],
            text=tot_tid_sums['tid'],
            mode='text',
            textposition='top center',
            textfont=dict(
                size=12,
            ),
            showlegend=False
        ))

        fig.update_layout(
            legend=dict(x=0.5, y=1.1, xanchor='center', yanchor='top'),
            legend_orientation='h'
        )


    fig.update_layout(
        legend=dict(x=0.5, y=1.1, xanchor='center', yanchor='top'),
        legend_orientation='h'
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig


def GRAPH_TREE_FOR_HOSP_TID(the_df_hosp):
    fig = px.treemap(
        the_df_hosp,
        path=[
            px.Constant("TOTAL ("+str(the_df_hosp.tid.sum()).replace(".0","")+")"),
            'hosp_cate','hosp_name','doct_name','prsc_period','tid'
        ],
        values='tid',
        color='tid',
        height=700,
    )

    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.update_xaxes(
        categoryorder='array',
        categoryarray=['상급종합병원','종합병원','병원','의원']
    )
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def GRAPH_TREE_FOR_HOSP_TID22(the_df_hosp):
    if 'year' in the_df_hosp.columns:
        fig = px.treemap(
            the_df_hosp,
            path=[
                px.Constant("TOTAL ("+str(the_df_hosp.tid.sum()).replace(".0","")+")"),
                'year','period','hosp_cate', 'hosp_name', 'doct_name', 'prsc_period', 'tid'
            ],
            values='tid',
            color='tid',
            height=700,
        )

    else:

        fig = px.treemap(
            the_df_hosp,
            path=[
                px.Constant("TOTAL ("+str(the_df_hosp.tid.sum()).replace(".0","")+")"),
                'period','hosp_cate','hosp_name','doct_name','prsc_period','tid'
            ],
            values='tid',
            color='tid',
            height=700,
            # color_continuous_midpoint = 0.1
        )

    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.update_xaxes(
        categoryorder='array',
        categoryarray= sorted(the_df_hosp.period.unique().tolist())#['상급종합병원','종합병원','병원','의원']
    )

    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def GRAPH_BAR_FOR_TID_QUARTER(df_hosp):
    fig = px.bar(
        df_hosp,  # df_hosp[df_hosp['period_type']=='TOTAL'],
        x='hosp_name',
        y='tid',
        text='tid',
        height=400,
        template='plotly_white',
        color='since',
        category_orders={
            'since': sorted(df_hosp.since.unique().tolist())
        },
    )
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig.update_yaxes(matches=None)
    fig.update_layout(hovermode='x')
    fig.update_xaxes(showspikes=True, spikecolor="grey", spikesnap="cursor", spikemode="across", spikethickness=1)
    fig.update_yaxes(showspikes=True, spikecolor="grey", spikesnap="cursor", spikemode="across", spikethickness=1)
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def TID_BY_HOSP(df_hosp):
    #### 병원별 상세 최근 분기 tid 많은 순
    fig = px.bar(
        df_hosp.sort_values(['period', 'tid'], ascending=[False, False]),
        x='hosp_name',
        y='tid',
        text='tid',
        facet_row='hosp_cate',
        height=1400,
        template='plotly_white',
        color='period',
        barmode='group',
        category_orders={
            'hosp_cate': ['상급종합병원', '종합병원', '병원', '의원'],
            'since': sorted(df_hosp.since.unique().tolist())
        }
    )
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig.update_yaxes(matches=None)
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def PROC_TID_BY_WEEK(df_prsc_by_hosp):
    aaa = df_prsc_by_hosp.groupby(['week_range', 'type']).agg({'tid': 'sum'}).reset_index()
    aaa['rank'] = aaa.groupby('type')['tid'].rank(ascending=False)
    aaa['changes'] = round(aaa.groupby('type')['tid'].pct_change() * 100, 2)
    aaa = aaa.sort_values(['type', 'week_range'])
    return aaa

def PROC_TID_RESULT(aaa, range_lst, index_now):
    prsc_now = aaa[(aaa['week_range'] == range_lst[index_now]) & (aaa['type'] == 'prsc')]['tid'].values[0]
    upld_now = aaa[(aaa['week_range'] == range_lst[index_now]) & (aaa['type'] == 'upld')]['tid'].values[0]
    rept_now = aaa[(aaa['week_range'] == range_lst[index_now]) & (aaa['type'] == 'rept')]['tid'].values[0]

    prsc_now_pct = aaa[(aaa['week_range'] == range_lst[index_now]) & (aaa['type'] == 'prsc')]['changes'].values[0]
    upld_now_pct = aaa[(aaa['week_range'] == range_lst[index_now]) & (aaa['type'] == 'upld')]['changes'].values[0]
    rept_now_pct = aaa[(aaa['week_range'] == range_lst[index_now]) & (aaa['type'] == 'rept')]['changes'].values[0]
    return prsc_now, upld_now, rept_now, prsc_now_pct, upld_now_pct, rept_now_pct

def GRAPH_PIE_PERIOD(aa_period, val):
    df = aa_period[(aa_period['week_range'] == str(val))]
    df['val_type'] = [str(i)+'일' if type(i) == int else i for i in df['val_type']]

    fig = px.pie(df,
                 values='tid', names='val_type', facet_col='type',
                 hole=0.3)
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.update_layout(showlegend=False, font_size=12)

    total_tid = str(df['tid'].sum()).replace(".0","")

    text_positions = [0.105, 0.375, 0.625, 0.895]

    # 각 파이 차트에 텍스트 추가
    for i, text in enumerate([
        str(df['tid'][df['type']=='prsc_period'].sum()).replace(".0",""),
        str(df['tid'][df['type']=='prod_type'].sum()).replace(".0",""),
        str(df['tid'][df['type']=='prsc_days'].sum()).replace(".0",""),
        str(df['tid'][df['type']=='prod_detail'].sum()).replace(".0","")]
    ):
        fig.add_annotation(
            x=text_positions[i % len(text_positions)], y=0.5,
            text=str(text),
            showarrow=False,
            xref="paper", yref="paper",
            font_size=20,
            font_color="black"
        )

    fig.update_traces(textinfo='label+percent+value')
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def GRAPH_BAR_HOSPITAL(df_prsc_by_hosp, range_lst, index_now):
    bbb = df_prsc_by_hosp[df_prsc_by_hosp['week_range'].isin(range_lst[index_now:index_now + 2])]
    # bbb = df.groupby(['type', 'week_range', 'hosp_name']).agg({'tid': 'sum'})
    bbb = bbb.reset_index().sort_values(['type', 'tid'],ascending=[True,False])
    bbb = bbb.reset_index().drop(columns=['index'])
    bbb['rank'] = bbb.groupby(['week_range', 'type']).tid.rank(method='min', ascending=False)
    bbb = bbb[bbb['rank']<=10].sort_values(['week_range','tid'], ascending = [False, False])

    fig = px.bar(bbb, x='hosp_name', y='tid', text='tid', color='type', hover_name = 'changes',
                 facet_col='type', facet_row='week_range', height=700,
                 facet_row_spacing=0.2,
                 template='plotly_white', category_orders={'type': ['prsc', 'upld', 'rept']})
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.update_layout(
        legend=dict(x=0.5, y=1.1, xanchor='center', yanchor='top'),
        legend_orientation='h'
    )
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1], textangle= -360))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def GRAPH_BAR_DOCTOR(df_prsc_by_doct, range_lst, index_now):
    ccc = df_prsc_by_doct[df_prsc_by_doct['week_range'].isin(range_lst[index_now:index_now + 2])]
    ccc = ccc.groupby(['type', 'week_range', 'hosp_name', 'doct_name']).agg({'tid': 'sum'})
    ccc = ccc.reset_index().sort_values(['type', 'tid'],ascending=[True,False]).reset_index()
    ccc = ccc.drop(columns=['index'])

    ccc['rank'] = ccc.groupby(['type','week_range']).tid.rank(method='min', ascending=False)
    ccc['doctors'] = ccc['hosp_name'] + ' - ' + ccc['doct_name']

    fig = px.bar(ccc[ccc['rank'] <= 10], x='doctors', y='tid', text='tid', color='type',
                 facet_col='type', facet_row='week_range', height=700,
                 facet_row_spacing=0.2,
                 template='plotly_white', category_orders={'type': ['prsc', 'upld', 'rept']})
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.update_layout(
        legend=dict(x=0.5, y=1.1, xanchor='center', yanchor='top'),
        legend_orientation='h'
    )
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1], textangle= -360))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig


def GRAPH_TREE_BY_HOSP(df_prsc_by_hosp, val, type):
    df = df_prsc_by_hosp[(df_prsc_by_hosp['period'] == str(val)) & (df_prsc_by_hosp['type']==str(type))]
    fig = px.treemap(
        df,
        path=['hosp_cate', 'hosp_name', 'tid'],
        values='tid',
        color='tid',
        height=700,
    )
    # fig.update_coloraxes(showscale=False)

    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.update_xaxes(
        categoryorder='array',
        categoryarray=['상급종합병원','종합병원','병원','의원']
    )
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig#.show()

def GRPH_TREE_BY_DOCT(df_prsc_by_doct, val, type):
    df = df_prsc_by_doct[(df_prsc_by_doct['period'] == str(val)) & (df_prsc_by_doct['type']==str(type))]
    fig = px.treemap(
        df,
        path=['hosp_cate', 'hosp_name', 'doct_name', 'tid'],
        values='tid',
        color='tid',
        height=700
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.update_xaxes(
        categoryorder='array',
        categoryarray=['상급종합병원','종합병원','병원','의원']
    )
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig  # .show()