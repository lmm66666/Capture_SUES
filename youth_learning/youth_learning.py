import requests
import time
import json
import random

'''
the start time of youth learning (example 2020-07-05 14:54:23) 
如果用户的上次登录时间晚于青年大学习开始时间，则证明他已完成本次大学习
'''
standard_time = '2020-07-06 14:54:23' 
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobi'
                  'le/15E148 MicroMessenger/7.0.13(0x17000d29) NetType/WIFI Language/zh_CN',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Host': 'qcsh.h5yunban.com'
}
url_login = 'http://qcsh.h5yunban.com/youth-learning/cgi-bin/login/we-chat/callback'
url_last_info = 'http://qcsh.h5yunban.com/youth-learning/cgi-bin/user-api/info'
url_study = 'http://qcsh.h5yunban.com/youth-learning/cgi-bin/user-api/course/join'
params_login = {
    'callback': 'http://qcsh.h5yunban.com/youth-learning/index.php',
    'scope': 'snsapi_userinfo',
    'appid': '',                                   
    'openid': '',                                  
    'nickname': 'random',                           # random 
    'heading': 'http://thirdwx.qlogo.cn/mmopen/vi_32/E7XLbDS0gRJibYGpzxcEwXibyTwQAAHX9Koia7oln1821c8Djkibtpf6O20J3nacpnb0pg1UmtpdfDznHYBZvL78kw/132',     # random
    'time': '10',                                   
    'source': 'common',
    'sign': 'F12500A046DFD870500E3370F30C5689',     # random
    't': 'time' 
}
params_last_info = {
    'accessToken': 'A6DA2ED4-1B61-4591-9D40-F2348221E2EC'       # get from response
}
params_study = {
    'accessToken': 'A6DA2ED4-1B61-4591-9D40-F2348221E2EC'
}
data_study = {
    'course': 'C0155',                  # change（大学习期号）
    'subOrg': None,
    'nid': 'N0001001900021024',         # 学校+班级
    'cardNo': 'lmm'                     # 姓名或学号
}


def visit_login(s, openid, info):
    # get token
    params_login['openid'] = openid
    params_login['nickname'] = rand_nickname()
    params_login['time'] = str(get_time())
    params_login['t'] = str(get_time())
    params_login['sign'] = rand_sign()
    params_login['heading'] = rand_heading()
    r = s.get(url_login, headers=headers, params=params_login)
    # get token
    token = r.text[45:81]
    print("token:", token)
    info['token'] = token
    return token


def visit_last_info(s, token, info):
    # get last visit info
    params_last_info["accessToken"] = token
    r = s.get(url=url_last_info, params=params_last_info)
    f = do_or_not(r, info)
    return f


def visit_study(s, token, class_num, name, info):
    # useless func
    params_study["accessToken"] = token
    data_study['cardNo'] = name
    num = get_nid(class_num)
    data_study['nid'] = num
    r = s.post(url_study, headers=headers, params=params_study, data=json.dumps(data_study))
    res = success_or_not(r)
    info['res'] = res


def study(class_num, openid, name, info):
    s = requests.session()
    token = visit_login(s, openid, info)
    flag = visit_last_info(s, token, info)
    if flag == 'not do':
        visit_study(s, token, class_num, name, info)
    else:
        info['res'] = 'have done'


def main():
    info = {}
    openid = ''     # your openid
    appid = ''      # your appid   
    info["openid"] = openid
    info['appid'] = appid
    name = '哈' * i
    study("延毕、出国境等留校学生团支部", openid, name, info)
    time.sleep(0.3)
    save_info(info)


def success_or_not(r):
    r.encoding = r.apparent_encoding
    r = r.text
    try:
        j = json.loads(r)
        if j['status'] == 200:
            return 'success'
        else:
            return r
    except:
        return 'fail'



def save_info(info):
    # 保存信息
    with open('/Users/apple/PycharmProjects/spider/youth_learning/student_info.txt', 'a+') as f:
        for i in info.keys():
            f.write(i)
            f.write(':')
            f.write(info[i])
            f.write(' ')
        f.write('\n')
        f.close()


def do_or_not(r, info):
    r.encoding = r.apparent_encoding
    r = r.text
    j = json.loads(r)
    last_time = j["result"]['lastUpdTime']
    print('last_time:', last_time)
    info['last_time'] = last_time
    if last_time > standard_time:
        flag = 'do'
    else:
        flag = 'not do'
    return flag


def print_response(r):
    print(r.url)
    r.encoding = r.apparent_encoding
    print(r.text)
    return r.text


def get_time():
    t = time.time()
    return int(t)


def rand_nickname():
    data = 'qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJMIKOPL1234567890'
    length = random.randint(4, 10)
    name = ''
    for i in range(length):
        r = random.randint(0, 61)
        name += data[r]
    return name


def rand_heading():
    data = 'qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJMIKOPL1234567890'
    url = ''
    for i in range(90):
        r = random.randint(0, 61)
        url += data[r]
    url = 'http://thirdwx.qlogo.cn/mmopen/vi_32/' + url + '/132'
    return url


def rand_openid():
    data = 'qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJMIKOPL1234567890'
    temp1, temp2, temp3 = '', '', ''
    for i in range(9):
        r = random.randint(0, 61)
        temp1 += data[r]
    for i in range(8):
        r = random.randint(0, 61)
        temp2 += data[r]
    for i in range(8):
        r = random.randint(0, 61)
        temp3 += data[r]
    openid = temp1 + '_' + temp2 + '-' + temp3
    return openid


def rand_sign():
    data = '1234567890ABCDEF'
    sign = ''
    for i in range(32):
        r = random.randint(0, 15)
        sign += data[r]
    return sign


def get_nid(class_num):
    if class_num == "延毕、出国境等留校学生团支部":
        return 'N0001001900021044'
    c = class_num + '班团支部'
    with open('/Users/apple/PycharmProjects/spider/youth_learning/class_info.txt', 'r') as f:
        data = f.read()
        f.close()
    data = json.loads(data)
    for i in data:
        if i["title"] == c:
            nid = i["id"]
            break
    return nid


if __name__ == '__main__':
    main()
