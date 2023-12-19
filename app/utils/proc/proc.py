def custom_format(s):
    try:
        num = float(s)
        return "{:.0f}".format(num) if num.is_integer() else "{:.2f}".format(num)
    except Exception:
        return str(s)

def format_hover_list(hosp_list):
    # 5개씩 나눠서 줄바꿈 문자를 추가합니다.
    return '<br>'.join([', '.join(hosp_list[i:i+10]) for i in range(0, len(hosp_list), 5)])

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
