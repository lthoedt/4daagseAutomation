import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.chrome.options import Options
from twisted.internet import task, reactor
from threading import Thread
import threading

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

class Clicker: 

    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options) # Initialize the webdriver session
        self.actions = ActionChains(self.driver)

        self.driver.get('https://www.4daagse.nl/meedoen/ticket-overdragen') # replaces "ie.navigate"

        js_script = '''\
            for (element of document.getElementsByClassName('js-cookie-message')) {
                element.style.display = 'none'
            }
        '''
        self.driver.execute_script(js_script)

    # open modal
        buttons = self.driver.find_elements(By.CLASS_NAME, 'button')
        for button in buttons:
            if button.text.find("beschikbare tickets") == -1: continue
            self.actions.move_to_element(button).click().perform();

        time.sleep(2)

        iframes = self.driver.find_elements(By.TAG_NAME, 'iframe')
        for iframe in iframes:
            self.driver.switch_to.frame(iframe)
            buttons = self.driver.find_elements(By.TAG_NAME, 'a')
            refreshButton = None
            for button in buttons:
                if button.text.find("gewerkt") != -1 or button.text.find("nieuwen") != -1: 
                    refreshButton = button

            if refreshButton != None:
                print("Refresh button found.")
                self.tryRefresh(refreshButton)
            
            self.tryBuy()

    def tryRefresh(self, button):
        try :
            if button.text.find("nieuwen") != -1: 
                print("refresh")
                self.actions.move_to_element(button).click().perform();
        except:
            None

        time.sleep(0.02)
        # Call the function again
        threading.Timer(0.02, lambda: self.tryRefresh(button)).start()

    def tryBuy(self):
        try :
            buttons = self.driver.find_elements(By.TAG_NAME, 'a')
            buttons.extend(self.driver.find_elements(By.TAG_NAME, 'button'))
            buyButton = None
            for button in buttons:
                if button.text.lower().find("kopen") != -1:
                    buyButton = button
                    print("Buy button found")

            if buyButton != None: 
                print("kopen")
                self.actions.move_to_element(buyButton).click().perform()
        except:
            None

        time.sleep(0.005)
        # Call the function again
        threading.Timer(0.005, self.tryBuy).start()

refreshTimeout = 15
nTryers = 2

for i in range(nTryers):
    threading.Timer(0, lambda: Clicker()).start()
    time.sleep(refreshTimeout/nTryers)