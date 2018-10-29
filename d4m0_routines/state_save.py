"""
save_state.py

Started on: 28oct18

Class is going to be instantiated for each ship in order to provide access to
a bit of the history, their current mission status, and to provide useful
methods such as one to determine whether or not the ship has been in transit
to its destination for too long, being as my original (static method based)
algorithm wasn't working anyway.
"""

from . import myglobals


class StateSave:
    """
    Class holds the ship's relevant history for making smarter actions in the
    future
    """
    id = -1     # this will be set to something rational after init
    location = None
    destination = None
    turnstamp = -1
    # this will be set to something rational after init and setting
    # primary_mission; will then be compared to current turn to find out if
    # there's been too long of transit, etc
    current_mission = 'awaiting_orders'     # basically just 'transit' or not
    primary_mission = 'awaiting_orders'     # mining, dropoff, etc...

    def is_initialized(self):
        """
        Are we initialized?

        :return: boolean
        """
        if self.id == -1:
            return False
        else:
            return True

    def is_alive(self, me):
        """
        Are we representing a living ship?

        :param me:
        :return: boolean
        """
        if not self.is_initialized():
            return None     # an exception would be better here

        return me.has_ship(self.id)

    def is_transit_too_long(self, current_turn):
        """
        Has transit taken too long?

        :param current_turn:
        :return: boolean
        """
        return (current_turn - self.turnstamp) > myglobals.Const.Traveling_Too_Long

    def __init__(self, new_id, new_location, new_destination, new_turnstamp,
                 new_cmission, new_pmission):
        self.id = new_id
        self.location = new_location
        self.destination = new_destination
        self.turnstamp = new_turnstamp
        self.current_mission = new_cmission
        self.primary_mission = new_pmission

    def __str__(self):
        return "ship ID: " + str(self.id) + ", location: " + str(self.location) + ", destination: " \
               + str(self.destination) + ", turnstamp set: " + str(self.turnstamp) + ", current_mission: " + \
               self.current_mission + ", primary_mission: " + self.primary_mission

