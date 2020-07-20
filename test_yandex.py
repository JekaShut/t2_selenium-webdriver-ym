from selenium import webdriver
import pytest
import json
import time

with open('config.json') as config_file:
    data = json.load(config_file)



################################################
#
BROWSERS = ["ChromeBrowser", "FireFoxBrowser"]
#
################################################


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
                return(driver)
            if browsertype == "FireFoxBrowser":
                driver = FireFoxBrowser().runBrowser()# duplicating?
                return(driver)
            raise AssertionError("Browser not found")
        except AssertionError as _e:
            print(_e)


        
class StartTests():
    def runPositiveTests(self):
        TestMainPage().test_checkPage()
        pass

class TestMainPage(BrowserFactory):
    def test_checkPage(self):
        #driver = BrowserFactory.getBrowser(browsertype)
        PAGE = "https://market.yandex.ru/"
        driver.get(PAGE) 
        TITLE = driver.title
        assert TITLE == "Яндекс.Маркет — выбор и покупка товаров из проверенных интернет-магазинов"
        
        

class TestAutorize(BrowserFactory):
    def test_checkPage(self):
        enter = driver.find_element_by_xpath("//span[contains(text(),'Войти')]/..")
        enter.click()
        handles = driver.window_handles
        driver.switch_to.window(handles[1])
        TITLE = driver.title 
        assert TITLE == "Авторизация"
    def test_sendKeys_login(self):
        login = data['login']
        password = data['password']
        loginfield = driver.find_element_by_id("passp-field-login")
        loginfield.send_keys(login)
        enter = driver.find_element_by_css_selector(".passp-sign-in-button")
        enter.click()
        time.sleep(1)
        x = 1
        while x == 1:
            try :
                InputPass = driver.find_element_by_id("passp-field-passwd")
                x = 0
            except:
                time.sleep(3)
                x = 1
        InputPass.send_keys(password)
        enter = driver.find_element_by_css_selector(".passp-sign-in-button")
        enter.click()
        time.sleep(5)
        handle = driver.window_handles
        driver.switch_to.window(handle[0])
        checkPage = driver.find_elements_by_xpath("//a/span/div/span")
        assert checkPage[1].text == 'e2.shut'
        
        
        
    
class Start(metaclass=Singleton):
    def __init__(self):
        self.actualBrowser = data['actualBrowser']
        self.driver = BrowserFactory.getBrowser(BROWSERS[self.actualBrowser])
        
        
driver = Start().driver




#driver = BrowserFactory.getBrowser(BROWSERS[0])
#driver1 = BrowserFactory.getBrowser(BROWSERS[0])

#StartTests().runPositiveTests()
#if __name__ == "__main__":
#    driver = BrowserFactory.getBrowser(BROWSERS[0]) # тут вызов браузеров из жсона
#    