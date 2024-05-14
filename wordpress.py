from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv

# load .env
load_dotenv()

# 옵션 설정
options = Options()
# 사용자 에이전트 변경
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36")
# 자동화 소프트웨어로 인식되는 것을 방지하기 위한 설정
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# 크롬 드라이버 서비스 설정
service = Service('/home/pori/chromedriver-linux64/chromedriver')
browser = webdriver.Chrome(service=service, options=options)

post_url = os.environ.get('post_url')
browser.get(post_url)

# 로그인 폼 입력
username = os.environ.get('username')  # 사용자 이름 입력
password = os.environ.get('password')  # 비밀번호 입력

# 사용자 이름 입력
username_field = browser.find_element(By.ID, 'user_login')
username_field.send_keys(username)

time.sleep(1)

# 비밀번호 입력
password_field = browser.find_element(By.ID, 'user_pass')
password_field.send_keys(password)

# 로그인 버튼 클릭
login_button = browser.find_element(By.ID, 'wp-submit')
login_button.click()

# 현재 날짜 및 시간을 가져옵니다.
now = datetime.now()
date_string = now.strftime("%Y-%m-%d")  # 날짜를 YYYY-MM-DD 형식의 문자열로 변환합니다.

# API 키
weather_api_key = os.environ.get('weather_api_key')
news_api_key = os.environ.get('news_api_key')

# 도시 목록
cities = {'Seoul': '서울'}

# 영어 설명과 한글 설명 매핑
weather_desc_mapping = {
    'Thunderstorm': '천둥번개',
    'Drizzle': '이슬비',
    'Rain': '비',
    'Snow': '눈',
    'Clear': '맑음',
    'Clouds': '구름',
    'Mist': '안개',
    'Smoke': '연기',
    'Haze': '안개',
    'Dust': '먼지',
    'Fog': '안개',
    'Sand': '모래',
    'Dust': '먼지',
    'Ash': '재',
    'Squall': '돌풍',
    'Tornado': '토네이도'
}

# 현재 시간
current_time = datetime.now()

# 오늘 날짜의 시작 시각
start_of_today = current_time.replace(hour=0, minute=0, second=0, microsecond=0)

# 현재 시간부터 오늘 자정까지의 시간 리스트 생성 (3시간 간격)
forecast_times = [start_of_today + timedelta(hours=i) for i in range(0, 24, 3)]

# 현재 시간부터 오늘 자정까지의 시간 문자열 리스트 생성
forecast_time_strings = [time.strftime("%Y-%m-%d %H:%M:%S") for time in forecast_times]

# 현재 시간별 날씨 정보를 가져와 출력
weather_info = ""
for city, korean_city in cities.items():
    # API 엔드포인트 URL
    weather_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weather_api_key}&units=metric'

    # API에 요청을 보냄
    response = requests.get(weather_url)

    # 응답 데이터를 JSON 형식으로 파싱
    data = response.json()

    # 날씨 정보 출력
    if data['cod'] == '200':
        city_title = (f"{korean_city} 날씨:")
        for forecast in data['list']:
            dt_txt = forecast['dt_txt']  # 시간대 정보
            if dt_txt in forecast_time_strings:
                weather_desc = forecast['weather'][0]['main']  # 날씨 설명
                temp = forecast['main']['temp']  # 온도
                humidity = forecast['main']['humidity']  # 습도

                # 한글로 변환된 날씨 설명 출력
                korean_weather_desc = weather_desc_mapping.get(weather_desc, weather_desc)

                # 시간대, 날씨 설명, 온도, 습도 출력
                weather_info += f" {dt_txt}, 날씨: {korean_weather_desc}, 온도: {temp} °C, 습도: {humidity}%\n"
    else:
        city_title = (f"{korean_city} 날씨 정보를 가져오지 못했습니다.")

# 블록체인, 크립토, 비트코인 관련 뉴스 가져오기
def get_crypto_news(news_api_key):
    # News API의 키워드 검색 엔드포인트 URL
    news_url = f"https://newsapi.org/v2/everything"

    # 요청 파라미터 설정
    params = {
        "q": "블록체인 OR 크립토 OR 비트코인 OR 코인",  # 키워드 검색
        "apiKey": news_api_key  # News API 액세스 키
    }

    # API 요청 보내기
    response = requests.get(news_url, params=params)

    # 응답 데이터를 JSON 형식으로 파싱
    data = response.json()

    # 뉴스 정보 출력
    if response.status_code == 200:
        articles = data.get("articles", [])
        news_info = "블록체인 관련 뉴스:\n"
        for article in articles[:10]:
            news_info += f"제목: {article['title']}\n"
            news_info += f"{article['description']}\n"
        
        return news_info
    else:
        return "블록체인 관련 뉴스를 가져오지 못했습니다."

print("블록체인 관련 뉴스 가져오기 시작...")
crypto_news = get_crypto_news(news_api_key)

# 상위 10개 암호화폐를 가져오는 함수
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    crypto_info = "시가총액 상위 10개 코인 정보:\n"
    for coin in data:
        crypto_info += f"{coin['name']} (기호: {coin['symbol'].upper()}): 시가총액: ${coin['market_cap']:,.0f}, 가격: ${coin['current_price']:,.2f}, 24시간 변동률: {coin['price_change_percentage_24h']:.2f}%\n"
    return crypto_info

# 함수 호출 및 데이터 가져오기
top_crypto_data = fetch_crypto_data()

# 게시글 제목과 내용 입력
title = (date_string + "날씨정보 블록체인 뉴스")
content = crypto_news + top_crypto_data + weather_info

time.sleep(1)  # 페이지 로딩 대기
browser.find_element(By.CLASS_NAME, 'wp-block').send_keys(title) 
time.sleep(1)
browser.find_element(By.CLASS_NAME, 'block-editor-default-block-appender__content').send_keys(content)  # 내용 입력

# 게시글 발행
time.sleep(2)  # 입력 지연
publish_button = browser.find_element(By.CLASS_NAME, 'editor-post-publish-panel__toggle')
browser.execute_script("arguments[0].scrollIntoView(true);", publish_button)  # 발행 버튼으로 스크롤

# publish_button.click()
# time.sleep(1)
# publish_button = browser.find_element(By.CLASS_NAME, 'editor-post-publish-button')
# publish_button.click()

# 웹 페이지가 열려 있는 동안 확인 가능
input("Press Enter to exit...")  # 사용자가 엔터를 누를 때까지 대기 
