from app.utils.proc import proc
import json
import plotly
import plotly.express as px

def GET_NO_SID(df_no_sid):
    df_no_sid = df_no_sid.dropna(subset='sid')
    df_no_sid['index'] = df_no_sid['index'].apply(proc.custom_format)
    df_no_sid['처방수'] = df_no_sid['처방수'].apply(proc.custom_format)
    sid_col = df_no_sid.columns.values
    sid_val = df_no_sid.values.tolist()
    return sid_col, sid_val

def GRAPH_DEV_COUNT(df_dev_cumsum):
    # df_dev_cumsum['period'] = [int(str(i).replace("00%","")) for i in df_dev_cumsum['period']]
    fig = px.bar(
        df_dev_cumsum,
        x='period',
        y='count',
        text='count',
        color='val_type',
        barmode='group',
        height=400,
        template='plotly_white',
        facet_col = 'type'
    )
    fig.update_layout(
        legend=dict(x=0.5, y=1.2, xanchor='center', yanchor='top'),
        legend_orientation='h',
        font_size=12
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    # fig.update_xaxes(dtick='M1', tickformat='%b\n%Y')
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def GRAPH_DEV_COUNT_BY_HOSPITAL(df_dev_multi):
    fig = px.bar(
        df_dev_multi,
        x='period',
        y='count',
        text='count',
        color='hosp_cate',
        category_orders={
            'hosp_cate': ['상급종합병원', '종합병원', '병원', '의원'],
        },
        color_discrete_sequence=["#636EFA", "#EF553B", "#00CC96", "#19D3F3"],
        height=400,
        template='plotly_white',
        facet_col='type',
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.update_layout(
        legend=dict(x=0.5, y=1.2, xanchor='center', yanchor='top'),
        legend_orientation='h'
    )
    fig.for_each_xaxis(lambda yaxis: yaxis.update(showticklabels=True, matches=None))
    # fig.update_xaxes(dtick='M1', tickformat='%b\n%Y')
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig


def PIE_HOSPITAL_PCT(df_device_thus):
    fig = px.pie(
        df_device_thus.groupby(['hosp_cate','hosp_name']).agg({'sid':'nunique'}).reset_index(),
        values='sid',
        names='hosp_cate',
        category_orders={
            'hosp_cate': ['상급종합병원', '종합병원', '병원', '의원'],
        },
        hole=0.3,
        width=500,
        height=500,
        color_discrete_sequence=["#636EFA", "#EF553B", "#00CC96", "#19D3F3"],
    )
    # fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        legend=dict(x=0.5, y=1.1, xanchor='center', yanchor='top'),
        legend_orientation='h',
        font_size=12
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def PIE_BY_HOPITAL_TYPE(df_device_thus):
    df = df_device_thus.groupby(['establishment', 'hosp_cate', 'hosp_name']).agg(
            {'sid': 'nunique'}).reset_index().sort_values('sid', ascending=False)
    fig = px.sunburst(
        df,
        path=['hosp_cate', 'hosp_name'],
        values='sid',
        color='sid',
        width=500,
        height=500,
        color_continuous_midpoint = df.sid.mean()
    )
    fig.update_coloraxes(showscale=False)

    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def FUNNEL_PCT(df_device_thus):
    fig = px.funnel_area(
        df_device_thus.groupby(['status']).agg({'sid':'nunique'}).reset_index().rename(columns = {'sid':'count'}).sort_values('count', ascending = False),
        values='count',
        names='status',
        template='plotly_white',
        height=400,
    )
    fig.update_layout(
        legend=dict(x=0.5, y=1.1, xanchor='center', yanchor='top'),
        legend_orientation='h',
        font_size=12
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def FUNNEL_CNT(df_device_thus):
    fig = px.funnel(
        df_device_thus.groupby(['status']).agg({'sid':'nunique'}).reset_index().rename(columns = {'sid':'count'}).sort_values('count', ascending = False),
        x='count',
        y='status',
        template='plotly_white',
        height=400,
    )
    fig.update_layout(
        legend=dict(x=0.5, y=1.1, xanchor='center', yanchor='top'),
        legend_orientation='h',
        font_size=12
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def GET_THE_HOSP_MAP(df_device_in):
    fig = px.scatter_mapbox(
        df_device_in,
        lat="lat",
        lon="lon",
        hover_name='hosp_name',
        color='sid',
        size="sid",
        height=1000,
        size_max=40,
        zoom=6,
        title=str(
            df_device_in['hosp_name'].count()),
        mapbox_style="carto-positron",
        category_orders={'hosp_cate': ['상급종합병원', '종합병원', '병원', '의원']},
        color_discrete_sequence=["#636EFA", "#EF553B", "#00CC96", "#19D3F3"],
    )
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig