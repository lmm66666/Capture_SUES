import requests
import bs4
import os
import time
import re

web = "http://jxxt.sues.edu.cn/eams/index.action"
code_path = '/Users/apple/Desktop/IDCode.png'
course_path = '/Users/apple/Desktop/course.txt'
data = {'loginForm.name': '021718120', 'loginForm.password': 'Laomengan39!', 'encodedPassword': ""}
code_src = 'http://jxxt.sues.edu.cn/eams/captcha/image.action'
headers = {'Referer': 'http://jxxt.sues.edu.cn/eams/login.action',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) '
           'Chrome/75.0.3770.100 Safari/537.36'}
course_list = []


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
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    return soup


def get_course():
    r = session.get('http://jxxt.sues.edu.cn/eams/courseTableForStd.action?method=courseTable&'
                    'setting.forSemester=1&setting.kind=std&semester.id=422&ids=72146903&ignoreHead=1')
    print(r.status_code)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    # if os.path.exists(course_path):
    #     os.remove(course_path)
    # with open(course_path, 'w') as f:
    #     f.write(soup.text)
    #     f.close()
    #     print('Succceed!')
    return soup.text


def progress_course(html):
    temp = []
    re_course = '(("\S+",){6}"[0-1]{53}"\);[\s\S]*?new)'
    m = re.findall(re_course, html)
    for i in m:
        if not (i[0] in temp):
            temp.append(i[0])
    for i in temp:
        raw_data = ''.join(i)
        raw_data = raw_data.split(',')
        data = raw_data[1] + raw_data[3] + raw_data[5]
        raw_data = raw_data[6].split(';')
        data += raw_data[0][:-1]
        for j in raw_data[1::2]:
            m = re.findall('\d+', j)
            num = 0
            for i in m:
                t = int(i) + 1
                if(num % 2) == 0:
                    time = '星期' + str(t)
                    data += time
                else:
                    time = '第' + str(t) + '节'
                    data += time
                num += 1
        print(data)

    #     course_list.append(temp2)
    # for i in course_list:
    #     print(i)



session = requests.session()
getHTMLText()
save_image()
code = analysis_image()
login(code)
html = get_course()
progress_course(html)




