from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# 옵션 설정
options = Options()
# 사용자 에이전트 변경
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36")
# 자동화 소프트웨어로 인식되는 것을 방지하기 위한 설정
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# 사용자 입력을 받습니다.
question = input("Please enter your question:")
content = input("Please enter your content:")

# 크롬 드라이버 서비스 설정
service = Service()
browser = webdriver.Chrome(service=service, options=options)

post_url = ''
browser.get(post_url)

# 로그인 폼 입력
username = ''  # 사용자 이름 입력
password = ''  # 비밀번호 입력

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

# 게시글 제목과 내용 입력
time.sleep(1)  # 페이지 로딩 대기
browser.find_element(By.CLASS_NAME, 'wp-block').send_keys(question) 
time.sleep(1)
browser.find_element(By.CLASS_NAME, 'block-editor-default-block-appender__content').send_keys(content)  # 내용 입력

# 게시글 발행
time.sleep(2)  # 입력 지연
publish_button = browser.find_element(By.CLASS_NAME, 'editor-post-publish-panel__toggle')
browser.execute_script("arguments[0].scrollIntoView(true);", publish_button)  # 발행 버튼으로 스크롤
publish_button.click()
time.sleep(1)
publish_button = browser.find_element(By.CLASS_NAME, 'editor-post-publish-button')
publish_button.click()

# 웹 페이지가 열려 있는 동안 확인 가능
input("Press Enter to exit...")  # 사용자가 엔터를 누를 때까지 대기