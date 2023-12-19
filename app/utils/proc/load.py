import pandas as pd
import numpy as np
from datetime import datetime
from app.utils.proc import load_meta
from app.utils.constant import constant


def LOAD_MEMO_DATA():
    '''
        the_api from Redash Query#6
    '''
    the_sheet = 'no_lst'
    no_lst = load_meta.GET_META_DATA_BY(the_sheet)['prsc_id'].unique()#.dropna(subsets = ['prsc_id'])

    df_redash = pd.read_csv(
        "http://15.165.172.175/api/queries/6/results.csv?api_key=x33uFBo2cXFBth3iiaEdyZAu8JiBApu8lJTIbPos")

    df_redash = df_redash[~df_redash['검사번호'].isin(no_lst)]
    df_redash = df_redash.drop(
        columns=['기기사용 차수', '확인의 교수님 성명', '환자 성별', '병원 반납시점', '분석차수', '병원 리포트 컨펌 기한', '병원 레포트 컨펌 시점', '삭제 여부'],
        axis=1)
    df_redash['환자 나이(만)'] = df_redash['환자 나이(만)'].apply(GET_AGE_GROUP)
    df_redash['처방일'] = [str(i).split()[0] for i in df_redash['검사시작']]
    df_redash['처방월단위'] = df_redash['검사시작'].apply(GET_MONTHS)
    df_redash['처방년도'] = df_redash['검사시작'].apply(GET_YEARS)
    df_redash['처방월'] = df_redash['처방년도'] + df_redash['처방월단위']
    df_redash['처방분기'] = df_redash['처방년도'] + '-' + df_redash['처방월단위'].apply(GET_QUARTER)
    df_redash['처방요일'] = df_redash['처방일'].apply(GET_DAY_OF_WEEK)

    df_redash['처방종료일'] = [str(i).split()[0] for i in df_redash['처방기준 종료시점']]
    df_redash['처방종료년도'] = df_redash['처방기준 종료시점'].apply(GET_YEARS)
    df_redash['처방종료월단위'] = df_redash['처방기준 종료시점'].apply(GET_MONTHS)
    df_redash['처방종료월'] = df_redash['처방종료년도'] + '-' + df_redash['처방종료월단위']
    df_redash['처방종료요일'] = df_redash['처방종료일'].apply(GET_DAY_OF_WEEK)

    df_redash['리드오프일'] = [str(i).split()[0] for i in df_redash['리드오프시점']]
    df_redash['리드오프년도'] = df_redash['리드오프시점'].apply(GET_YEARS)
    df_redash['리드오프월단위'] = df_redash['리드오프시점'].apply(GET_MONTHS)
    df_redash['리드오프월'] = df_redash['리드오프년도'] + '-' + df_redash['리드오프월단위']
    df_redash['리드오프요일'] = df_redash['리드오프일'].apply(GET_DAY_OF_WEEK)

    df_redash['record_expt'] = round((df_redash['처방기준 종료시점'].apply(pd.to_datetime) - df_redash['검사시작'].apply(
        pd.to_datetime)).dt.total_seconds() / (60 * 60))
    df_redash['record_real'] = round((df_redash['데이터업로드'].apply(pd.to_datetime) - df_redash['리드오프시점'].apply(
        pd.to_datetime)).dt.total_seconds() / (60 * 60))

    df_redash['업로드일'] = [str(i).split()[0] for i in df_redash['데이터업로드']]
    df_redash['업로드년도'] = df_redash['데이터업로드'].apply(GET_YEARS)
    df_redash['업로드월단위'] = df_redash['데이터업로드'].apply(GET_MONTHS)
    df_redash['업로드월'] = df_redash['업로드년도'] + '-' + df_redash['업로드월단위']
    df_redash['업로드요일'] = df_redash['업로드일'].apply(GET_DAY_OF_WEEK)

    df_redash['레포트제공일'] = [str(i).split()[0] for i in df_redash['병원 레포트 제공 시점']]
    df_redash['레포트제공년도'] = df_redash['병원 레포트 제공 시점'].apply(GET_YEARS)
    df_redash['레포트제공월단위'] = df_redash['병원 레포트 제공 시점'].apply(GET_MONTHS)
    df_redash['레포트제공월'] = df_redash['업로드년도'] + '-' + df_redash['레포트제공월단위']
    df_redash['레포트제공요일'] = df_redash['레포트제공일'].apply(GET_DAY_OF_WEEK)

    df_redash['처방구간'] = df_redash['처방일수'].apply(GET_PRES_DAYS)
    df_redash['처방주'] = df_redash['검사시작'].apply(GET_WEEK_NUMBER)
    df_redash['처방종료주'] = df_redash['처방기준 종료시점'].apply(GET_WEEK_NUMBER)
    df_redash['리드오프주'] = df_redash['리드오프시점'].apply(GET_WEEK_NUMBER)
    df_redash['업로드주'] = df_redash['데이터업로드'].apply(GET_WEEK_NUMBER)

    df_redash['레포트제공주'] = df_redash['병원 레포트 제공 시점'].apply(GET_WEEK_NUMBER)

    df_redash['업로드아이디'] = [lst[0] if str(lst[1]).lower() != 'nan' else np.nan for lst in
                           df_redash[['검사번호', '데이터업로드']].values]
    df_redash['레포트아이디'] = [lst[0] if str(lst[1]).lower() != 'nan' else np.nan for lst in
                           df_redash[['검사번호', '병원 레포트 제공 시점']].values]

    # df_redash = df_redash.rename(columns={'처방 교수님 성명': '처방교수명'})
    df_redash.columns = df_redash.columns.map(constant.dict_columns)
    df_redash['prsc_ldff_leadtime'] = round((df_redash['ldff_at'].apply(pd.to_datetime) - df_redash[
        'prsc_start_at'].apply(pd.to_datetime)).dt.total_seconds() / (60 * 60))
    df_redash['ldff_upld_leadtime'] = round((df_redash['upld_at'].apply(pd.to_datetime) - df_redash[
        'ldff_at'].apply(pd.to_datetime)).dt.total_seconds() / (60 * 60))
    df_redash['upld_rept_leadtime'] = round((df_redash['rept_at'].apply(pd.to_datetime) - df_redash[
        'upld_at'].apply(pd.to_datetime)).dt.total_seconds() / (60 * 60))

    df_redash = df_redash[list(constant.dict_columns.values())]
    df_redash['names'] = df_redash['hosp_type'] + ' - ' + df_redash['hosp_name'] + ' - ' + df_redash['doct_name']

    return df_redash

def GET_AGE_GROUP(i: str):
    return str(i) + '~' + str(i + 4)

def GET_MONTHS(i: str):
    try:
        val = i.split("-")[1]
    except AttributeError:
        val = np.nan
    return val

def GET_YEARS(i: str):
    try:
        val = i.split("-")[0]
    except AttributeError:
        val = np.nan
    return val

def GET_DAY_OF_WEEK(dt: str):
    try:
        return pd.Timestamp(dt).strftime('%A')
    except Exception:
        return np.nan

def GET_PRES_DAYS(i: str):
    if i < 3:
        val = '1~2일'
    elif i >= 3 and i < 8:
        val = '4~7일'
    else:
        val = '8~14일'
    return val

def GET_WEEK_NUMBER(i: str):
    try:
        params_yr = str(datetime.strptime(str(i).split()[0], '%Y-%m-%d').isocalendar()[0])
        params_wk = str(datetime.strptime((i).split()[0], '%Y-%m-%d').isocalendar()[1])
        if len(params_wk) == 1:
            params_wk = '0' + params_wk
        val = params_yr + '-W' + params_wk
    except Exception:
        val = np.nan
    return val

def GET_QUARTER(i):
    try:
        if i<='03':
            val = 'Q1'
        elif i > '03' and i <='06':
            val = 'Q2'
        elif i > '07' and i <= '09':
            val = 'Q3'
        elif i > '09' and i <= '12':
            val = 'Q4'
        return val
    except Exception:
        return np.nan