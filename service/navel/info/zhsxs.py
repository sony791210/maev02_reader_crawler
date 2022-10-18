from bs4 import BeautifulSoup
import requests
import re
import time
from fake_useragent import UserAgent
from flask import current_app
import datetime
import base64

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey,TIMESTAMP,Text,func
from sqlalchemy.orm import Session
from sqlalchemy import func
from db.dbname import Platform_info


url = "http://tw.zhsxs.com"
ua = UserAgent(verify_ssl=False)
user_agent = ua.random
headers = {'user-agent': user_agent}

global DBCLIENTNAME
class navelInfo:
    def getIntroduction(self,idd):

        res = requests.get(url + "/zhsbook/" + str(idd), headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        imgurl = soup.find('img', {"width": "180px"})['src']
        if ("http" in imgurl):
            imgurl = imgurl
        else:
            imgurl = url + imgurl
        return soup.find(style='line-height: 30px').text, imgurl

    def splicInfo(self,alltext):
        author_index=alltext.index('【作    者】')
        tags_index=alltext.index('【標    簽】')
        content_index=alltext.index('【內容簡介】')
        alert_index=alltext.index('【閱讀提示】')

        author=alltext[author_index:tags_index].replace('【作    者】','')
        tagss=alltext[tags_index:content_index].replace('【標    簽】','').replace('\xa0','').split('|')
        cat=tagss[0]
        title=tagss[-1]
        tags=",".join(str(x) for x in tagss)
        long_info=alltext[content_index:alert_index].replace('【內容簡介】','').replace('\n單擊閱讀 \n閱讀目錄 加入書架','').replace('\r','').replace('\n','').replace('\u3000','')

        return title,author,cat,long_info,tags

    def photoUrl2Base64(self,new_url):
        return base64.b64encode(requests.get(new_url).content)


    def gotoDataInfo(self,title, author, cat, long_info, tags, photoBase64, novel_name_id):

        engine = create_engine(DBCLIENTNAME, echo=True)
        session = Session(engine)
        session.begin()

        instance = session.query(Platform_info).filter_by(novel_name_id=novel_name_id).first()
        if instance:
            session.close()
            return True
        try:
            all_info = Platform_info(title=title,
                                     novel_name_id=novel_name_id,
                                     data_update_time=datetime.datetime.now(),
                                     author=author,
                                     long_info=long_info,
                                     tags=tags,
                                     cat=cat,
                                     title_photo_url=photoBase64,
                                     content_type="text",
                                     crawbing=0
                                  )
            session.add(all_info)
            session.flush()
            session.commit()
        except:
            session.rollback()
            raise
        session.close()


    def main(self,novel_name_id,dbname=None):
        global DBCLIENTNAME
        DBCLIENTNAME=dbname
        novel_name_id = int(novel_name_id)
        text, photoUrl = self.getIntroduction(novel_name_id)
        photoBase64 = self.photoUrl2Base64(photoUrl)
        title, author, cat, long_info, tags = self.splicInfo(text)
        self.gotoDataInfo(title, author, cat, long_info, tags, photoBase64, novel_name_id)


        return True
