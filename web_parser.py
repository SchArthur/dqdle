from bs4 import BeautifulSoup
import requests
import json
from tqdm import tqdm   # Gestion des barres de chargement

monster_json_file = 'data/joker_1/monsters_auto.json'
monster_list_page = "https://dqmj.fandom.com/wiki/Monster_list"

requete = requests.get(monster_list_page)
page = BeautifulSoup(requete.text, 'html.parser')

def readTable(table_body) -> list:
    # for table_body in page.select("div.mw-parser-output table tbody")
    data = []
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    return data
    
""" 
"name_en" : "_",
"family_en" : "_",
"rank" : "_",
"description_en" : "_",
"weapons" : ["_"],
"traits" : ["_"],
"resistance" : ["_"],
"skill" : ["_"],
"location" : ["_"]   
 """


def tryNone(str):
    if str == "none" :
        return None
    else :
        return str


def parseMonster(table_line):
    url_solo = "https://dragon-quest.org/wiki/" + table_line[1].replace(" ", "_").replace("'", "%27")
    monster_requete = requests.get(url_solo)
    monster_page = BeautifulSoup(monster_requete.text, 'html.parser')

    # Trouver le <span> qui contient le texte "Dragon Quest Monsters: Joker"
    span = monster_page.find('span', string='Dragon Quest Monsters: Joker')

    # Trouver tous les <tbody> après ce <span>
    tbody_list = span.find_all_next('tbody') if span else []

    # Rechercher le <tbody> spécifique
    target_tbody = None
    for tbody in tbody_list:
        if tbody.find('tr', style='background:blue; color:white'):
            target_tbody = tbody
            break

    monster_dict = {}
    monster_dict["name_en"] = table_line[1]
    monster_dict["family_en"] = table_line[2]
    monster_dict["rank"] = table_line[3]
    monster_dict["traits"] = [tryNone(table_line[5]), tryNone(table_line[6])]
    monster_dict["resistance"] = tryNone(table_line[7]).split("\u00a0\u2022") if 7 < len(table_line) else [None]

    # Afficher le <tbody> trouvé
    if target_tbody != None :
        solo_wiki_data = readTable(target_tbody)
        monster_dict["description_en"] = solo_wiki_data[4][1]
        monster_dict["weapons"] = solo_wiki_data[5][1].split(", ")
        if len(monster_dict["weapons"]) == 1 :
            monster_dict["weapons"] = [solo_wiki_data[5][1]]
        elif len(monster_dict["weapons"]) == 0:
            monster_dict["weapons"] = [None]
        monster_dict["skill"] = solo_wiki_data[8][1].split(", ")
        if len(monster_dict["skill"]) == 1 :
            monster_dict["skill"] = [solo_wiki_data[8][1]]
        elif len(monster_dict["skill"]) == 0:
            monster_dict["skill"] = [None]
        monster_dict["location"] = solo_wiki_data[9][1].split(" (")[0]
        if len(monster_dict["location"]) == 1 :
            monster_dict["location"] = [solo_wiki_data[9][1]]
        elif len(monster_dict["location"]) == 0:
            monster_dict["location"] = [None]
    else:
        monster_dict["ERREUR"] = ["Erreur dans wiki solo", url_solo]

    return monster_dict


def saveJson(file, data : dict):
    with open(file, 'w', encoding ='utf8') as fp:
        json.dump(data, fp, indent=3)


monsters_data = {}        

lines = readTable(page.select("div.mw-parser-output table tbody")[0])
for i in tqdm(range(len(lines)), 
               desc="Téléchargement des monstres...", 
               ascii=False, ncols=75):
    line = lines[i]
    if len(line) > 2:
        monsters_data[line[0]] = parseMonster(line)

saveJson(monster_json_file, monsters_data)