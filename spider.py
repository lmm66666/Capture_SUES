import requests
import bs4
import os

web = "http://jxxt.sues.edu.cn/eams/index.action"
IDPath = '/Users/apple/Desktop/IDCode.png'
data = {'loginForm.name': '021718120', 'loginForm.password': 'Laomengan39!', 'loginForm.captcha': ''}
ID_src = 'http://jxxt.sues.edu.cn/eams/captcha/image.action'

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = bs4.BeautifulSoup(r.text, "html.parser")
    except:
        return "访问失败"
    #print(soup.find('img', id='captcha')['src'])
    #获取二维码图片
    if os.path.exists(IDPath):
        os.remove(IDPath)
        r_image = requests.get(ID_src)
        with open(IDPath, 'wb') as f:
            f.write(r_image.content)
            f.close()
        print('Succceed!')
    #解析二维码


html = getHTMLText(web)



