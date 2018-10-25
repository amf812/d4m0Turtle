"""
primary.py

Started on: 25oct18

The core algorithm has grown significantly in complexity over the past day;
it's definitely starting to get a bit rough to manage, so it's time to
break up the bigger chunks and farm them out to here.
"""

from . import myglobals, analytics

import logging

class Core:
    @staticmethod
    def has_transit_been_too_long(turn, ship):
        if ((turn - myglobals.Variables.current_assignments[ship.id]['turnstamp']) >
                (myglobals.Const.Maximal_Consideration_Distance * 2)):
            if (myglobals.Const.DEBUGGING['seek'] or myglobals.Const.DEBUGGING['mine'] or
               myglobals.Const.DEBUGGING['dropoff']) or myglobals.Const.DEBUGGING['core']:
                logging.debug("  - seeking new ore or dropoff due to mission time elapsed in transit - ")

            # been traveling too long; time to select a new destination/mission
            cmd_n_dest = analytics.Analyze.can_we_embark_and_start_mining(ship, game_map, me)
            myglobals.Misc.save_ship_state(ship.id, 'transit', turn, cmd_n_dest['destination'])
            # BREAK IT UP

            myglobals.Misc.loggit('save_state', 'debug', "  - updated former transit state to new transit: " +
                                  str(cmd_n_dest['destination']))

            return cmd_n_dest['c_queue_addition']
        else:
            return False

