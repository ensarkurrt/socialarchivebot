from time import sleep
from selenium import webdriver
import urllib.request
import requests
import os 

def pr(text,item):
    print('['+item+'] '+text)

def setup():
    return webdriver.Firefox(executable_path=r'/Users/ensarkurt/Developer/geckodriver')

def getUsernames():
    with open('usernames.txt','r') as f: 
        return [word for line in f for word in line.split()]

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
    pr('Instagram girişi yapılıyor','*')
    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    sleep(3)
    send_to_element_name(driver,'username',username)
    send_to_element_name(driver,'password',password)
    click_to_element_xpath(driver,'//*[@id="loginForm"]/div/div[3]/button')
    pr('Instagram girişi tamamlandı','!')

def getStoryTime(driver):
    datetime = get_attribute_xpath(driver,'//*[@id="react-root"]/section/div[1]/div/section/div/header/div[2]/div[1]/div/div/div/time','datetime')
    return {'day': datetime[8:10],'mounth': datetime[5:7],'year': datetime[0:4],'hour': datetime[11:13],'minute':datetime[14:16],'second':datetime[17:19]}

def checkAndCreateFile(path):
    if not os.path.exists(path):
        os.mkdir(path)

def createFileSystem(driver,username,filetype):
    datetime = getStoryTime(driver)
    path = './stories/' + username
    
    checkAndCreateFile(path)
    path = path + '/'+ datetime['year']
    checkAndCreateFile(path)
    path = path + '/'+ datetime['mounth']
    checkAndCreateFile(path)
    path = path + '/'+ datetime['day']
    checkAndCreateFile(path)

    return path+'/'+datetime['hour']+'_'+datetime['minute']+'_'+datetime['second']+'_'+filetype

def goToStories(driver,username):
    driver.get('https://www.instagram.com/stories/'+username+'/')

def startStories(driver):
    click_to_element_xpath(driver,'//*[@id="react-root"]/section/div[1]/div/section/div/div[1]/div/div/button')

def stopResumeStory(driver):
    click_to_element_xpath(driver,'//*[@id="react-root"]/section/div[1]/div/section/div/header/div[2]/div[2]/button[1]')        

def nextStory(driver):
    if get_by_element_xpath(driver,'//*[@id="react-root"]/section/div[1]/div/section/div/button[2]/div'):
        click_to_element_xpath(driver,'//*[@id="react-root"]/section/div[1]/div/section/div/button[2]/div')

def recognizeVideo(driver):
    try:
        get_by_element_xpath(driver,'//*[@id="react-root"]/section/div[1]/div/section/div/div[1]/div/div/video')
    except:
        return False
    return True

def getVideo(driver,username):
    url_link = get_attribute_xpath(driver,'//*[@id="react-root"]/section/div[1]/div/section/div/div[1]/div/div/video/source','src')
    datetime = getStoryTime(driver)
    urllib.request.urlretrieve(url_link, createFileSystem(driver,username,'video.mp4'))

def getImage(driver,username):
    pic_url = get_attribute_xpath(driver,'//*[@id="react-root"]/section/div[1]/div/section/div/div[1]/div/div/img','src')

    with open(createFileSystem(driver,username,'foto.png'), 'wb') as handle:
        response = requests.get(pic_url, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

def getStory(driver,username):
    if recognizeVideo(driver):
        getVideo(driver,username)
    else:
        getImage(driver,username)

def checkStory(driver):
    try:
        get_by_element_xpath(driver,'//*[@id="react-root"]/section/div[1]/div/section/div/div[1]')
    except:
        return False
    return True

def startProccess(driver,username):
    pr(username+' Kullanıcısının hikayeleri çekiliyor','*')
    goToStories(driver,username)
    sleep(3)
    startStories(driver)
    sleep(0.5)
    while checkStory(driver):
        pr('Hikaye indirme başladı','*')
        sleep(0.3)
        stopResumeStory(driver)
        getStory(driver,username)
        pr('Hikaye indirme tamamlandı','!')
        stopResumeStory(driver)
        nextStory(driver)
    pr('Hikayeleri çekme işlemi tamamlandı','!')
        
def main():
    driver = setup()
    login(driver,'sosyalmedyaarsivi','159753Ensar')
    sleep(3)
    for username in getUsernames():
        startProccess(driver,username)
    
if __name__ == "__main__":
    main()
    pass