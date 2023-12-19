import json
import plotly
import plotly.express as px

def GRAPH_REVENUE_BY_HOSPITALS(df_revenue):
    fig = px.bar(
        df_revenue,
        x='establishment',
        y='revenue',
        text='hosp_cnt',
        color='revenue',
        facet_row='hosp_cate',
        hover_name='hosp_name',
        template='plotly_white',
        height=800,
    )
    fig.update_layout(
        legend=dict(x=0.5, y=1.2, xanchor='center', yanchor='top'),
        legend_orientation='h',
        font_size=12
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def GRAPH_REVENUE_BY_PRIOD(df_revenue_by_period):
    fig = px.scatter(
        df_revenue_by_period,
        x = 'prsc_period',
        y = 'revenue',
        hover_name = 'hosp_name',
        size = 'revenue_per_tid',
        log_y = True,
        facet_row = 'hosp_cate',
        color = 'establishment',
        height = 800,
        template = 'plotly_white'
    )
    fig.update_layout(
        legend=dict(x=0.5, y=1.2, xanchor='center', yanchor='top'),
        legend_orientation='h',
        font_size=12
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def GRAPH_REVENUE(df_revenue_stat):
    fig = px.bar(
        df_revenue_stat,
        x='period',
        y='revenue',
        color='prsc_period',
        facet_col='period_type',
        template='plotly_white',
        height=400
    )

    fig.update_layout(
        legend=dict(x=0.5, y=1.2, xanchor='center', yanchor='top'),
        legend_orientation='h',
        font_size=12
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig