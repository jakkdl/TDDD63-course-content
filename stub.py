#
# This file can be used as a starting point for the bots
#

import sys
import traceback
import math
import libpyAI as ai
from optparse import OptionParser


#
# Create a class used to store the internal state of the bot
#
tickCount = 0
mode = "ready"

def tick(self):
    try:

        #
        # If we die then restart the state machine in the "ready" state
        #
        if not ai.selfAlive():
            tickCount = 0
            self.mode = "ready"
            return

        self.count += 1

        #
        # Read some "sensors" 
        #

        selfHeading = ai.selfHeadingRad() 
        # 0-2pi, 0 in x direction, positive toward y

        selfSpeed = ai.selfSpeed()
        selfX = ai.selfX()
        selfY = ai.selfY()
        selfVelX = ai.selfVelX()
        selfVelY = ai.selfVelY()

        # Add more sensors readings here if they are needed

        print (mode, selfX, selfY, selfVelX, selfVelY)


        if mode == "ready":
            pass


    except:
        print(traceback.print_exc())
        print(sys.exc_info())


#
# Parse the command line arguments
#
parser = OptionParser()

parser.add_option ("-g", "--group", action="store", type="int", 
                   dest="group", default=0, 
                   help="The group number. Used to avoid port collisions when" 
                   " connecting to the server.")

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
