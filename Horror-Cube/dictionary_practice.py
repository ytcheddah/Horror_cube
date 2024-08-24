




# there are 4 collection data types:

# list          - ordered, changeable, allow duplicate values
#                   1           1           1       
# Tuple         - ordered, unchangeable, allow duplicate values
#                   1           0           1       
# set           - unordered, unchangeable, do NOT allow duplicate values
#                   0           0           0       
# Dictionary    - ordered, changeable, do NOT allow duplicate values
#                   1           1           0       

# When accessing a range of items in a list, the first number is INCLUSIVE and the last is EXCLUSIVE, Ex:
# print(list[2:5]) will print the third and fourth item in the list, and NOT the fifth.

#================================================================================================================#

pokedex = ['Bulbasaur', 'Ivysaur', 'Venesaur']


input1 = input(f'which pokemon would you like to see:\n\n1: {pokedex[0]}\n2: {pokedex[1]}\n3: {pokedex[2]}\n')

if input1 == '1':
    print(f'you picked {pokedex[0]}')
elif input1 == '2':
    print(f'you picked {pokedex[1]}')
elif input1 == '3':
    print(f'you picked {pokedex[2]}')
else:
    print('\n***invalid answer***\n')

print('\n')

#================================================================================================================#

types = ('Bug','Dark','Dragon','Electric','Fairy','Fighting','Fire',
         'Flying','Ghost','Grass','Ground','Ice','Normal','Poison','Psychic','Rock','Steel','Water')



# Nested Dictionary for pokedex makes the most sense when it comes to potential functionability
# .keys() and .values() will return the desired information, in this case the values
# will be another dictionary



dict_pokedex = {
    '1' : {
        'name': 'Bulbasaur',
        'type': [types[9],types[13]],
        'stats': [318, 45, 49, 49, 65, 65, 45],
        'ability': ['Overgrow','Chlorophyll'],
        'sprite' : 'N/A'
    },
    '2' : {
        'name': 'Ivysaur',
        'type': [types[9],types[13]],
        'stats': [405, 60, 62, 63, 80, 80, 60],
        'ability': ['Overgrow','Chlorophyll'],
        'sprite' : 'N/A'
    },
    '3' : {
        'name': 'Venusaur',
        'type': [types[9],types[13]],
        'stats': [525, 80, 82, 83, 100, 100, 80],
        'ability': ['Overgrow','Chlorophyll'],
        'sprite' : 'N/A'
    },   
}

input2 = input(f'which pokemon would you like to see:\n\n1: {dict_pokedex["1"]["name"]}\n2: {dict_pokedex["2"]["name"]}\n3: {dict_pokedex["3"]["name"]}\n')

if input2 == '1':
    print(f'you picked {dict_pokedex["1"]}')
elif input2 == '2':
    print(f'you picked {dict_pokedex["2"]}')
elif input2 == '3':
    print(f'you picked {dict_pokedex["3"]}')
else:
    print('\n***invalid answer***\n')

print('\n')

# Try to code a way to add a pokemon and all its stats into the Pokedex then print out a list of all pokemon in the pokedex
# as well as a list of all the pokemons associated data
# Extra Credit: Format the printed data from the pokemon
