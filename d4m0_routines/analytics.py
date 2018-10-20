"""
analytics.py

"""

#from hlt import constants, game_map
from hlt.positionals import Direction, Position
from . import myglobals

#constant schitt should now be in myglobals
#Worth_Mining_Halite = constants.MAX_HALITE - (constants.MAX_HALITE * 0.2)
#Maximal_Consideration_Distance = game_map.width / 2

def locate_significant_halite(current_ship, current_map, max_distance):
    """
    Current algorithm idea:
    as noted in issue #2 on the github repo, I think that an expanding
    perimeter check will be the most efficient way to handle this, for now.
    We'll go out in expanding 1-cell thickness squares from the point of
    origin, stopping when a halite deposit within 20% of max is found, when
    the maximal distance from the origin is found, or reasonable defaults.

    Original Plan:
    if there isn't maximal halite on this very spot, this routine will
    locate at least 3 of the closest halite resources, with at least one being
    a maximal halite deposit (more than 3, until maximal deposit is located,
    perhaps up to a certain limit

    Args:
        current_ship: data for the current ship being processed
        current_map: the map's data after the most recent update
        max_distance: integer signifying how far from location to search

    Returns:


    """

    #main routine has already determined whether or not we're too close to full
    #for this to be viable

    relative_halite_positions = [ ]

    if max_distance == 0:   #until we learn to override in python
        max_distance = myglobals.Constants.Maximal_Consideration_Distance

    if current_map[current_ship.position].halite_amount >= myglobals.Constants.Worth_Mining_Halite:
        relative_halite_positions.append( { 'position': current_ship.position },
                                          { 'quantity': current_map[current_ship.position].halite_amount }, )

        #return { 'relative_halite' : relative_halite }
    else:
        #start snooping around
        cntr = 1
        current_search_position = Position(current_ship.position)

        for downward_step in [0..max_distance - 1]:
            if (downward_step == 1) or (downward_step == max_distance):
                #start at the left
                for ouah in [0..int(max_distance / 2)]:
                    current_search_position = current_search_position.directional_offset(Direction.West)

                for right_step in [0..max_distance - 1]:
                    current_search_position = current_search_position.directional_offset(Direction.East)
                    relative_halite_positions.append( { 'position': current_search_position,
                                                        'quantity': current_map[current_search_position].halite_amount }, )


def locate_nearest_base(current_ship, current_map):
    """
    locates the closest base we own in order to go drop off the halite ore
    """


