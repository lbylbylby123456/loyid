#coding=utf-8
# from selenium import webdriver
# driver = webdriver.Chrome()
# driver.get("http://www.baidu.com")
#
# #返回输入框内容
# driver.find_element_by_id('kw').send_keys('hello')
# attribute=driver.find_element_by_id("kw").get_attribute('value')
# print(attribute)
# #返回元素可见结果
# result=driver.find_element_by_id("kw")
# print(result)
# #元素是否被启动
# enabled=driver.find_element_by_id("kw").is_enabled()
# print(enabled)

from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen('http://www.pythonscraping.com/pages/page3.html')
soup = BeautifulSoup(html, 'lxml')
children = soup.find('table',{'id':'giftList'}).children
descendants = soup.find('table',{'id':'giftList'}).descendants
sum = 0
for child in children:
    print(child)
    sum +=1
print(sum)
sum2 = 0
for descendant in descendants:
    sum2+=1
    print(descendant)
print(sum2)
