from bs4 import BeautifulSoup
import requests
import re
import time
from fake_useragent import UserAgent
from flask import current_app
#
import datetime
import base64
import cloudscraper
from opencc import OpenCC

cc = OpenCC('s2tw')
scraper = cloudscraper.create_scraper()
class Search:


    def zhsxs(self,keyword):
        print(current_app.config)
        ua = UserAgent(use_cache_server=False)
        user_agent = ua.random
        headers = {'user-agent': user_agent}
        print('OKOKOK')
        res = requests.get("http://tw.zhsxs.com/zhslist/%s.html"%(keyword), headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        result=[];
        for i in soup.find_all(class_="td2"):
            print(i.find('a')['title'].split(' ')[0] )
            print(i.find('a')['href'].split('/')[-1][:-5])
            result.append({
                "title":i.find('a')['title'].split(' ')[0],
                "author": "",
                "navel_name_id":i.find('a')['href'].split('/')[-1][:-5]
            })
        return result


    def sto(self,keyword):
        res = scraper.get("https://www.sto.cx/sbn.aspx?k=%s" % (keyword))
        soup = BeautifulSoup(res.text, "html.parser")
        print("https://www.sto.cx/sbn.aspx?k=%s" % (keyword) )
        result=[]
        for st, i in enumerate(soup.find_all(class_="slistbody")):
            title = cc.convert(i.find('a', target=True).text.split("作者：")[0])
            author = cc.convert(i.find('a', target=True).text.split("作者：")[1])
            navel_name_id =i.find('a', target=True)['href'].split('-')[1]
            result.append({
                "title": title,
                "author": author,
                "navel_name_id":navel_name_id
            })

        return result
