"""
analytics.py

"""

from hlt import constants, game_map, positionals
from . import myglobals

import math

#constant schitt
Worth_Mining_Halite = constants.MAX_HALITE - (constants.MAX_HALITE * 0.2)
Maximal_Consideration_Distance = game_map.width / 2

class Halite_Position:
    def __init__(self, pos, ore_qty):
        self.pos = pos
        self.ore_qty = ore_qty


def locate_significant_halite(current_ship, current_map):
    """
    if there isn't maximal halite on this very spot, this routine will
    locate 3 of the closest halite resources, with at least one being
    a maximal halite deposit
    """

    #main routine has already determined whether or not we're too close to full
    #for this to be viable

    relative_halite = { }
    positions = { }

    if current_map[current_ship.position].halite_amount >= Worth_Mining_Halite:
        relative_halite = { 'position' = [ current_ship.position ] }
        return { 'relative_halite' : relative_halite }
    else:
        #start snooping around
        start_x = math.modf(-Maximal_Consideration_Distance / 2)[1]
        start_y = start_x
        end_x = -startx
        end_y = -startx
        cur_pos = Position(current_ship.position)
 
        for x in [start_x..end_x]:
            if x == start_x:
                #test the entire line
                for y in [start_y..end_y]:
                    
        


def locate_nearest_base(current_ship, current_map):
    """
    locates the closest base we own in order to go drop off the halite ore
    """

