import os
from selenium import webdriver
from bs4 import BeautifulSoup
import time


class Post:
    def __init__(self, url, page_query, post_xpath, post_limit):
        self.url = url
        self.page_query = page_query
        self.post_xpath = post_xpath
        self.post_limit = post_limit

    def get_page_url(self, num: int) -> str:
        return self.url + self.page_query + str(num)

    def get_post_title(self, title_tag: str, num: int) -> str:
        result = (self.post_xpath % (num)) + title_tag
        # print(result)
        return result

    def get_post_xpath(self, num: int) -> str:
        result = (self.post_xpath % (num))
        return result


URLS = []
URLS.append(Post(url='https://www.bizinfo.go.kr/see/seea/selectSEEA100.do',
                 page_query='?pageIndex=',
                 post_xpath="""//*[@id="content"]/div[3]/div[2]/table/tbody/tr[%d]/td[2]/a""",
                 post_limit=20))
PAGE_LIMIT = 1
WAIT_SEC = 1

if __name__ == '__main__':
    driver = webdriver.Chrome('./driver/chromedriver')

    for page_num in range(1, PAGE_LIMIT+1):
        driver.get(URLS[0].get_page_url(page_num))
        time.sleep(WAIT_SEC)
        for post_num in range(1, URLS[0].post_limit+1):
            title = driver.find_element_by_xpath(URLS[0].get_post_title("/span", post_num)).text
            if title.find('창업') != -1:  # 키워드 기반 필터링
                # 키워드가 존재하면
                driver.find_element_by_xpath(URLS[0].get_post_xpath(post_num)).click()
                time.sleep(WAIT_SEC)
                if not os.path.isfile("./crawled/" + title + ".txt"):
                    with open("./crawled/"+title+".txt", "w", encoding='UTF8') as f:
                        f.write(driver.page_source)
                driver.back()
                time.sleep(WAIT_SEC)

    file_list = os.listdir("./crawled")
    for file_name in file_list:
        with open("./crawled/"+file_name, "r", encoding='UTF8') as f:
            html = f.read()
        soup = BeautifulSoup(html, 'html.parser')