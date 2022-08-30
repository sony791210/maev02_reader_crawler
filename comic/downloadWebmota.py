import os
from tool.seleniumoption import getOptions
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import concurrent.futures

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey ,TIMESTAMP ,Text ,func
from sqlalchemy.orm import Session
from sqlalchemy import func


from  tool.download import download
from db.dbname import Comic,Platform_info

URLORIGEN="https://www.baozimh.com"
URL="https://www.baozimh.com/comic"
webname="webmota"
global DBCLIENTNAME


def list_page(comicId):
    chrome = webdriver.Chrome('./chromedriver', chrome_options=getOptions())
    chrome.get("%s/%s" % (URL, comicId))
    soup = BeautifulSoup(chrome.page_source, 'html.parser')
    # 合併list
    mergedlist = [];
    mergedlist.extend( soup.find(id="chapter-items").find_all("a") )
    mergedlist.extend(  soup.find(id="chapters_other_list").find_all("a") )

    title=soup.title.text.replace('包子漫畫', '').replace(" ","")
    tags=[i.text.replace("\n","").replace(" ","") for i in soup.find(class_="tag-list").find_all("span")]
    dec=soup.find(class_="comics-detail__desc").text

    chrome.close()
    chrome.quit()

    return title,tags,dec,mergedlist


def getImgUrl(path):
    chrome = webdriver.Chrome('./chromedriver', chrome_options=getOptions())
    newPath="%s/%s" % (URLORIGEN, path)

    mergedlist = [];
    isNext=True;
    st=0;
    while isNext:
        chrome.get(newPath)
        soup = BeautifulSoup(chrome.page_source, 'html.parser')

        mergedlist.extend( soup.find_all("img") );

        # 取出是否要下一頁 或 下一話之類的問題
        name=soup.find(class_="next_chapter").find('a').text.replace(" ", "").replace("\n", "")
        newPath=soup.find(class_="next_chapter").find('a')['href']

        st +=1 ;
        # 爬太多頁 ，怕當機
        if(st>10):
            isNext = False
        #  怕爬到掛了
        if(name==""):
            isNext = False
        # end page 會出現
        if(name=="點選進入下一話"):
            isNext=False

    return mergedlist


def saveTxt(page,array,comicId):
    os.makedirs("public/webmota/%s"%(comicId), exist_ok=True)
    with open("public/webmota/%s/%03d" %(comicId,page), 'w') as f:
        for st,j in enumerate(array):
            f.write(j["src"])
            f.write('\n')



def save_comic_info(comic_name_id,page,title,path):
    engine = create_engine(DBCLIENTNAME, echo=True)
    session = Session(engine)
    session.begin()
    instance = session.query(Comic).filter_by(comic_name_id=comic_name_id, page=page).first()

    if instance:
        session.close()
        return True
    try:
        novel_value = Comic(comic_name_id=comic_name_id, page=page,path=path,title=title)
        session.add(novel_value)
        session.flush()
        session.commit()
    except:
        session.rollback()
        raise
    session.close()


def save_info(comic_name_id,title,tags,dec):
    engine = create_engine(DBCLIENTNAME, echo=True)
    session = Session(engine)
    session.begin()
    instance = session.query(Platform_info).filter_by(comic_name_id=comic_name_id).first()

    if instance:
        session.close()
        return True
    try:
        ttag=",".join(str(x) for x in tags)
        platform_value = Platform_info(comic_name_id=comic_name_id,title=title,long_info=dec,tags=ttag)
        session.add(platform_value)
        session.flush()
        session.commit()
    except:
        session.rollback()
        raise
    session.close()


def main_webmota(comicId,config):
    global DBCLIENTNAME
    DBCLIENTNAME = config["DBCLIENTNAME"]

    title,tags,dec,pages=list_page(comicId);
    save_info(comicId,title,tags,dec)
    for st,page in enumerate(pages):
        imgUrlList=getImgUrl(page['href'])
        # 拿取漫畫頁面所有的圖片url，並存成落地黨
        saveTxt(st, imgUrlList, comicId)
        time.sleep(1)
        # 開始下載 影像
        download(webname,comicId,st,URLORIGEN)
        time.sleep(1)
        #紀錄到DB才行
        save_comic_info(comicId, st, page.text, "public_download/comic/%s/%03d"%(comicId,st) )
        break

