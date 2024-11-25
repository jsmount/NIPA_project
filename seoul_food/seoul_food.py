from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def switch_left(driver):
    ############## iframe으로 왼쪽 포커스 맞추기 ##############
    driver.switch_to.parent_frame()
    iframe = driver.find_element(By.XPATH,'//*[@id="searchIframe"]')
    driver.switch_to.frame(iframe)
    
def switch_right(driver):
    ############## iframe으로 오른쪽 포커스 맞추기 ##############
    driver.switch_to.parent_frame()
    iframe = driver.find_element(By.XPATH,'//*[@id="entryIframe"]')
    driver.switch_to.frame(iframe)

# 크롬 드라이버 실행
driver = webdriver.Chrome()

# 네이버 지도 페이지 열기
driver.get("https://map.naver.com/v5/search/서울%20맛집")

# 페이지 로딩 대기
time.sleep(3)

# 1. iframe 전환 (로딩 확인 후)
try:
    # iframe 로딩 대기
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "searchIframe"))
    )
    print("iframe 로드 완료")
    driver.switch_to.frame(iframe)
    print("iframe 전환 완료")
except Exception as e:
    print(f"iframe 전환 중 오류 발생: {e}")

# 2. 필터 버튼 클릭 (전체 필터)
try:
    filter_button = driver.find_element(By.CSS_SELECTOR, "a.T46Lb.pTP9T.LXtsf")
    print("필터 버튼 찾음")
    filter_button.click()
    time.sleep(1)
    print("필터 버튼 클릭 완료")
except Exception as e:
    print(f"필터 버튼 클릭 중 오류 발생: {e}")

# 3. 저장많은 버튼 클릭
try:
    save_most_button = driver.find_element(By.XPATH, "//a[@class='qP6uz SbSKx' and contains(text(), '저장많은')]")
    print("저장많은 버튼 찾음")
    save_most_button.click()
    time.sleep(1)
    print("저장많은 버튼 클릭 완료")
except Exception as e:
    print(f"저장많은 버튼 클릭 중 오류 발생: {e}")

# 4. 검색 버튼 클릭 (결과보기)
try:
    search_button = driver.find_element(By.CSS_SELECTOR, "a.GZe5x.Mj_l3")
    print("검색 버튼 찾음")
    search_button.click()
    time.sleep(3)  # 페이지가 로딩될 때까지 대기
    print("검색 버튼 클릭 완료")
except Exception as e:
    print(f"검색 버튼 클릭 중 오류 발생: {e}")

# 저장할 파일 경로 설정
output_file = "./seoul_food.csv"

# 이미 파일이 존재한다면 이어서 저장 (기존 데이터 읽기)
if os.path.exists(output_file):
    seoul_food = pd.read_csv(output_file)
else:
    seoul_food = pd.DataFrame(columns=['name', 'category', 'rating', 'address', 'link'])
print(seoul_food)
while True:
    switch_left(driver=driver)

    # 페이지 버튼 상태 확인
    next_page = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div[3]/div[2]/a[7]').get_attribute('aria-disabled')

    # 스크롤 끝까지 내리기
    scrollable_element = driver.find_element(By.CLASS_NAME, "Ryr1F")
    last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)

    while True:
        driver.execute_script("arguments[0].scrollTop += 600;", scrollable_element)
        sleep(1)
        new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)
        if new_height == last_height:
            break
        last_height = new_height

    # 현재 페이지 번호 가져오기
    page_no = driver.find_element(By.XPATH, '//a[contains(@class, "mBN2s qxokY")]').text
    elemets = driver.find_elements(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]//li')

    for index, e in enumerate(elemets, start=1):
        store_name, category, rating, address = '', '', 0.0, ''

        if str(e) in seoul_food['link'].values:
            print(f"이미 존재하는 링크: {e}, 건너뜁니다.")
            continue  # 아래 try-finally 블록을 건너뛰고 다음 e로 이동

        try:
            # 순서대로 값 클릭
            e.find_element(By.CLASS_NAME, 'CHC5F').find_element(By.XPATH, ".//a/div/div/span").click()
            sleep(2)
            switch_right(driver=driver)

            # 데이터 추출
            title = driver.find_element(By.XPATH, '//div[@class="zD5Nm undefined"]')
            store_name = title.find_element(By.XPATH, './/div[1]/div[1]/span[1]').text
            category = title.find_element(By.XPATH, './/div[1]/div[1]/span[2]').text

            rating_xpath = f'.//div[2]/span[1]'
            rating_element = title.find_element(By.XPATH, rating_xpath)
            rating = rating_element.text.replace("\n", " ")
            address = driver.find_element(By.XPATH, '//span[@class="LDgIH"]').text

            print([store_name, category, rating, address])

            # DataFrame에 추가
            seoul_food.loc[len(seoul_food)] = [store_name, category, rating, address, e]
            
        except Exception as data_error:
            print(f"데이터 추출 중 오류 발생: {data_error}")
        
        finally:
            switch_left(driver=driver)

    # 페이지 저장
    seoul_food.to_csv(output_file, index=False)
    print(f"현재까지 크롤링한 데이터 저장 완료: {output_file}")

    # 다음 페이지로 이동
    if next_page == 'false':
        driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div[3]/div[2]/a[7]').click()
        sleep(2)
    else:
        print("크롤링 완료")
        break

# 마지막 저장
seoul_food.to_csv(output_file, index=False)
print(f"최종 데이터 저장 완료: {output_file}")