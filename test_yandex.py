from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
#from webdrivermanager import ChromeDriverManager
import pytest
import json
import time
import random
import csv



with open('config.json') as config_file:
    data = json.load(config_file)
    
BROWSERS = ["ChromeBrowser", "FireFoxBrowser"]
class JsonGetter():
    def __init__(self):    
        
        
        self.actualBrowser = data["actualBrowser"]
        self.login = data["login"]
        self.password = data["password"]
        self.SITE = data["SITE"]

get = JsonGetter() 

class ChromeBrowser():
    def runBrowser(self):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        return(driver)

class FireFoxBrowser():
    def runBrowser(self):
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        return(driver)
    

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]



class BrowserFactory(metaclass=Singleton):        
    @staticmethod
    def getBrowser(browsertype):
        
        try:
            if browsertype == BROWSERS[BROWSERS.index(browsertype)]:
                
                driver = ChromeBrowser().runBrowser()
                #driver.set_window_size(get.resolutionH, get.resolutionW)
                driver.maximize_window()
                
                return(driver)
            if browsertype == BROWSERS[BROWSERS.index(browsertype)]:
                driver = FireFoxBrowser().runBrowser()
                #driver.set_window_size(get.resolutionH, get.resolutionW)
                driver.maximize_window()
                return(driver)
            raise AssertionError("Browser not found")
        except AssertionError as _e:
            print(_e)


        


class TestMainPage():
    def test_checkPage(self):
        PAGE = get.SITE
        driver.get(PAGE) 
        TITLE = driver.title
        assert TITLE == "Яндекс.Маркет — выбор и покупка товаров из проверенных интернет-магазинов", "Название страницы не совпадает с ОР"
        
        

class TestAutorize():
    def test_checkPage(self):
        enter = driver.find_element_by_xpath("//span[contains(text(),'Войти')]/..")
        enter.click()
        handles = driver.window_handles
        driver.switch_to.window(handles[1])
        TITLE = driver.title 
        assert TITLE == "Авторизация", "Название страницы не совпадает с ОР"

    def test_sendKeys_login(self):
        login = get.login
        loginfield = driver.find_element_by_id("passp-field-login")
        loginfield.send_keys(login)
        enter = driver.find_element_by_css_selector(".passp-sign-in-button")
        enter.click()
        time.sleep(2)
        InputPass = driver.find_element_by_class_name("passp-form-field__label")  
        assert InputPass.text == "Введите пароль", "Название поля ввода пароля не совпадает с ОР"

    def test_sendKeys_password(self):
        time.sleep(1)
        password = get.password
        InputPass = driver.find_element_by_id("passp-field-passwd")  
        InputPass.send_keys(password)
        enter = driver.find_element_by_css_selector(".passp-sign-in-button")
        enter.click()
        time.sleep(2)

    def test_checkAutorize(self):
        handle = driver.window_handles
        driver.switch_to.window(handle[0])
        menuButton = driver.find_element_by_xpath("//div[6]/div/div/div/div/div/div/div/button")
        menuButton.click()
        time.sleep(2)
        checkAuth = driver.find_element_by_xpath("//div[6]/div/div/div/div/div/div/div/div/div[2]")
        assert checkAuth.text == get.login, "Логин не соответствует ожидаемому"
        
class TestCategiries(BrowserFactory):  
                                                                                        
    def test_getCategories(self):
        self.categories = driver.find_elements_by_xpath("//div/div[3]/noindex/div/div/div/div/div[1]/div[1]/div")
        self.categories.pop(0)
        randomcat = random.choice(self.categories)
        rndtxt = randomcat.find_element_by_xpath("div/a/span").text
        randomcat.click()
        time.sleep(2)
        TITLE = driver.find_element_by_tag_name("h1")
        assert rndtxt == TITLE.text, "Название категории '" + rndtxt + "' не совпадает с заголовком категории '" + TITLE.text + "'" 
csvData = ["ID", "Element"] 
class TestCategiriesAtMainPage():    
      
    def test_goToMainPage(self):
        time.sleep(2)
        TestMainPage().test_checkPage()
        categories = driver.find_elements_by_xpath("//div/div[3]/noindex/div/div/div/div/div[1]/div[1]/div")
        categories[0].click()
        time.sleep(2)
        
    def test_writeToCSV(self):
        n = 1
        categories = driver.find_elements_by_xpath("//div/div[3]/noindex/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[1]/div")
        
        with open("test.csv", "w", newline="", encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow(csvData)
            for element in categories:
                elementW = element.find_element_by_xpath("button/a/span")
                writer.writerow([n, elementW.text])
                n = n + 1

    def test_compareCategories(self):    
        x3 = []
        x6 = []                                                                                        
        with open("test.csv", "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                x3.append(row[csvData[1]])

        categories = driver.find_elements_by_xpath("//div/div[3]/noindex/div/div/div/div/div[1]/div[1]/div")
        categories.pop(0)
        for cat in categories:
            if cat.is_displayed(): #13
                catTXT = cat.find_element_by_xpath("div/a/span").text
                x6.append(catTXT)
        
        for elem in x6:
            assert elem in x3 == True, "Элемент '"+ elem +"' отсутствует в «Популярные категории»"
            

class TestLogOut():
    def test_logout(self):
        time.sleep(2)
        TestMainPage().test_checkPage()
        forDOM = driver.find_element_by_xpath("//div[6]/div/div/div/div/div/div/div/button")
        forDOM.click()
        time.sleep(1)
        exitsite = driver.find_element_by_xpath("//div[2]/a[6]/span")
        exitsite.click()
        try:
            enter = driver.find_element_by_xpath("//span[contains(text(),'Войти')]/..").text
        except:
            enter = "logged in"
        assert enter == "Войти"
        
        
class TestStop():
    def test_seleniumQuit(self):
        time.sleep(2)
        driver.stop_client()
        driver.quit()    
    
class Start(metaclass=Singleton):
    def __init__(self):
        
        self.actualBrowser = get.actualBrowser
        if self.actualBrowser in BROWSERS:
            BROWSERindex = BROWSERS.index(self.actualBrowser)
        else:
            raise Exception("Такого браузера нет!")
        self.driver = BrowserFactory.getBrowser(BROWSERS[BROWSERindex])
        
   
driver = Start().driver 


