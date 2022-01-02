from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
from random import randint




class InstaBot():

    def __init__(self,username,password,webdriver_path=None,unfollow_rate=30):
        '''
        Constructor
            __username: insta username of target entity
            __password: insta password of target entity
            __driver:   chrome webdriver
        '''
        self.__username = username
        self.__password = password
        self.__unfollow_rate = unfollow_rate
        options = webdriver.ChromeOptions()
        options.add_argument('log-level=3')
        if(webdriver_path):
            self.__driver = webdriver.Chrome(executable_path=webdriver_path,options=options)
        else:
            self.__driver = webdriver.Chrome(options=options)
    
    
    def login(self)->None:
        '''
            generate login session in webdriver
        '''
        driver = self.__driver
        username = self.__username
        password = self.__password
         
        driver.maximize_window()
        driver.get("https://instagram.com")
        sleep(3)
        
        # put credentials
        email_field_xpath = "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input"
        email_field = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,email_field_xpath)))
        email_field.send_keys(username)

        pass_field_xpath = "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input"
        pass_field = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,pass_field_xpath)))
        pass_field.send_keys(password)
        email_field.send_keys(Keys.RETURN)
        
        sleep(3)
        
        # bypass not now popup
        not_now1_xpath = "/html/body/div[1]/section/main/div/div/div/div/button"
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,not_now1_xpath))).click()
        sleep(2)
        not_now2_xpath = "/html/body/div[5]/div/div/div/div[3]/button[2]"
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,not_now2_xpath))).click()

    def goto_profile(self)->None:
        '''
            takes webdriver to targeted user's profile
        '''
        self.__driver.get(f"https://www.instagram.com/{self.__username}/")
    
    def get_follower_count(self)->int:
        '''
            returns int:number_of_followers of the parent username
        '''
        
        return int((WebDriverWait(self.__driver,3).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span"))).get_attribute('title')).replace(".",""))

    def get_all_followers_usernames(self,total_followers,remove=False,fake_followers=None,start=0,limit=5)->list:
        
        '''
            int:total_followers: total followers of targeted parent username
            returns list of selenium web object of all the followers of parent username
        '''
        
        driver = self.__driver
        
        # go to followers div
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/section/main/div/header/section/ul/li[2]/a"))).click()

        #scroll the div till last user 

        scroll_div = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[6]/div/div/div[2]")))
        sleep(2)

        total_count = 0 # no of followers fetched
        user_list = None
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',scroll_div)

        if(remove):
            
            
            
            counter = 0
           
            while(True):
                if(len(fake_followers)==0):
                    break
                list_of_users = driver.find_elements_by_xpath("/html/body/div[6]/div/div/div[2]/ul/div/li")[start:]
                total_count = len(list_of_users)
                
                for user_index in range(1,total_count):
                    # user = list_of_users[user_index]
                    try:                        
                        href = driver.find_element_by_xpath(f"/html/body/div[6]/div/div/div[2]/ul/div/li[{user_index}]/div/div[1]/div[2]/div[1]/span/a").get_attribute('href')
                    except:
                        print("error occ here")
                        raise "re"
                    if(href not in fake_followers):
                        continue
                        
                        # remove button click
                    
                    try:
                        driver.find_element_by_xpath(f"/html/body/div[6]/div/div/div[2]/ul/div/li[{user_index}]/div/div[2]/button").click()
                        driver.find_element_by_xpath("/html/body/div[7]/div/div/div/div[3]/button[1]").click()
                        print("fake follower removed going to unfollow sleep",href)
                        fake_followers.remove(href)
                        sleep(self.__unfollow_rate+randint(0,5))
                    except:
                        print("error occ") 
                        raise "dsd"  
                    counter+=1
                if(total_count<total_followers-3):
                    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',scroll_div)

                if(counter==total_followers-3):
                    break
                    
                if(counter>=start+limit):
                    break
                
            return None
        
        else:
            
            while(True):
                        
                sleep(2)
                list_of_users = driver.find_elements_by_xpath("/html/body/div[6]/div/div/div[2]/ul/div/li")
                total_count = len(list_of_users)
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',scroll_div)
                print(total_count,"users fetched out of",total_followers)
                if(total_count>=total_followers-3):
                    user_list = list_of_users
                    break
                if(total_count>=start+limit):
                    user_list = list_of_users
                    break
                
        return user_list
    
    
    def get_followers_href(self,user_list)->list:
        '''
            user_list(selenium object): list of object of all followers of the parent username
            returns a list of href links of all the followers of 
        '''
        followers_username = []
        for user in user_list:
            href = (user.find_elements_by_tag_name("a")[0]).get_attribute('href')
            followers_username.append(href)
        
        return followers_username
    
    def get_contitional_user(self,user_link,min_followers=10,min_posts=3)->bool:
        driver = self.__driver
            
        driver.get(user_link)
        
        sleep(randint(2,10))
        
        posts_xpath = "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span"
        followers_xpath = "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span"
        
        posts = int((WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,posts_xpath))).text).replace(".",""))
        try:
            followers =  int((WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,followers_xpath))).get_attribute('title')).replace(".",""))
        except:
            #if usser account is private
            followers =  int((WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/section/main/div/header/section/ul/li[2]/span/span"))).get_attribute('title')).replace(".",""))

        
        if(posts<=min_posts and followers<min_followers):
            return True
        
        return False
            

if __name__=='__main__':
    
    username = ""
    password = ""

    start = 0
    limit = 5
    # sleep after each follow  default = 30s + randome sleep 
    #imp -> this  script takes unfollow_rate and adds extra random sleep btween 2,20 seconds
    unfollow_rate = 30
    
    bot = InstaBot(username,password,unfollow_rate=unfollow_rate)
    bot.login()
    bot.goto_profile()
    total_followers = bot.get_follower_count()
    
    
    for i in range(int(total_followers/limit)):
        bot.goto_profile()
        user_list = bot.get_all_followers_usernames(total_followers,start=start,limit=limit)[start+1:start+limit+1]
        
        followers_href = bot.get_followers_href(user_list)
        
        fake_followers = []
    
        count = 0
        for href in followers_href:
            condition = bot.get_contitional_user(user_link=href,min_followers=10,min_posts=3)
                    
            if(not condition):
                continue
            
            fake_followers.append(href)
            print("fake follower found")
        
        start+=limit
        
        if(len(fake_followers)==0):
            print("no fake followers found in this batch")
            print("moving to batch",i)
            continue
        
        with open("fake_followers.txt","a",encoding='utf8') as f:
            for follower in fake_followers:
                f.write(f"{follower}")    
        
        bot.goto_profile()
        bot.get_all_followers_usernames(total_followers,remove=True,fake_followers=fake_followers,start=start,limit=limit)
        print("moving to batch",i)
        
    print("bot ended")
    
        
    
           
    
