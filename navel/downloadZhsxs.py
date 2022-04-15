
from bs4 import BeautifulSoup
import requests
import re
import time
from fake_useragent import UserAgent


from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey ,TIMESTAMP ,Text ,func
from sqlalchemy.orm import Session
from sqlalchemy import func
from db.dbname import Novel_crawler_zhou ,Novel ,Novel_info
import random

from navel.info.zhsxs import navelInfo


import logging
logger = logging.getLogger()

DBClientName ="mysql+pymysql://root:19990704@192.168.88.55:3306/app"
ua = UserAgent()
user_agent = ua.random
headers = {'user-agent': user_agent}
url ="http://tw.zhsxs.com"

NavelInfoInit=navelInfo()


def gotoDB(title ,content ,page ,novel_name_id ,nid ,pid):
    engine = create_engine(DBClientName, echo=True)
    session = Session(engine)
    session.begin()

    # 先讀取看是否有資料，如果有就不存
    instance =session.query(Novel).filter_by(novel_name_id=novel_name_id ,page=page).first()
    if instance:
        session.close()
        return True

    try:
        # 儲存資訊
        novel_value =Novel(title=title ,novel_name_id=novel_name_id ,content=content ,page=page)
        session.add(novel_value)
        session.flush()
        session.add(  Novel_crawler_zhou(nid=nid ,pid=pid ,novel_id=novel_value.id) )
        session.commit()
    except:
        session.rollback()
        raise
    session.close()



def start_crawl(novel_name_id):
    res =requests.get(url +"/zhschapter/ " +str(novel_name_id ) +".html" ,headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    listArray =soup.find_all(class_='chapterlist')
    return listArray

def get_nid_pid_page(html):
    pattern = re.compile(r'\d+')   # 查找数字
    nid ,pid =pattern.findall(html['href'])

    return nid ,pid

def get_novel_text(url):
    ua = UserAgent()
    user_agent = ua.random
    headers = {'user-agent': user_agent}
    novel_res =requests.get(url ,headers=headers)
    novel_soup = BeautifulSoup(novel_res.text, "html.parser")
    text =novel_soup.find('div' ,style=lambda value: value and 'word-wrap: break-word;' in value).text
    return text

def get_db_pid(nid):
    engine = create_engine(DBClientName, echo=True)
    session = Session(engine)
    session.begin()

    maxPid =session.query(  func.max(Novel_crawler_zhou.pid)  ).filter_by(nid=nid).first()

    if (maxPid[0] is None):
        maxPid =0
    else:
        maxPid =int(maxPid[0])

    maxPage =session.query(  func.max(Novel.page)  ).filter_by(novel_name_id=nid).first()

    if(maxPage[0] is None):
        maxPage =0
    else:
        maxPage =int(maxPage[0])

    session.close()
    return maxPid ,maxPage


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

    return  result;

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





def main_zhsxs(novel_id):
    novel_id=int(novel_id)
    try:
        NavelInfoInit.main(novel_id);
    except Exception as e:
        print(e)
        logger.debug(str(e))

    try:
        # 查看是否在抓取中
        if(check_crawbing(novel_id)==1):
            logger.warning(("novel_id %s 抓取中") % (novel_id))
            return "抓取中"
        else:
            save_crawbing(1,novel_id)
    except Exception as e:
        print(e)
        logger.debug(str(e))


    # 定義小說id
    novel_name_id =novel_id
    # 抓取小說目錄
    listArray =start_crawl(novel_id)
    # 查看上次爬到第幾頁
    maxPid ,page =get_db_pid(novel_id)
    for st ,i in enumerate(listArray):
        try:
            nid ,pid =get_nid_pid_page(i.find("a"))

            if(int(pid ) >int(maxPid)):
                logger.info(("nid %s pid %s page %s") % (nid, pid, st))
                page =page +1
                content =get_novel_text(   url +i.find('a')['href'])
                title =i.find("a").text
                gotoDB(title ,content ,page ,novel_name_id ,nid ,pid)
                time.sleep(random.random( ) *10)
        except Exception as e:
            logger.debug(str(e))
            break
    logger.warning(("novel_id %s 結束抓取") % (novel_id))
    save_crawbing(0, novel_id)




