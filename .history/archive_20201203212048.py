#coding: utf-8
from selenium.webdriver.common.by import By
from selenium import webdriver

driver = webdriver.Safari()
driver.get('https://www.instagram.com/accounts/login/')
dom = driver.find_element_by_xpath('//*')

username = dom.find_e('username')
password = dom.find_element_by_name('password')
login_button = dom.find_element_by_xpath('//*[@class="_qv64e _gexxb _4tgw8 _njrw0"]')

username.clear()
password.clear()
username.send_keys('your username')
password.send_keys('your password')

login_button.click()
driver.get('https://www.instagram.com/accounts/login')

if 'logged-in' in driver.page_source:
    print('Logged in')