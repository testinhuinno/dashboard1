### PACKAGES FOR ENVIRONMENT
from app import app
from app.utils.func import home, realtime, crm_doctor, crm_hospital, devices, analytics, sub_page, overview, report
from app.utils.proc import load_meta, proc
from flask import render_template, request, redirect, url_for
from app.utils.constant import constant
### BASIC PACKAGES
from pytrends.request import TrendReq
from datetime import datetime, timedelta
import pandas as pd
@app.route('/dashboard', methods=['GET', 'POST'])
def func_dashboard():
    df_thug = load_meta.GET_THE_DATA("STAT_BY_PERIOD")
    df_device = load_meta.GET_THE_DATA("[RAW DATA] 기기 데이터 마스터")

    ### define period
    year_lst = df_thug[df_thug['period_type'] == 'year']['period'].unique().tolist()
    quarter_lst = df_thug[df_thug['period_type'] == 'quarter']['period'].unique().tolist()
    month_lst = df_thug[df_thug['period_type'] == 'month']['period'].unique().tolist()
    week_lst = df_thug[df_thug['period_type'] == 'week']['period'].unique().tolist()

    return render_template(
        'sub_pages/report.html', zip=zip,
    )
@app.route('/overview', methods=['GET', 'POST'])
def func_overview():
    ### data load
    # df_thug = load_meta.GET_THE_DATA("SUMMARY_TOTAL")
    df_thug = load_meta.GET_THE_DATA("STAT_BY_PERIOD")
    df_thug2 = load_meta.GET_THE_DATA("STAT_BY_HOSPITAL")
    ACTIVE_SID = overview.ACTIVE_SID(df_thug)
    MEMO_OPS_COUNT = overview.MEMO_OPS_COUNT(df_thug)
    LEADTIME_STATUS = overview.LEADTIME_STATUS(df_thug)
    PRSC_BY_HOSPITAL = overview.PRSC_BY_HOSPITAL(df_thug2)


    return render_template(
        'pages/overview.html',
        zip=zip,
        ACTIVE_SID=ACTIVE_SID,
        MEMO_OPS_COUNT=MEMO_OPS_COUNT,
        LEADTIME_STATUS=LEADTIME_STATUS,
        PRSC_BY_HOSPITAL=PRSC_BY_HOSPITAL,

    )


@app.route('/report', methods=['GET', 'POST'])
def func_report():
    ### data load
    # df_summary = load_meta.GET_THE_DATA("STAT_BY_DOCTOR")
    df_summary = load_meta.GET_THE_DATA("MASTER_SUMMARY")
    df_first_in_thus = load_meta.GET_THE_DATA("FIRST_IN")
    # ### period variable
    # the_date = str(datetime.now()).split()[0]
    # the_month = str(datetime.now()).split()[0][:7]
    # the_quarter = report.GET_QUARTER(the_date)
    # the_year = 'Y'+str(datetime.now()).split()[0][:4]
    # this_week, week_last, week_prev = report.GET_WEEK_PARAMS(df_summary)
    # the_year, the_month, the_quarter, week_last, the_date

    #### Data Load
    df_hosp = load_meta.GET_THE_DATA("MASTER_HOSP")
    df_revenue = load_meta.GET_THE_DATA("REVENUE")


    ### THIS WEEK
    # df_week_last = report.GET_STATUS_NUMBER(df_summary, the_month)
    # graph_last_week_doct = report.GRAPH_DOCTORS_TID(df_summary, the_month)
    #### FORM GET
    if request.method == 'POST':
        the_period = request.form.get('the_period')
        the_range = request.form.get('the_range')
        range_lst = sorted(df_summary[df_summary['period_type'] == str(the_period)]['period'].unique().tolist())[::-1]
        # range_lst = [the_range] + [i for i in the_range if i != the_range]
        if str(the_range) == '':
            the_range = range_lst[0]

    else:
        the_period = 'MONTH'#.lower()
        range_lst = sorted(df_summary[df_summary['period_type'] == str(the_period)]['period'].unique().tolist())[::-1]
        # print("@@@@@@@@", range_lst)
        # range_lst = [the_range] + [i for i in the_range if i != the_range]
        the_range = range_lst[0]

    #### table for the digits
    df_week_last = report.GET_STATUS_NUMBER(df_summary, the_range)
    # print(df_week_last)
    #### doctors
    graph_last_week_doct = report.GRAPH_DOCTORS_TID(df_summary, the_range)

    GRAPH_PRSC = report.GRAPH_PRSC(df_hosp, the_period)
    GRAPH_REV = report.GRAPH_REPT_REV(df_revenue, the_period)
    GRAPH_ANI = report.GRAPH_ANIMATED(df_hosp, the_period)
    GRAPH_PIE = report.GRAPH_PIE(df_hosp, the_period)
    GRAPH_FIRST_IN = report.GRAPH_FIRST_IN(df_first_in_thus, the_period)

    return render_template(
        'sub_pages/report.html', zip=zip,
        range_lst=range_lst, the_range=the_range,
        ### last week
        df_week_last=df_week_last.values[0].tolist(),
        graph_last_week_doct=graph_last_week_doct,

        the_period=the_period,
        GRAPH_PRSC = GRAPH_PRSC,
        GRAPH_REV = GRAPH_REV,
        GRAPH_ANI=GRAPH_ANI,
        GRAPH_PIE=GRAPH_PIE,
        GRAPH_FIRST_IN=GRAPH_FIRST_IN,
        # SCATTER_WEEKLY_HOSP_CHANGE=SCATTER_WEEKLY_HOSP_CHANGE,
        # SCATTER_WEEKLY_DOCT_CHANGE=SCATTER_WEEKLY_DOCT_CHANGE,
    )


@app.route('/by_hospital', methods=['GET', 'POST'])
def func_by_hospital():
    # 필터링 로직
    df_hosp = load_meta.GET_THE_DATA("MASTER_HOSP")
    df_doct = home.GET_HOSPITAL_DATA(df_hosp)
    column_names11 = df_doct.columns.values
    row_data11 = df_doct.values.tolist()

    df_check = load_meta.GET_THE_DATA("SCATTER")
    # df_check = sub_page.GET_DF_HOSPITAL(df_thus)
    # Plotly Timeline 생성
    df_check11 = df_check[df_check['hosp_cate'].isin(['상급종합병원'])]
    high = sub_page.GET_SCATTER_DOCTOR(df_check11)

    df_check22 = df_check[df_check['hosp_cate'].isin(['종합병원'])]
    middle = sub_page.GET_SCATTER_DOCTOR(df_check22)

    hosp_lst = df_check[~df_check['hosp_cate'].isin(['상급종합병원','종합병원'])]['hosp_name'].unique()
    avg_val = round(len(hosp_lst) / 2)

    df_check33 = df_check[(~df_check['hosp_cate'].isin(['상급종합병원', '종합병원'])) & (df_check['hosp_name'].isin(hosp_lst[:avg_val]))]
    bottom11 = sub_page.GET_SCATTER_DOCTOR(df_check33)

    df_check44 = df_check[
        (~df_check['hosp_cate'].isin(['상급종합병원', '종합병원'])) & (df_check['hosp_name'].isin(hosp_lst[avg_val:]))]
    bottom22 = sub_page.GET_SCATTER_DOCTOR(df_check44)


    if request.method == 'POST':

    # 검색어 가져오기
        selected_rows = request.form.getlist('selectedRow')
        for row in selected_rows:
            # print("@@@@@@",row)
            hosp_cate, hosp_name = row.split(',')

        # print("@@@@", hosp_cate, hosp_name, doct_name)
        # the_doct = hosp_name + '-' + doct_name

        #### 프로덕트 비율
        df_prod = load_meta.GET_THE_DATA('PRODUCT')
        df_prod_doct = df_prod[(df_prod['hosp_name'] == str(hosp_name)) ]
        pie_doct_prsc = home.PIE_DOCT_PRSC(df_prod_doct)

        #### 기간별 TID
        df_hosp_tid = df_hosp[(df_hosp['hosp_name'] == str(hosp_name)) ].groupby(
            ['period_type', 'period']).agg({'tid': 'sum'}).reset_index()
        df_hosp_tid = home.GET_DOCT_DATA_BY_PERIOD(df_hosp_tid, df_hosp)
        bar_doct_prsc = home.BAR_DOCT_PRSC(df_hosp_tid)

        df_doct_tid = df_hosp[(df_hosp['hosp_name'] == str(hosp_name))].groupby(
            ['doct_name','period_type', 'period']).agg({'tid': 'sum'}).reset_index()
        # df_doct_tid = home.GET_DOCT_DATA_BY_PERIOD(df_doct_tid, df_hosp)
        bar_doct_prsc22 = home.BAR_HOSP_PRSC_BY_DOCT(df_doct_tid)

        # #### 처방 히트맵
        # df_thus = load_meta.GET_THE_DATA('RAW_DATA')
        # df_thus_doct = df_thus[(df_thus['hosp_name'] == str(hosp_name)) ]
        # heat_map = home.GET_HEAT_MAP(df_thus_doct)df_thus_doct

        return render_template(
            'pages/by_hospital.html', zip=zip,
            column_names11=column_names11,
            row_data11=row_data11,
            pie_doct_prsc=pie_doct_prsc,
            the_doct=hosp_name,
            bar_doct_prsc=bar_doct_prsc,
            bar_doct_prsc22=bar_doct_prsc22,
            # heat_map=heat_map,
        )

    else:

        return render_template(
            'pages/by_hospital_main.html', zip=zip,
            column_names11=column_names11,
            row_data11 = row_data11,
            high=high, middle=middle,
            bottom11=bottom11,
            bottom22=bottom22,
        )

@app.route('/by_doctor', methods=['GET', 'POST'])
def func_by_doctor():
    # 필터링 로직
    df_hosp = load_meta.GET_THE_DATA("MASTER_HOSP")
    df_doct = home.GET_DOCTOR_DATA(df_hosp)
    column_names11 = df_doct.columns.values
    row_data11 = df_doct.values.tolist()

    if request.method == 'POST':

    # 검색어 가져오기
        selected_rows = request.form.getlist('selectedRow')
        for row in selected_rows:
            hosp_cate, hosp_name, doct_name = row.split(',')

        # print("@@@@", hosp_cate, hosp_name, doct_name)
        the_doct = hosp_name + '-' + doct_name

        #### 프로덕트 비율
        df_prod = load_meta.GET_THE_DATA('PRODUCT')
        df_prod_doct = df_prod[(df_prod['hosp_name'] == str(hosp_name)) & (df_prod['doct_name'] == str(doct_name))]
        pie_doct_prsc = home.PIE_DOCT_PRSC(df_prod_doct)

        #### 기간별 TID
        df_doct_tid = df_hosp[(df_hosp['hosp_name'] == str(hosp_name)) & (df_hosp['doct_name'] == str(doct_name))].groupby(
            ['period_type', 'period']).agg({'tid': 'sum'}).reset_index()
        df_doct_tid = home.GET_DOCT_DATA_BY_PERIOD(df_doct_tid, df_hosp)
        bar_doct_prsc = home.BAR_DOCT_PRSC(df_doct_tid)

        #### 처방 히트맵
        df_thus = load_meta.GET_THE_DATA('RAW_DATA')
        df_thus_doct = df_thus[(df_thus['hosp_name'] == str(hosp_name)) & (df_thus['doct_name'] == str(doct_name))]
        heat_map = home.GET_HEAT_MAP(df_thus_doct)

        return render_template(
            'pages/by_doctor.html', zip=zip,
            column_names11=column_names11,
            row_data11=row_data11,
            pie_doct_prsc=pie_doct_prsc,
            the_doct=the_doct,
            bar_doct_prsc=bar_doct_prsc,
            heat_map=heat_map,
        )

    else:

        return render_template(
            'pages/by_doctor_main.html', zip=zip,
            column_names11=column_names11,
            row_data11 = row_data11
        )


@app.route('/home/patch', methods=['GET', 'POST'])
def func_patch_home():
    # 기본값 설정
    the_period = request.form.get('the_period', 'WEEK')
    the_range = request.form.get('the_range')

    df = load_meta.GET_THE_DATA("MASTER_DATA")
    df_hosp = load_meta.GET_THE_DATA("MASTER_HOSP")

    # print("@@@@@", the_period, the_range)
    if the_range not in df[df['period_type']==str(the_period)]['period'].unique().tolist():
        if the_period == 'YEAR':
            val_first = 'YoY'
        elif the_period == 'QUARTER':
            val_first = 'QoQ'
        elif the_period == 'MONTH':
            val_first = 'MoM'
        elif the_period == 'WEEK':
            val_first = 'WoW'
        else:
            val_first = 'ALL'

        cnt_lst = [val_first] + df[df['period_type'] == str('ALL')].values[0].tolist()[2:]
        range_lst = sorted(df_hosp[df_hosp['period_type'] == str(the_period)]['period'].unique().tolist())[::-1]

        the_df_hosp = df_hosp[(df_hosp['period_type']==str(the_period)) ].groupby(['period','hosp_cate']).agg({'tid':'sum','hosp_name':'nunique'}).reset_index()
        graph11 = home.GRAPH_BAR_TID_OVER_TIME(the_df_hosp)
        the_df_hosp22 = df_hosp[(df_hosp['period_type']==str(the_period)) ].groupby(['period','hosp_cate','hosp_name','doct_name','prsc_period']).agg({'tid':'sum'}).reset_index()
        the_df_hosp22 = home.DATA_LABELING(the_df_hosp22)
        graph22 = home.GRAPH_TREE_FOR_HOSP_TID22(the_df_hosp22)
        #### DOCTOR
        df_by_doct = df_hosp[(df_hosp['period_type'] == str(the_period))].groupby(
            ['period', 'hosp_cate', 'hosp_name', 'doct_name', 'prsc_period']).agg({'tid': 'sum'}).reset_index()
        pivot_data = home.PIVOT_DATA(df_by_doct)
        column_names11 = pivot_data.columns.values
        row_data11 = pivot_data.values.tolist()

    elif the_range =='ALL':
        cnt_lst = df[df['period_type'] == str(the_period)].values[0].tolist()[1:]
        range_lst = sorted(df_hosp[df_hosp['period_type'] == str(the_period)]['period'].unique().tolist())[::-1]
        the_df_hosp = df_hosp[df_hosp['period_type'] == str(the_period)]
        graph11 = home.GRAPH_BAR_FOR_TID_QUARTER(the_df_hosp)

        the_df_hosp22 = home.DATA_LABELING(the_df_hosp)
        # if the_period == 'WEEK':
        #     the_df_hosp22['year'] = [i.split("-")[0] for i in the_df_hosp22['period']]
        graph22 = home.GRAPH_TREE_FOR_HOSP_TID(the_df_hosp22)
        #### DOCT
        df_by_doct = df_hosp[(df_hosp['period_type'] == str(the_period)) & (df_hosp['period'] == str(the_range))].groupby(
            ['period', 'hosp_cate', 'hosp_name', 'doct_name', 'prsc_period']).agg({'tid': 'sum'}).reset_index()
        pivot_data = home.PIVOT_DATA(df_by_doct)
        column_names11 = pivot_data.columns.values
        row_data11 = pivot_data.values.tolist()

    else:### SPECIFIC RANGE
        cnt_lst = df[(df['period_type'] == str(the_period)) & (df['period'] == str(the_range))].values[0].tolist()[1:]
        range_lst = sorted(df_hosp[df_hosp['period_type'] == str(the_period)]['period'].unique().tolist())[::-1]
        the_df_hosp = df_hosp[(df_hosp['period_type'] == str(the_period)) & (df_hosp['period'] == str(the_range))].groupby(['period','hosp_cate','hosp_name']).agg({'tid':'sum','since':'min'}).reset_index()
        graph11 = home.GRAPH_BAR_FOR_TID_QUARTER(the_df_hosp)
        the_df_hosp22 = df_hosp[(df_hosp['period_type'] == str(the_period)) & (df_hosp['period'] == str(the_range))].groupby(['period', 'hosp_cate', 'hosp_name','doct_name','prsc_period']).agg({'tid': 'sum'}).reset_index()
        the_df_hosp22 = home.DATA_LABELING(the_df_hosp22)

        graph22 = home.GRAPH_TREE_FOR_HOSP_TID(the_df_hosp22)
        #### DOCT
        df_by_doct = df_hosp[(df_hosp['period_type'] == str(the_period)) & (df_hosp['period'] == str(the_range))].groupby(
            ['period', 'hosp_cate', 'hosp_name', 'doct_name', 'prsc_period']).agg({'tid': 'sum'}).reset_index()
        pivot_data = home.PIVOT_DATA(df_by_doct)
        column_names11 = pivot_data.columns.values
        row_data11 = pivot_data.values.tolist()

    return render_template(
        'pages/patch_home.html',
        zip=zip,
        the_period=the_period,
        range_lst=range_lst,
        cnt_lst=cnt_lst,
        graph11=graph11, graph22=graph22,
        column_names11=column_names11, row_data11=row_data11,
        # column_names22=column_names22, row_data22=row_data22

    )


@app.route('/')
@app.route('/home')
def func_home():
    df_home = load_meta.GET_DASHBOARD_DATA("[HOME] STATS")
    the_vals = [proc.custom_format(i) for i in df_home.home.dropna().values]
    df_no_tid = load_meta.GET_THE_DATA("no_lst").sort_values(['upld_date'], ascending = False).reset_index()
    df_no_tid['index'] = [i+1 for i in df_no_tid['index']]
    no_test_size = df_no_tid.shape[0]
    column_names11 = df_no_tid.columns.values
    row_data11 = df_no_tid.values.tolist()

    return render_template(
        'pages/home.html', zip=zip,
        #### HOSPITALS & DOCTORS
        code_cnt = the_vals[0],
        hosp_cnt = the_vals[1],
        doct_cnt = the_vals[2],
        #### PRSC & UPLD & REPT
        prsc_cnt = the_vals[3],
        upld_cnt = the_vals[4],
        rept_cnt = the_vals[5],
        #### DEVICES
        tot_cumm_cnt = the_vals[6],
        tot_cumm_pct = the_vals[7],

        tot_valid_cnt = the_vals[8],
        tot_valid_pct = the_vals[9],
        tot_repl_cnt = the_vals[10],
        tot_repl_pct = the_vals[11],

        tot_active_cnt=the_vals[12],
        tot_active_pct=the_vals[13],
        tot_nonact_cnt = the_vals[14],
        tot_nonact_pct = the_vals[15],
        no_rec_cnt = the_vals[16],
        no_rec_pct = the_vals[17],

        no_test_size=no_test_size,
        column_names11=column_names11,
        row_data11=row_data11,
    )
##################### PAGENATION ######################
@app.route('/page/no_test', methods = ['GET','POST'])
def page_no_test():
    df_no_tid = load_meta.GET_THE_DATA("no_lst22").sort_values(['upld_date'], ascending=False).reset_index()
    df_no_tid['index'] = [i + 1 for i in df_no_tid['index']]
    no_test_size = df_no_tid.shape[0]
    column_names11 = df_no_tid.columns.values
    row_data11 = df_no_tid.values.tolist()

    BAR_NO_TEST_MONTH = sub_page.BAR_NO_TEST_MONTH(df_no_tid)
    PIE_NO_TEST_MONTH = sub_page.PIE_NO_TEST_MONTH(df_no_tid)
    return render_template(
        'sub_pages/no_test.html', zip=zip,
        no_test_size = no_test_size,
        column_names11 = column_names11,
        row_data11 = row_data11,
        BAR_NO_TEST_MONTH=BAR_NO_TEST_MONTH,
        PIE_NO_TEST_MONTH=PIE_NO_TEST_MONTH
    )

@app.route('/home/week', methods = ['GET','POST'])
def func_home_week():
    ### data load
    df_prsc_by_hosp = load_meta.GET_DASHBOARD_DATA("[HOME] WEEK_BY_HOSP")
    df_prsc_by_doct = load_meta.GET_DASHBOARD_DATA("[HOME] WEEK_BY_DOCT")
    aa_period = load_meta.GET_DASHBOARD_DATA("[HOME] WEEK_BY_PERIOD")
    df_by_week = load_meta.GET_DASHBOARD_DATA("[HOME] 전주 비교").fillna(0)
    df_tree_hosp = load_meta.GET_DASHBOARD_DATA("[HOME] TREE_HOSP")
    df_tree_doct = load_meta.GET_DASHBOARD_DATA("[HOME] TREE_DOCT")

    ### global var
    the_range = request.values.get("the_range")
    range_lst = ['(SELECT THE WEEK)']+sorted(df_by_week['week_range'].unique().tolist())[::-1]

    ### proc
    if str(the_range) == 'None':
        ### global var
        index_now = range_lst.index(range_lst[1])
        index_prev = index_now + 1
        the_week = range_lst[1]

        prsc_now, upld_now, rept_now, prsc_now_pct, upld_now_pct, rept_now_pct = home.PROC_TID_RESULT(df_by_week, range_lst, index_now)
        prsc_prev, upld_prev, rept_prev, prsc_prev_pct, upld_prev_pct, rept_prev_pct = home.PROC_TID_RESULT(df_by_week, range_lst, index_prev)
        fig_pie = home.GRAPH_PIE_PERIOD(aa_period, range_lst[1])
        fig_hosp = home.GRAPH_BAR_HOSPITAL(df_prsc_by_hosp, range_lst, index_now)
        fig_doct = home.GRAPH_BAR_DOCTOR(df_prsc_by_doct, range_lst, index_now)
        fig_tree_hosp = home.GRAPH_TREE_BY_HOSP(df_tree_hosp, the_week, 'week')
        fig_tree_doct = home.GRPH_TREE_BY_DOCT(df_tree_doct, the_week, 'week')

    else:
        ### global var
        index_now = range_lst.index(the_range)
        index_prev = index_now + 1
        the_week = range_lst[index_now]

        prsc_now, upld_now, rept_now, prsc_now_pct, upld_now_pct, rept_now_pct = home.PROC_TID_RESULT(df_by_week, range_lst, index_now)
        prsc_prev, upld_prev, rept_prev, prsc_prev_pct, upld_prev_pct, rept_prev_pct = home.PROC_TID_RESULT(df_by_week, range_lst, index_prev)
        fig_pie = home.GRAPH_PIE_PERIOD(aa_period, the_range)
        fig_hosp = home.GRAPH_BAR_HOSPITAL(df_prsc_by_hosp, range_lst, index_now)
        fig_doct = home.GRAPH_BAR_DOCTOR(df_prsc_by_doct, range_lst, index_now)
        fig_tree_hosp = home.GRAPH_TREE_BY_HOSP(df_tree_hosp, the_week, 'week')
        fig_tree_doct = home.GRPH_TREE_BY_DOCT(df_tree_doct, the_week, 'week')

    return render_template(
        'pages/home_by_week.html', zip=zip,
        #### HOSPITALS & DOCTORS
        range_lst = range_lst, the_week=the_week,
        prsc_now=prsc_now, upld_now=upld_now, rept_now=rept_now,
        prsc_now_pct=prsc_now_pct, upld_now_pct=upld_now_pct, rept_now_pct=rept_now_pct,
        prsc_prev=prsc_prev, upld_prev=upld_prev, rept_prev=rept_prev,
        fig_pie = fig_pie, fig_hosp=fig_hosp, fig_doct = fig_doct,
        fig_tree_hosp=fig_tree_hosp, fig_tree_doct=fig_tree_doct,

    )

@app.route('/status/realitime')
def func_realtime():
    the_time = str(datetime.now()).split()[1].split('.')[0]

    date_today = str(datetime.now()).split()[0]
    date_yest = str(datetime.now() - timedelta(days=1)).split()[0]
    df = pd.read_csv(
        "http://15.165.172.175/api/queries/6/results.csv?api_key=x33uFBo2cXFBth3iiaEdyZAu8JiBApu8lJTIbPos"
    )
    df = realtime.GET_REALTIME_DATA(df)
    prsc_yest, prsc_now, prsc_change, hosp_yest, hosp_now, hosp_change, doct_yest, doct_now, doct_change, upld_yest, upld_now, upld_change, rept_yest, rept_now, rept_change = realtime.GET_REALTIME_VALUES(df, date_today, date_yest)

    the_active_map = realtime.GET_ACTIVE_MAP(df, date_today)
    the_prsc_chart = realtime.GET_THE_CHART(df, date_today, 'prsc_date')
    the_upld_chart = realtime.GET_THE_CHART(df, date_today, 'upld_date')
    the_rept_chart = realtime.GET_THE_CHART(df, date_today, 'rept_date')


    return render_template(
        'pages/realtime.html', zip=zip,
        date_today = date_today, the_time=the_time,
        prsc_yest = prsc_yest, prsc_now = prsc_now, prsc_change = prsc_change,
        hosp_yest = hosp_yest, hosp_now = hosp_now, hosp_change = hosp_change,
        doct_yest = doct_yest, doct_now = doct_now, doct_change = doct_change,
        upld_yest = upld_yest, upld_now = upld_now, upld_change = upld_change,
        rept_yest = rept_yest, rept_now = rept_now, rept_change = rept_change,
        the_active_map = the_active_map, the_prsc_chart = the_prsc_chart,
        the_upld_chart=the_upld_chart, the_rept_chart=the_rept_chart

    )


@app.route('/devices/status', methods = ['GET','POST'])
def func_devices_stats():
    #### STATS
    df_home = load_meta.GET_DASHBOARD_DATA("[HOME] STATS")
    the_vals = [proc.custom_format(i) for i in df_home.devices.dropna().values]

    #### Tables
    df_no_sid = load_meta.GET_DASHBOARD_DATA("[HOME] nosid")
    sid_col, sid_val = devices.GET_NO_SID(df_no_sid)

    return render_template(
        'pages/devices_stats.html', zip=zip,
        date_today = the_vals[0],
        tot_cumm_cnt = the_vals[1],
        tot_sid_cnt = the_vals[2],
        tot_sid_pct = the_vals[3],
        not_use_cnt = the_vals[4],
        not_use_pct = the_vals[5],
        tot_hosp_cnt = the_vals[6],
        tot_hosp_once_cnt = the_vals[7],
        tot_hosp_once_pct = the_vals[8],
        hosp_not_use_cnt = the_vals[9],
        hosp_not_use_pct = the_vals[10],
        tot_once_cnt = the_vals[11],
        tot_once_pct = the_vals[12],
        not_once_cnt = the_vals[13],
        not_once_pct = the_vals[14],
        no_record_cnt = the_vals[15],
        no_record_pct = the_vals[16],
        tot_repl_cnt = the_vals[17],
        re_reple_cnt = the_vals[18],
        repl_normal_cnt = the_vals[19],
        diff_cnt = the_vals[20],
        re_reple_pct = the_vals[21],
        repl_normal_pct = the_vals[22],
        re_released_cnt = the_vals[23],
        never_cnt = the_vals[24],
        sid_col = sid_col, sid_val = sid_val,
    )


@app.route('/devices/graphs', methods = ['GET','POST'])
def func_analytics_devices():
    #### DATA
    df_device_thus = load_meta.GET_DASHBOARD_DATA("[DEVICES] MASTER")
    df_dev_count = load_meta.GET_DASHBOARD_DATA("[HOME] DEVICE COUNT")
    df_dev_count = df_dev_count[df_dev_count['type'].notnull()]
    df_dev_count['period'] = [i if '-' in str(i) else float(i) for i in df_dev_count['period']]
    df_dev_multi = load_meta.GET_DASHBOARD_DATA("[HOME] DEVICE COUNT BY HOSP")
    df_dev_multi = df_dev_multi[df_dev_multi['type'].notnull()]
    df_dev_multi['period'] = [i if '-' in str(i) else float(i) for i in df_dev_multi['period']]

    df_device_in = load_meta.GET_DASHBOARD_DATA('[DEVICES] LIST_IN').dropna(subset = ['lat'])
    df_device_out = load_meta.GET_DASHBOARD_DATA('[DEVICES] LIST_OUT').dropna(subset = ['lat'])


    #### BAR CHART
    bar_monthly_cnt = devices.GRAPH_DEV_COUNT(df_dev_count)
    bar_hospital_type = devices.GRAPH_DEV_COUNT_BY_HOSPITAL(df_dev_multi)

    #### PIE CHART
    pie_hospital_pct = devices.PIE_HOSPITAL_PCT(df_device_thus)
    pie_hospital_type = devices.PIE_BY_HOPITAL_TYPE(df_device_thus)

    #### FUNNEL CHART
    funnel_cnt = devices.FUNNEL_CNT(df_device_thus)
    funnel_pct = devices.FUNNEL_PCT(df_device_thus)

    #### MAO_CHART
    in_chart = devices.GET_THE_HOSP_MAP(df_device_in)
    out_chart = devices.GET_THE_HOSP_MAP(df_device_out)

    return render_template(
        'pages/devices_graph.html', zip=zip,
        bar_monthly_cnt=bar_monthly_cnt,
        bar_hospital_type=bar_hospital_type,
        pie_hospital_pct = pie_hospital_pct,
        pie_hospital_type = pie_hospital_type,
        funnel_cnt=funnel_cnt, funnel_pct=funnel_pct,
        in_chart = in_chart, out_chart = out_chart
    )

@app.route('/report/revenue', methods = ['GET','POST'])
def func_analytics_revenue():
    df_revenue_stat = load_meta.GET_DASHBOARD_DATA("[HOME] STATS REVENUE")
    df_revenue_stat = df_revenue_stat.dropna(subset = ['period_type'])
    the_chart3 = analytics.GRAPH_REVENUE(df_revenue_stat)

    df_revenue = load_meta.GET_DASHBOARD_DATA("[HOME] ANALYTICS_REVENUE")
    df_revenue = df_revenue.dropna(subset = ['hosp_cate'])
    the_chart = analytics.GRAPH_REVENUE_BY_HOSPITALS(df_revenue)

    df_revenue_by_period = load_meta.GET_DASHBOARD_DATA("[HOME] ANALYTICS_REVENUE_PERIOD")
    the_chart2 = analytics.GRAPH_REVENUE_BY_PRIOD(df_revenue_by_period)
    return render_template(
        'pages/analytics.html', zip=zip,
        the_chart=the_chart, the_chart2=the_chart2,the_chart3=the_chart3
    )
@app.route('/report/creation', methods = ['GET','POST'])
def func_report_creation():
    df_report_creation = load_meta.GET_DASHBOARD_DATA("[MA] TID")
    df_report_creation = df_report_creation.dropna(subset = ['rept_month'])
    df_report_creation = df_report_creation.fillna('')
    return render_template(
        'pages/report_creation.html', zip=zip,
        column_names11=df_report_creation.columns.values,
        row_data11=df_report_creation.values.tolist()
    )


@app.route('/crm_hospital/', methods = ['GET','POST'])
def func_crm_hospital():
    the_name_lst = sorted(crm_doctor.GET_DOCTOR_DATA()['hospitals'].unique().tolist())[::-1]
    the_name_lst = ['( SEARCH FOR THE HOSPITAL PAGE )'] + the_name_lst

    df_raw = crm_doctor.GET_DOCTOR_DATA()

    the_graph_year = crm_hospital.GRAPH_RANK(df_raw, 'prsc_year')
    the_graph_quarter = crm_hospital.GRAPH_RANK(df_raw, 'prsc_quarter')
    the_graph_month = crm_hospital.GRAPH_RANK(df_raw, 'prsc_month')
    the_graph_week = crm_hospital.GRAPH_RANK(df_raw, 'prsc_week')


    return render_template(
        'pages/crm_hospital.html', zip=zip,
        the_name_lst=the_name_lst,
        the_graph_year=the_graph_year, the_graph_quarter=the_graph_quarter,
        the_graph_month = the_graph_month, the_graph_week=the_graph_week,
    )

@app.route('/crm_doctors/', methods = ['GET','POST'])
def func_crm_doctors():
    the_name_lst = sorted(crm_doctor.GET_DOCTOR_DATA()['names'].unique().tolist())[::-1]
    the_name_lst = ['( SEARCH FOR THE DOCTORS PAGE )'] + the_name_lst

    df_raw = crm_doctor.GET_DOCTOR_DATA()
    the_graph_year = crm_doctor.GRAPH_RANK(df_raw, 'prsc_year')
    the_graph_quarter = crm_doctor.GRAPH_RANK(df_raw, 'prsc_quarter')
    the_graph_month = crm_doctor.GRAPH_RANK(df_raw, 'prsc_month')
    the_graph_week = crm_doctor.GRAPH_RANK(df_raw, 'prsc_week')

    return render_template(
        'pages/crm_doctor.html', zip=zip,
        the_name_lst=the_name_lst,
        the_graph_year=the_graph_year, the_graph_quarter=the_graph_quarter,
        the_graph_month = the_graph_month, the_graph_week=the_graph_week,

    )

@app.route('/crm_doctors/select/', methods=['GET','POST'])
def func_crm_doctor_select():
    try:
        ### month
        the_sheet = '[CRM] DOCTORS MONTHLY'
        df_month = load_meta.GET_META_DATA_BY(the_sheet)

        the_name = request.values.get("the_name")
        the_name_lst = [the_name] + df_month['names'].unique().tolist()[::-1]

        df_hence = load_meta.GET_META_DATA_BY('[REVENUE] RAW')
        df_doct = df_hence[df_hence['names']==the_name]
        the_graph_multiple = crm_doctor.GRAPH_THE_MULTIPLE_PERIOD(df_doct)

        df_meta = load_meta.GET_THE_LOCATION('META_HOSPITAL')
        the_hospital = the_name.split(' - ')[1]
        the_active_map = load_meta.GET_ACTIVE_MAP(df_meta, the_hospital)

        hosp_type = the_name.split(" - ")[0]
        hosp_name = the_name.split(" - ")[1]
        doct_name = the_name.split(" - ")[2]

        min_date, max_date, tot_dur, duration = crm_doctor.GET_INFO(the_name)

        df_stat = crm_doctor.GET_COUNT_BY_PERIOD(the_name)
        the_cols = df_stat.columns.values
        the_vals = df_stat.values.tolist()

        df_rept = load_meta.GET_META_DATA_BY("[REPORT] RAW")
        df_prsc = load_meta.GET_META_DATA_BY("[PRSC] RAW")
        df_upld = load_meta.GET_META_DATA_BY("[UPLOAD] RAW").dropna(subset=['upld_year'])

        df_rept_thus = crm_doctor.GET_DATA_ARCH(df_rept, 'rept')
        df_prsc_thus = crm_doctor.GET_DATA_ARCH(df_prsc, 'prsc')
        df_upld_thus = crm_doctor.GET_DATA_ARCH(df_upld, 'upld')

        df_therefore = pd.concat([df_rept_thus, df_prsc_thus])
        df_therefore = pd.concat([df_therefore, df_upld_thus])
        df_therefore['period'] = [str(i).split(".")[0] if '.' in str(i) else i for i in df_therefore['period']]
        # df_therefore['period'] = df_therefore['period'].replace({".0": ""})

        df_therefore=df_therefore[df_therefore['names']==str(the_name)]
        fig_multi = crm_doctor.GRAPH_SHOW_MULTI(df_therefore)

        return render_template(
            'pages/crm_doctors_select.html', zip=zip,
            the_name_lst=the_name_lst, the_name=the_name,
            the_active_map=the_active_map,
            hosp_type=hosp_type, hosp_name=hosp_name, doct_name=doct_name,
            min_date=min_date, max_date=max_date, tot_dur=tot_dur, duration=duration,
            the_cols = the_cols, the_vals = the_vals,
            the_graph_multiple=the_graph_multiple,
            fig_multi=fig_multi,
        )
    except Exception as e:
        print('@@@@@@',e)
        return redirect(url_for("func_crm_doctors"))

@app.route('/google_trends', methods=['GET', 'POST'])
# @oauth2.required
def google_trends():
    pytrends = TrendReq()
    the_search1 = 'south_korea'
    the_search3 = 'united_states'
    the_search4 = 'canada'
    the_search5 = 'united_kingdom'
    the_search6 = 'germany'
    the_search7 = 'france'
    the_search2 = 'japan'
    the_search8 = 'taiwan'
    the_search9 = 'singapore'

    df1 = pytrends.trending_searches(pn=str(the_search1))
    df2 = pytrends.trending_searches(pn=str(the_search2))
    df3 = pytrends.trending_searches(pn=str(the_search3))
    df4 = pytrends.trending_searches(pn=str(the_search4))
    df5 = pytrends.trending_searches(pn=str(the_search5))
    df6 = pytrends.trending_searches(pn=str(the_search6))
    df7 = pytrends.trending_searches(pn=str(the_search7))
    df8 = pytrends.trending_searches(pn=str(the_search8))
    df9 = pytrends.trending_searches(pn=str(the_search9))

    thus = pd.concat([df1.rename({0:the_search1}, axis = 1),
                    df3.rename({0:the_search3}, axis = 1), df4.rename({0:the_search4}, axis = 1),
                    df5.rename({0:the_search5}, axis = 1), df6.rename({0:the_search6}, axis = 1),
                    df7.rename({0:the_search7}, axis = 1),df2.rename({0:the_search2}, axis = 1),
                      df8.rename({0:the_search8}, axis = 1),
                    df9.rename({0:the_search9}, axis = 1), ], axis = 1)
    for col in thus.columns:
        thus[col] = ['''<a  target='_blank' href = 'https://www.google.com/search?q="'''+str(i)+''''">'''+str(i)+'''</a>''' for i in thus[col].values]
    thus['rank'] = [i for i in range(1,len(thus)+1)]
    thus = thus[['rank'] + [i for i in thus.columns[:-1]]]
    country_map = {
        'south_korea':'KOREA',
        'japan': 'JAPAN',
        'united_states':'USA',
        'canada':'CANADA',
        'united_kingdom':'UK',
        'germany':'GERMANY',
        'italy':'ITALY',
        'france': 'FRANCE',
        'taiwan':'TAIWAN',
        'singapore':'SINGAPORE',
    }
    thus.columns = [country_map[i] if i in country_map else i for i in thus.columns]
    main_title = "Dashboard - Google Trends"

    the_date = "as of Now"
    data_resource = "Data Source : Google Trends"
    return render_template(
        "pages/google_trend.html",
        main_title = main_title, the_date = the_date, data_resource = data_resource,
        column_names11=thus.columns.values, row_data11= thus.values.tolist(), zip=zip)
