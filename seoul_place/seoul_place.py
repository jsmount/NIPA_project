from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import math

# 데이터 프레임 초기화
df = pd.DataFrame(columns=['name', 'location', 'tags'])

# 카테고리 ID 목록
spot_ls =[ 
    "3f36ca4b-6f45-45cb-9042-265c96a4868c",  # tour_spot
    "651c5b95-a5b3-11e8-8165-020027310001",  # culture_spot
    "e6875575-2cc2-43ba-9651-28d31a7b3e23",  # reports_spot
    "0f29b431-75ac-4ab4-a892-b247d516b31d",  # shopping_spot
    "2d4f4e06-2d37-4e54-ad5c-172add6e6680",  # indoor_spot
    "23bc02b8-da01-41bf-8118-af882436cd3c",  # activity_spot
    "d3fd4d9f-fbd4-430f-b5d5-291b4d9920be",  # historical_spot
    "c24d515f-3202-45e5-834e-1a091901aeff"   # nature_spot
]


def clickTags(page, loc_id):
    button = page.find_element(By.ID, loc_id)
    button.click()

def getLastPageIndex(page):
    totalCnt = page.find_element(By.ID, 'totalCnt').text
    print(totalCnt)
    lastIndex = math.ceil(int(totalCnt.replace(',', '')) / 10)
    return lastIndex

def clickNextPage(page, index):
    try:
        if (index % 5 == 0):
            button = page.find_element(By.CSS_SELECTOR, 'a.btn_next')
            button.click()
        else:
            page_box = page.find_element(By.CSS_SELECTOR, '#contents > div.wrap_contView.clfix > div.box_leftType1 > div.page_box')
            button = page_box.find_element(By.ID, str(index + 1))
            button.click()
    except Exception as ex:
        print(ex)

def eachPageInfo(page):
    info = page.find_elements(By.CSS_SELECTOR, "ul.list_thumType.place > li") # 한 페이지의 모든 장소 정보
    print(f"Found {len(info)} places on the page")  # 디버깅용 출력
    df_new = pd.DataFrame(columns=['name', 'location', 'tags'])  # 데이터프레임 초기화

    for i in info:
        try:
            name = i.find_element(By.CSS_SELECTOR, "div.tit").text  # 장소 이름
            location = i.find_element(By.CSS_SELECTOR, "p").text.split('서울 ')[1]  # 장소 위치
            tag = i.find_element(By.CSS_SELECTOR, "p.tag").text  # 태그
            df_new = pd.concat([df_new, pd.DataFrame({'name': [name], 'location': [location], 'tags': [tag]})], ignore_index=True)
        except Exception as ex:
            print(f"Error processing place: {ex}")
    return df_new


def main():
    global df  # 전역 변수 df 사용
    url = "https://korean.visitkorea.or.kr/list/ms_list.do?areacode=1"
    driver = wd.Chrome()
    driver.get(url)
    sleep(3)

    try:
        for i in spot_ls:
            clickTags(driver, i)
            sleep(3)
            last_page = getLastPageIndex(driver)
            for j in range(1, last_page + 1):
                sleep(1)
                df_new = eachPageInfo(driver)
                df_new['category'] = spot_ls.index(i) + 1  # 카테고리 추가
                df = pd.concat([df, df_new], ignore_index=True)
                if j < last_page:
                    clickNextPage(driver, j)
                print(f"Category: {i}, Last Page: {last_page}, Current Page: {j}")
            clickTags(driver, i)
            sleep(5)
        return df
    except Exception as ex:
        print(ex)
        return df
    


if __name__ == '__main__':
    result = main()  
    # 'category' 컬럼이 추가되었는지 확인 후 출력
    if 'category' in result.columns:
        result = result[['name', 'location', 'category', 'tags']]
    else:
        print("Error: 'category' column is missing.")

    result = result.drop_duplicates(subset='name', keep='first')
    result.to_csv('./seoul_place.csv', index=False, header=True)
