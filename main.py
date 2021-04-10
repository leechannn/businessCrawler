import os
from selenium import webdriver
from bs4 import BeautifulSoup
import time


class Post:
    def __init__(self, page_type=0, post_start=1, page_start=1, url='', next_page='', post_xpath='', more_page_xpath='', more_page_xpath_offset='', post_limit=10, page_sub_limit=10, page_offset=2, page_offset_start=1, title='', post_mul_for_url=1, special: list=None):
        self.page_type = page_type
        self.post_start = post_start
        self.page_start = page_start
        self.url = url
        self.next_page = next_page
        self.post_xpath = post_xpath
        self.more_page_xpath = more_page_xpath
        if more_page_xpath_offset == '':
            self.more_page_xpath_offset = more_page_xpath
        else:
            self.more_page_xpath_offset = more_page_xpath_offset
        self.post_limit = post_limit
        self.page_sub_limit = page_sub_limit
        self.page_offset = page_offset
        self.page_offset_start = page_offset_start
        self.title = title
        self.post_mul_for_url = post_mul_for_url
        self.special = special

    def get_page_url(self, num: int) -> str:
        try:
            url1 = self.url.split('/')[2]
            url2 = self.next_page.split('/')[2]
            if url1 != url2:
                return ((self.url + self.next_page) % (num*self.post_mul_for_url))
            else:
                return (self.next_page % (num*self.post_mul_for_url))
        except IndexError as e:
            return ((self.url + self.next_page) % (num*self.post_mul_for_url))

    def get_page_xpath(self, num: int) -> str:
        result = self.next_page % (num)
        return result

    def get_special_xpath(self, num: int) -> str:
        result = self.special[0] % (num)
        return result


URLS = []
URLS.append(Post(page_type=1,  #이거 안됨
                 url='https://www.k-startup.go.kr/common/announcement/announcementList.do?mid=30004&bid=701&searchAppAt=A',
                 next_page='//*[@id="btn_listAll"]',
                 post_xpath='/html/body/div[1]/div[6]/form/div[2]/div[3]/ul[1]/li[%d]/h4/a',
                 more_page_xpath='@@@@@here@@@@@@@@',
                 post_limit=20))
'''
URLS.append(Post(page_type=0,
                 url='https://www.bizinfo.go.kr/see/seea/selectSEEA100.do',
                 next_page='?pageIndex=%d',
                 post_xpath='//*[@id="content"]/div[3]/div[2]/table/tbody/tr[%d]/td[2]/a',
                 post_limit=20))
URLS.append(Post(page_type=0,
                 url='https://www.sdm.go.kr/news/notice/notice.do',
                 next_page='//*[@id="frm"]/div[2]/a[%d]',
                 post_xpath='//*[@id="frm"]/table/tbody/tr[%d]/td[2]/a',
                 more_page_xpath='//*[@id="frm"]/div[2]/a[11]',
                 more_page_xpath_offset='//*[@id="frm"]/div[2]/a[13]',
                 page_offset_start=11))
URLS.append(Post(page_type=2,
                 url='https://kbinnovationhub.com/apply/',
                 title='KB이노베이션 허브'))
URLS.append(Post(page_type=0,
                 post_start=2,
                 url='https://www.bi.go.kr/board/list.do?boardID=RECRUIT&pager.offset=0&frefaceCode=ANNOUNCE',
                 next_page='https://www.bi.go.kr/board/list.do?boardID=RECRUIT&pager.offset=%d&frefaceCode=ANNOUNCE',
                 post_xpath='//*[@id="boardFormVO"]/div[2]/div[2]/div/table/tbody/tr[%d]/td[4]/a',
                 post_limit=16,
                 post_mul_for_url=15))
URLS.append(Post(page_type=0,
                 url='https://sbsc.seoul.go.kr/fe/support/seoul/NR_list.do?bbsCd=1',
                 next_page='&bbsSeq=&currentPage=%d&searchVals=&bbsGrpCds_all=on&orgCd=',
                 post_xpath='//*[@id="container"]/div/div[2]/table/tbody/tr[%d]/td[2]/a'))
URLS.append(Post(page_type=0,
                 url='https://youthhub.kr/hub/category/notice',
                 next_page='/page/%d',
                 post_xpath='//*[@id="main-content"]/div/div[4]/div/div/div[1]/div/div[%d]/div/div[2]/h2/a',
                 post_limit=12))
URLS.append(Post(page_type=0,  # 각 페이지 첫번째 게시물 처리 필요
                 url='https://agro.seoul.go.kr/archives/category/institution_c1/institution_news_c1/institution_news_gosi-n2',
                 next_page='/page/%d',
                 post_xpath='//*[@id="child_policyUL"]/li[%d]/a',
                 post_limit=9,
                 special=['/html/body/div[3]/div[3]/div[2]/div[%d]/div[2]/span[1]/a', '3', '3']))
'''


PAGE_LIMIT = 20
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


def crawl_post(post_start, post_limit, post_xpath, keyword):
    global driver
    for post_num in range(post_start, post_limit + 1):
        title = driver.find_element_by_xpath(post_xpath % (post_num)).text
        title = string_escaping_for_file(title)
        print(title)
        if title.find(keyword) != -1:  # 키워드 기반 필터링
            # 키워드가 존재하면
            driver.find_element_by_xpath(post_xpath % (post_num)).click()
            time.sleep(WAIT_SEC)
            if not os.path.isfile("./crawled/" + title + ".txt"):
                with open("./crawled/" + title + ".txt", "w", encoding='UTF8') as f:
                    f.write(driver.page_source)
            driver.back()
            time.sleep(WAIT_SEC)


def type_page_num(URL: Post):
    global WAIT_SEC
    global driver

    driver.get(URL.url)
    for page_num in range(URL.page_start, PAGE_LIMIT + 1):
        next_page_num = get_page_num(page_num)
        # print("page_num : " + str(page_num) + ", next_page_num : " + str(next_page_num))
        if "//*" in URL.next_page:
            if URL.page_offset_start <= page_num:
                driver.find_element_by_xpath(URL.get_page_xpath(next_page_num+URL.page_offset)).click()
            else:
                driver.find_element_by_xpath(URL.get_page_xpath(next_page_num)).click()
        else:
            driver.get(URL.get_page_url(page_num))
        time.sleep(WAIT_SEC)
        if URL.special:
            crawl_post(int(URL.special[1]), int(URL.special[2]), URL.special[0], '창업')
        crawl_post(URL.post_start, URL.post_limit, URL.post_xpath, '창업')
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
        title = driver.find_element_by_xpath(URL.post_xpath % (post_num)).text
        title = string_escaping_for_file(title)
        print(title)
        if title.find('창업') != -1:  # 키워드 기반 필터링
            # 키워드가 존재하면
            driver.find_element_by_xpath(URL.post_xpath % (post_num)).click()
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


def type_one_page(URL: Post):
    global WAIT_SEC
    global driver

    driver.get(URL.url)
    time.sleep(WAIT_SEC)
    if not os.path.isfile("./crawled/" + URL.title + ".txt"):
        with open("./crawled/" + URL.title + ".txt", "w", encoding='UTF8') as f:
            f.write(driver.page_source)


if __name__ == '__main__':
    driver = webdriver.Chrome('./driver/chromedriver')

    for URL in URLS:
        if URL.page_type == 0:
            type_page_num(URL)
        elif URL.page_type == 1:
            type_more_post(URL)
        elif URL.page_type == 2:
            type_one_page(URL)

