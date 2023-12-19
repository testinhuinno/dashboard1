import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime
from gspread_dataframe import get_as_dataframe
from app.utils.constant import env
from app.utils.proc import load_meta, upto_date

def GRAPH_RANK(df_raw, the_period):
    df_month = df_raw.groupby(['hospitals', str(the_period)]).agg({'tid': 'nunique'}).reset_index()
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
        df_month, x='hospitals', y='tid', color=str(the_period), height=400,
        text = 'tid', template='plotly_white'
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
    fig.update_layout(title_text = title, title_x = 0)

    fig.update_layout(
        updatemenus=[
            {
                "buttons": list({i['label']: i for i in data_lst}.values()),
                'showactive': True,
                'x': 0.0,
                'xanchor': "left",
                'y': 1.2,
                'yanchor': "top"
            }
        ]
    )
    fig.update_layout(showlegend=False, font_size=10)
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.update_yaxes(matches=None)
    fig.for_each_xaxis(lambda yaxis: yaxis.update(showticklabels=True))

    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig