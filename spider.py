import requests
import bs4
import os

web = "http://jxxt.sues.edu.cn/eams/index.action"
IDPath = '/Users/apple/Desktop/IDCode.png'
data = {'loginForm.name': '021718120', 'loginForm.password': 'Laomengan39!', 'loginForm.captcha': ''}
ID_src = 'http://jxxt.sues.edu.cn/eams/captcha/image.action'

def getHTMLText():
    try:
        r = requests.get(web, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = bs4.BeautifulSoup(r.text, "html.parser")
    except:
        return "访问失败"
    return soup


def save_image():
    # print(soup.find('img', id='captcha')['src'])
    if os.path.exists(IDPath):
        os.remove(IDPath)
        r_image = requests.get(ID_src)
        with open(IDPath, 'wb') as f:
            f.write(r_image.content)
            f.close()
        print('Succceed!')


def analysis_image():
    code = input()
    return code


def login(code):
    pass



getHTMLText()
save_image()
code = analysis_image()
login(code)



