#/usr/bin/env python
# vim: set fileencoding=utf-8

import requests
from bs4 import BeautifulSoup
from slacker import Slacker
from datetime import datetime
import time

class SNC():
    def __init__(self):
        self.news_data = []

    def get_news(self, link):
        res = requests.get(link)
        soup = BeautifulSoup(res.content)
        title = soup.find('div',{'class':'article_info'}).find('h3',{'id':'articleTitle'}).text.encode('utf-8')
        content = soup.find('div',{'id':'articleBody'}).find('div',{'id':'articleBodyContents'}).text.encode('utf-8')
        data = {'link': link, 'title': title, 'content': content}
        self.news_data.append(data)

    def get_politics(self):
        politics_url = 'http://news.naver.com/main/list.nhn?sid2=269&sid1=100&mid=shm&mode=LS2D&date=%s&page=%s'
        today = datetime.now().strftime('%Y%m%d')
        page = 0
        flag = True
        while(flag):
            page += 1
            print page
            res = requests.get(politics_url%(today,page))
            soup = BeautifulSoup(res.content)
            data_list = soup.find('div',{'class':'newsflash_body'}).findAll('li')
            for data in data_list:
                link = data.findAll('a')[0]['href']
                self.get_news(link)
                time.sleep(0.5)

            page_list = soup.find('div',{'class':'paging'}).findAll('a')
            last_page = page_list[-1].text.encode('utf-8')
            if last_page != '다음' and int(last_page) < page:
                flag = False


    def report_to_slack(self):
        slack = Slacker('SLACK_API_TOKEN')
        slack.chat.post_message('#general', '네이버 뉴스 크롤링')
        slack.chat.post_message('#general', '수집한 뉴스 갯수: '+str(len(self.news_data)))

    def processing(self):
        self.get_politics()
        self.report_to_slack()

if __name__ == '__main__':
    snc = SNC()
    snc.processing()
