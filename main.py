import os

import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
import time


class Post:
    def __init__(self, page_type, post_start, url, next_page, post_xpath, post_limit):
        self.page_type = page_type
        self.post_start = post_start
        self.url = url
        self.next_page = next_page
        self.post_xpath = post_xpath
        self.post_limit = post_limit

    def get_page_url(self, num: int) -> str:
        return self.url + self.next_page + str(num)

    def get_post_title(self, title_tag: str, num: int) -> str:
        result = (self.post_xpath % (num)) + title_tag
        return result

    def get_post_xpath(self, num: int) -> str:
        result = (self.post_xpath % (num))
        return result


URLS = []
'''
URLS.append(Post(page_type=0, 
                 post_start=1
                 url='https://www.bizinfo.go.kr/see/seea/selectSEEA100.do',
                 next_page='?pageIndex=',
                 post_xpath="""//*[@id="content"]/div[3]/div[2]/table/tbody/tr[%d]/td[2]/a""",
                 post_limit=20))
'''
URLS.append(Post(page_type=1,
                 post_start=13,
                 url='https://www.k-startup.go.kr/common/announcement/announcementList.do?mid=30004&bid=701&searchAppAt=A',
                 next_page="""/html/body/div[1]/div[6]/form/div[2]/div[3]/ul[1]/li[14]/h4/a""",
                 post_xpath="""//*[@id="liArea%d"]/h4/a""",
                 post_limit=20))
PAGE_LIMIT = 1
WAIT_SEC = 1


def string_escaping_for_file(string: str) -> str:
    result = string.strip()
    result = result.replace("\\", "")
    result = result.replace("/", "")
    result = result.replace(":", "")
    result = result.replace("*", "")
    result = result.replace("?", "")
    result = result.replace("\"", "")
    result = result.replace("<", "")
    result = result.replace(">", "")
    result = result.replace("|", "")
    return result


def type_page_num(URL: Post):
    global WAIT_SEC
    global driver

    for page_num in range(URL.post_start, PAGE_LIMIT + 1):
        driver.get(URL.get_page_url(page_num))
        time.sleep(WAIT_SEC)
        for post_num in range(1, URL.post_limit + 1):
            title = driver.find_element_by_xpath(URL.get_post_title("/span", post_num)).text
            title = string_escaping_for_file(title)
            if title.find('창업') != -1:  # 키워드 기반 필터링
                # 키워드가 존재하면
                driver.find_element_by_xpath(URL.get_post_xpath(post_num)).click()
                time.sleep(WAIT_SEC)
                if not os.path.isfile("./crawled/" + title + ".txt"):
                    with open("./crawled/" + title + ".txt", "w", encoding='UTF8') as f:
                        f.write(driver.page_source)
                driver.back()
                time.sleep(WAIT_SEC)

    file_list = os.listdir("./crawled")
    for file_name in file_list:
        with open("./crawled/" + file_name, "r", encoding='UTF8') as f:
            html = f.read()
        soup = BeautifulSoup(html, 'html.parser')


def type_more_post(URL: Post):
    global WAIT_SEC
    global driver

    driver.get(URL.url)
    time.sleep(WAIT_SEC)
    '''
    for tmp in range(999):
        try:
            driver.find_element_by_xpath(URL.get_post_xpath(tmp))
        except selenium.common.exceptions.NoSuchElementException as e:
            URL.post_limit = tmp - 1
            break
    '''
    URL.post_limit = 30
    print(URL.post_limit)

    for post_num in range(URL.post_start, URL.post_limit + 1):
        print(post_num)
        title = driver.find_element_by_xpath(URL.get_post_title("", post_num)).text
        title = string_escaping_for_file(title)
        print(title)
        if title.find('창업') != -1:  # 키워드 기반 필터링
            # 키워드가 존재하면
            driver.find_element_by_xpath(URL.get_post_xpath(post_num)).click()
            time.sleep(WAIT_SEC)
            if not os.path.isfile("./crawled/" + title + ".txt"):
                with open("./crawled/" + title + ".txt", "w", encoding='UTF8') as f:
                    f.write(driver.page_source)
            driver.back()
            time.sleep(WAIT_SEC)
'''
    file_list = os.listdir("./crawled")
    for file_name in file_list:
        with open("./crawled/" + file_name, "r", encoding='UTF8') as f:
            html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
'''
if __name__ == '__main__':
    driver = webdriver.Chrome('./driver/chromedriver')

    for URL in URLS:
        if URL.page_type == 0:
            type_page_num(URL)
        elif URL.page_type == 1:
            type_more_post(URL)

