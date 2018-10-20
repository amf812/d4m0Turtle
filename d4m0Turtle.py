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

# This library contains constant values.
from hlt import constants
from hlt.positionals import Direction
import random
import logging

#d4m0 imports
import d4m0_routines

""" <<<Game Begin>>> """

game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("D4m0Turtle")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully hatched! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """

while True:
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    
    #keeps things speedier
    me = game.me
    game_map = game.game_map

    command_queue = []

    for ship in me.get_ships():
        #d4m0 schitt starts

        #decide whether or not to mine with this ship
        #is it full?
        if ship.is_full:	#we'll test this for being close to full, also
            #locate closest base & deposit (for now we'll do this w/initial
            #base only)
            #locate_nearest_base() in analytics will handle this eventually
            command_queue.append(
                game_map.naive_navigate(ship, locate_nearest_base(ship, game_map)))
            #NOTE: docking analogous routine is ship.make_dropoff()

            if d4m0_routines.myglobals.Constants.DEBUGGING['seek']:
                d4m0_routines.myglobals.Wrap.log.info("Seeking nearest base")
        else:
            #find some ore, por dios

        

        #d4m0 schitt ends

        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:
            command_queue.append(
                ship.move(
                    random.choice([ Direction.North, Direction.South, Direction.East, Direction.West ])))
        else:
            command_queue.append(ship.stay_still())

    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)

