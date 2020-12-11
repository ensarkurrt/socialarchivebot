from time import sleep
from selenium import webdriver

driver = webdriver.Firefox(executable_path=r'/Users/ensarkurt/Developer/geckodriver')
username = "sosyalmedyaarsivi"
password = "159753Ensar"

driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')

sleep(3)

driver.find_element_by_name("username").send_keys(username)
dr.find_element_by_name("password").send_keys(password)
 
drv.find_element_by_name("password").send_keys(u'\ue007')