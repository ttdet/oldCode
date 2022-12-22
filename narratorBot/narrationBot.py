from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import random


class bot():
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.get("https://www.douyu.com")
        self.wait = WebDriverWait(self.browser, 5)
        with open("mrz.txt", "r") as f:
            self.data = f.read()

    def findLastPunc(self, start):
        c = start
        while self.data[c] != '，' and self.data[c] != '。' and self.data[c] != '！' and self.data[c] != '？' and self.data[c] != '：' and self.data[c] != '“' and self.data[c] != '”' and self.data[c] != '；':
            c -= 1

        c+=1
        return c


    def runBot(self):
        self.browser.get('https://www.douyu.com/topic/S11JJBD_3?rid=12306')
        i = 0
        while i < len(self.data):
            end = self.findLastPunc(i+40)
            substring = self.data[int(i):int(end)]
            textBox = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ChatSend-txt')))
            textBox.send_keys(substring)
            i += end
            sleep(random.randint(4,6) + random.random())
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ChatSend-button'))).click()
            print(substring+"\n")
            sleep(random.randint(10,12) + random.random())


    def start_login(self):
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'UnLogin-icon'))).click()
        ver = input("欢迎来到吉吉国！\n请登录。登录完成后，输入‘1’。若想终止程序，输入任何别的字符。\n")
        if ver == '1':
            self.runBot()
        else:
            self.browser.quit()


def main():
    a = bot()
    a.start_login()

if __name__ == '__main__':
    main()
