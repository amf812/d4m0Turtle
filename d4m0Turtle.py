#!/usr/bin/env python3
# Python 3.6

"""
d4m0Turtle.py

Started on: 19oct18 (or well that's when I remembered at add this note,
anyway)

Just my first attempt at getting a bot going decently in the Halite III AI
coding competition; still have 2.75 months left to go on it right now.  So
I guess the estimated final version has to be in right around the middle of
January.  Good project to keep me busy in winter, and to get my skills up to
the best level they can be (at least in py3).
"""

import hlt

import random
import logging
import traceback
import sys

from hlt import Position, Direction

# d4m0 imports
from d4m0_routines import analytics, seek_n_nav, state_save, myglobals, primary

""" <<<Game Begin>>> """

game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("D4m0Turtle")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
myglobals.Misc.loggit('any', 'info', "Successfully hatched! My Player ID is {}.".format(game.my_id))

# d4m0's init stuff
turn = 0

""" <<<Game Loop>>> """

while True:
    myglobals.Misc.loggit('core', 'info', " - updating frame")
    game.update_frame()

    myglobals.Misc.loggit('core', 'info', " - updating 'me'")
    # keeps things speedier
    me = game.me

    myglobals.Misc.loggit('core', 'info', " - updating 'game_map'")
    # speed, again (see if there are any places to implement anything like
    # this with my own structs)
    game_map = game.game_map

    myglobals.Misc.loggit('core', 'info', " - initializing 'command_queue'")
    command_queue = []

    myglobals.Misc.loggit('core', 'debug', " -* me.get_ships() dump: " + str(me.get_ships()))

    for ship in me.get_ships():
        # is this ship already in transit to mine?
        try:
            # we'll bounce to 'except' if this is a new ship
            if myglobals.Variables.current_assignments[ship.id]['primary_mission'] \
                    and myglobals.Const.DEBUGGING['core']:
                logging.debug(" Determining status of ship " + str(ship.id))

            # everything at this block level has already had mission assigned, so
            # long as it makes it past the conditional statement w/out going to
            # 'except'

            myglobals.Misc.loggit('save_state', 'debug', "  - ship id: " + str(ship.id) + " has state set to " +
                                  myglobals.Variables.current_assignments[ship.id]['primary_mission'] + ": " +
                                  myglobals.Variables.current_assignments[ship.id]['current_mission'])

            if myglobals.Variables.current_assignments[ship.id]['current_mission'] == 'transit':
                # have we been a ramblin'?
                myglobals.Misc.loggit('core', 'debug', "  - checking to see if ship id: " + str(ship.id) +
                                      " has been a ramblin' man...")

                if primary.Core.check_for_too_long_transit(turn, ship.id):
                    # set new mission & destination; add try/except-- if exception is found, we need to expand the
                    # perimeter for searches (as well as exclude already searched spots) and try again
                    new_dest = seek_n_nav.FindApproach.target_halite_simple(ship, game_map,
                                                                            analytics.Analyze.
                                                                            locate_significant_halite(ship, game_map))
                    myglobals.Variables.current_assignments[ship.id]['destination'] = new_dest
                    myglobals.Variables.current_assignments[ship.id]['position'] = ship.position
                    myglobals.Variables.current_assignments[ship.id]['turnstamp'] = turn
                    myglobals.Variables.current_assignments[ship.id]['current_assignment'] = 'transit'
                    myglobals.Variables.current_assignments[ship.id]['primary_assignment'] = 'mining'
                    myglobals.Misc.loggit('core', 'debug', "Resetting due to too long of transit: " +
                                          str(myglobals.Variables.current_assignments[ship.id]))
                else:
                    continue
            # the following is now redundant
            # elif myglobals.Variables.current_assignments[ship.id]['primary_mission'] == 'get_minimum_distance' and \
            #         (turn - myglobals.Variables.current_assignments[ship.id]['turnstamp']) > \
            #         myglobals.Const.Traveling_Too_Long:     # NOTE: is this conditional w/'turns' right?
            #
            #     myglobals.Misc.loggit('core', 'debug', "  - continuing minimum distance transit for ship id: " +
            #                           str(ship.id))
            #     command_queue.append(primary.Core.minimum_distance_processing(turn, ship, game_map))

            else:   # we must be set for dropoff; check and make sure that we're done nao
                # TODO: continue debugging at this point
                myglobals.Misc.loggit('core', 'info', "  - in transit to: " +
                                      str(myglobals.Variables.current_assignments[ship.id]['destination']))
                command_queue.append(ship.move(game_map.naive_navigate(ship,
                                                                       myglobals.Variables.
                                                                       current_assignments[ship.id]['destination'])))
                myglobals.Misc.save_ship_state(ship.id, 'transit', turn,
                                               myglobals.Variables.current_assignments[ship.id]['destination'])

        except KeyError as ke:
            # TODO: verify new ship mission seeking code

            logging.debug("In KeyError try/except loop: " + str(ke.__traceback__))
            logging.debug("Line No: " + str(ke.__traceback__.tb_lineno))

            if not ship.is_full:    # if nothing is set, this should ALWAYS be the case
                # for testing purposes right now we'll just send out mining no matter what;
                # but first, we need to get to a minimum distance away
                target = ship.position
                rdir = random.choice([ Direction.North, Direction.South, Direction.East, Direction.West ])
                for cntr in range(0, myglobals.Const.Maximal_Consideration_Distance):
                    target = target.directional_offset(rdir)

                myglobals.Variables.current_assignments[ship.id] = \
                    state_save.StateSave.get_save_ship_state(ship.id, me, 'get_minimum_distance', turn, target, turn)
                myglobals.Misc.loggit('core', 'debug', " - ship id: " + str(ship.id) + " getting minimum distance at :"
                                      + str(target))
            else:
                # how in the hell did we end up here?
                raise Exception("Uninitialized StateSave for ship id " + str(ship.id) + " is full?!?")
                #target = seek_n_nav.FindApproach.locate_nearest_base(ship, game_map, me)
                #myglobals.Misc.save_ship_state(ship.id, 'transit', turn, target)
                #myglobals.Misc.loggit('core', 'debug', " - ship id: " + str(ship.id) + " *not sure how we ended up " +
                #                      "here, but now we're heading to " + str(target) + " for dropoff after transit")

            command_queue.append(ship.move(game_map.naive_navigate(ship, target)))

        # d4m0 schitt ends

        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        #if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:
        #    command_queue.append(
        #        ship.move(
        #            random.choice([ Direction.North, Direction.South, Direction.East, Direction.West ])))

    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if (game.turn_number <= 200) and (me.halite_amount > myglobals.Const.Enough_Ore_To_Spawn) and \
            (not game_map[me.shipyard].is_occupied):
        command_queue.append(me.shipyard.spawn())

    # d4m0 end of turn schitt
    turn += 1

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)

