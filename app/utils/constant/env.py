from oauth2client.service_account import ServiceAccountCredentials
import gspread

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

#### 구글 드라이브 접근 폴더 설정
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

#### 구글 드라이브 credential 및 상호 수신 확인
credentials = ServiceAccountCredentials.from_json_keyfile_dict(json_file_name, scope)
gc = gspread.authorize(credentials)

the_url = "https://docs.google.com/spreadsheets/d/1cVyI-MQ7xVWqO3QGCKTF5KT3DvIQKisyskeZ4b33T6U/edit#gid=1152818663"
# the_url = "https://docs.google.com/spreadsheets/d/1JmgbWtcxE0jbVO2l_dpQkNW24gupjMklD-R0rbOfa7o/edit#gid=474282581"
sh = gc.open_by_url(the_url)
