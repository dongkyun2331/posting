import requests
import os

# API 키와 요청 URL 설정
api_key = '6d61aad7afd24079bf07e94693c4268d'
url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'

# News API로부터 데이터 요청
response = requests.get(url)
data = response.json()

# 이미지 저장할 디렉토리 생성 (없으면)
if not os.path.exists('downloaded_images'):
    os.makedirs('downloaded_images')

# 최대 10개의 기사 이미지 다운로드
for i, article in enumerate(data['articles'][:10]):
    image_url = article['urlToImage']
    if image_url:  # 이미지 URL이 있는지 확인
        img_data = requests.get(image_url).content
        # 파일로 이미지 저장
        with open(f'downloaded_images/image_{i+1}.jpg', 'wb') as handler:
            handler.write(img_data)
        print(f'Image {i+1} downloaded and saved.')
    else:
        print(f'Image {i+1} not available.')
