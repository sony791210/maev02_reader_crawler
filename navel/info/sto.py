

from bs4 import BeautifulSoup
import re

import datetime
import base64


from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db.dbname import Novel_info


import cloudscraper
from opencc import OpenCC

cc= OpenCC('s2tw')
scraper = cloudscraper.create_scraper(delay=10) # returns a CloudScraper instance
DBClientName="mysql+pymysql://root:19990704@192.168.88.55:3306/app"

class navelInfo:
    def __init__(self):
        self.url="https://www.sto.cx/"


    def getIntroduction(self,idd):
        res = scraper.get(self.url + "mbookintro-" + str(idd) + ".html")
        soup = BeautifulSoup(res.text,"html.parser")

        return soup

    def photoUrl2Base64(self,new_url):
        return base64.b64encode(scraper.get(new_url).content)

    def gotoDataInfo(self,title, author, cat, long_info, tags, photoBase64, novel_name_id):
        engine = create_engine(DBClientName, echo=True)
        session = Session(engine)
        session.begin()

        instance = session.query(Novel_info).filter_by(novel_name_id=novel_name_id).first()
        if instance:
            session.close()
            return True
        try:
            all_info = Novel_info(title=title,
                                 novel_name_id=novel_name_id,
                                 data_update_time=datetime.datetime.now(),
                                 author=author,
                                 long_info=long_info,
                                 tags=tags,
                                 cat=cat,
                                 title_photo_url=photoBase64,
                                 content_type="text")
            session.add(all_info)
            session.flush()
            session.commit()
        except:
            session.rollback()
            raise
        session.close()

    def getTitle(self,soup):
        pattern = re.compile(r'《\S+》')  # 查找数字
        title, = pattern.findall(soup.title.text)
        return title[1:-1]

    def getAuthor(self,soup):
        pattern = re.compile(r'作者:\S+_')  # 查找数字
        author, = pattern.findall(soup.title.text)
        return author[3:-1]

    def getImgUrl(self,soup):
        try:
            return self.url + soup.img['src'][1:]
        except:
            return None

    def getTag(self,soup):
        pattern = re.compile(r'分类：\S+ ')  # 查找数字
        tag, = pattern.findall(soup.find(class_="c").text)
        return cc.convert(tag[3:-1])

    def getLongInfo(self,soup):
        return cc.convert(soup.find(class_="i").text)

    def main(self,novel_name_id):
        novel_name_id = int(novel_name_id)
        soup = self.getIntroduction(novel_name_id)

        title = self.getTitle(soup)
        author = self.getAuthor(soup)
        cat = self.getTag(soup)
        long_info = self.getLongInfo(soup)
        tags = self.getTag(soup)
        photoBase64 = self.getImgUrl(soup)
        self.gotoDataInfo(title, author, cat, long_info, tags, photoBase64, novel_name_id)
        return True