import json
import random

class game_data:
    def __init__(self, game_name : str) -> None:
        self.monster_data = {}
        with open('data/' + game_name + '/monsters_auto.json') as monster_json :
            self.monster_data = json.load(monster_json)

    def test_error(self):
        for key in self.monster_data:
            for rekey in self.monster_data[key]:
                if self.monster_data[key][rekey] == '_' and key != '0':
                    print("Invalide info in " + str(key) + ' ' + str(self.monster_data[key]['name_en']))
        print("Fin du parcours d'erreurs")

    def getByName(self, name:str) -> dict:
        for key in self.monster_data:
            if self.monster_data[key]["name_en"].lower() == name.lower():
                return self.monster_data[key]
        return None

    def get_random_monster(self) -> dict:
        random_id = random.choice(list(self.monster_data.keys()))
        return self.monster_data[random_id]
    
    def get_count(self) -> int:
        return len(self.monster_data) -1
    
if __name__ == '__main__':
    print(game_data("joker_1").monster_data)