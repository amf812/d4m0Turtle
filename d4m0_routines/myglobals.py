"""
myglobals.py

Started on: 19oct18 (or well that's when I remembered at add this note,
anyway)

Holds debugging and other constant values
"""

import logging
import hlt
from hlt import constants


class Const:
    DEBUGGING = {
        'core': True,
        'seek': True,
        'locate_ore': True,
        'perimeter_search': True,
        'save_state': True,
    }

    Worth_Mining_Halite = 25  # int(constants.MAX_HALITE * 0.2)
    # Worth_Mining_Halite = int(constants.MAX_HALITE * 0.2)
    Maximal_Consideration_Distance = 5
    Enough_Ore_To_Spawn = 2000
    Traveling_Too_long = 5  #this times Maximal_Consideration_Distance is the
    # limit for number of turns to get to the destination


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

    @staticmethod
    def loggit(debugging_type, log_level, log_message):
        """
        I've got to say, I'm getting pretty sick of having to type in the
        whole if myglobals.Const.DEBUGGING['blah']: and logging() bits every
        time that I need to throw something into the log.  While this method
        won't be suitable for logging based on multiple Const.DEBUGGING flags,
        most of the ones I'm using are based on a single flag, so this will
        make things a lot easier for adding more, code maintainability, etc.

        :param debugging_type: see Const.DEBUGGING flags ('any' also works)
        :param log_level: debug, info, and any are implemented so far
        :param log_message: message to throw into the log @ log_level
        :return:
        """

        if debugging_type == 'any' or Const.DEBUGGING[debugging_type]:
            if log_level == 'debug' or log_level == 'any':
                logging.debug(log_message)
            elif log_level == 'info' or log_level == 'any':
                logging.info(log_message)
            else:
                raise RuntimeError("Log level specified is not implemented in myglobals.Misc.loggit()")

        return
