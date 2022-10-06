bind = '0.0.0.0:4000' #需要配合docker port
workers = 4   # 获取cpu数量来设置进程数量
 
backlog = 2048
# worker_class = "gevent" #  默认为sync, 也可以使用eventlet, gevent, tornado, gthread
worker_connections = 1000
daemon = False
debug = True
proc_name = 'app'         # Flask 主程序文件名
pidfile = './logs/gunicorn.pid'
errorlog = './logs/gunicorn.log'
