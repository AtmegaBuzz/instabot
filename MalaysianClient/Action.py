from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
from random import randint


class ActionBot():
    
    def __init__(self,driver,username,password,comments=["nice","good"]):
        self.__driver = driver
        self.__username = username
        self.__password = password
        self.comments = comments
    
    def login(self):
        
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

    
    def get_followers(self,filename):
        followers = None
        with open(filename,"r",encoding="utf8") as f:
            followers = f.read()
            followers = followers.split(",")
        
        return followers
    
    def scrape_posts_href(self,follow_button):
        sleep(2)
        driver = self.__driver
        try:
            counter = 0
            flag = True
            alternate = False
            rows = driver.find_elements(By.XPATH,"/html/body/div[1]/section/main/div/div[2]/article/div[1]/div/div")
            if(len(rows)==0):
                rows = driver.find_elements(By.XPATH,"/html/body/div[1]/section/main/div/div[3]/article/div/div/div")
                alternate = True                                       
            posts_href_list = []
            print(len(rows))
            for row in range(1,len(rows)+1):
                # posts = driver.find_elements(By.XPATH,f"/html/body/div[1]/section/main/div/div[2]/article/div[1]/div/div{row}/div")
                if(alternate):
                    posts = driver.find_elements_by_xpath(f"/html/body/div[1]/section/main/div/div[3]/article/div/div/div[{row}]/div")
                                                       
                else:
                    posts = driver.find_elements_by_xpath(f"/html/body/div[1]/section/main/div/div[2]/article/div[1]/div/div[{row}]/div")
                                       
                
                for i in range(1,len(posts)+1):
                    if(counter>=3):
                        flag = False
                        break
                    if(alternate):
                        post_href = driver.find_element(By.XPATH,f"/html/body/div[1]/section/main/div/div[3]/article/div/div/div[{row}]/div[{i}]/a").get_attribute('href')
                    else:
                        post_href = driver.find_element(By.XPATH,f"/html/body/div[1]/section/main/div/div[2]/article/div[1]/div/div[{row}]/div[{i}]/a").get_attribute('href')
         
                    posts_href_list.append(post_href)
                    counter+=1
                if(not flag):
                    break   
            follow_button.click()
            return posts_href_list
            
        except Exception as e:
            print("error on user posts",e)
            return None
        
    def like_on_post(self,href,comment=False):
        driver = self.__driver
        driver.get(href)
        
        try:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button"))).click()
            if(comment):
                random_comment = randint(1,len(self.comments)-1)
                WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[3]/div/form/textarea"))).click()
                WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[3]/div/form/textarea"))).send_keys(self.comments[random_comment])
                WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[3]/div/form/textarea"))).send_keys(Keys.RETURN)
        except Exception as e:
            print("comment section is diabled",e)
        sleep(randint(1,5))
        return None
        
    
    def action(self,user_url):
        driver = self.__driver
        driver.get(user_url)
        sleep(2)
        button = None
        try:
            button = driver.find_element(By.XPATH,"/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button")
        except:
            button = driver.find_element(By.XPATH,"/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button")
            
        
        if(button.text=="Follow Back"):
            print("user already a follower")
            return None
        public_account = False
        try:
            driver.find_element(By.XPATH,"/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")
            public_account = True
        except:
            pass
        
        if(not public_account):
            print("not public account")
            return None
        
        posts_href = self.scrape_posts_href(button)
        
        print(posts_href)
        if(posts_href==None):
            return None
        commented = True
        for href in posts_href:
            self.like_on_post(href,comment=commented)
            if(commented):
                commented = False
            
        
        
def run_action(username,password):     
    driver = webdriver.Chrome()
    driver.maximize_window()
    bot = ActionBot(driver,username,password)
    bot.login()
    users = bot.get_followers("followers.txt")
    if(users!=None):
        for user in users:
            bot.action(user)
            sleep(10+randint(1,10))
            print("action completed for",user)
    
    driver.close()