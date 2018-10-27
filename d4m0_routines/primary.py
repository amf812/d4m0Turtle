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
    def has_transit_been_too_long(turn, ship, game_map, me):
        """
        if the ship has been in transit for more than
        3*Maximal_Consideration_Distance turns, it is time to assign a new
        destination/mission for that ship, as it may be blocked or some less
        expected condition may be at play

        :param turn:
        :param ship:
        :param game_map:
        :param me:
        :return: c_queue_addition or False
        """

        if ((turn - myglobals.Variables.current_assignments[ship.id]['turnstamp']) >
                (myglobals.Const.Maximal_Consideration_Distance * myglobals.Const.Traveling_Too_long)):
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

    @staticmethod
    def transit_processing_done_or_not(ship, game_map, turn, me):
        """
        checks to see if the ship in transit has made it to its destination
        Position yet; if so, it changes its mission and starts it dropping
        halite or mining, etc

        :param ship:
        :param game_map:
        :param turn:
        :param me:
        :return: c_queue or False
        """
        # are we at our destination yet?
        if ship.position == myglobals.Variables.current_assignments[ship.id]['destination']:
            # switch to mining or dropoff
            if game_map[ship.position].has_structure:
                myglobals.Misc.save_ship_state(ship.id, 'dropoff', turn, ship.position)
                c_queue = ship.make_dropoff()
                if myglobals.Const.DEBUGGING['save_state'] or myglobals.Const.DEBUGGING['dropoff']:
                    logging.debug("  - changed mission to dropoff @ " + str(ship.position))
            elif game_map[ship.position].halite_amount > 0:
                # gotta make sure there's still halite here, too
                myglobals.Misc.save_ship_state(ship.id, 'mining', turn, ship.position)
                c_queue = ship.stay_still()     # collect it
                if myglobals.Const.DEBUGGING['save_state'] or myglobals.Const.DEBUGGING['mining']:
                    logging.debug("  - changed mission to mining @ " + str(ship.position))
            else:
                # we need to pick somewhere else to go - it's been stripped
                cmd_n_dest = analytics.Analyze.can_we_embark_and_start_mining(ship, game_map, me)
                c_queue = cmd_n_dest['c_queue_addition']
                myglobals.Misc.save_ship_state(ship.id, 'transit', turn, cmd_n_dest['destination'])

                myglobals.Misc.loggit('save_state', 'info', "  - this area is stripped - in transit to new target: " +
                                      str(cmd_n_dest['destination']))

            return c_queue
        else:
            return False

    @staticmethod
    def minimum_distance_processing(ship, game_map, turn, me):
        """
        processing if a ship is still trying to get minimum_distance away
        from the shipyard

        :param ship:
        :param game_map:
        :param turn:
        :param me:
        :return:
        """
        if ship.position == myglobals.Variables.current_assignments[ship.id]['destination']:
            # we're here, now seek out the best halite
            myglobals.Misc.loggit('core', 'debug', "  - ship id: " + str(ship.id) + " at min distance; " +
                                  "seeking halite ore now")
            # at some point this will need to include searching other
            # ships' current_assignments to verify there will be no
            # conflict in destination to avoid pointless transit
            dest = analytics.Analyze.locate_significant_halite(ship, game_map)[0]['destination']
            myglobals.Misc.save_ship_state(ship.id, 'transit', turn, dest)
            myglobals.Misc.loggit('seek-n-nav', 'debug', "  - * found halite @ " + str(dest))
            c_queue = ship.move(game_map.naive_navigate(ship, myglobals.Variables.
                                                        current_assignments[ship.id]['destination']))

        elif (turn - myglobals.Variables.current_assignments[ship.id]['turn']) < \
                (myglobals.Const.Maximal_Consideration_Distance * 2):
            # continue minimum distance transit
            myglobals.Misc.loggit('core', 'debug', "  - ship id: " + str(ship.id) + " continuing transit to " +
                                  str(myglobals.Variables.current_assignments[ship.id]['destination']))
            c_queue = ship.move(game_map.naive_navigate(ship, myglobals.Variables.
                                                        current_assignments[ship.id]['destination']))
        else:
            # we've been ramblin' too long, just look for the halite now
            dest = analytics.Analyze.locate_significant_halite(ship, game_map)[0]['destination']
            myglobals.Misc.save_ship_state(ship.id, 'transit', turn, dest)
            myglobals.Misc.loggit('seek-n-nav', 'debug', " - ship id: " + str(ship.id) +
                                  " ramblin' too long, transit to: " + str(dest) + " initiated")
            c_queue = ship.move(game_map.naive_navigate(ship, dest))

        return c_queue
