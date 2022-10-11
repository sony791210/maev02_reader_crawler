

from tool.seleniumoption import openChrome
from bs4 import BeautifulSoup


class Search:

    def webmota(self,keyword):
        print('go get')
        URL = "https://www.baozimh.com/search?q="
        # 開啟chrome
        print('QQ')
        chrome = openChrome()
        print('open chrome')
        print("%s%s" % (URL, keyword))
        chrome.get("%s%s" % (URL, keyword))
        print('get url in  chrome')
        # 解析網域
        soup = BeautifulSoup(chrome.page_source, 'html.parser')
        #
        soup.find(class_="classify-items").find_all(class_="comics-card")[0].find('a')['href']

        result=[]
        for i in soup.find(class_="classify-items").find_all(class_="comics-card"):
            print( i.find('a')['title'])
            result.append(
                {
                    "comic_name_id":i.find('a')['href'].split('/')[-1],
                    "title": i.find('a')['title'],
                    "author": "",
                    "img":i.find_all('img')[-1]["src"]
                }
            )
        return result

