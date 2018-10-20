"""
myglobals.py

Started on: 19oct18 (or well that's when I remembered at add this note,
anyway)

Holds debugging and other constant values
"""

from hlt import constants, game_map
import logging

#import logging

class Constants:
    DEBUGGING = {
        'seek': True,
        'locate_ore': True,
        'perimeter_search': True,
    }

    #constant schitt
    Worth_Mining_Halite = constants.MAX_HALITE - (constants.MAX_HALITE * 0.2)
    Maximal_Consideration_Distance = game_map.width / 2

class Wrap:
    log = logging.getLogger(__name__)
