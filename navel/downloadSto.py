
from bs4 import BeautifulSoup
import requests
import re
import time
from fake_useragent import UserAgent

import datetime
import base64


from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey,TIMESTAMP,Text,func
from sqlalchemy.orm import Session


from db.dbname import Novel ,Novel_info,Novel_crawler_sto

from navel.info.sto import navelInfo

import time
import random

import cloudscraper
scraper = cloudscraper.create_scraper(delay=10)
from opencc import OpenCC
cc= OpenCC('s2tw')

import logging
logger = logging.getLogger()

DBClientName="mysql+pymysql://root:19990704@192.168.88.55:3306/app"
ua = UserAgent()
user_agent = ua.random
headers = {'user-agent': user_agent}
url="https://www.sto.cx/"


NavelInfoInit=navelInfo()

def getContent(soup):
    content = (soup.find(id="BookContent").text).replace("\u3000\u3000", "\n").replace("\u3000\u3000", "\n").replace(
        "\u3000", "\n")

    return cc.convert(content)


def gotoDBCrawlPage(page, novel_name_id):
    engine = create_engine(DBClientName, echo=True)
    session = Session(engine)
    session.begin()

    instance = session.query(Novel_crawler_sto).filter_by(nid=novel_name_id, pid=page).first()

    if instance:
        session.close()
        return True

    try:
        novel_value = Novel_crawler_sto(nid=novel_name_id, pid=page)
        session.add(novel_value)
        session.flush()
        session.commit()
    except:
        session.rollback()
        raise
    session.close()


def gotoDBCrawlInfo(title, content, novel_name_id, page):
    engine = create_engine(DBClientName, echo=True)
    session = Session(engine)
    session.begin()
    if (len(title) > 20):
        title = title[0:20]

    instance = session.query(Novel).filter_by(novel_name_id=novel_name_id, page=page).first()

    if instance:
        session.close()
        return True

    try:
        novel_value = Novel(title=title, novel_name_id=novel_name_id, content=content, page=page)
        session.add(novel_value)
        session.flush()
        session.commit()
    except:
        session.rollback()
        raise
    session.close()

def check_crawbing(novel_name_id):
    engine = create_engine(DBClientName, echo=True)
    session = Session(engine)
    session.begin()

    isCrawbing = session.query(Novel_info.crawbing ).filter_by(novel_name_id=novel_name_id).first()
    session.close()


    try:
        result=int(isCrawbing[0])
    except:
        result=0;

    return  result

def save_crawbing(isCrawbing,novel_name_id):
    engine = create_engine(DBClientName, echo=True)
    session = Session(engine)
    session.begin()

    try:
        # 儲存資訊
        Novel_info_sql =session.query(Novel_info ).filter(Novel_info.novel_name_id==novel_name_id).update({"crawbing":isCrawbing})

        session.commit()
    except Exception as e:
        print(e)
        raise
    session.close()


def get_db_pid(nid):
    engine = create_engine(DBClientName, echo=True)
    session = Session(engine)
    session.begin()

    maxPage =session.query(  func.max(Novel_crawler_sto.pid)  ).filter_by(nid=nid).first()

    if (maxPage[0] is None):
        maxPage =0
    else:
        maxPage =int(maxPage[0])

    session.close()
    return maxPage





def main_sto(novel_id):
    novel_name_id = int(novel_id)
    NavelInfoInit.main(novel_id);

    # 查看是否在抓取中
    if(check_crawbing(novel_name_id)==1):
        logger.warning(("novel_id %s 抓取中") % (novel_name_id))
        return "抓取中"
    else:
        save_crawbing(1,novel_name_id)


    try:
        page = 1
        url = "https://www.sto.cx/"

        # init page
        page_url = "%sbook-%s-%s.html" % (url, novel_name_id, page)
        scraper = cloudscraper.create_scraper(delay=10)  # returns a CloudScraper instance
        res = scraper.get(page_url)
        soup = BeautifulSoup(res.text,"html.parser")
    except Exception as e:
        logger.debug("sto,init失敗,nid is %s"%(novel_name_id))
        logger.debug(str(e))
        save_crawbing(0, novel_id)
        return False

    # lastpage
    lastPage = soup.find(id="webPage").findAll('a')[-1]["href"].split('-')[2][:-5]
    lastPage = int(lastPage)

    # 查看上次爬到第幾頁
    maxPage=get_db_pid(novel_name_id)
    try:
        for leaf in range(lastPage):
            if( (leaf+1) > int(maxPage) ):
                logger.info(("nid %s  page %s") % (novel_name_id,  leaf+1))
                now_page_url = "%sbook-%s-%s.html" % (url, novel_name_id, leaf + 1)
                res = scraper.get(now_page_url)
                soup = BeautifulSoup(res.text,"html.parser")

                content = getContent(soup)
                title = "第%s頁" % (leaf + 1)
                page = leaf + 1
                gotoDBCrawlInfo(title, content, novel_name_id, page)
                gotoDBCrawlPage(leaf + 1, novel_name_id)
                time.sleep(random.random() * 5)
    except Exception as e:
        logger.debug("sto,for leaf 失敗,nid is %s" % (novel_name_id))
        logger.debug(str(e))

    save_crawbing(0, novel_id)
    return  True;