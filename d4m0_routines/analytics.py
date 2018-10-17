"""
analytics.py

"""

from hlt import constants, game_map

#constant schitt
Worth_Mining_Halite = constants.MAX_HALITE - (constants.MAX_HALITE * 0.2)
Maximal_Consideration_Distance = game_map.width / 2

def locate_significant_halite(current_ship, current_map):
    """
    if there isn't maximal halite on this very spot, this routine will
    locate at least 3 of the closest halite resources, with at least one being
    a maximal halite deposit (more than 3, until maximal deposit is located,
    perhaps up to a certain limit
    """

    #main routine has already determined whether or not we're too close to full
    #for this to be viable

    relative_halite = { }
    positions = [ ]

    if current_map[current_ship.position].halite_amount >= Worth_Mining_Halite:
        relative_halite = { 'position' = [ current_ship.position ] }
        return { 'relative_halite' : relative_halite }
    else:
        #start snooping around
        for outward_step in [1..Maximal_Consideration_Distance]:
            if current_map[current_ship.position


def locate_nearest_base(current_ship, current_map):
    """
    locates the closest base we own in order to go drop off the halite ore
    """

