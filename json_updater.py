import json
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

def merge_two_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z

class jsonUpdater():
    def __init__(self, json_file) -> None:
        self.file = json_file

    def saveAndSort(self, updated_json):
        with open("data/joker_1/monsters_auto.json", 'w', encoding='utf8') as f:
            print(updated_json)
            json.dump(updated_json, f, indent=3, ensure_ascii=False)

    def mergeFiles(self, file_to_merge):
        with open(self.file, encoding ='utf8') as f:
            data1 = json.load(f)
        with open(file_to_merge, encoding ='utf8') as f: 
            data2 = json.load(f)

        new_data = self.mergeMonsterInfos(data1, data2)

        self.saveAndSort(new_data)
        
    def updateFromDict(self, new_data : dict):
        with open(self.file, 'r', encoding ='utf8') as json_file:
            json_old = json.load(json_file)
            json_new = self.mergeMonsterInfos(json_old, new_data)

        self.saveAndSort(json_new)

    def mergeMonsterInfos(self, old_data, new_data):
        return_data = {}
        for key in old_data :
            return_data[key] = merge_two_dicts(old_data[key], new_data[key])
        return return_data

    def setTableUrl(self, url):
        driver = webdriver.Chrome()
        self.requete = driver.get(url)
        time.sleep(5)
        html = driver.page_source
        self.page = BeautifulSoup(html, 'html.parser')
        driver.quit()

    def setTbody(self, select_param : str) -> list:
        self.tbody = self.page.select(select_param)[0]
        return self.readTable()

    def readTable(self) -> list:
        data = []
        rows = self.tbody.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        return data

joker_french = jsonUpdater("data/joker_1/monsters.json")
joker_french.setTableUrl("https://wikidragonquest.fr/Liste_des_monstres_de_Dragon_Quest_Monsters:_Joker")
tbody = joker_french.setTbody("table.standard.cmonstre.sortable.jquery-tablesorter")

new_data = {}
for line in tbody:
    if len(line) == 5:
        monster_id = line[0]
        monster_nom = line[1]
        monster_description = line[4]
        new_data[line[0]] = {"name_fr" : monster_nom,
                            "description_fr" : monster_description}
    elif len(line) == 4:
        monster_id = line[0]
        monster_nom = line[1]
        monster_description = "NO FR DESCRIPTION"
        new_data[line[0]] = {"name_fr" : monster_nom,
                             "description_fr" : monster_description}

joker_french.updateFromDict(new_data)
print("ENDED")