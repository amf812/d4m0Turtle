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
    }

    Worth_Mining_Halite = 25  # int(constants.MAX_HALITE * 0.2)
    #Worth_Mining_Halite = int(constants.MAX_HALITE * 0.2)
    Maximal_Consideration_Distance = 5


#class Misc:
    # def sort_list_of_dicts_by_key(current_list, sort_key):
    #     """
    #     This will probably end up getting moved somewhere out of the analytics
    #     codebase here, as I end up with more generalized routines to go with it.
    #     Note that it expects that the value contained under the sort_key will be
    #     numeric, for sorting (derp).
    #
    #     :param current_list:
    #     :param sort_key:
    #     :return: sorted list
    #     """
    #
    #     #new_list = current_list
    #
    #     # I guess we'll just bubble sort for now; my motivation for remembering or
    #     # rediscovering a different algorithm is a little lacking; I really need to
    #     # try to get to that at some point, though, because speed demands will end
    #     # up making it pretty significant if this is heavily utilized
    #     for cntr in range(0, len(current_list) - 2):
    #         for cntr2 in range(0, len(current_list) - 1):
    #             if current_list[cntr2][sort_key] > current_list[cntr2 + 1][sort_key]:
    #                 x = current_list[cntr2]
    #                 y = current_list[cntr2 + 1]
    #                 current_list[cntr2] = y
    #                 current_list[cntr2 + 1] = x
    #
    #     return current_list
