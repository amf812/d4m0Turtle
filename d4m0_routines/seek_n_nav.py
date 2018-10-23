"""
seek_n_nav.py

Started on: 19oct18 (or well that's when I remembered at add this note,
anyway)

routines for general seeking out of halite ore resources w/basic resource
location determination and navigation to it
"""

from operator import itemgetter

class FindApproach:
    def locate_nearest_base(current_ship, current_map, myself):
        """
        This will locate the closest dropoff we own in order to go drop off the
        halite ore.  I'm thinking that maybe more of a generalizing of the
        perimeter searching algorithm is in order, so that it can be used for
        this, as well as the ore location; keep from recreating the wheel, and
        all of that schitt.

        :param current_ship: derp
        :param current_map: also derp
        :param myself: the 'me' info hash from main d4m0Turtle
        :return: Position of the closest dropoff point
        """

        #for now we're just going to leave this as a stub that'll return the
        #first base, since I just want this active for testing purposes now
        #that it's time to try out the ore's perimeter search
        return myself.get_dropoff()

    def target_halite_simple(current_turtle, current_map, halite):
        """
        This method will, for now, just pick a mining location, preferring
        the highest quantity it can get, but dropping to the next ranked
        spot on the list, if there is already a turtle present.

        :param current_turtle:
        :param current_map:
        :param halite:
        :return: location to navigate to
        """

        for loc_data in sorted(halite, key=itemgetter('quantity'), reverse=True):
            if current_map[loc_data['position']].is_occupied:
                continue
            else:
                return loc_data['position']     #find a way to raise exception
                                                #if nothing is found
