import requests
import bs4
import os
import time

web = "http://jxxt.sues.edu.cn/eams/index.action"
code_path = '/Users/apple/Desktop/IDCode.png'
data = {'loginForm.name': '021718120', 'loginForm.password': 'Laomengan39!', 'encodedPassword': ""}
code_src = 'http://jxxt.sues.edu.cn/eams/captcha/image.action'
headers = {'Referer': 'http://jxxt.sues.edu.cn/eams/login.action',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) '
           'Chrome/75.0.3770.100 Safari/537.36'}


def getHTMLText():
    try:
        r = session.get(web, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except:
        print("访问失败")


def save_image():
    t = time.time()
    timestamp = int(round(t * 1000))
    mes = {'d': timestamp}
    r_image = session.get(code_src, params=mes)
    if os.path.exists(code_path):
        os.remove(code_path)
        with open(code_path, 'wb') as f:
            f.write(r_image.content)
            f.close()
        print('Succceed!')


def analysis_image():
    code = input("请输入验证码\n")
    return code


def login(code):
    data['loginForm.captcha'] = code
    print(data)
    r = session.post('http://jxxt.sues.edu.cn/eams/login.action', data=data, headers=headers)
    print(r.status_code)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    return soup


session = requests.session()
getHTMLText()
save_image()
code = analysis_image()
html = login(code)
print(html)


