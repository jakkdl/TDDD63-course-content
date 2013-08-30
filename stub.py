#
# This is the file stub.py that can be used as a starting point for the bots
#

import libpyAI as ai

import sys
import traceback
import math

from optparse import OptionParser

parser = OptionParser()

parser.add_option ("-g", "--group", action="store", type="int", 
                   dest="group", default=0, 
                   help="The group number. Used to avoid port collisions when" 
                   " connecting to the server.")

#
# Create a class used to store the internal state of the bot
#

class myai:
    """Simple Stub for a Bot"""

    def __init__(self):
        self.count = 0
        self.mode = "ready"

    def tick(self):
        try:

            #
            # If we die then restart the state machine in the state "ready"
            #
            if not ai.selfAlive():
                self.count = 0
                self.mode = "ready"
                return

            self.count += 1

            #
            # Read the "sensors"
            #

            heading = ai.selfHeadingRad() 
            # 0-2pi, 0 in x direction, positive toward y

            speed = ai.selfSpeed()
            x = ai.selfX()
            y = ai.selfY()
            vx = ai.selfVelX()
            vy = ai.selfVelY()

            # Add more sensors readings here if they are needed

            print (self.mode, x, y, vx, vy, speed, heading)


            if self.mode == "ready":
                pass


        except:
            print(traceback.print_exc())
            print(sys.exc_info())

#
# Create an instace of the bot class myai.
#

bot = myai()

#
# Connect the bot instance with the AI loop
#

def AI_loop():
    bot.tick()

#
# Parse the command line arguments
#

(options, args) = parser.parse_args()

port = 15345 + options.group
name = "Stub"

#
# Start the main loop. Callback are done to AI_loop.
#

ai.start(AI_loop,["-name", name, 
                  "-join",
                  "-turnSpeed", "64",
                  "-turnResistance", "0",
                  "-port", str(port)])
