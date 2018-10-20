from hlt import constants, game_map

import logging

"""
debugging and other constant values
"""

class Constants:
    DEBUGGING = {
        'seek': True,
        'locate_ore': True,
    }

    #constant schitt
    Worth_Mining_Halite = constants.MAX_HALITE - (constants.MAX_HALITE * 0.2)
    Maximal_Consideration_Distance = game_map.width / 2

