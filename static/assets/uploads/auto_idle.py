from selenium import webdriver
import time
import pyautogui

driver = webdriver.Chrome(executable_path=r"C:\\Users\\TPC-User\\Downloads\\chromedriver_win32 (3)\\chromedriver.exe")
driver.get('https://www.google.com/')

# Open a new window
driver.execute_script('window.open("");')
# Switch to the new window
driver.switch_to.window(driver.window_handles[1])
driver.get("http://stackoverflow.com")
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the page.
        driver.implicitly_wait(10) # seconds
        new_height = driver.execute_script("return document.body.scrollHeight")
    
        if new_height == last_height:
            break
        last_height = new_height
        # sleep for 30s
        driver.implicitly_wait(10) # seconds
time.sleep(40)

# Open a new window
driver.execute_script("window.open('');")
# Switch to the new window
driver.switch_to.window(driver.window_handles[2])
driver.get("https://stackoverflow.com/questions/41271299/how-can-i-get-the-first-two-digits-of-a-number")
# time.sleep(10)
# while True:
#     # Scroll down
#     pyautogui.scroll(-300)
#     time.sleep(5)
driver.close()
time.sleep(20)

# Open a new window
driver.execute_script("window.open('');")
# Switch to the new window
driver.switch_to.window(driver.window_handles[3])
driver.get("https://www.google.com/")
# while True:
#     # Scroll down
#     pyautogui.scroll(-300)
#     time.sleep(10)
# time.sleep(10)
# close the active tab
# driver.close()
time.sleep(10)

driver.execute_script("window.open('');")
# Switch to the new window
driver.switch_to.window(driver.window_handles[4])
driver.get("https://www.odoo.com/forum/help-1/how-to-call-a-javascript-function-from-odoo-86782")
# while True:
#     # Scroll down
#     pyautogui.scroll(-300)
#     time.sleep(10)
# time.sleep(10)
# close the active tab
# driver.close()
time.sleep(10)