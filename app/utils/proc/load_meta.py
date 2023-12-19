from gspread_dataframe import get_as_dataframe
from app.utils.constant import env
import folium

def GET_THE_DATA(the_sheet):
    #### 구글 드라이브 접근 폴더 설정

    the_url = "https://docs.google.com/spreadsheets/d/1JmgbWtcxE0jbVO2l_dpQkNW24gupjMklD-R0rbOfa7o/edit#gid=474282581"
    sh = env.gc.open_by_url(the_url)
    df = get_as_dataframe(sh.worksheet(str(the_sheet)))
    df = df[[i for i in df.columns if 'Unn' not in i]]
    df = df.dropna(subset=[df.columns[0]])
    return df
def GET_META_DATA_BY(the_sheet):
    df = get_as_dataframe(env.sh.worksheet(str(the_sheet)))
    df = df[[i for i in df.columns if 'Unn' not in i]]
    df = df.dropna(subset=[df.columns[0]])
    return df

def GET_DASHBOARD_DATA(the_sheet):
    df = get_as_dataframe(env.sh.worksheet(str(the_sheet)))
    df = df[[i for i in df.columns if 'Unn' not in i]]
    return df

def GET_XAXES_LABEL(df_week):
    yr_lst = []
    wk_lst = []
    for i in df_week['prsc_week']:
        yr = i.split("-")[0]
        wk = i.split("-")[1]

        if yr not in yr_lst:
            yr_lst.append(yr)
        else:
            yr_lst.append('')
        wk_lst.append(wk)

    lst = []
    for i,j in zip(yr_lst, wk_lst):
        lst.append(j+'\n'+i)
    return lst

def GET_THE_LOCATION(the_sheet):
    df_meta = get_as_dataframe(env.sh.worksheet(str(the_sheet)))
    df_meta = df_meta[[i for i in df_meta.columns if 'Unn' not in i]]
    df_meta = df_meta.dropna(subset=['hospital'])
    return df_meta

def GET_ACTIVE_MAP(df_meta, the_hospital):
    try:
        df_meta = df_meta[df_meta['hospital'] == str(the_hospital)]
        lat = df_meta['lat'].values[0]
        lon = df_meta['lon'].values[0]
        the_map = folium.Map(location=[lat, lon],
                             zoom_start=13,
                             )
        folium.Marker(
            location=[lat, lon],
            popup=the_hospital,
            tooltip=the_hospital,
            radius=2,
        ).add_to(the_map)
        the_map.get_root().width = "400px"
        the_map.get_root().height = "400px"
    except Exception:
        the_map = folium.Map(location=[36, 127],
                            zoom_start=6,
                            )

        the_map.get_root().width = "400px"
        the_map.get_root().height = "400px"
    return the_map.get_root()._repr_html_()