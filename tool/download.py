

import requests
import os
import time
import re

def header(refererURL=None):
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    if(refererURL):
        headers = {'user-agent': user_agent, "Referer": refererURL}
    else:
        headers = {'user-agent': user_agent}
    return headers


def download(webname,comicId,page,refererURL=None):
    headers=header(refererURL)
    check_list = {
        "image/jpeg": "jpeg",
        "image/png": "png",
        "image/jpg": "jpg"
    }
    with open("public/%s/%s/%03d" %(webname,comicId,page), 'r') as f:
        contents = f.readlines()
    output_dir="public_download/comic/%s/%03d"%(comicId,page)
    os.makedirs(output_dir, exist_ok=True)
    for index,url in enumerate(contents):
        # replace /n
        newURL=url[:-1]
        # 爬取圖片
        response = requests.get(newURL, headers=headers)
        count=0
        while response.status_code!=200:
            count=count+1
            time.sleep(1)
            response = requests.get(newURL, headers=headers)
            print(response.status_code)
            if(count>=2):
                response.status_code=200

        # file_format=check_list[ response.headers["content-type"]  ] if (response.headers["content-type"] in check_list) else "png"


        # 找出檔名
        names=re.compile(r"\w+\.jpg").findall(newURL)
        if names:
            # remove .jpg
            name=names[0][:-4]
        else:
            # remove .jpg
            name=0

        # 存檔
        file_format = "png"
        with open("%s/%03d.%s"%(output_dir,name,file_format), 'wb') as f:
            f.write(response.content)