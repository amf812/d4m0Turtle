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

from hlt.positionals import Direction

import logging

#d4m0 imports
from d4m0_routines import analytics, seek_n_nav, myglobals
from operator import itemgetter

""" <<<Game Begin>>> """

game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("D4m0Turtle")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully hatched! My Player ID is {}.".format(game.my_id))

#d4m0's init stuff
turn = 0
current_assignments = { }

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
    #keeps things speedier
    me = game.me

    if myglobals.Const.DEBUGGING['core']:
        logging.info(" - updating 'game_map'")
    #speed, again (see if there are any places to implement anything like
    # this with my own structs)
    game_map = game.game_map

    if myglobals.Const.DEBUGGING['core']:
        logging.info(" - initializing 'command_queue'")
    command_queue = []

    if myglobals.Const.DEBUGGING['core']:
        logging.info("me.get_ships() dump: " + str(me.get_ships()))

    for ship in me.get_ships():
        #d4m0 schitt starts

        #is this ship already in transit to mine?
        if current_assignments[ship.id]:
            if current_assignments[ship.id]['mission'] != 'mining' \
                and current_assignments[ship.id]['mission'] != 'transit' \
                and current_assignments[ship.id].mission != 'dropoff':
                #we should be good to send it on its way
                if myglobals.Const.DEBUGGING['core']:
                    logging.info("Found ship " + str(ship.id) + " ready for mission.")

                #so yeah, now we incorporate the whether or not to mine/dropoff block below  with new indent levels

            else:
                command_queue.append(game_map.naive_navigate(ship, current_assignments[ship.id]['destination']))
                continue

        #decide whether or not to mine with this ship
        #is it full?
        if ship.is_full:	#we'll test this for being close to full, also
            #locate closest base & deposit (for now we'll do this w/initial
            #base only)
            #locate_nearest_base() in analytics will handle this eventually

            command_queue.append(
                game_map.naive_navigate(ship, seek_n_nav.locate_nearest_base(ship, game_map, me)))

            #NOTE: docking analogous routine is ship.make_dropoff()

            if myglobals.Const.DEBUGGING['seek']:
                logging.info("Seeking nearest dropoff")


        else:
            #find some ore, por dios
            if myglobals.Const.DEBUGGING['locate_ore']:
                logging.info("Looking for close ore deposits...  Maximal " + \
                             "consideration distance: " + \
                             str(myglobals.Const.Maximal_Consideration_Distance) + \
                             "; halite to be worth mining: " + \
                             str(myglobals.Const.Worth_Mining_Halite))

            relative_halite = analytics.Analyze.locate_significant_halite(ship, game_map)
            if myglobals.Const.DEBUGGING['locate_ore']:
                logging.info(" - relative_halite: " + str(
                    sorted(relative_halite, key=itemgetter('quantity'), reverse=True)))

            command_queue.append(
                ship.move(game_map.naive_navigate(
                    ship, seek_n_nav.FindApproach.target_halite_simple(ship, game_map, relative_halite))))

        #d4m0 schitt ends

        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        #if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:
        #    command_queue.append(
        #        ship.move(
        #            random.choice([ Direction.North, Direction.South, Direction.East, Direction.West ])))
        #else:
        #indent the command below to recover this functionality when the hlt.constants shit is fixed
        #the conditional bit and north movement is d4m0 schitt; just the stay_still() was original
        #if turn >= 3:
        #    command_queue.append(ship.stay_still())
        #    logging.info("queued command for the ship to stay still")
        #else:
        #    command_queue.append(ship.move(Direction.North))
        #    logging.info("queued command for the ship to move north (1st turn)")

    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if game.turn_number <= 200 and me.halite_amount >= 1000 and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    #d4m0 end of turn schitt
    turn += 1

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)

