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

driver = webdriver.Chrome(options=chrome_options) # Initialize the webdriver session
actions = ActionChains(driver)


driver.get('https://www.4daagse.nl/meedoen/ticket-overdragen') # replaces "ie.navigate"

js_script = '''\
    for (element of document.getElementsByClassName('js-cookie-message')) {
        element.style.display = 'none'
    }
'''
driver.execute_script(js_script)

# open modal
buttons = driver.find_elements(By.CLASS_NAME, 'button')
for button in buttons:
    if button.text.find("beschikbare tickets") == -1: continue
    actions.move_to_element(button).click().perform();

time.sleep(2)

def tryRefresh(button):
    if button.text.find("nieuwen") != -1: 
        print("refresh")
        actions.move_to_element(button).click().perform();
    time.sleep(0.02)
    # Call the function again
    threading.Timer(0.02, lambda: tryRefresh(refreshButton)).start()

def tryBuy(driver):
    buttons = driver.find_elements(By.TAG_NAME, 'a')
    buyButton = None
    for button in buttons:
        if button.text.find("kopen") != -1:
            buyButton = button
            print("Buy button found")
        if button.text.find("serveerd") != -1:
            print("Gereserveerd")

    if buyButton != None: 
        print("kopen")
        actions.move_to_element(buyButton).click().perform();

    time.sleep(0.02)
    # Call the function again
    threading.Timer(0.02, lambda: tryBuy(driver)).start()

iframes = driver.find_elements(By.TAG_NAME, 'iframe')
for iframe in iframes:
    driver.switch_to.frame(iframe)
    buttons = driver.find_elements(By.TAG_NAME, 'a')
    refreshButton = None
    for button in buttons:
        if button.text.find("gewerkt") != -1 or button.text.find("nieuwen") != -1: 
            refreshButton = button

    if refreshButton != None:
        print("Refresh button found.")
        tryRefresh(refreshButton)
    
    tryBuy(driver)