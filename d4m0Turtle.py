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

# Import the Halite SDK, which will let you interact with the game.
import hlt
import random
import logging

from hlt import Position, Direction

# d4m0 imports
from d4m0_routines import analytics, seek_n_nav, myglobals, primary

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
        # d4m0 schitt starts

        # is this ship already in transit to mine?
        try:
            #everything at this block level has already had mission assigned
            if myglobals.Variables.current_assignments[ship.id] and myglobals.Const.DEBUGGING['core']:
                logging.debug(" Determining status of ship " + str(ship.id))

            myglobals.Misc.loggit('save_state', 'debug', "  - ship id: " + str(ship.id) + " has state set to " +
                                  myglobals.Variables.current_assignments[ship.id]['mission'])

            # I did things this way because of the potential for adding moar
            # assignment types, this may be changed for efficiency in the near
            # future
            # so what the fsck is it supposed to ACTUALLY DO? - not sure, so
            # it's just getting commented out for now
            #elif myglobals.Variables.current_assignments[ship.id]['mission'] != 'mining' \
            #        and myglobals.Variables.current_assignments[ship.id]['mission'] != 'transit' \
            #        and myglobals.Variables.current_assignments[ship.id]['mission'] != 'dropoff':

            #    # we should be good to send it on its way
            #    if myglobals.Const.DEBUGGING['save_state'] or myglobals.Const.DEBUGGING['core']:
            #        logging.info("  - Ship id: " + str(ship.id) + "  ready for mission.")

            #    # so yeah, now we incorporate the whether or not to mine/dropoff
            #    # block (now in analytics) with new indent levels
            #    cmd_n_dest = analytics.Analyze.can_we_embark_and_start_mining(ship, game_map, me)
            #    command_queue.append(cmd_n_dest['c_queue_addition'])

            #    myglobals.Misc.save_ship_state(ship.id, 'transit', turn, cmd_n_dest['destination'])

            #    if myglobals.Const.DEBUGGING['save_state'] or myglobals.Const.DEBUGGING['core']:
            #        logging.debug(" - updated former unset state to new transit: " + str(cmd_n_dest['destination']))

            if myglobals.Variables.current_assignments[ship.id]['mission'] == 'transit':
                # have we been a ramblin'?
                potential_cmd = primary.Core.has_transit_been_too_long(turn, ship, game_map, me)
                if not potential_cmd:
                    potential_cmd = primary.Core.transit_processing_done_or_not(ship, game_map, turn, me)

                if potential_cmd:
                    command_queue.append(potential_cmd)
                    continue
            elif myglobals.Variables.current_assignments[ship.id]['mission'] == 'get_minimum_distance':
                if ship.position == myglobals.Variables.current_assignments[ship.id]['destination']:
                    #we're here, now seek out the best halite

                elif (turn - myglobals.Variables.current_assignments[ship.id]['turn']) < \
                        (myglobals.Const.Maximal_Consideration_Distance * 2):
                    #continue minimum distance transit
                    command_queue.append(ship.move(game_map.
                                                   naive_navigate(ship, myglobals.Variables.
                                                                        current_assignments[ship.id]['destination'])))
                else:
                    #we've been ramblin' too long, just look for the halite now
                    
            else:   # we must be set for dropoff; check and make sure that we're done nao
                myglobals.Misc.loggit('core', 'info', "  - in transit to: " +
                                      str(myglobals.Variables.current_assignments[ship.id]['destination']))
                command_queue.append(ship.move(game_map.naive_navigate(ship,
                                                                       myglobals.Variables.
                                                                       current_assignments[ship.id]['destination'])))
                myglobals.Misc.save_ship_state(ship.id, 'transit', turn,
                                               myglobals.Variables.current_assignments[ship.id]['destination'])

        except KeyError:
            logging.debug("In KeyError try/except loop")

            if not ship.is_full:    # if nothing is set, this should ALWAYS be the case
                # for testing purposes right now we'll just send out mining no matter what;
                # but first, we need to get to a minimum distance away
                target = ship.position
                rdir = random.choice([ Direction.North, Direction.South, Direction.East, Direction.West ])
                for cntr in range(0, myglobals.Const.Maximal_Consideration_Distance):
                    target = Position(target).directional_offset(rdir)

                myglobals.Misc.save_ship_state(ship.id, 'get_minimum_distance', turn, target)
                #relative_halite = analytics.Analyze.locate_significant_halite(ship, game_map)
                #target = seek_n_nav.FindApproach.target_halite_simple(ship, game_map, relative_halite)
            else:
                target = seek_n_nav.FindApproach.locate_nearest_base(ship, game_map, me)
                myglobals.Misc.save_ship_state(ship.id, 'transit', turn, target)

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

