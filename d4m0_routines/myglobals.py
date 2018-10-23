"""
myglobals.py

Started on: 19oct18 (or well that's when I remembered at add this note,
anyway)

Holds debugging and other constant values
"""

import hlt
from hlt import constants


class Const:
    DEBUGGING = {
        'core': False,
        'seek': True,
        'locate_ore': True,
        'perimeter_search': True,
        'save_state': True,
    }

    Worth_Mining_Halite = 25  # int(constants.MAX_HALITE * 0.2)
    # Worth_Mining_Halite = int(constants.MAX_HALITE * 0.2)
    Maximal_Consideration_Distance = 5

# Class Misc:
