from selenium import webdriver
import requests
import numpy as np
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from pyquery import PyQuery as pq


Wayne_url = 'https://www.op.gg/summoner/userName=jkjkjkjkk'

class opgg:
    def __init__(self):
        self.op = Options()
        self.op.add_argument('--headless')
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)
        self.pd = pd.DataFrame(index = np.arange(0,1240), columns = ['result', 'champion', 'd', 'f', 'mainRune', 'minorRune', 'kill', 'death', 'assist', 'player', 'item1', 'item2', 'item3', ''])

    def getDataSource(self, url):
        self.browser.get(url)
        self.wait.until(EC.presence_of_element_located((By.ID, 'right_gametype_soloranked'))).click()
        loadTryTime, loadMaxTryTime = 0, 25
        while loadTryTime < loadMaxTryTime:
            try:
                sleep(1.5)
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'GameMoreButton'))).click()
                print(loadTryTime)
                loadTryTime += 1
            except:
                self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")

        return self.browser.page_source

    def DataSource2DataFrame(self, data_source, name):
        matches_data = pq(data_source)

        gameTryTime, gameMaxTryTime = 0, 500

        gameItemLists = matches_data('.GameItemList').items()

        for gameItemList in gameItemLists:
            flag = False
            gameItems = gameItemList('.GameItemWrap').items()
            for gameItem in gameItems:
                if gameTryTime >= gameMaxTryTime:
                    flag = True
                    break

                self.pd.iloc[gameTryTime]['result'] = gameItem('.GameResult').text()

                self.pd.iloc[gameTryTime]['champion'] = gameItem('.ChampionName').text()

                spells = gameItem('.Spell').items()
                spell_count = 0
                for spell in spells:
                    spell_img = spell('.Image')
                    if spell_count == 0:
                        self.pd.iloc[gameTryTime]['f'] = spell_img.attr('alt')
                    elif spell_count == 1:
                        self.pd.iloc[gameTryTime]['d'] = spell_img.attr('alt')
                    spell_count += 1

                runes = gameItem('.Rune').items()
                rune_count = 0
                for rune in runes:
                    rune_img = rune('.Image')
                    if rune_count == 0:
                        self.pd.iloc[gameTryTime]['mainRune'] = rune_img.attr('alt')
                    elif rune_count == 1:
                        self.pd.iloc[gameTryTime]['minorRune'] = rune_img.attr('alt')
                    rune_count += 1


                self.pd.iloc[gameTryTime]['kill'] = int(gameItem('.KDA .KDA .Kill').text())

                self.pd.iloc[gameTryTime]['death'] = int(gameItem('.KDA .KDA .Death').text())

                self.pd.iloc[gameTryTime]['assist'] = int(gameItem('.KDA .KDA .Assist').text())

                items = gameItem('.Item').items()
                item_count = 1
                for item in items:
                    try:
                        item_img = item('img')
                        if item_count == 1:
                            self.pd.iloc[gameTryTime]['item1'] = item_img.attr('alt')
                        elif item_count == 2:
                            self.pd.iloc[gameTryTime]['item2'] = item_img.attr('alt')
                        elif item_count == 3:
                            self.pd.iloc[gameTryTime]['item3'] = item_img.attr('alt')
                        elif item_count == 4:
                            self.pd.iloc[gameTryTime]['item4'] = item_img.attr('alt')
                        elif item_count == 5:
                            self.pd.iloc[gameTryTime]['item5'] = item_img.attr('alt')
                        elif item_count == 6:
                            self.pd.iloc[gameTryTime]['item6'] = item_img.attr('alt')

                        item_count += 1

                    except:
                        if item_count == 1:
                            self.pd.iloc[gameTryTime]['item1'] = 'no item'
                        elif item_count == 2:
                            self.pd.iloc[gameTryTime]['item2'] = 'no item'
                        elif item_count == 3:
                            self.pd.iloc[gameTryTime]['item3'] = 'no item'
                        elif item_count == 4:
                            self.pd.iloc[gameTryTime]['item4'] = 'no item'
                        elif item_count == 5:
                            self.pd.iloc[gameTryTime]['item5'] = 'no item'
                        elif item_count == 6:
                            self.pd.iloc[gameTryTime]['item6'] = 'no item'

                        item_count += 1



                if name == 'Wayne':
                    self.pd.iloc[gameTryTime]['player'] = 0
                elif name == 'gmys':
                    self.pd.iloc[gameTryTime]['player'] = 1

                print('fetching match ' + str(gameTryTime))
                gameTryTime += 1

            if flag == True:
                break

    def getDataFrame(self):
        return self.pd



Wayne = opgg()
Wayne_data = Wayne.getDataSource(Wayne_url)
Wayne_matches = Wayne.DataSource2DataFrame(Wayne_data, Wayne)
Wayne.getDataFrame().to_csv('Wayne2.csv')
