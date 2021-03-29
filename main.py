from selenium import webdriver
from bs4 import BeautifulSoup
import time


class Post:
    def __init__(self, url, page_query, post_xpath):
        self.url = url
        self.page_query = page_query
        self.post_xpath = post_xpath

    def get_page_url(self, num: int) -> str:
        return self.url + self.page_query + str(num)

    def get_post_title(self, title_tag: str, num: int) -> str:
        result = (self.post_xpath % (num)) + title_tag
        print(result)
        return result

    def get_post_xpath(self, num: int) -> str:
        result = (self.post_xpath % (num))
        return result


URLS = []
URLS.append(Post('https://www.bizinfo.go.kr/see/seea/selectSEEA100.do', '?pageIndex=', """//*[@id="content"]/div[3]/div[2]/table/tbody/tr[%d]/td[2]/a"""))
PAGE_LIMIT = 10
WAIT_SEC = 3
page_num = 3

if __name__ == '__main__':
    driver = webdriver.Chrome('./driver/chromedriver')
    driver.implicitly_wait(WAIT_SEC)

    driver.get(URLS[0].url)

    for page_num in range(1, 2):
        driver.get(URLS[0].get_page_url(page_num))
        for post_num in range(1, 21):
            title = driver.find_element_by_xpath(URLS[0].get_post_title("/span", post_num))
            if title.text.find('창업') != -1:
                print(title.text)

            #driver.find_element_by_xpath(URLS[0].get_post_xpath(post_num)).click()
            #html = driver.page_source
            #print(html)
