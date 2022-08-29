from selenium import webdriver

import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import concurrent.futures
import os
from tool.seleniumoption import getOptions

URL="https://www.mhgui.com"



def saveTxt(page,array,comicId):
    os.makedirs("public/mhgui/%s"%(comicId), exist_ok=True)
    with open("public/mhgui/%s/%03d" %(comicId,page), 'w') as f:
        for st,j in enumerate(array):
            f.write(j["src"])
            f.write('\n')

def getPhotoUrl(comicpath):
    newChrome = webdriver.Chrome('./chromedriver', chrome_options=getOptions())
    newChrome.get(URL+comicpath)

    time.sleep(5)
    newChrome.find_element(By.CSS_SELECTOR,"a[onclick^='SMH.setFunc(3)']").click()

    if len(newChrome.window_handles)>1:
        newChrome.switch_to.window(newChrome.window_handles[0])

    newHeight=0
    for timestep in range(500):
        print("series is %s" %timestep)
        # document.body.scrollHeight
        jsGoToBottom="var action=document.documentElement.scrollTop=100000000000"
        newChrome.execute_script(jsGoToBottom)
        time.sleep(0.5)
        jsGetHeight = "return document.body.scrollHeight;"
        height=newChrome.execute_script(jsGetHeight)
        height=int(height)
        if(newHeight==height):
            break
        else:
            newHeight=height





    soup2=BeautifulSoup(newChrome.page_source, 'html.parser')
    newChrome.close()
    newChrome.quit()

    return soup2

def goDownload(comicpath,i,comicId):
    # 拿取漫畫頁面所有的圖片soup
    soup2=getPhotoUrl(comicpath)

    return soup2.find_all("img")



def main_mhgui(comicId,config):
    # 初始化
    chrome = webdriver.Chrome('./chromedriver', chrome_options=getOptions())
    # 讀取漫畫目錄頁面
    chrome.get("https://www.mhgui.com/comic/%s/" % comicId)
    # 取出soup
    soup = BeautifulSoup(chrome.page_source, 'html.parser')
    # 拿出目錄的url
    arrays = soup.find(id="chapter-list-0").find_all('a')

    for i in range(len(arrays)):
        # 如果有下載過 就不要下載了拉
        if( os.path.exists("public/mhgui/%s/%03d" %(comicId,i)) ):
            pass
        else:
            print(i)
            if (i > 1):
                break
            # 從最後面，第一頁開始抓取
            st = len(arrays) - i - 1
            time.sleep(2)
            comicpath = arrays[st]["href"]
            imgUrlList=goDownload(comicpath, i,comicId)
            # 拿取漫畫頁面所有的圖片url，並存成落地黨
            saveTxt(i, imgUrlList, comicId)
            time.sleep(1)

