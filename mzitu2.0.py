# -*- coding:utf -8-*-
from bs4 import BeautifulSoup
from modified_request import download
import re
import os
import lxml
from pymongo import MongoClient

class mzitu(object):#此处已经import了download对象，不必在定义类时继承此对象
    def __init__(self, url):
        client = MongoClient()#与MongoDB建立连接
        db = client['SexyGirl']#初始化一个数据库
        self.mzitu_collection = db['mzitu']
        self.url = url
        self.count_num = 1

    def get_all_index(self):
        start_html = download.get(self.url)
        soup = BeautifulSoup(start_html.text, 'lxml')
        year_tag = soup.find('div', class_="main").find_all('div', class_="year")
        li_tags = soup.find('div', class_="main").find_all('li')#找到所有叫li的tag并存在一个可循环对象li_tags中
        for li_tag in li_tags:#对每一个li_tag操作
            a_tags = li_tag.find(class_="url").find_all("a")#找出li_tag的所偶a tag
            for a_tag in a_tags:
                self.get_per_folder(a_tag['href'])
                print self.count_num
                self.count_num += 1

    def get_per_folder(self, start_page):
        html = download.get(start_page)
        soup = BeautifulSoup(html.text, 'lxml')
        all_index = int(soup.find('div', class_="pagenavi").find_all('a')[-2].get_text())
        original_folder_name = soup.find('div', class_="main-image").img['alt']
        folder_name = re.sub('\?', r' ', original_folder_name)#Windows files cannot contain the ':' character: (or any of \ / : * ? " < > | as they are reserved characters.)参考印象笔记的记录内容
        os.makedirs(os.path.join(r'F:\projects\DailyMm\\', folder_name))
        print folder_name
        for index in range(1, all_index+1):
            page = start_page + r'/' + str(index)
            html = download.get(page)
            soup = BeautifulSoup(html.text, 'lxml')
            img_tag = soup.find('div', class_="main-image").img
            img_href = img_tag['src']
            original_pic_name = img_href[-17:]
            pic_name = re.sub(r'/', '-', original_pic_name)
            os.chdir(r'F:\projects\DailyMm\\' + folder_name)
            img = download.get(img_href)
            f = open(pic_name, 'ab')
            f.write(img.content)
            f.close()








test = mzitu("http://www.mzitu.com/all")
test.get_all_index()
#test.get_per_folder('http://www.mzitu.com/88373')

