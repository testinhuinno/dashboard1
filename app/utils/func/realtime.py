from app.utils.constant import constant
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe
import pandas as pd
import gspread
import folium
import plotly
import plotly.express as px
import json

json_file_name = {
  "type": "service_account",
  "project_id": "huinno-coo",
  "private_key_id": "0b1d2d81150db623f782db678de7648f8a77a384",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDnAYgZJeGIqDUm\nTYE2ALUOnZMdaTGOlncKImReepJMvffJBoOFOu4QStned8GN+HFape1prDYf0V2m\nbDF7zup+TQJ6kbWILVUfyrKsmYWTsfYt73IkD/wNd5VZTh/C84DzJjW7+3GPl/W5\nYLOSN5CFDUNuP5DGDu1hXoQd4/wuVADtMRF5a97O0zWQ0Cc3BlHZfxskHZ9KJzig\nd8YR/lh0uS7zlrq8YBiZy569aihBX4N0A1bzSQkomRiAVEsKERx8mJZSn+UVGhwZ\nhNbBpXlZjIYGjrCHVAcof5Mi4YYDQcvIQhlYdhBdruE31qWlrqO20IHM7F1bkDL2\nVcX2bzazAgMBAAECggEAUARSzUs21SxWxL7CDB+wl7BzXhOrC9YIw+Tn2WYhuR1w\ncBymgAbKobAbyZi33eJ5+UlSdHEnilvuUZBWj6k7xqYMPsKsG9CAFPQUcf73qxJQ\n0NaJNf6nc07B195c2B2axB6vLD9Ltc6QWjcp3HMMx1mxysWP81sGVNz1bJklKDJe\nSzhiRa5odEh3ZhbQvtDgo1NyNPbtLXWAe5Cir45WEeeyo1INkoWF2d3rD+HJaAdn\nrBmOrd0wSD6BCum+p5xW8CE5xVHdKV9MFpw8oJ5gQQBhlXp2yYTzqhgGW/zBDGyb\nQZWfVHOTzwloKWat/hDKNFPqAig6usdYN21hPsv2EQKBgQD8tXhV3DcgpwKtsvLH\nw8vmqoqCtXjyf8GT8WxY7Q/lOO5p10rp2kkdFUYD+PuE1lPkZJ85Gl01kb1rqr7p\nGsfY4RhJzVGonqOG7jNw3ap95cH29LWMVfUo56tAo7nSjc7KJxwJfOFF13j6qzR7\nYwi6uezI4YLaU5eZz9y+C0lFmwKBgQDqA7RLoeO9Aj2JxCaS7xaQWakfnd63XTdl\nlobrGGcEY4vWhaZTn2V0hvL1cr43ltYU0g19J/ajuYPNHaKJVSm6MQKg9P9b8hDN\nYAAn0shq3XvWq1EdYbfaayTyrPMpMGR/FZjC+znCi2Jf/nFuvMUCVllTpqdEI5Z0\nSckljXewyQKBgDKFXQ9dPTAr818ifWLug98TjSlgelOQsvSOuWh1zE25OgCy5+kk\nmKVV0W+N4UrHRnJMo4BZAvVos4PI2O3lSrrTFXX7tC2PuYWKLYKM7j7JJiPm/DyY\nGrEYz6XWlZnAe+zyMKq86pR55VfHznA0dlROQ0ZNv0lCmPZJFgpwWy+tAoGBAN8G\nFr96E2ygBPwWR9kDKdL60HcEYy0IFvKnif/mqs+A+9XAXCsYH3312vlXmLer9m2z\nXw2nl6Sj+lvy4WPXGUSMzv+NXw1G3wKMerl5Zm6KlSqa7Vx+M9VjBbyOXdQkfbKs\nZ4F0IrEpW+E2wu6R04SNvOY/TuxeqlY7uAslDywZAoGAFb0odR1r06bHaX8GiVAq\nlm5oOfIuvHZFIuHN6b7QQsBXA0zAZbO9jkuuB1hPsO7Uv8PB/Bfk/ijEzmtTIHmy\nZC/a2EzfAyTEOqn+dq/HqNc/92Mi9I5O6/4Ajh3EPpr0CDDNsk1UfFXCH/IBscuT\nutkArYzxCLGNsFuYh4M+eY4=\n-----END PRIVATE KEY-----\n",
  "client_email": "huinno-coo-683@huinno-coo.iam.gserviceaccount.com",
  "client_id": "117838592498488061103",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/huinno-coo-683%40huinno-coo.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

def GET_REALTIME_DATA(df):
    df.columns = [constant.dict_columns[i] if i in constant.dict_columns.keys() else i for i in df.columns]
    df['name'] = df['hosp_type'] + ' - ' + df['hosp_name'] + ' - ' + df['doct_name']
    df['prsc_date'] = df['prsc_start_at'].apply(GET_DATE_ONLY)
    df['upld_date'] = df['upld_at'].apply(GET_DATE_ONLY)
    df['rept_date'] = df['rept_at'].apply(GET_DATE_ONLY)
    df['prsc_period'] = df['prsc_days'].apply(GET_PRES_DAYS)
    return df

def GET_REALTIME_VALUES(df, date_today, date_yest):
    ## prsc
    prsc_yest = df['tid'][df['prsc_date'] == str(date_yest)].nunique()
    prsc_now = df['tid'][df['prsc_date'] == str(date_today)].nunique()
    try:
        prsc_change = round((prsc_now - prsc_yest) * 100 / prsc_yest, 2)
    except Exception:
        if prsc_yest == 0:
            prsc_change = prsc_now * 100
        else:
            prsc_change = 0

    hosp_yest = df['hosp_name'][df['prsc_date'] == str(date_yest)].nunique()
    hosp_now = df['hosp_name'][df['prsc_date'] == str(date_today)].nunique()
    try:
        hosp_change = round((hosp_now - hosp_yest) * 100 / hosp_yest, 2)
    except Exception:
        if hosp_yest == 0:
            hosp_change = hosp_now * 100
        else:
            hosp_change = 0

    doct_yest = df['doct_name'][df['prsc_date'] == str(date_yest)].nunique()
    doct_now = df['doct_name'][df['prsc_date'] == str(date_today)].nunique()
    try:
        doct_change = round((doct_now - doct_yest) * 100 / doct_yest, 2)
    except Exception:
        if doct_yest == 0:
            doct_change = doct_now * 100
        else:
            doct_change = 0

    upld_yest = df['tid'][df['upld_date'] == str(date_yest)].nunique()
    upld_now = df['tid'][df['upld_date'] == str(date_today)].nunique()
    try:
        upld_change = round((upld_now - upld_yest) * 100 / upld_yest, 2)
    except Exception:
        if upld_yest == 0:
            upld_change = upld_now * 100
        else:
            upld_change = 0

    rept_yest = df['tid'][df['rept_date'] == str(date_yest)].nunique()
    rept_now = df['tid'][df['rept_date'] == str(date_today)].nunique()
    try:
        rept_change = round((rept_now - rept_yest) * 100 / rept_yest, 2)
    except Exception:
        if rept_yest == 0:
            rept_change = rept_now * 100
        else:
            rept_change = 0
    return prsc_yest, prsc_now, prsc_change, hosp_yest, hosp_now, hosp_change, doct_yest, doct_now, doct_change, upld_yest, upld_now, upld_change, rept_yest, rept_now, rept_change
def GET_DATE_ONLY(i):
    try:
        val = str(i).split()[0]
    except Exeption:
        val = np.nan
    return val

def GET_PRES_DAYS(i):
    if i < 4:
        val = '1~3일'
    elif i>=4 and i < 8:
        val = '4~7일'
    else:
        val = '8~14일'
    return val
def GET_ACTIVE_MAP(df, date_today):
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(json_file_name, scope)
    gc = gspread.authorize(credentials)
    the_url = "https://docs.google.com/spreadsheets/d/1cVyI-MQ7xVWqO3QGCKTF5KT3DvIQKisyskeZ4b33T6U/edit#gid=0"
    sh = gc.open_by_url(the_url)
    df_meta = get_as_dataframe(sh.worksheet('[HOSP] MASTER'))  #[HOSP] MASTER
    # df_meta = get_as_dataframe(sh.worksheet(str('[HOSP] MASTER')))
    df_meta = df_meta[[i for i in df_meta.columns if 'Unn' not in i]]
    df_meta = df_meta.dropna(subset=['hosp'])

    df = df[df['prsc_date'] == str(date_today)]
    df_active = df[['hosp_type', 'hosp_name']].value_counts().reset_index()
    df_active.columns = ['hosp_type', 'hosp_name', 'count']
    df_meta = pd.merge(df_active, df_meta[['hosp_name', 'lat', 'lon']], on='hosp_name', how='left')
    df_meta = df_meta.dropna(subset=['lat'])


    the_map = folium.Map(
        location=[36.0, 127.9],
        zoom_start=6
    )

    for hosp_type, hospital, lat, lon, cnt in df_meta[['hosp_type','hosp_name', 'lat', 'lon', 'count']].values:
        if hosp_type == '1차 병원':
            color = 'green'
        elif hosp_type == '2차 병원':
            color = 'blue'
        else:
            color = 'red'
        if str(hosp_type).lower() == 'nan':
            popup_val = '<p>' + str(hospital) + '</p>'
        else:
            popup_val = '<p>' + str(hosp_type) + ' | ' + str(hospital) + ' | 처방 ' + str(cnt) + '건</p>'


        folium.Marker(
            location=[lat, lon],
            popup = hospital,
            tooltip = popup_val,
            icon=folium.Icon(color=color),
            radius=2,
        ).add_to(the_map)
    the_map.get_root().width = "400px"
    the_map.get_root().height = "400px"
    return the_map.get_root()._repr_html_()#.render()

def GET_THE_CHART(df, date_today, col):
    date_today = str(datetime.now()).split()[0]
    fig = px.bar(
        df[df[str(col)] == str(date_today)].groupby(['name', 'prsc_period']).agg(
            {'tid': 'count'}
        ).reset_index(),
        x='name', y='tid',
        color='prsc_period',
        template='plotly_white',
        text='tid',
        height=400
    )
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20), font = dict(size = 10))
    fig.update_traces(width=0.7)
    fig.for_each_annotation(lambda x: x.update(text=x.text.split("=")[1]))
    fig.update_layout(xaxis_title=None, legend = dict(y=1, x = 0.5, xanchor = 'center',yanchor="bottom",orientation="h",))
    fig.update_xaxes(tickangle = 40)
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig

def GET_THE_CHART22(df, date_today):
    # date_today = str(datetime.now()).split()[0]
    fig = px.bar(
        df[df['upld_date'] == str(date_today)].groupby(['name','prsc_period']).agg(
            {'tid': 'count'}
        ).reset_index(),
        x='name', y='tid',
        color='prsc_period',
        template='plotly_white',
        text='tid',
        height=400
    )
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20), font = dict(size = 10))
    fig.update_traces(width=0.7)
    fig.for_each_annotation(lambda x: x.update(text=x.text.split("=")[1]))
    fig.update_layout(xaxis_title=None, legend = dict(y=1, x = 0.5, xanchor = 'center',yanchor="bottom",orientation="h",))
    fig.update_xaxes(tickangle = 40)
    the_chart = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return the_chart