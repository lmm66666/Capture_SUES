import requests
import bs4
import os

web = "http://jxxt.sues.edu.cn/eams/index.action"
code_path = '/Users/apple/Desktop/IDCode.png'
data = {'loginForm.name': '021718120', 'loginForm.password': 'Laomengan39!'}
code_src = 'http://jxxt.sues.edu.cn/eams/captcha/image.action'
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
          'Accept-Encoding': 'gzip, deflate',
          'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
          'Content-Length': '98',
          'Content-Type': 'application/x-www-form-urlencoded',
          'Cookie': 'JSESSIONID=5DBB43AB605CB7806F6F669FAC450D32; UM_distinctid=16b3c4c9404a07-0b5cee0616a2f-37647e03-13c680-16b3c4c94059d6; test=20111139',
          'Host': 'jxxt.sues.edu.cn',
          'Origin': 'http://jxxt.sues.edu.cn',
          'Pragma': 'no-cache',
          'Referer': 'http://jxxt.sues.edu.cn/eams/login.action',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}


def getHTMLText():
    try:
        r = requests.get(web, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = bs4.BeautifulSoup(r.text, "html.parser")
    except:
        print("访问失败")
    return soup


def save_image():
    # print(soup.find('img', id='captcha')['src'])
    if os.path.exists(code_path):
        os.remove(code_path)
        r_image = requests.get(code_src)
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
    r = requests.post('http://jxxt.sues.edu.cn/eams/login.action', data=data, headers=headers)
    print(r.status_code)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    return soup


#getHTMLText()
save_image()
code = analysis_image()
html = login(code)
print(html)


