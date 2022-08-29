# save this as app.py
from flask import Flask,request,session
from navel.search import Search
from tool.response import sucess,fail
import os
from datetime import timedelta
app = Flask(__name__)
app.config.from_object('config.ProdConfig')
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

from navel.downloadZhsxs import  main_zhsxs
from navel.downloadSto import  main_sto

from comic.downloadMhgui import  main_mhgui
from comic.downloadWebmota import main_webmota

# 設定多線程
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(3)


# 增加lgo
import logging
import logging.config


log_level = "DEBUG"
LOGFILENAME = "logs/flask.log"
class LoggerConfig:
    dictConfig = {
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] {%(pathname)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s',
        }},
        'handlers': {'default': {
                    'level': 'DEBUG',
                    'formatter': 'default',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': LOGFILENAME,
                    'maxBytes': 5000000,
                    'backupCount': 10
                }},
        'root': {
            'level': log_level,
            'handlers': ['default']
        },
    }

logging.config.dictConfig(LoggerConfig.dictConfig)

@app.route("/")
@app.route("/hello")
@app.route("/apiflask")
def hello():
    return "Hello, World!"



@app.route('/apiflask/v1/navel/search', methods=['GET'])
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


@app.route('/apiflask/v1/navel/download', methods=['POST'])
def getNavelDownload():
    try:
        data = request.get_json()
        website =data["website"]
        navelId =data["navelId"]

        if not(navelId):
            raise ValueError("no navelId")
        elif not(website):
            raise ValueError("no website")

        print(navelId)

        if(website=="zhsxs"):
            print('執行多線程')
            executor.submit(main_zhsxs, navelId, app.config)
        elif (website == "sto"):
            print('執行多線程')
            executor.submit(main_sto, navelId, app.config)
        return  "testtesttest"

    except Exception as e:
        return  fail("9999",e)




@app.route('/apiflask/v1/comic/download', methods=['POST'])
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
            executor.submit(main_mhgui,comicId, app.config)
        elif(website == "webmota"):
            print('執行多線程')
            executor.submit(main_webmota, comicId, app.config)


        return "testtesttest"
    except Exception as e:
        return  fail("9999",e)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port="4000")
