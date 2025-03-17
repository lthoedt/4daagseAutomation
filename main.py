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
        self.isBuying = False

        self.driver.get('https://www.4daagse.nl/meedoen/ticket-overdragen') # replaces "ie.navigate"

        js_script = '''\
            document.getElementById('CybotCookiebotDialogBodyUnderlay').style.display = 'none';
            document.getElementById('CybotCookiebotDialog').style.display = 'none';
            document.getElementsByTagName("body")[0].style.overflow = 'visible';
        '''
        print("Cookie dialog hidden")
        self.driver.execute_script(js_script)

    # open modal
        buttons = self.driver.find_elements(By.CLASS_NAME, 'button')
        for button in buttons:
            if button.text.strip().find("Zoek ticket") == -1: continue
            print("Zoek ticket button found")
            self.actions.move_to_element(button).click().perform();

        time.sleep(2)

        iframes = self.driver.find_elements(By.TAG_NAME, 'iframe')
        for iframe in iframes:
            self.driver.switch_to.frame(iframe)
            buttons = self.driver.find_elements(By.TAG_NAME, 'a')
            refreshButton = None
            for button in buttons:
                if button.text.find("gewerkt") != -1 or button.text.find("nieuwen") != -1 or button.text.find("fresh") != -1: 
                    refreshButton = button

            self.tryBuy()
            
            if refreshButton != None:
                print("Refresh button found.")
                self.tryRefresh(refreshButton)

    def tryRefresh(self, button):
        try :
            if button.text.find("nieuwen") != -1 or (button.text.find("Refresh") != -1 & button.text.find("Refreshed") == -1): 
                print("refresh")
                self.actions.move_to_element(button).click().perform();
        except:
            if self.isBuying == False:
                buttons = self.driver.find_elements(By.TAG_NAME, 'a')
                for btn in buttons:
                    if btn.text.find("gewerkt") != -1 or btn.text.find("nieuwen") != -1 or btn.text.find("fresh") != -1: 
                        button = btn

        time.sleep(0.02)
        # Call the function again
        threading.Timer(0.02, lambda: self.tryRefresh(button)).start()

    def tryBuy(self):
        try :
            buttons = self.driver.find_elements(By.TAG_NAME, 'a')
            buttons.extend(self.driver.find_elements(By.TAG_NAME, 'button'))
            buyButton = None
            for button in buttons:
                if button.text.lower().find("kopen") != -1 or button.text.lower().find("buy") != -1:
                    buyButton = button
                    print("Buy button found")
                    self.isBuying = False

            if buyButton != None: 
                print("kopen")
                self.isBuying = True
                self.actions.move_to_element(buyButton).click().perform()
        except:
            None

        time.sleep(0.005)
        # Call the function again
        threading.Timer(0.005, self.tryBuy).start()

refreshTimeout = 15
nTryers = 1

for i in range(nTryers):
    threading.Timer(0, lambda: Clicker()).start()
    time.sleep(refreshTimeout/nTryers)