#coding: utf-8
from selenium.webdriver.common.by import By
from selenium import webdriver

driver = webdriver.Safari()
driver.get('https://www.instagram.com/accounts/login/')


username = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
password = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
login_button = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')

username.clear()
password.clear()
username.send_keys('sosyalmedyaarsivi')
password.send_keys('159753')

login_button.click()
driver.get('https://www.instagram.com/accounts/login')

if 'logged-in' in driver.page_source:
    print('Logged in')