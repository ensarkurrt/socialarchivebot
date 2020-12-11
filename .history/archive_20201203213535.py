from time import sleep
from selenium import webdriver

story = 'https://medium.com/dropout-analytics/selenium-and-geckodriver-on-mac-b411dbfe61bc'
story = story + '?source=friends_link&sk=18e2c2f07fbe1f8ae53fef5ad57dbb12'   # 'https://bit.ly/2WaKraO' <- short link

def gecko_test(site_000=story):
    """
    simple overview:
        1) set up webdriver
        2) load this article 
        3) close up shop 
    
    input:
        >> site_000
            > default: url of this article ('friend link')
    """
    # set the driver 
    driver = webdriver.Firefox(executable_path=r'/Users/ensarkurt/Developer/geckodriver')

from selenium.webdriver.common.keys import Keys
drv= webdriver.Firefox(executable_path=r'/Users/ensarkurt/Developer/geckodriver')
drv.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
drv.find_element_by_name("username").send_keys('your_username_here')
drv.find_element_by_name("password").send_keys('your_password_here') 
drv.find_element_by_name("password").send_keys(u'\ue007')