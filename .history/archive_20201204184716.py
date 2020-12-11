from time import sleep
from selenium import webdriver
import urllib.request
import requests
import os
import json
from datetime import datetime as timepicker

def pr(text,item):
    print('['+item+'] '+text)

def setup():
    return webdriver.Firefox(executable_path=r'/Users/ensarkurt/Developer/geckodriver')

def checkAndCreateFile(path):
    if not os.path.exists(path):
        os.mkdir(path)

def checkAndCreateJson(path):
    if not os.path.exists(path): 
        with open(path, mode='w', encoding='utf-8') as file:
            file.write('[]')

def logError(username,data):
    x = {'username':username,'datetime':timepicker.now().strftime("%d/%m/%Y %H:%M:%S"),'detail':data}
    path = './config/errorlogs.txt'

    checkAndCreateJson(path)
    with open(path, mode='r', encoding='utf-8') as feedsjson:
        feeds = json.load(feedsjson)
    with open(path, mode='w', encoding='utf-8') as feedsjson:
        entry = x
        feeds.append(entry)
        json.dump(feeds, feedsjson)

def getUsernames():
    path = './config/usernames.txt'
    with open(path,'r') as f: 
        return [word.strip() for line in f for word in line.split()]

def setUsernames():
    path = './config/usernames.txt'
    if os.path.exists(path):
        os.remove(path)
    while True:
        username = input("[?] Kullanıcı adı girin (Başlatmak için boş bırak): ")
        if username.strip() == "":
            break
        with open(path, "a+") as file:
            file.seek(0)
            data = file.read(100)
            if len(data) > 0 :
                file.write("\n")
            file.write(username)

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

def checkStoryDownloaded(path):
    return os.path.exists(path)

def getStoryTime(driver):
    datetime = get_attribute_xpath(driver,'//*[@id="react-root"]/section/div[1]/div/section/div/header/div[2]/div[1]/div/div/div/time','datetime')
    date = get_attribute_xpath(driver,'//*[@id="react-root"]/section/div[1]/div/section/div/header/div[2]/div[1]/div/div/div/time','title')
    day = date.split(' ')[0]
    # day = datetime[8:10]
    return {'day': day,'mounth': datetime[5:7],'year': datetime[0:4],'hour': datetime[11:13],'minute':datetime[14:16],'second':datetime[17:19]}

def createFileSystem(driver,username,filetype):
    datetime = getStoryTime(driver)
    path = './instagram/' + username
    
    checkAndCreateFile(path)
    path = path + '/stories'
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
    try:
        url_link = get_attribute_xpath(driver,'//*[@id="react-root"]/section/div[1]/div/section/div/div[1]/div/div/video/source','src')
        datetime = getStoryTime(driver)
        path = createFileSystem(driver,username,'video.mp4')
        if checkStoryDownloaded(path)==False:
            urllib.request.urlretrieve(url_link, path)
        else:
            pr('Bu hikaye daha önce indirilmiş','!')
    except Exception as e:
        logError(username,{'url':driver.current_url,'exception':str(e),'message':'video did not download'})
        pr('Bu hikaye indirilemedi.','!!!')

def getImage(driver,username):
    try:
        pic_url = get_attribute_xpath(driver,'//*[@id="react-root"]/section/div[1]/div/section/div/div[1]/div/div/img','src')
        path = createFileSystem(driver,username,'foto.png')
        if checkStoryDownloaded(path)==False:
            with open(path, 'wb') as handle:
                response = requests.get(pic_url, stream=True)

                if not response.ok:
                    print(response)

                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)
        else:
            pr('Bu hikaye daha önce indirilmiş','!')
    except Exception as e:
        logError(username,{'url':driver.current_url,'exception':str(e),'message':'image did not download'})
        pr('Bu hikaye indirilemedi.','!!!')

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

def recordScan(username,sType):
    path = './config/scanlog.txt'
    checkAndCreateJson(path)   
    datetime = timepicker.now().strftime("%d/%m/%Y %H:%M:%S")
    index = -1
    found = False

    with open(path, mode='r', encoding='utf-8') as feedsjson:
        feeds = json.load(feedsjson)
        for data in feeds:
            index = index + 1
            if data["username"] == username:
                x = data['scans']
                x.append({'type':sType,'datetime':datetime})
                feeds[index]['scans'] = x
                found = True
                with open(path, mode='w', encoding='utf-8') as feedsjson:
                    json.dump(feeds, feedsjson)
                break
        if not found:
            with open(path, mode='w', encoding='utf-8') as feedsjson:
                    feeds.append({'username':username,'scans': [{'type':sType,'datetime':datetime}]})
                    json.dump(feeds, feedsjson)

def recordProfile(driver,username):
    pr(username+' Kullanıcısının profil bilgileri çekiliyor','*')
    driver.get('https://instagram.com/'+username+'/')
    sleep(2)
    path = './instagram/'+username+'/profile.txt'

    fullname=''
    desc=''
    link=''
    follower=''
    following=''
    postCount=''

    try:
        fullname = get_by_element_xpath(driver,'//*[@id="react-root"]/section/main/div/header/section/div[2]/h1').text
    except Exception as e:
        logError(username,{'url':driver.current_url,'exception':str(e),'message':'profile fullname did not download'})
        
    try:
         desc = get_attribute_xpath(driver,'//*[@id="react-root"]/section/main/div/header/section/div[2]/span','innerHTML')
    except Exception as e:
        logError(username,{'url':driver.current_url,'exception':str(e),'message':'profile desc did not download'})
    
    try:
        link = get_by_element_xpath(driver,'//*[@id="react-root"]/section/main/div/header/section/div[2]/a').text
    except Exception as e:
        logError(username,{'url':driver.current_url,'exception':str(e),'message':'profile link did not download'})
    
    try:
        follower = get_attribute_xpath(driver,'//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span','title')
    except Exception as e:
        logError(username,{'url':driver.current_url,'exception':str(e),'message':'profile follower did not download'})

    try:
        following = get_by_element_xpath(driver,'//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text
    except Exception as e:
        logError(username,{'url':driver.current_url,'exception':str(e),'message':'profile following did not download'})

    try:
        postCount = get_by_element_xpath(driver,'//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span').text
    except Exception as e:
        logError(username,{'url':driver.current_url,'exception':str(e),'message':'profile post count did not download'})
        
    datetime = timepicker.now().strftime("%d/%m/%Y %H:%M:%S")

    checkAndCreateFile('./instagram/'+username)

    x = {'username':username,'datetime':datetime,'detail': {'fullname':fullname,'postCount':postCount,'follower':follower,'following':following,'desc':desc,'link':link}}

    checkAndCreateJson(path)
    with open(path, mode='r', encoding='utf-8') as feedsjson:
        feeds = json.load(feedsjson)
    with open(path, mode='w', encoding='utf-8') as feedsjson:
        entry = x
        feeds.append(entry)
        json.dump(feeds, feedsjson)
    recordScan('reynmen','profile')
    pr(username+' Kullanıcısının profil kaydı tamamlandı','*')

def startProccess(driver,username):
    pr(username+' Kullanıcısının hikayeleri çekiliyor','*')
    goToStories(driver,username)
    sleep(3)
    if checkStory(driver):
        startStories(driver)
        if checkStory(driver):
            sleep(0.8)
            while checkStory(driver):
                pr('Hikaye indiriliyor','*')
                sleep(0.3)
                stopResumeStory(driver)
                sleep(1)
                getStory(driver,username)
                stopResumeStory(driver)
                nextStory(driver)
        else:
            pr(username+' Kullanıcısının hikayesi bulunamadı','!')
    else:
        pr(username+' Kullanıcısının hikayesi bulunamadı','!')
    recordScan('reynmen','story')

def main():
    setUsernames()
    driver = setup()
    login(driver,'sosyalmedyaarsivi','159753Ensar')
    sleep(3)
    for username in getUsernames():
        recordProfile(driver,username)
        sleep(2)
        startProccess(driver,username)    
    
if __name__ == "__main__":
    #main()
    recordScan('reynmen','')
    pass