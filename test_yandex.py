from selenium import webdriver
import pytest


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
    





class BrowserFactory():
    
            
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
    def test_sendKeys(self):
        pass
    

driver = BrowserFactory.getBrowser(BROWSERS[0])
driver = BrowserFactory.getBrowser(BROWSERS[0])

StartTests().runPositiveTests()
#if __name__ == "__main__":
#    driver = BrowserFactory.getBrowser(BROWSERS[0]) # тут вызов браузеров из жсона
#    