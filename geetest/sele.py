from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome()
url = 'https://www.zhihu.com/explore'
browser.get(url)
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')



#use js to open a window: window.open()

# browser.forward()
# browser.back()
# browser.close()
# browser.switch_to_window(browser.window_handles[1]) handles start at 0

# wait = WebDriverWait(browser, 10)   where 10 is the maximum response time
# input = wait.until(EC.presence_of_element_located((By.ID, 'q')))
# button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))
# other methods of EC:
# text_to_be_present_in_element()
# http://selenium-python.readthedocs.io
