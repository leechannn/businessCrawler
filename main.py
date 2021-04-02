import os

import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
import time


class Post:
    def __init__(self, page_type=0, page_start=1, url='', next_page='', post_xpath='', post_title_ends='', more_page_xpath='', more_page_xpath_offset='', post_limit=10, page_sub_limit=10, page_offset=2, page_offset_start=1):
        self.page_type = page_type
        self.page_start = page_start
        self.url = url
        self.next_page = next_page
        self.post_xpath = post_xpath
        self.more_page_xpath = more_page_xpath
        if more_page_xpath_offset == '':
            self.more_page_xpath_offset = more_page_xpath
        else:
            self.more_page_xpath_offset = more_page_xpath_offset
        self.post_title_ends = post_title_ends
        self.post_limit = post_limit
        self.page_sub_limit = page_sub_limit
        self.page_offset = page_offset
        self.page_offset_start = page_offset_start

    def get_page_url(self, num: int) -> str:
        return self.url + self.next_page + str(num)

    def get_page_xpath(self, num: int) -> str:
        result = self.next_page % (num)
        return result

    def get_post_title(self, title_tag: str, num: int) -> str:
        result = (self.post_xpath % (num)) + title_tag
        return result

    def get_post_xpath(self, num: int) -> str:
        result = (self.post_xpath % (num))
        return result


URLS = []
URLS.append(Post(page_type=0,
                 url='https://www.bizinfo.go.kr/see/seea/selectSEEA100.do',
                 next_page='?pageIndex=',
                 post_xpath="""//*[@id="content"]/div[3]/div[2]/table/tbody/tr[%d]/td[2]/a""",
                 post_title_ends='/span',
                 more_page_xpath='//*[@id="paging_div"]/a[12]',
                 post_limit=20))
'''

URLS.append(Post(page_type=1,
                 url='https://www.k-startup.go.kr/common/announcement/announcementList.do?mid=30004&bid=701&searchAppAt=A',
                 next_page="""//*[@id="btn_listAll"]""",
                 post_xpath="""/html/body/div[1]/div[6]/form/div[2]/div[3]/ul[1]/li[%d]/h4/a""",
                 more_page_xpath='@@@@@here@@@@@@@@'
                 post_limit=20))
URLS.append(Post(page_type=0,
                 url='https://www.sdm.go.kr/news/notice/notice.do',
                 next_page="""//*[@id="frm"]/div[2]/a[%d]""",
                 post_xpath="""//*[@id="frm"]/table/tbody/tr[%d]/td[2]/a""",
                 more_page_xpath='//*[@id="frm"]/div[2]/a[11]',
                 more_page_xpath_offset='//*[@id="frm"]/div[2]/a[13]',
                 page_offset_start=11))
'''
PAGE_LIMIT = 30
WAIT_SEC = 1


def get_page_num(num: int) -> int:
    result = num % 10
    if not result:
        result = 10
    return result


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

    driver.get(URL.url)
    for page_num in range(URL.page_start, PAGE_LIMIT + 1):
        next_page_num = get_page_num(page_num)
        #print("page_num : " + str(page_num) + ", next_page_num : " + str(next_page_num))
        if "//*" in URL.next_page:
            if URL.page_offset_start <= page_num:
                driver.find_element_by_xpath(URL.get_page_xpath(next_page_num+URL.page_offset)).click()
            else:
                driver.find_element_by_xpath(URL.get_page_xpath(next_page_num)).click()
        else:
            driver.get(URL.get_page_url(page_num))
        time.sleep(WAIT_SEC)
        for post_num in range(1, URL.post_limit + 1):
            title = driver.find_element_by_xpath(URL.get_post_title(URL.post_title_ends, post_num)).text
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
        if next_page_num == 10 and "//*" in URL.next_page:
            if URL.page_offset_start <= page_num:
                driver.find_element_by_xpath(URL.more_page_xpath_offset).click()
            else:
                driver.find_element_by_xpath(URL.more_page_xpath).click()
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

    for post_num in range(1, URL.post_limit + 1):
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

