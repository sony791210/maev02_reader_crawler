
from celery import Celery
from time import sleep
 
CELERY_BROKER_URL = 'redis://:secret_redis@redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://:secret_redis@redis:6379/0'
app = Celery("app", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
 
@app.task                              # 这里写了一个异步方法，等待被调用
def mul(arg1, arg2):
    sleep(10)
    result = arg1*arg2
    return result
 
def get_result(task_id):               # 通过任务id可以获取该任务的结果
    result = app.AsyncResult(task_id)

