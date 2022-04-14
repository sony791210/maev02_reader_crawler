# save this as app.py
from flask import Flask,request
from navel.search import Search
from tool.response import sucess,fail
app = Flask(__name__)

from navel.downloadZhsxs import  main_zhsxs
from navel.downloadSto import  main_sto


# 設定多線程
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(10)

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
def hello():
    return "Hello, World!"



@app.route('/apiflask/v1/navel/search', methods=['GET'])
def getNavelSearch():
    search = Search();
    try:
        website = request.args.get('website')
        keyword = request.args.get('keyword')

        if not(keyword):
            raise ValueError("no keyword")
        elif not(website):
            raise ValueError("no website")

        # 測試宙斯
        if (website=="zhsxs"):
            result = search.zhsxs(keyword)
        elif(website=="sto"):

            result = search.sto(keyword)
        print('QQQ')
        return sucess(result)
    except Exception as e:
        return  fail("9999",e)


@app.route('/apiflask/v1/navel/download', methods=['GET'])
def getNavelDownload():
    try:
        website = request.args.get('website')
        navelId = request.args.get('navelId')

        if not(navelId):
            raise ValueError("no navelId")
        elif not(website):
            raise ValueError("no website")

        print(navelId)

        if(website=="zhsxs"):
            print('執行多線程')
            executor.submit(main_zhsxs, (navelId))
        elif (website == "sto"):
            print('執行多線程')
            executor.submit(main_sto, (navelId))
        return  "testtesttest"

    except Exception as e:
        return  fail("9999",e)

if __name__ == '__main__':
    app.run()