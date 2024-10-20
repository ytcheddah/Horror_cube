import pygame
import math
import sys
from game.settings import *

monster_dict = { # used for the monster base stats/info
    "Angremlin" : {
        "name": "Angremlin",
        "health": 500,
        "speed": 2,
        "agro_type": ("Sight","Sound"),
        "agro_dist": 400,
    },
    "the_Carne": {
        "name": "the Carne",
        "health": 200,
        "speed": 3,
        "agro_type": ("Sight"),
        "agro_dist": 500,
    },
    "the_Filth": {
        "name": "the Filth",
        "health": 2000,
        "speed": .5,
        "agro_type": ("Sound", "Location"),
        "agro_dist": 400,
    },
    "Louis": {
        "name": "Louis",
        "health": 300,
        "speed": 1,
        "agro_type": ("Sight","Sound","Location"),
        "agro_dist": 600,
    },
    "Squihomie": {
        "name": "Squihomie",
        "health": 750,
        "speed": 1,
        "agro_type": ("Sound"),
        "agro_dist": 1000,
    },
    "Umo": {
        "name": "Umo",
        "health": 400,
        "speed": 1,
        "agro_type": ("Sight","Sound"),
        "agro_dist": 800,
    },
    "Zenba": {
        "name": "Zenba",
        "health": 1000,
        "speed": .5,
        "agro_type": ("Sound"),
        "agro_dist": 800,
    }  
}