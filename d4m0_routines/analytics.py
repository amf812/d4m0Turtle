"""
analytics.py

Started on: 19oct18 (or well that's when I remembered at add this note,
anyway)

Just a little bit of logic for making the game data a little more useful to
us for smarter (and quicker!) processing.
"""

#import hlt

from hlt.positionals import Direction, Position
from operator import itemgetter
from . import myglobals

import logging


class Analyze:
    def locate_significant_halite(current_ship, current_map):
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
        if myglobals.Const.DEBUGGING['locate_ore']:
            logging.info("Gathering information to seek halite ore intelligently")

        relative_halite_positions = [ ]

        max_distance = myglobals.Const.Maximal_Consideration_Distance

        # start at the 'top' of the grid
        current_search_position = PerimeterSearch.top_start(current_ship.position, max_distance)

        for downward_step in range(0, (max_distance - 1)):  # [0..max_distance - 1]:
            # start at the left
            current_search_position = PerimeterSearch.left_start(current_search_position, max_distance)

            if (downward_step == 0) or (downward_step == (max_distance - 1)):
                for right_step in range(0, (max_distance - 1)):  # [0..max_distance - 1]:    #aaaand move to the right
                    current_search_position = current_search_position.directional_offset(Direction.East)

                    if myglobals.Const.DEBUGGING['perimeter_search']:
                        logging.info("Checking for ore at position: " + str(current_search_position))
                        logging.info(" * found " + str(current_map[current_search_position].halite_amount) + \
                                     " ore")

                    relative_halite_positions.append({'position': current_search_position,
                                                      'quantity':
                                                          current_map[current_search_position].halite_amount}, )

            else:
                # left perimeter edge for this row
                relative_halite_positions.append({'position': current_search_position,
                                                  'quantity':
                                                      current_map[current_search_position].halite_amount}, )

                # right perimeter edge for this row
                current_search_position = PerimeterSearch.right_margin(current_search_position, max_distance)
                relative_halite_positions.append({'position': current_search_position,
                                                  'quantity':
                                                      current_map[current_search_position].halite_amount}, )

        #sort that shit, don't leave it all messy
        #relative_halite_positions = myglobals.Misc.sort_list_of_dicts_by_key(relative_halite_positions, 'quantity')
        #if myglobals.Const.DEBUGGING['perimeter_search']:
        #    logging.info("Sorting perimeter search results")
        #relative_halite_positions = sorted(relative_halite_positions, key=itemgetter('quantity'), reverse=True)

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
        for ouah in range(0, int(max_dist / 2)):    #[0..int(max_dist / 2)]:
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

        for ouah in range(1, max_dist):
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

        zero = 0

        #start at the top, return the position, etc
        for cntr in range(0, int(max_dist / 2)): #[0..max_dist / 2]:
            search_pos = search_pos.directional_offset(Direction.North)

        return search_pos



