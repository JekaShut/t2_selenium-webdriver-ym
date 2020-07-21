from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import json
import time
import random
import csv



with open('config.json') as config_file:
    data = json.load(config_file)


class ChromeBrowser():
    def runBrowser(self):
        driver = webdriver.Chrome()
        return(driver)

class FireFoxBrowser():
    def runBrowser(self):
        driver = webdriver.Firefox()
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
            if browsertype == "ChromeBrowser":
                driver = ChromeBrowser().runBrowser()
                driver.set_window_size(data['resolutionH'], data['resolutionW'])
                
                return(driver)
            if browsertype == "FireFoxBrowser":
                driver = FireFoxBrowser().runBrowser()
                driver.set_window_size(data['resolutionH'], data['resolutionW'])
                return(driver)
            raise AssertionError("Browser not found")
        except AssertionError as _e:
            print(_e)


        


class TestMainPage(BrowserFactory):
    def test_checkPage(self):
        #driver = BrowserFactory.getBrowser(browsertype)
        PAGE = "https://market.yandex.ru/"
        driver.get(PAGE) 
        TITLE = driver.title
        assert TITLE == "Яндекс.Маркет — выбор и покупка товаров из проверенных интернет-магазинов", "Название страницы не совпадает с ОР"
        
        

class TestAutorize(BrowserFactory):
    #wait = WebDriverWait(driver, 10)
    def test_checkPage(self):
        enter = driver.find_element_by_xpath("//span[contains(text(),'Войти')]/..")
        enter.click()
        handles = driver.window_handles
        driver.switch_to.window(handles[1])
        TITLE = driver.title 
        assert TITLE == "Авторизация", "Название страницы не совпадает с ОР"

    def test_sendKeys_login(self):
        login = data['login']
        loginfield = driver.find_element_by_id("passp-field-login")
        loginfield.send_keys(login)
        enter = driver.find_element_by_css_selector(".passp-sign-in-button")
        enter.click()
        #time.sleep(3)
        #wait = WebDriverWait(driver, 10)
        #InputPass = wait.until(EC.element_to_be_selected(driver.find_element_by_class_name("passp-form-field__label")))
        time.sleep(2)
        InputPass = driver.find_element_by_class_name("passp-form-field__label")    
        assert InputPass.text == "Введите пароль", "Название поля ввода пароля не совпадает с ОР"

    def test_sendKeys_password(self):
        password = data['password']
        InputPass = driver.find_element_by_id("passp-field-passwd")    
        InputPass.send_keys(password)
        enter = driver.find_element_by_css_selector(".passp-sign-in-button")
        enter.click()
        time.sleep(2)

    def test_checkAutorize(self):
        handle = driver.window_handles
        driver.switch_to.window(handle[0])
        #checkPage = driver.find_elements_by_xpath("//a/span/span")
        #assert checkPage[0].text == 'Избранное', "Название элемента не совпадает с ОР"
        
class TestCategiries(BrowserFactory):                                                                                         #ШАГ 3
    def test_getCategories(self):
        self.categories = driver.find_elements_by_xpath("//div/div[3]/noindex/div/div/div/div/div[1]/div[1]/div")
        self.categories.pop(0)
        randomcat = random.choice(self.categories)
        rndtxt = randomcat.find_element_by_xpath("div/a/span").text
        randomcat.click()
        time.sleep(2)
        TITLE = driver.find_element_by_tag_name("h1")
        assert rndtxt == TITLE.text, "Название категории '" + rndtxt + "' не совпадает с заголовком категории '" + TITLE.text + "'" 

class TestCategiriesAtMainPage():    
    def test_goToMainPage(self):
        time.sleep(2)
        TestMainPage().test_checkPage()
        categories = driver.find_elements_by_xpath("//div/div[3]/noindex/div/div/div/div/div[1]/div[1]/div")
        categories[0].click()
        time.sleep(4)
        
    def test_writeToCSV(self):
        n = 1
        categories = driver.find_elements_by_xpath("//div/div[3]/noindex/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[1]/div")
        
        with open("test.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow(["ID", "Element"])
            for element in categories:
                elementW = element.find_element_by_xpath("button/a/span")
                writer.writerow([n, elementW.text])
                n = n + 1

    def test_compareCategories(self):    
        x3 = []
        x6 = []                                                                                        #ШАГ 6
        with open("test.csv", "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                x3.append(row['Element'])

        categories = driver.find_elements_by_xpath("//div/div[3]/noindex/div/div/div/div/div[1]/div[1]/div")
        categories.pop(0)
        for cat in categories:
            catTXT = cat.find_element_by_xpath("div/a/span").text
            x6.append(catTXT)
        
        for elem in x6:
            assert elem in x3 == True, "Элемент '"+ elem +"' отсутствует в «Популярные категории»"

class TestLogOut(BrowserFactory):
    def test_logout(self):
        time.sleep(2)
        TestMainPage().test_checkPage()
        forDOM = driver.find_element_by_xpath("//div[6]/div/div/div/div/div/div/div/button")
        forDOM.click()
        time.sleep(1)
        exitsite = driver.find_element_by_xpath("//div[2]/a[6]/span")
        exitsite.click()
        
        
        
class TestStop(BrowserFactory):
    def test_seleniumQuit(self):
        time.sleep(2)
        driver.stop_client()
        driver.quit()    
    
class Start(metaclass=Singleton):
    def __init__(self):
        
        self.actualBrowser = data['actualBrowser']
        self.BROWSERS = data['BROWSERS'] 
        self.driver = BrowserFactory.getBrowser(self.BROWSERS[self.actualBrowser])
        
   
driver = Start().driver 


