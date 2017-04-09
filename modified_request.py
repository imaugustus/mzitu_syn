#-*- coding:utf-8 -*-
import requests
import re
import random
import time
from bs4 import BeautifulSoup

class download(object):
    def __init__(self):
        self.ip_list = []#构造存储IP用的空列表
        html = requests.get('http://haoip.cc/tiqu.htm') #获取代理网站网页
        pattern = re.compile(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,4}', re.S)#利用正则表达式提取IP代理
        ip_result = re.findall(pattern, html.text)
        for item in ip_result:#将匹配到的IP填入上面构造的代理列表
            self.ip_list.append(item)
        self.UA_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]#构造UA存储列表
    #定义一个健壮的包含超时设定，代理使用，重复尝试的网页获取函数
    def get(self, url, timeout=3, proxy = None, num_retries = 6):#设定了默认了重试次数为6
        UA = random.choice(self.UA_list)#获取一个随机UA
        headers = {"User-Agent": UA}#利用此随机UA构造头
        #第一层判断，是对是否使用代理的判定
        if proxy == None:#当调用函数并且代理参数为空时，则不用代理
            try:#尝试直接调用requests的get函数，并设置超时
                return requests.get(url, headers=headers, timeout=timeout)
            except:#如果直接调用出错，则进行下一步
                if num_retries>0:#第二层判断，是对重试次数的判定
                    print u'获取网页出错，10s后将重复倒数第%d次' % (num_retries)
                    time.sleep(10)#爬虫休眠10秒
                    return self.get(url, num_retries-1)#调用自身函数且不使用代理，并将重复爬网页限制次数-1
                else:#此时重复爬次数已经归零
                    print u'开始使用代理'
                    time.sleep(10)#休眠10秒
                    IP = str(random.choice(self.ip_list))#构造一个随机代理
                    proxy = {"http": IP}
                    return self.get(url, proxy)#调用自身并使用代理


        else:#第一层判断的反面，即调用函数时代理参数为非空
            try:#第二重判定是对使用代理是否成功的判定
                #IP = ' '.join(random.choice(self.ip_list).strip())#the operation on IP is to be discussed,i think ip can't have blank ,it must be:123.23.4.14, but not (1 2 3.2 3.1 4)
                #print IP, "it is false"#示范对代理IP的错误处理方式
                IP = str(random.choice(self.ip_list))#示范代理IP的正确获取方式
                print IP, "this is the right usage"
                proxy = {"http": IP}
                return requests.get(url, headers=headers, proxies=proxy, timeout=timeout)#调用requests的get函数并使用代理获取网页
            except:#第二重判定的反面，上一个代理失败
                if num_retries > 0:#第三重判定，如果重试次数大于0，则重复爬取
                    time.sleep(10)#休眠10秒后继续爬取
                    IP = str(random.choice(self.ip_list))#随机选择另一个代理爬取
                    proxy = {"http": IP}
                    print u"正在更换代理，10秒后重新获取倒数第%d次"%(num_retries-1)
                    print u"当前使用的代理是", proxy
                    return self.get(url, proxy, num_retries-1)#调用自身并设置代理参数为非空，并将重试计数减1
                else:#第三重判定的反面，重试次数归零，即重试了num_retries次后还是失败
                    print u"代理全部失败，直接连接"
                    return self.get(url)#达到重试次数上限，调用自身，设置超时并将代理参数设为空
download = download()






