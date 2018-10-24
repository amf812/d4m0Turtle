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

import logging

# d4m0 imports
from d4m0_routines import analytics, seek_n_nav, myglobals

""" <<<Game Begin>>> """

game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("D4m0Turtle")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully hatched! My Player ID is {}.".format(game.my_id))

# d4m0's init stuff
turn = 0
# current_assignments = { } NOTE: this got moved to myglobals.Variables

""" <<<Game Loop>>> """

while True:
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    if myglobals.Const.DEBUGGING['core']:
        logging.info("-init-")
        logging.info(" - updating frame")

    game.update_frame()

    if myglobals.Const.DEBUGGING['core']:
        logging.info(" - updating 'me'")
    # keeps things speedier
    me = game.me

    if myglobals.Const.DEBUGGING['core']:
        logging.info(" - updating 'game_map'")
    # speed, again (see if there are any places to implement anything like
    # this with my own structs)
    game_map = game.game_map

    if myglobals.Const.DEBUGGING['core']:
        logging.info(" - initializing 'command_queue'")
    command_queue = []

    if myglobals.Const.DEBUGGING['core']:
        logging.info("me.get_ships() dump: " + str(me.get_ships()))

    for ship in me.get_ships():
        # d4m0 schitt starts

        # is this ship already in transit to mine?
        try:
            if myglobals.Const.DEBUGGING['save_state']:
                logging.debug("Ship id " + str(ship.id) + " has state set to " +
                              myglobals.Variables.current_assignments[ship.id]['mission'])

            # have we been a ramblin'?
            if ((turn - myglobals.Variables.current_assignments[ship.id]['turnstamp']) >
                (myglobals.Const.Maximal_Consideration_Distance * 2)):
                if myglobals.Const.DEBUGGING['seek'] or myglobals.Const.DEBUGGING['mine'] or \
                    myglobals.Const.DEBUGGING['dropoff']:
                    logging.debug(" - seeking new ore or dropoff due to mission time elapsed in transit - ")

                # been traveling too long; time to select a new destination/mission
                cmd_n_dest = analytics.Analyze.can_we_embark_and_start_mining(ship, game_map, me)
                command_queue.append(cmd_n_dest['c_queue_addition'])
                myglobals.Misc.save_ship_state(ship.id, 'transit', turn, cmd_n_dest['destination'])
                # NOTE: these 3 blocks are used at least twice below, also;
                # BREAK IT UP
                if myglobals.Const.DEBUGGING['save_state']:
                    logging.debug(" - updated former transit state to transit: " + str(cmd_n_dest['destination']))

            # I did things this way because of the potential for adding moar
            # assignment types, this may be changed for efficiency in the near
            # future
            elif myglobals.Variables.current_assignments[ship.id]['mission'] != 'mining' \
                    and myglobals.Variables.current_assignments[ship.id]['mission'] != 'transit' \
                    and myglobals.Variables.current_assignments[ship.id]['mission'] != 'dropoff':

                # we should be good to send it on its way
                if myglobals.Const.DEBUGGING['save_state']:
                    logging.info("Found ship " + str(ship.id) + " ready for mission.")

                # so yeah, now we incorporate the whether or not to mine/dropoff
                # block (now in analytics) with new indent levels
                cmd_n_dest = analytics.Analyze.can_we_embark_and_start_mining(ship, game_map, me)
                command_queue.append(cmd_n_dest['c_queue_addition'])
                # the above ^^^ appended command is probably the tuple instead
                # of proper command string error ;)

                myglobals.Misc.save_ship_state(ship.id, 'transit', turn, cmd_n_dest['destination'])

            elif myglobals.Variables.current_assignments[ship.id]['mission'] == 'transit':
                # are we at our destination yet?
                if ship.position == myglobals.Variables.current_assignments[ship.id]['destination']:
                    # switch to mining or dropoff
                    if game_map[ship.position].has_structure:
                        myglobals.Misc.save_ship_state(ship.id, 'dropoff', turn, ship.position)
                        command_queue.append(ship.make_dropoff())
                        if myglobals.Const.DEBUGGING['save_state'] or myglobals.Const.DEBUGGING['dropoff']:
                            logging.debug(" - changed mission to dropoff @ " + str(ship.position))
                    elif game_map[ship.position].halite_amount > 0:
                        # gotta make sure there's still halite here, too
                        myglobals.Misc.save_ship_state(ship.id, 'mining', turn, ship.position)
                        command_queue.append(ship.stay_still())   # collect that halite
                        if myglobals.Const.DEBUGGING['save_state'] or myglobals.Const.DEBUGGING['mining']:
                            logging.debug(" - changed mission to mining @ " + str(ship.position))
                    else:
                        # we need to pick somewhere else to go - it's been stripped
                        cmd_n_dest = analytics.Analyze.can_we_embark_and_start_mining(ship, game_map, me)
                        command_queue.append(cmd_n_dest['c_queue_addition'])
                        myglobals.Misc.save_ship_state(ship.id, 'transit', turn, cmd_n_dest['destination'])
                        # NOTE: same 3 lines of code as above the [outer] 'elif'
                        # statement; where can we put this to avoid dupe coad?

                        if myglobals.Const.DEBUGGING['save_state']:
                            logging.debug(" - this area is stripped - in transit to new target: " +
                                          str(cmd_n_dest['destination']))
            else:   # we must be set for dropoff; check and make sure that we're done nao
                command_queue.append(ship.move(game_map.naive_navigate(ship,
                                                                       myglobals.Variables.
                                                                       current_assignments[ship.id]['destination'])))

                myglobals.Misc.save_ship_state(ship.id, 'transit', turn,
                                               myglobals.Variables.current_assignments[ship.id]['destination'])
                #continue    # is this necessary at this level?

        except KeyError:
            logging.debug("In KeyError try/except loop")

            if not ship.is_full:
                # for testing purposes right now we'll just send out mining no matter what
                relative_halite = analytics.Analyze.locate_significant_halite(ship, game_map)
                target = seek_n_nav.FindApproach.target_halite_simple(ship, game_map, relative_halite)
            else:
                target = seek_n_nav.FindApproach.locate_nearest_base(ship, game_map, me)

            myglobals.Misc.save_ship_state(ship.id, 'transit', turn, target)
            # remember to change 'transit' in the above to something different if the ship is already over the
            # destination ore deposit, dropoff, or base
            #command_queue.append(game_map.naive_navigate(ship, target))
            # this one was a tuple, too ^^^^
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
    if game.turn_number <= 200 and me.halite_amount >= 1000 and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    # d4m0 end of turn schitt
    turn += 1

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)

