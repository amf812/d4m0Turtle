# d4m0Turtle

## Halite III

For more information on the contest, see the [Halite III coding contest web site](http://Halite.io).

For an overview from the level of the ISS, Halite is an artificial intelligence coding challenge, built around coding bots in a virtual environment to 'mine' _halite ore_ for usage for movement, creating more ships/turtles, and determining which player has won in any particular simulation.

## d4m0Turtle Particulars

Stay tuned for more information here.  I'm just getting started on the bot at this point and really don't know where the new virtual environment is going to be leading me, in terms of different routines.

I think, at this point, that I'm going to steal and modify as much of the navigation algorithm structure that I can from my previous bot version, instead of trying to recreate the wheel, and then go into the differences between the game rules and optimizing for the new ruleset.

## Project Structure

### d4m0_routines

**NOTE**: This should be moved to the wiki

Holds all of my particular different libraries for usage from within **d4m0Turtle.py**.  First on the agenda will be working with seeking out ore and navigation to it, so _seek-n-nav_ will probably be my first real work here, fueled by data compiled by the _analytics_ routines to determine closest location & quantity of resources.

#### analytics

  * locate_significant_halite: locates at least 3 halite resources, with at least one being a maximal ore deposit

#### seek-n-nav


