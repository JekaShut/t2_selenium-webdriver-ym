from selenium import webdriver
import pytest
import json
import time

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
        assert TITLE == "Яндекс.Маркет — выбор и покупка товаров из проверенных интернет-магазинов", "Название страницы не совпадает с ОР"
        
        

class TestAutorize(BrowserFactory):
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
        time.sleep(3)
        InputPass = driver.find_element_by_class_name("passp-form-field__label")    
        assert InputPass.text == "Введите пароль", "Название поля ввода пароля не совпадает с ОР"

    def test_sendKeys_password(self):
        password = data['password']
        InputPass = driver.find_element_by_id("passp-field-passwd")    
        InputPass.send_keys(password)
        enter = driver.find_element_by_css_selector(".passp-sign-in-button")
        enter.click()
        time.sleep(5)

    def checkAutorize(self):
        handle = driver.window_handles
        driver.switch_to.window(handle[0])
        TITLE = driver.find_element_by_xpath("/html/head/title[2]")
        assert TITLE == "Яндекс.Маркет", "Название страницы не совпадает с ОР"
        checkPage = driver.find_elements_by_xpath("//a/span/span")
        assert checkPage[0].text == 'Избранное', "Название элемента не совпадает с ОР"
        
        
        
    
class Start(metaclass=Singleton):
    def __init__(self):
        self.actualBrowser = data['actualBrowser']
        self.BROWSERS = data['BROWSERS']
        self.driver = BrowserFactory.getBrowser(self.BROWSERS[self.actualBrowser])
        
        
driver = Start().driver




#driver = BrowserFactory.getBrowser(BROWSERS[0])
#driver1 = BrowserFactory.getBrowser(BROWSERS[0])

#StartTests().runPositiveTests()
#if __name__ == "__main__":
#    driver = BrowserFactory.getBrowser(BROWSERS[0]) # тут вызов браузеров из жсона
#    