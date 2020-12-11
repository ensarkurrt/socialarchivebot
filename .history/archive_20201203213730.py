from time import sleep
from selenium import webdriver

drv= webdriver.Firefox(executable_path=r'/Users/ensarkurt/Developer/geckodriver')
username = "sosyalmedyaarsivi"
password = "159753Ensar"

drv.get('https://www.instagram.com/accounts/login/?source=auth_switcher')

sleep(3)

drv.find_element_by_name("username").send_keys(username)
drv.find_element_by_name("password").send_keys('your_password_here') 
drv.find_element_by_name("password").send_keys(u'\ue007')