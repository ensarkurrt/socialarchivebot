from time import sleep
from selenium import webdriver

driver = setup()



def setup():
    return webdriver.Firefox(executable_path=r'/Users/ensarkurt/Developer/geckodriver')

def get_by_element_name(driver,elementName):
    return driver.find_element_by_name(elementName)

def get_by_element_name(driver,elementName):
    return driver.find_element_by_name(elementName)

def send_to_element_name(driver,elementName,value):
    return get_by_element_name(elementName).send_keys(value)

def login(driver,username,password):
    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    send_to_element_name(driver,'username',username)
    send_to_element_name(driver,'password',password)
    
