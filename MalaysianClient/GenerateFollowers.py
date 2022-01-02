from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep




class InstaBot():

    def __init__(self,username,password,webdriver_path=None):
        '''
        Constructor
            __username: insta username of target entity
            __password: insta password of target entity
            __driver:   chrome webdriver
        '''
        self.__username = username
        self.__password = password

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

    def goto_profile(self,user)->None:
        '''
            takes webdriver to targeted user's profile
        '''
        self.__driver.get(f"https://www.instagram.com/{user}/")
   

    def get_all_followers_usernames(self,start,limit)->list:
        
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

        while(total_count<=start+limit):  
                sleep(2)
                user_list = driver.find_elements_by_xpath("/html/body/div[6]/div/div/div[2]/ul/div/li")
                total_count = len(user_list)
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',scroll_div)
                print(total_count,"users fetched out of")
                
                
        return user_list[start:]
    
    
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
    
    def close_driver(self):
        self.__driver.close()
        
        
def get_followers(username,password,users,start,limit):          
    bot = InstaBot(username,password)
    bot.login()
    followers_href = []
    for user in users:
        bot.goto_profile(user)
        followers = bot.get_all_followers_usernames(start,limit)
        followers_href += bot.get_followers_href(user_list=followers)
    
    with open("followers.txt","w",encoding="utf8") as f:
        f.write("")
    
    file = open("followers.txt","a",encoding="utf8")
    for foll in followers_href:
        file.write(foll+",")
        
    file.close()       
    print("fetched all users")
    file = open("followers.txt","r",encoding="utf8")
    usernames = (file.read()).split(",")
    print(len(usernames))
    bot.close_driver()
    
    