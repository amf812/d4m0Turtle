"""
seek_n_nav.py

Started on: 19oct18 (or well that's when I remembered at add this note,
anyway)

routines for general seeking out of halite ore resources w/basic resource
location determination and navigation to it
"""


def locate_nearest_base(current_ship, current_map, myself):
    """
    This will locate the closest dropoff we own in order to go drop off the
    halite ore.  I'm thinking that maybe more of a generalizing of the
    perimeter searching algorithm is in order, so that it can be used for
    this, as well as the ore location; keep from recreating the wheel, and
    all of that schitt.

    :param current_ship:
    :param current_map:
    :param myself:
    :return: Position of the closest dropoff point
    """

    #for now we're just going to leave this as a stub that'll return the
    #first base, since I just want this active for testing purposes now
    #that it's time to try out the ore's perimeter search
    return myself.get_dropoff(1)


#def def_target_halite_simple(current_turtle, halite_ranked_by_distance, halite_ranked_by_qty):
