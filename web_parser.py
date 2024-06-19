from bs4 import BeautifulSoup
import requests

monster_list_page = "https://dqmj.fandom.com/wiki/Monster_list"

requete = requests.get(monster_list_page)
page = BeautifulSoup(requete.text, 'html.parser')

def read_table() -> list:
    for table_body in page.select("div.mw-parser-output table tbody"):
        data = []
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        return data
        
for line in read_table():
    if len(line) > 2:
        print(line[1])