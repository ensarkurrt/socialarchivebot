#coding: utf-8
from selenium import webdriver

driver = webdriver.Safari()
driver.get('https://www.instagram.com/accounts/login/')

drv= webdriver.Chrome()
drv.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
drv.find_element_by_name("username").send_keys('your_username_here')
drv.find_element_by_name("password").send_keys('your_password_here') 
drv.find_element_by_name("password").send_keys(u'\ue007')

if 'logged-in' in driver.page_source:
    print('Logged in')