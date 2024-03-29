
from selenium.webdriver.chrome.options import Options

from selenium import webdriver

def openChrome():
    try:
        chrome = webdriver.Remote(
            command_executor='http://platform_chrome:4444/wd/hub',
            options=getOptions(True)
        )
        return chrome
    except:
        try:
            chrome = webdriver.Remote(
                command_executor='http://platform_chrome:4444/wd/hub',
                options=getOptions(True)
            )
            return chrome
        except:
            return False




def getOptions(openImage=False):
    options = Options()
    options.add_argument("--disable-notifications")
    # 指定浏览器分辨率
    options.add_argument('window-size=1920x3000')
    # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('--disable-gpu')
    # 不加载图片, 提升速度
    if(openImage):
        options.add_argument('blink-settings=imagesEnabled=false')
    # 以最高权限运行
    options.add_argument('--no-sandbox')
    # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    options.add_argument('--headless')
    return options

