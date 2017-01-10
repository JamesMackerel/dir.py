import requests
from bs4 import BeautifulSoup
import chardet

s = requests.session()

DEBUG = True

header = {
    'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',

}

def login():
    payload = {'username':'1300330227', 'passwd':'1300330227', 'login':'%B5%C7%A1%A1%C2%BC'};
    s.post('http://bkjw.guet.edu.cn/student/public/login.asp', data=payload, headers=header)
    info_page = BeautifulSoup(s.get('http://bkjw.guet.edu.cn/student/Info.asp', headers=header).content, 'html.parser')
    print('login successfully')
    for p in info_page('p'):
        print(p.string)

    print()

def walk():
    #get majorities
    majority = {}
    majority_value = []
    select_page = BeautifulSoup(s.get('http://bkjw.guet.edu.cn/student/select.asp', headers=header).content, 'html.parser')
    for option in select_page('option'):
        if 'value' in option.attrs:
            majority_value.append(option['value'])
            majority[option['value']] = option.string

    if DEBUG:
        print(majority)

    payload = {
        'spno':'',
        'grade':'2016',
        'selecttype':'%D6%D8%D0%DE', #“重修”
        'lwPageSize':'1000',
        'lwBtnquery':'%B2%E9%D1%AF' #“查询”
    }

    for m in majority_value: #遍历所有专业
        if m=='000000':
            continue
        payload['spno'] = m
        page = s.post('http://bkjw.guet.edu.cn/student/select.asp', data=payload, headers=header)
        soup = BeautifulSoup(page.content, 'html.parser')

        print(majority[str(m)])
        table = soup.find('table')
        if table==None: #如果没有课表，跳过这个专业
            continue

        for tr in soup.find_all('tr'): #直接找到表格的行
            res = ''
            for td in tr.find_all('td'): #遍历列
                #有些单元格里面的内容是链接，有些是直接的字符串
                #对于链接，输出链接内容
                #对于直接字符串，输出字符串内容
                a = td.find('a')
                if a is None:
                    c = td.string
                else:
                    c = a.string

                #最后一列是“是否订购教材”，内容包含在input里面，又没有链接
                #所以碰到的话就直接不管他了
                if c is not None:
                    res = res + c + '\t'

            #找到有物理的行
            if '物理' not in res:
                continue

            print(res)

if __name__=='__main__':
    login()
    walk()
