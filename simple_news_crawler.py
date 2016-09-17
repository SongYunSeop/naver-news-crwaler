#/usr/bin/env python
# vim: set fileencoding=utf-8

import requests
from bs4 import BeautifulSoup
from slacker import Slacker
from datetime import datetime, timedelta
import time
import pdb
class SNC():
    def __init__(self):
        self.news_data = []

    def get_news(self, link):
        res = requests.get(link)
        soup = BeautifulSoup(res.content)
        try:
            # title = soup.find('div',{'class':'article_info'}).find('h3',{'id':'articleTitle'}).text.encode('utf-8')
            content = soup.find('div',{'id':'articleBody'}).find('div',{'id':'articleBodyContents'}).text.encode('utf-8').replace('\n','')
            data = {'link': link, 'content': content}

            self.news_data.append(data)
        except:
            print 'ERR ON '+ link

    def get_politics(self):
        politics_url = 'http://news.naver.com/main/list.nhn?sid2=269&sid1=100&mid=shm&mode=LS2D&date=%s&page=%s'
        # today = datetime.now().strftime('%Y%m%d')
        max_page = 30
        numdays = 30
        date_list = [datetime.now() - timedelta(days=x) for x in range(21, numdays)]
        for date in date_list:
            page = 0
            flag = True
            today = date.strftime('%Y%m%d')
            while(flag):
                page += 1


                if page > max_page:
                    flag = False

                print '정치 | '+today + ' | ' +str(page)
                res = requests.get(politics_url%(today,page))
                soup = BeautifulSoup(res.content)
                data_list = soup.find('div',{'class':'newsflash_body'}).findAll('li')

                for data in data_list:
                    link = data.findAll('a')[0]['href']
                    self.get_news(link)
                    time.sleep(0.5)

                try:
                    page_list = soup.find('div',{'class':'paging'}).findAll('a')
                    last_page = page_list[-1].text.encode('utf-8')
                except:
                    continue


                if last_page != '다음' and int(last_page) < page:
                    flag = False

            self.report_to_slack2(today)
            self.content_save2(today)

    def get_economy(self):
        economy_url = 'http://news.naver.com/main/list.nhn?sid2=263&sid1=101&mid=shm&mode=LS2D&date=%s&page=%s'
        numdays = 5
        date_list = [datetime.now() - timedelta(days=x) for x in range(0, numdays)]
        for date in date_list:
            page = 0
            flag = True
            today = date.strftime('%Y%m%d')
            while(flag):
                page += 1
                print '경제 | '+today + ' | ' +str(page)
                res = requests.get(economy_url%(today,page))
                soup = BeautifulSoup(res.content)
                data_list = soup.find('div',{'class':'newsflash_body'}).findAll('li')
                for data in data_list:
                    link = data.findAll('a')[0]['href']
                    self.get_news(link)
                    time.sleep(0.5)
                try:
                    page_list = soup.find('div',{'class':'paging'}).findAll('a')
                    last_page = page_list[-1].text.encode('utf-8')
                except:
                    continue

                if last_page != '다음' and int(last_page) < page:
                    flag = False

    def get_it(self):
        it_url = 'http://news.naver.com/main/list.nhn?sid2=230&sid1=105&mid=shm&mode=LS2D&date=%s&page=%s'
        numdays = 5
        date_list = [datetime.now() - timedelta(days=x) for x in range(0, numdays)]
        for date in date_list:
            page = 0
            flag = True
            today = date.strftime('%Y%m%d')
            while(flag):
                page += 1
                print 'IT | '+today + ' | ' +str(page)
                res = requests.get(it_url%(today,page))
                soup = BeautifulSoup(res.content)
                data_list = soup.find('div',{'class':'newsflash_body'}).findAll('li')
                for data in data_list:
                    link = data.findAll('a')[0]['href']
                    self.get_news(link)
                    time.sleep(0.5)
                try:
                    page_list = soup.find('div',{'class':'paging'}).findAll('a')
                    last_page = page_list[-1].text.encode('utf-8')
                except:
                    continue

                if last_page != '다음' and int(last_page) < page:
                    flag = False

    def report_to_slack(self):
        slack = Slacker('<SLACK_TOKEN>')
        slack.chat.post_message('#general', '네이버 뉴스 크롤링')
        slack.chat.post_message('#general', '수집한 뉴스 갯수: '+str(len(self.news_data)))

    def report_to_slack2(self, today):
        slack = Slacker('<SLACK_TOKEN>')
        slack.chat.post_message('#general', '네이버 뉴스 크롤링: '+today)
        slack.chat.post_message('#general', '수집한 뉴스 갯수: '+str(len(self.news_data)))

    def fail_report(self):
        slack = Slacker('<SLACK_TOKEN>')
        slack.chat.post_message('#general', '실패다 헤헤')

    def content_save(self):
        with open('test.txt', 'wb') as news:
            for data in self.news_data:
                news.write(data['content'])

    def content_save2(self, today):
        with open(today, 'wb') as news:
            for data in self.news_data:
                news.write(data['content'].replace('\n',''))
        self.news_data = []

    def processing(self):
        try:
            self.get_politics()
            # self.get_economy()
            # self.get_it()
            self.content_save()
            # self.report_to_slack()
        except:
            self.fail_report()

if __name__ == '__main__':
    snc = SNC()
    snc.processing()
