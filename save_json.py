# vim: set fileencoding=utf-8


import os
import json
import requests
import pdb
from bs4 import BeautifulSoup
from urlparse import parse_qs, urlparse
import time


def get_news_data(row):
    link = row['link']
    res = requests.get(link)
    soup = BeautifulSoup(res.content)

    try:
        query = parse_qs(urlparse(link).query, keep_blank_values=True)
        aid = query.get('aid','')[0]

        title = soup.find('div',{'class':'article_info'}).find('h3',{'id':'articleTitle'}).text.encode('utf-8')
        content = soup.find('div',{'id':'articleBody'}).find('div',{'id':'articleBodyContents'}).text.encode('utf-8').replace('\n','').replace('\r','').replace('\t','')
        pub_date = soup.find('div',{'class':'sponsor'}).find('span',{'class':'t11'}).text.encode('utf-8')

        data = {'title': title, 'link': link, 'content': content, 'aid':int(aid), 'pub_date':pub_date}
        # pdb.set_trace()
        return data
    except:
        print 'ERR ON '+ link


def main():
    file_list = os.listdir('./data')

    for file in file_list[28:]:
        data_list = []
        cnt = 1
        with open('./data/'+file,'rb') as json_file:
            json_data = json_file.readlines()
            for data in json_data:
                print file+' | '+ str(cnt) + ' / ' +str(len(json_data))
                cnt += 1

                row = json.loads(data)
                data_list.append(get_news_data(row))
                # news_data = get_news_data(row)

                time.sleep(0.5)
        with open('./json_data/'+file,'wb') as json_file:
            for data in data_list:
                json_file.write(json.dumps(data, ensure_ascii=False,encoding='utf8').encode('utf-8')+'\n')


if __name__ == '__main__':
    main()
