from game import GameData

joker_1 = GameData("joker_1")
selected_monster = joker_1.get_random_monster()
print(selected_monster["name"])

monster_ranks = ['Incarni', 'X', 'S', 'A', 'B', 'C', 'D', 'E', 'F']
# print(selected_monster)

def testRank(selected_rank, guess_rank) -> str :
    selected_rank_index = monster_ranks.index(selected_rank)
    guess_rank_index = monster_ranks.index(guess_rank)
    
    if guess_rank_index < selected_rank_index:
        return guess_rank + " \u21D8"
    elif guess_rank_index > selected_rank_index:
        return guess_rank + " \u21D7"
    else:
        return guess_rank + " \u2705"

def compareStats(stat_string, monster1, monster2):
    stat_1 = monster1[stat_string]
    stat_2 = monster2[stat_string]
    match stat_string:
        case "rank":
            return testRank(stat_1, stat_2)
        case _:
            if stat_1 == stat_2:
                return "\u2705"
            else:
                return '\u274C'

def takeAGuess():
    guess_name = str(input("Nom du monstre: "))
    guess_monster = joker_1.getByName(guess_name)
    if guess_monster == None:
        print("Invalide monster")
    return guess_monster

guessed_monster = takeAGuess()
while selected_monster != guessed_monster:
    if guessed_monster != None:
        print("Non !")

        for key in selected_monster:
            print(key + ':' + compareStats(key, selected_monster, guessed_monster))

    guessed_monster = takeAGuess()

print(f'Vous avez trouvé le monstre : {selected_monster["name"]}')
print(selected_monster["description"])