# save this as app.py
from celery_task import *
from flask import Flask,request,session


import os
from datetime import timedelta


from controller.navel import navel
from controller.comic import comic

app = Flask(__name__)
app.config.from_object('config.ProdConfig')
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)


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



# 小說
app.register_blueprint(navel,url_prefix='/apiflask/v1/navel')
# 漫畫
app.register_blueprint(comic,url_prefix='/apiflask/v1/comic')




@app.route("/mul/<arg1>/<arg2>")
def mul_(arg1,arg2):
    result = mul.delay(int(arg1),int(arg2))        # 调用异步方法并传参数
    return result.id
 
@app.route("/get_result/<result_id>")
def result_(result_id):
    result = get_result(result_id)
    return str(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
