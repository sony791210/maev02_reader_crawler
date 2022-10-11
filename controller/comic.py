from flask import Blueprint, render_template, redirect
from flask import Flask,request,session,current_app
from service.comic.search import Search

from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(3)


from service.comic.downloadMhgui import  main_mhgui
from service.comic.downloadWebmota import main_webmota

from tool.response import sucess,fail


comic = Blueprint('comic',__name__)
@comic.route('/search', methods=['GET'])
def getComicSearch():
    search = Search();
    try:
        website = request.args.get('website')
        keyword = request.args.get('keyword')
        print('ok1')

        if not(keyword):
            raise ValueError("no keyword")
        elif not(website):
            raise ValueError("no website")
        print(website)

        result=""
        # 測試webmota
        if (website=="webmota"):
            print('go')
            result = search.webmota(keyword)

        return sucess(result)
    except Exception as e:
        return  fail("9999",e)



@comic.route('/download', methods=['POST'])
def getComicDownload():
    try:
        data = request.get_json()
        website =data["website"]
        comicId =data["comicId"]

        if not(comicId):
            raise ValueError("no navelId")
        elif not(website):
            raise ValueError("no website")

        if (website == "mhgui"):
            print('執行多線程')
            executor.submit(main_mhgui,comicId, current_app.config)
        elif(website == "webmota"):
            print('執行多線程')
            # main_webmota(comicId, app.config)
            executor.submit(main_webmota, comicId, current_app.config)


        return "testtesttest"
    except Exception as e:
        return  fail("9999",e)


