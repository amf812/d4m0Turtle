"""
analytics.py

Started on: 19oct18 (or well that's when I remembered at add this note,
anyway)

Just a little bit of logic for making the game data a little more useful to
us for smarter (and quicker!) processing.
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
        relative_halite_positions: array of dicts, w/'position' & 'quantity'
    """

    #main routine has already determined whether or not we're too close to full
    #for this to be viable
    if myglobals.Constants.DEBUGGING['locate_ore']:
        myglobals.Wrap.log.info("Gathering information to seek halite ore intelligently")

    relative_halite_positions = [ ]

    if max_distance == 0:   #until we learn to override in python
        max_distance = myglobals.Constants.Maximal_Consideration_Distance

    if current_map[current_ship.position].halite_amount >= myglobals.Constants.Worth_Mining_Halite: #massage
        #add the current ship's position, if we need it
        if myglobals.Constants.DEBUGGING['perimeter_search']:   #technically not part of the perimeter, but #whadevah
            myglobals.Wrap.log.info("Checking original position")

        relative_halite_positions.append( { 'position': current_ship.position },
                                          { 'quantity': current_map[current_ship.position].halite_amount }, )

    else:
        #start at the 'top' of the grid
        current_search_position = PerimeterSearch.top_start(current_ship.position, max_distance)

        for downward_step in [0..max_distance - 1]:
            # start at the left
            current_search_position = PerimeterSearch.left_start(current_search_position, max_distance)

            if (downward_step == 0) or (downward_step == (max_distance - 1)):
                for right_step in [0..max_distance - 1]:    #aaaand move to the right
                    current_search_position = current_search_position.directional_offset(Direction.East)
                    relative_halite_positions.append( { 'position': current_search_position,
                                                        'quantity':
                                                            current_map[current_search_position].halite_amount }, )

                    if myglobals.Constants.DEBUGGING['perimeter_search']:
                        myglobals.Wrap.log.info("")

            else:
                #left perimeter edge for this row
                relative_halite_positions.append( { 'position': current_search_position,
                                                    'quantity':
                                                        current_map[current_search_position].halite_amount }, )

                #right perimeter edge for this row
                current_search_position = PerimeterSearch.right_margin(current_search_position, max_distance)
                relative_halite_positions.append( { 'position': current_search_position,
                                                    'quantity':
                                                        current_map[current_search_position].halite_amount }, )

    return relative_halite_positions

class PerimeterSearch:
    def left_start(search_pos, max_dist):
        """
        Simply bumps the search position to the far left of its grid area for this
        iteration and returns it.

        :param search_pos:
        :param max_dist:
        :return:
        """

        #start at the left, return the position where we can do this
        for ouah in [0..int(max_dist / 2)]:
            search_pos = search_pos.directional_offset(Direction.West)

        return search_pos

    def right_margin(search_pos, max_dist):
        """
        Moves from the far left of the grid boundary to the far right and returns
        the Position

        :param search_pos:
        :param max_dist:
        :return:
        """

        for ouah in [1..max_dist]:
            search_pos = search_pos.directional_offset(Direction.East)

        return search_pos

    def top_start(search_pos, max_dist):
        """
        Simply bumps the search position to the top of its grid area for this
        iteration and returns it.

        :param search_pos:
        :param max_dist:
        :return:
        """

        #start at the top, return the position, etc
        for ouah in [0..int(max_dist / 2)]:
            search_pos = search_pos.directional_offset(Direction.North)

        return search_pos

def locate_nearest_base(current_ship, current_map):
    """
    locates the closest base we own in order to go drop off the halite ore
    """

def sort_list_of_dicts_by_key(current_list, sort_key):
    """
    This will probably end up getting moved somewhere out of the analytics
    codebase here, as I end up with more generalized routines to go with it.
    Note that it expects that the value contained under the sort_key will be
    numeric, for sorting (derp).

    :param current_list:
    :param sort_key:
    :return: sorted list
    """

    new_list = current_list

    #I guess we'll just bubble sort for now; my motivation for remembering or
    #rediscovering a different algorithm is a little lacking; I really need to
    #try to get to that at some point, though, because speed demands will end
    #up making it pretty significant if this is heavily utilized
    for cntr in [0..len(current_list) - 2]:
        for cntr2 in [0..len(current_list) - 1]:
            if new_list[cntr2][sort_key] > new_list[cntr2 + 1][sort_key]:
                x = new_list[cntr2]
                y = new_list[cntr2 + 1]
                new_list[cntr2] = y
                new_list[cntr2 + 1] = x

    return new_list

