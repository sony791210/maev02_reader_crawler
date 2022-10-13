from flask import Blueprint, render_template, redirect
from flask import Flask,request,session,current_app
from service.navel.search import Search

from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(3)


from service.navel.downloadZhsxs import  main_zhsxs
from service.navel.downloadSto import  main_sto

from tool.response import sucess,fail

navel = Blueprint('navel',__name__)

# /apiflask/v1/navel
# /apiflask/v1/navel

@navel.route('/search', methods=['GET'])
def getNavelSearch():
    print('okok')
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
        # 測試宙斯
        if (website=="zhsxs"):
            result = search.zhsxs(keyword)
        elif(website=="sto"):
            result = search.sto(keyword)
        return sucess(result)
    except Exception as e:
        return  fail("9999",e)


@navel.route('/download', methods=['POST'])
def getNavelDownload():
    try:
        data = request.get_json()
        website =data["website"]
        navelId =data["id"]

        if not(navelId):
            raise ValueError("no navelId")
        elif not(website):
            raise ValueError("no website")

        print(navelId)

        if(website=="zhsxs"):
            print('執行多線程')
            executor.submit(main_zhsxs, navelId, current_app.config)
        elif (website == "sto"):
            print('執行多線程')
            executor.submit(main_sto, navelId, current_app.config)
        return  "testtesttest"

    except Exception as e:
        return  fail("9999",e)



