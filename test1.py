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

# from urllib.request import urlopen
# from bs4 import BeautifulSoup
# html = urlopen('http://www.pythonscraping.com/pages/page3.html')
# soup = BeautifulSoup(html, 'lxml')
# children = soup.find('table',{'id':'giftList'}).children
# descendants = soup.find('table',{'id':'giftList'}).descendants
# sum = 0
# for child in children:
#     print(child)
#     sum +=1
# print(sum)
# sum2 = 0
# for descendant in descendants:
#     sum2+=1
#     print(descendant)
# print(sum2)
# coding=utf-8
# import time
# from selenium import webdriver
#
#
# driver = webdriver.Chrome()
# driver.maximize_window()
# driver.implicitly_wait(6)
#
# driver.get("http://www.baidu.com/")
# time.sleep(1)
# driver.find_element_by_link_text("新闻").click()
# time.sleep(1)
# print (driver.current_url) # current_url 方法可以得到当前页面的URL
# driver.quit()

number=123434
numberAsString = numberAsString.replace( "[^0-9.,]","")