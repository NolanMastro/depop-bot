import os
import random
import traceback
import requests
import datetime
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

load_dotenv()

if not os.environ["LOGIN"]:
    raise Exception("LOGIN not set. Please enter your login information in .env variable 'LOGIN' in the following format: 'EMAIL:PASSWORD'")
else:
    ACCOUNT = os.environ["LOGIN"].replace(" ", "").split(",")
if not os.environ["SLEEP"]:
    raise Exception("SLEEP not set, please enter a time to sleep inbetween actions in the .env file.")
else:
    SLEEP_TIME = os.environ["SLEEP"]
    SLEEP_TIME = int(SLEEP_TIME)
if not os.environ["WAITTIME"]:
    raise Exception("WAITTIME not set, please enter a time to sleep after following in the .env file (this number should be very big) in seconds!")
else:
    WAITTIME = os.environ["WAITTIME"]
    WAITTIME = int(WAITTIME)



DESCRIBING_WORDS = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'black', 'white', 'vintage', 'used', 'grey', 'discount', 'brown']
SEARCHTERMS = ['stussy', 'fleece', 'obey', 'nike', 'hoodie', 'rick owens', 'bape', 'dunks', 'pants', 'cargos', 'crewnecks', 'sherpa', 'puffer', 'north face', 'affliction', 'carhartt', 'dickies', 'patagonia', 'converse', 'blazers', 'nike sweatshirt', 'stussy shirt', 'vest', 'golf']


def login(EMAIL, PASSWORD, driver):
    try:
        #accept cookies
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/button[2]').click()
    except:
        print("Failed to click accept cookies.")
    try:
        #enter username and password fields
        driver.find_element(By.ID, 'username').send_keys(EMAIL)
        sleep(random.randint(0,1))
        driver.find_element(By.ID, 'password').send_keys(PASSWORD)
    except:
        try:
            #wait for page to load.
            username_field = driver.find_element(By.ID, value='username')
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(username_field)
            )
            username_field.send_keys(EMAIL)
            driver.find_element(By.ID, 'password').send_keys(PASSWORD)
        except:
            print("Failed sign in, goodbye.")
    #click login button
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/form/button').click()
    print("Logged in.")
    sleep(SLEEP_TIME)


def get_following(driver):
    try:
        #go to own profile
        sleep(SLEEP_TIME)
        driver.find_element(By.CSS_SELECTOR, '#mainNavigation > li:nth-child(6) > div > div > button').click()
        driver.find_element(By.CSS_SELECTOR, '#userNavItem > a:nth-child(1)').click()
        sleep(2)
        #get following
        elem = driver.find_element(By.CSS_SELECTOR, '#main > div:nth-child(1) > div.styles__FollowsContainer-sc-__r941b9-6.cDHEId > div > button:nth-child(2) > p.sc-jqUVSM.styles__StatsValue-sc-__sc-1hm9q0m-0.cZBwWq.iDhVgb')
        following = elem.text.strip()
        global untilmax
        untilmax = 7400 - int(following)
        print(f'{untilmax} followers until max is reached.')
    except:
        pass
    if untilmax  <= 0:
        print("Starting unfollow.")
        unfollow(driver)


def search_term(driver):
    try:
        #search a term
        termtosearch = random.choice(DESCRIBING_WORDS) + ' ' + random.choice(SEARCHTERMS)
        driver.find_element(By.XPATH, '/html/body/div/div/header/div/div[2]/div/form/input').send_keys(termtosearch)
        sleep(random.randint(1,2))
        elem = driver.find_element(By.XPATH, '/html/body/div/div/header/div/div[2]/div/form/input')
        elem.send_keys(Keys.ENTER)
        sleep(random.randint(1,2))
        print(f"Searched {termtosearch}.")
    except:
        pass
    sleep(SLEEP_TIME)


def click_search(driver):
    clicked_search = False
    while clicked_search == False:
        try:
            #click a random listing
            num = random.randint(1,4)
            num = str(num)
            driver.find_element(By.CSS_SELECTOR, f'#main > div.Container-sc-__sc-1t5af73-0.SearchResultsContainer-sc-__sc-1e6uh47-0.gpIZuU.cfcYJn > div > ul > li:nth-child({num}) > div > a > div > div.styles__ProductImageGradient-sc-__sc-13q41bc-6.fSYbNP').click()
            sleep(random.randint(1,3))
            clicked_search = True
        except:
            pass
    sleep(SLEEP_TIME)


def get_info(driver):
    try:
        #click heart
        driver.find_element(By.CSS_SELECTOR, '#main > div.styles__Layout-sc-__sc-1fk4zep-5.iohQdO > div:nth-child(3) > div > div.styles__Desktop-sc-__sc-1fk4zep-4.eXhFrK > div.ProductInteractionstyles__ProductInteractionContainer-sc-__sc-1uq597j-0.dySLZK > button.ButtonMinimal-sc-__crp04f-0.ProductInteractionstyles__ProductInteractionButton-sc-__sc-1uq597j-1.ProductInteractionstyles__ProductInteractionLikeButton-sc-__sc-1uq597j-2.fZhHkY.hybhGH.ikyvQb > svg').click()
        sleep(random.randint(1,2))
        #click username
        driver.find_element(By.CSS_SELECTOR, '#main > div.styles__Layout-sc-__sc-1fk4zep-5.iohQdO > div:nth-child(3) > div > div.styles__Desktop-sc-__sc-1fk4zep-4.eXhFrK > div.styles__BioContainer-sc-__imzomr-1.bUrkoo.styles__StyledBio-sc-__sc-1fk4zep-8.BkkJT > div.styles__BioUserDetails-sc-__imzomr-2.gNApzb > div > span > a').click()
        sleep(random.randint(1,2))
        #get name
        global name
        elem = driver.find_element(By.CSS_SELECTOR, '#main > div:nth-child(1) > div.styles__UserInformationContainer-sc-__r941b9-0.bQEsqy > div > p')
        name = elem.text.strip()
        #check if already following them
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, '#main > div:nth-child(1) > div.styles__FollowsContainer-sc-__r941b9-6.cDHEId > div > button.sc-gFGZVQ.iiUPen.styles__SmallButton-sc-__sc-1ryjds-0.efhKVl').click()
    except:
        pass
    sleep(SLEEP_TIME)


def get_their_info(driver):
    global theirfollowers
    try:
        #get their followers
        elem = driver.find_element(By.CSS_SELECTOR, '#main > div:nth-child(1) > div.styles__FollowsContainer-sc-__r941b9-6.cDHEId > div > button:nth-child(1) > p.sc-jqUVSM.styles__StatsValue-sc-__sc-1hm9q0m-0.cZBwWq.iDhVgb')
        theirfollowers = elem.text.strip().replace('K', '000')
        theirfollowers = int(theirfollowers)
    except:
        theirfollowers = 0
        pass
    sleep(SLEEP_TIME)
    

def follow_them(driver, untilmax):
    print(f"Found user, {name} starting following.")
    #follow their followers
    if theirfollowers < 20:
        how_many_to_follow = theirfollowers
    else:
        how_many_to_follow = 20
    driver.find_element(By.XPATH, '/html/body/div/div/main/div[1]/div[2]/div/button[1]').click()
    sleep(random.randint(2,3))
    count = 1
    print(f"Following {name}'s followers {how_many_to_follow} times.")
    while count < how_many_to_follow:
        try:
            elem = driver.find_element(By.CSS_SELECTOR, f'#followers-tab > div > div > div:nth-child({count}) > button')
            WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(elem)
                )
            button = elem.text.strip()
            if button == "Following":
                count = count+1
                continue
            else:   
                elem.click()
                count = count+1
                untilmax = untilmax-1
                clear = lambda: os.system('cls')
                clear()
                print(f"Followed {count}/{how_many_to_follow} of {name}'s followers.")
                sleep(0.5)
        except:
            pass
    print(f"Still {untilmax} follows left until unfollow starts. ")
        
    #click x
    driver.find_element(By.XPATH, '/html/body/div[2]/div/aside/div[1]/button/div').click()
    print(f"Done with {name}, repeating.")
    sleep(SLEEP_TIME)
    if untilmax  <= 0:
        print("Starting unfollow.")
        unfollow(driver)


def unfollow(driver):
    try:
        #go to own profile
        sleep(SLEEP_TIME)
        driver.find_element(By.CSS_SELECTOR, '#mainNavigation > li:nth-child(6) > div > div > button').click()
        driver.find_element(By.CSS_SELECTOR, '#userNavItem > a:nth-child(1)').click()
        sleep(2)
        #get following
        elem = driver.find_element(By.CSS_SELECTOR, '#main > div:nth-child(1) > div.styles__FollowsContainer-sc-__r941b9-6.cDHEId > div > button:nth-child(2) > p.sc-jqUVSM.styles__StatsValue-sc-__sc-1hm9q0m-0.cZBwWq.iDhVgb')
        following = elem.text.strip()
        following = int(following) + 1
        sleep(2)
        #go to following
        driver.find_element(By.CSS_SELECTOR, '#main > div:nth-child(1) > div.styles__FollowsContainer-sc-__r941b9-6.cDHEId > div > button:nth-child(2)').click()
    except:
        pass
    print(f"Sleeping to allow time for people to follow back, sleeping for {WAITTIME} seconds.")
    sleepcount = 1
    while sleepcount < WAITTIME:
        clear = lambda: os.system('cls')
        clear()
        print(f"Sleeping: {sleepcount}/{WAITTIME}")
        sleepcount = sleepcount+1
        sleep(1)
    counter = 1
    print(f'Unfollowing {round(following)} followers.')
    try:
        while counter < following:
            elem = driver.find_element(By.CSS_SELECTOR, f'#following-tab > div > div > div:nth-child({counter}) > button')
            WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(elem)
                )
            elem.click()
            counter = counter +1
            clear = lambda: os.system('cls')
            clear()
            print(f"Unfollowed {counter}/{round(following)}.")
            sleep(0.3)
    except:
        pass
        

    try:
        driver.find_element(By.CSS_SELECTOR, '#modal__headerWrapper > button > div').click()
        sleep(1)
        elem = driver.find_element(By.CSS_SELECTOR, '#main > div:nth-child(1) > div.styles__FollowsContainer-sc-__r941b9-6.cDHEId > div > button:nth-child(2) > p.sc-jqUVSM.styles__StatsValue-sc-__sc-1hm9q0m-0.cZBwWq.iDhVgb')
        following = elem.text.strip()
        global untilmax
        untilmax = 7400 - int(following)
        driver.find_element(By.CSS_SELECTOR, '#globalHeader > div > a > span > svg').click()
        sleep(SLEEP_TIME)
    except:
        pass

    
def main():
    #get account email/pass
    for x in ACCOUNT:
        colonIndex = x.index(":")+1
        EMAIL = x[0:colonIndex-1]
        PASSWORD = x[colonIndex:len(x)]
    options = webdriver.ChromeOptions()
    driver = driver = webdriver.Chrome(service=Service(ChromeDriverManager(cache_valid_range=30).install()),options=options)
    driver.get("https://www.depop.com/login/")
    login(EMAIL, PASSWORD, driver)
    sleep(random.randint(1,2))
    while True:
        get_following(driver)
        search_term(driver)
        click_search(driver)
        get_info(driver)
        get_their_info(driver)
        follow_them(driver, untilmax)





main()
