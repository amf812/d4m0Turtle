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


class Variables:
    current_assignments = { }   # ships' states, indexed by 'id'


class Misc:
    @staticmethod
    def save_ship_state(id, mission, turnstamp, destination):
        """
        This will just save the ship's particular state, at least for a
        certain number of turns before updating.

        It occurs to me while deciding that this bit of work needs to be
        handled in its own method that, perhaps, it would be a good idea to
        create a wrapper class for the individual ships.  I don't know how
        much of a performance penalty there might be for such, but if it's
        not too bad, it'd be a lot easier serializing the objects, or
        portions thereof, if it were laid out this way, and would probably
        save some confusion when looking at parallel structures for ship
        related data.

        :param id: ship's id
        :param mission: currently supported are: mining, transit, and dropoff
        :param turnstamp: turn # when this information was last set
        :param destination: current operation coordinates or destination
                            coordinates
        :return:
        """

        Variables.current_assignments[id] = { 'mission': mission, 'turnstamp': turnstamp, 'destination': destination, }

        return
