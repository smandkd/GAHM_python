# ====================================================
# 관측소 번호 : 47929 -> 오키나와현 쿠메지마 
# 데이터 속성 : 
# '날짜 및 시간','현지기압(hPa)','해수면기압(hPa)','강수량(mm)','기온(degreeC)','이슬점온도(degreeC)','증기압(hPa)','습도(%)','풍속(m/s)','풍향','햇빛시간(h)','전천일사량(MJ/m^2)','강설','적설','날씨','구름량','시정(km)'
# 기간 2000/01/01 ~ 2023/12/31 
# 시간 간격 : 1시간 
# ====================================================
#%%
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import pandas as pd
import csv
from datetime import datetime, timedelta
import calendar
#%%
# 네트워크 요청 세션 설정
session = requests.Session()
retry = Retry(connect=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# 데이터를 저장할 CSV 파일 열기
with open('/home/tkdals/web_crowlling/JMAdata_yonaguni.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    # CSV 파일에 헤더 추가
    writer.writerow(['날짜 및 시간','현지기압(hPa)','해수면기압(hPa)','강수량(mm)','기온(degreeC)','이슬점온도(degreeC)','증기압(hPa)','습도(%)','풍속(m/s)','풍향','햇빛시간(h)','전천일사량(MJ/m^2)','강설','적설','날씨','구름량','시정(km)'])

    # 데이터 수집을 위한 날짜 범위 설정
    start_date = datetime(2000, 1, 1)
    end_date = datetime(2023, 12, 31)
    current_date = start_date
    
    while current_date <= end_date:
        print(f'Append {current_date} data to ')
        year = current_date.year
        month = current_date.month
        _, last_day = calendar.monthrange(year, month)  # 해당 월의 마지막 날 계산

        for day in range(1, last_day + 1):
            # 웹 페이지 URL
            url = f"https://www.data.jma.go.jp/obd/stats/etrn/view/hourly_s1.php?prec_no=91&block_no=47912&year={year}&month={month}&day={day}&view="
            
            # 웹 페이지 내용 가져오기
            try:
                response = session.get(url)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')

                # id='tablefix1'인 테이블 찾기
                table = soup.find('table', id='tablefix1')
                if table:
                    rows = table.find_all('tr')

                    # rows[2]부터 마지막 행까지 데이터를 추출하여 리스트에 추가
                    for row in rows[2:]:
                        cols = row.find_all('td')
                        cols = [col.get_text(strip=True) for col in cols]
                        if cols:
                            hour = cols[0]  # 첫 번째 열은 시간
                            datetime_str = f"{year}-{month:02d}-{day:02d} {int(hour):02d}:00"
                            cols[0] = datetime_str  # 날짜 및 시간으로 대체
                            writer.writerow(cols)

            except requests.exceptions.RequestException as e:
                print(f"데이터를 가져오는 중 오류 발생: {e}")

        # 다음 달로 이동
        if month == 12:
            current_date = datetime(year + 1, 1, 1)
        else:
            current_date = datetime(year, month + 1, 1)

print("모든 날짜의 데이터가 JMAdata_full.csv 파일에 저장되었습니다.")
# %%
