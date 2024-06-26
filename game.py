import json
import random

class GameData:
    def __init__(self, game_name : str, language = 'fr') -> None:
        with open('data/' + game_name + '/monsters_auto.json', encoding='utf-8') as monster_json :
            self.monster_data_raw = json.load(monster_json)

        with open('data/' + game_name + '/families.json', encoding='utf-8') as families_json :
            self.families_raw = json.load(families_json)
        # tryNone(table_line[7]).split("\u00a0\u2022") if 7 < len(table_line) else [None]
        self.monster_data = {}
        for monster_id in self.monster_data_raw:
            this_monster = self.monster_data_raw[monster_id]
            if len(this_monster) == 11:
                self.monster_data[monster_id] = {"name" : this_monster["name_" + language],
                                                "description" : this_monster["description_" + language] if this_monster["description_" + language] != None else this_monster["description_en"],
                                                "family" : self.families_raw[this_monster["family_id"]]["name_" + language],
                                                "rank" : this_monster["rank"],
                                                "traits" : this_monster["traits"],
                                                "resistance" : this_monster["resistance"],
                                                "weapons" : this_monster["weapons"],
                                                "skill" : this_monster["skill"],
                                                "location" : this_monster["location"]}
        print(str(len(self.monster_data)) + ' monstres chargés.')

    def test_error(self):
        for key in self.monster_data:
            for rekey in self.monster_data[key]:
                if self.monster_data[key][rekey] == '_' and key != '0':
                    print("Invalide info in " + str(key) + ' ' + str(self.monster_data[key]['name']))
        print("Fin du parcours d'erreurs")

    def getByName(self, name:str) -> dict:
        if name == "get_all":
            for key in self.monster_data:
                print(self.monster_data[key]["name"].lower())
            return None
        for key in self.monster_data:
            if self.monster_data[key]["name"].lower() == name.lower():
                return self.monster_data[key]
        return None

    def get_random_monster(self) -> dict:
        random_id = random.choice(list(self.monster_data.keys()))
        return self.monster_data[random_id]
    
    def get_count(self) -> int:
        return len(self.monster_data) -1
    
if __name__ == '__main__':
    print(GameData("joker_1").monster_data)