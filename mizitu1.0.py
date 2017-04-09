# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import random
from modified_request import download

class MmDaily(object):
    def __init__(self, baseurl):
        self.baseurl = baseurl
        #print 'whole path is :%s' %self.url

    def get_page(self, page):
        response = download.get(page)
        return response.text

    def get_pic(self, page):
        html = self.get_page(page)
        soup = BeautifulSoup(html, 'lxml')
        pic_tag = soup.find('div', class_="main-image")
        title = pic_tag.img['alt']
        pic_url = pic_tag.img['src']
        pic_name = pic_url[-17:]
        pattern = re.compile(r'/', re.S)
        name = re.sub(pattern, r'-', pic_name)
        img = download.get(pic_url)
        #文件名不能取a/b/c.jpg这一种，否则python会认为他是某路径下的文件
        f = open(name, 'ab')
        f.write(img.content)

    def get_title(self):
        html = self.get_page(self.baseurl)
        soup = BeautifulSoup(html, 'lxml')
        pic_tag = soup.find('div', class_="main-image")
        title = pic_tag.img['alt']
        return title

    def get_index(self, page):
        html = self.get_page(page)
        pattern = re.compile(r'<span>(\d+)</span>', re.S)
        result = re.findall(pattern, html)
        return result[-1]

    def get_all(self):
        pic_index = self.get_index(self.baseurl)
        os.makedirs(os.path.join(r'F:/projects/DailyMm', self.get_title()))
        os.chdir(r'F:/projects/DailyMm/' + self.get_title())
        for item in range(1, int(pic_index)+1):
            self.get_pic(self.baseurl + '//' + str(item))
            print '正在写入%s第%d张图片' %(self.baseurl, item)


class QC(object):
    def __init__(self, index_url):
        self.index_url = index_url
        self.all_index = []

    def get_page(self, page):
        response = download.get(page)
        return response.text

    def get_index(self, page):
        html = self.get_page(page)
        soup = BeautifulSoup(html, 'lxml')
        all_tag = soup.find('div', class_="postlist").find_all('li')
        for li_tag in all_tag:
            a_tag = li_tag.find('span').find('a')
            href = a_tag['href']#href need ''
            title = a_tag.get_text()
            #print href, title
            self.all_index.append(href)

    def get_page_numbers(self):
        html = self.get_page(self.index_url)
        soup = BeautifulSoup(html, 'lxml')
        all_number = soup.find('div', class_="nav-links").find_all('a', class_="page-numbers")[-2].get_text()
        print all_number
        return all_number # return means the end of this function ,so all code after return shall not be excuted

    def get_all_index(self):
        for page in range(1, int(self.get_page_numbers())+1):
            self.get_index(self.index_url + '/page/' + str(page))

    def all_QC(self):
        self.get_all_index()
        for item in self.all_index:
            MmDaily(item).get_all()

mm = QC('http://www.mzitu.com/xinggan')
mm.all_QC()

