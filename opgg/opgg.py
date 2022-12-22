from selenium import webdriver
import requests
import numpy as np
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

deft_url = 'https://www.op.gg/summoner/userName=%EC%9D%B4%EB%A6%84%EB%B3%80%EA%B2%BD%EC%88%9C%EC%84%9C1'
t1_url = 'https://www.op.gg/summoner/userName=T1+Gumayusi'

class opgg:
    def __init__(self):
        self.op = Options()
        self.op.add_argument('--headless')
        self.browser = webdriver.Chrome(options = self.op)
        self.wait = WebDriverWait(self.browser, 10)
        self.pd = pd.DataFrame(index = np.arange(0,1500), columns = ['result', 'champion', 'd', 'f', 'mainRune', 'minorRune', 'kill', 'death', 'assist', 'player'])

    def getPage(self, url, name):
        self.browser.get(url)
        self.wait.until(EC.presence_of_element_located((By.ID, 'right_gametype_soloranked'))).click()
        loadTryTime, loadMaxTryTime = 0, 64
        while loadTryTime < loadMaxTryTime:
            try:
                sleep(2.5)
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'GameMoreButton'))).click()
                print(loadTryTime)
                loadTryTime += 1
            except:
                self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")

        gameTryTime, gameMaxTryTime = 0, 1240
        gameItemLists = self.browser.find_elements(By.CLASS_NAME, 'GameItemList')
        for gameItemList in gameItemLists:
            flag = False
            gameItems = gameItemList.find_elements(By.CLASS_NAME, 'GameItemWrap')
            for gameItem in gameItems:
                if gameTryTime >= gameMaxTryTime:
                    flag = True
                    break
                gameRes = gameItem.find_element(By.CLASS_NAME, 'GameResult')
                self.pd.iloc[gameTryTime]['result'] = gameRes.text

                champion = gameItem.find_element(By.CLASS_NAME, 'ChampionName')
                self.pd.iloc[gameTryTime]['champion'] = champion.text

                spells = gameItem.find_elements(By.CLASS_NAME, 'Spell')
                spell_count = 0
                for spell in spells:
                    spell_img = spell.find_element(By.CLASS_NAME, 'Image')
                    if spell_count == 0:
                        self.pd.iloc[gameTryTime]['f'] = spell_img.get_attribute('alt')
                    elif spell_count == 1:
                        self.pd.iloc[gameTryTime]['d'] = spell_img.get_attribute('alt')
                    spell_count += 1

                runes = gameItem.find_elements(By.CLASS_NAME, 'Rune')
                rune_count = 0
                for rune in runes:
                    rune_img = rune.find_element(By.CLASS_NAME, 'Image')
                    if rune_count == 0:
                        self.pd.iloc[gameTryTime]['mainRune'] = rune_img.get_attribute('alt')
                    elif rune_count == 1:
                        self.pd.iloc[gameTryTime]['minorRune'] = rune_img.get_attribute('alt')
                    rune_count += 1

                kill = gameItem.find_element(By.CLASS_NAME, 'Kill')
                self.pd.iloc[gameTryTime]['kill'] = int(kill.text)
                death = gameItem.find_element(By.CLASS_NAME, 'Death')
                self.pd.iloc[gameTryTime]['death'] = int(death.text)
                assist = gameItem.find_element(By.CLASS_NAME, 'Assist')
                self.pd.iloc[gameTryTime]['assist'] = int(assist.text)

                if name == 'deft':
                    self.pd.iloc[gameTryTime]['player'] = 0
                elif name == 'gmys':
                    self.pd.iloc[gameTryTime]['player'] = 1
                print(str(gameTryTime) + '\n')
                gameTryTime += 1

            if flag == True:
                break

    def return_mat(self):
        return self.pd



'''
deft = opgg()
deft.getPage(deft_url, 'deft')
deft_data = deft.return_mat()
deft_data.to_csv('deft2.csv')
'''
guma = opgg()
guma.getPage(t1_url, 'gmys')
gmys_data = guma.return_mat()
gmys_data.to_csv('gumayushi2.csv')
