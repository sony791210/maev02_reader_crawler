import os
import datetime as dt

def logger(txt):
    os.makedirs("logs", exist_ok=True)
    with open("logs/%s.log" %(dt.datetime.now().strftime("%Y%m%d")), 'a') as f:
        f.write( "%s --%s"%(dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),txt))
        f.write('\n')