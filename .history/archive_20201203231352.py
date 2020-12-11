from time import sleep
from selenium import webdriver

driver = webdriver.Firefox(executable_path=r'/Users/ensarkurt/Developer/geckodriver')

username = "sosyalmedyaarsivi"
password = "159753Ensar"

driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')

sleep(3)

driver.find_element_by_name("username").send_keys(username)
driver.find_element_by_name("password").send_keys(password)
 
driver.find_element_by_name("password").send_keys(u'\ue007')


def get_by_elemne(driver,elementName):
    return driver.find_element_by_name(elementName)

def send_to_elemnet_name(driver,elementName,value):
    return driver.find_element_by_name(elementName).send_keys(value)

def 