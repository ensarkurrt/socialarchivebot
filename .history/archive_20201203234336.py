from time import sleep
from selenium import webdriver
import urllib.request

def setup():
    return webdriver.Firefox(executable_path=r'/Users/ensarkurt/Developer/geckodriver')

def get_by_element_name(driver,elementName):
    return driver.find_element_by_name(elementName)

def get_by_element_xpath(driver,xpath):
    return driver.find_element_by_xpath(xpath)

def send_to_element_name(driver,elementName,value):
    return get_by_element_name(driver,elementName).send_keys(value)

def send_to_element_xpath(driver,xpath,value):
    return get_by_element_xpath(driver,xpath).send_keys(value)

def click_to_element_name(driver,elementName):
    return get_by_element_name(driver,elementName).click()

def click_to_element_xpath(driver,xpath):
    return get_by_element_xpath(driver,xpath).click()

def get_attribute_element(element,attribute):
    return element.get_attribute(attribute)

def get_attribute_name(driver,elementName,attribute):
    return get_by_element_name(driver,elementName).get_attribute(attribute)

def get_attribute_xpath(driver,xpath,attribute):
    return get_by_element_xpath(driver,xpath).get_attribute(attribute)

def login(driver,username,password):
    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    sleep(3)
    send_to_element_name(driver,'username',username)
    send_to_element_name(driver,'password',password)
    click_to_element_xpath(driver,'//*[@id="loginForm"]/div/div[3]/button')

def goToStories(driver,username):
    driver.get('https://www.instagram.com/stories/{username}/')

def startStories(driver):
    click_to_element_xpath(driver,'//*[@id="react-root"]/section/div[1]/div/section/div/div[1]/div/div/button')

def recognizeVideo(driver):
    try:
        get_by_element_xpath(driver,'//*[@id="react-root"]/section/div[1]/div/section/div/div[1]/div/div/video')
    except NoSuchElementException:
        return False
    return True

def getVideo(driver,username):
    url_link = get_attribute_xpath(driver,'//*[@id="react-root"]/section/div[1]/div/section/div/div[1]/div/div/video','src')
    urllib.request.urlretrieve(url_link, 'video_{username}.mp4')

def getImage(driver):
    with open('pic1.jpg', 'wb') as handle:
        response = requests.get(pic_url, stream=True)

        if not response.ok:
                print response

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)

def getStory(driver):
    if recognizeVideo(driver):
        getVideo(driver)
    else:
        getImage(driver)

def main():

    driver = setup()
    login(driver,'sosyalmedyaarsivi','159753Ensar')
    goToStories(driver,'reynmen')
    sleep(3)
    startStories(driver)
    sleep(2)





if __name__ == "__main__":
    main()
    pass


