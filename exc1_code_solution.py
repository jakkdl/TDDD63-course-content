#
# This is the file stub.py that can be used as a starting point for the bots
#

import libpyAI as ai

import sys
import traceback
import math
import os

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
        self.mode = "aim"
        self.targetId = -1

    def tick(self):
        try:

            #
            # If we die then restart the state machine in the state "init"
            #
            if not ai.selfAlive():
                self.count = 0
                self.mode = "aim"
                return

            self.count += 1

            #
            # Read the "sensors"
            #


            x = ai.selfX()
            y = ai.selfY()
            heading = ai.selfHeadingRad() 
            # 0-2pi, 0 in x direction, positive toward y

            numTargets = ai.targetCountServer()
            numTargetsAlive = 0


            for i in range(numTargets):
              if ai.targetAlive(i):
                numTargetsAlive += 1

            #os.system('clear')


            print (self.count, self.mode, self.targetId, numTargetsAlive)


            if self.mode == "wait":
              if numTargetsAlive > 0:
                self.mode = "aim"
            elif self.mode == "aim":
              if numTargetsAlive == 0:
                self.mode = "wait"
                return

              for i in range(numTargets):
                if ai.targetAlive(i):
                  self.targetId = i
                  break

              targetX = ai.targetX(self.targetId)
              targetY = ai.targetY(self.targetId)

              wantedHeading = math.atan2(targetY-y, targetX-x)
              
              if self.count % 2 == 0:
                ai.turnToRad(wantedHeading)

              if ai.angleDiffRad(wantedHeading, heading) < ai.xdegToRad(2):
                self.mode = "shoot"

            elif self.mode == "shoot":
              targetX = ai.targetX(self.targetId)
              targetY = ai.targetY(self.targetId)
              wantedHeading = math.atan2(targetY-y, targetX-x)
              if ai.angleDiffRad(wantedHeading, heading) > ai.xdegToRad(2):
                self.mode = "aim"
                return

              if ai.targetAlive(self.targetId):
                ai.fireShot()
              else:
                self.mode = "aim"
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
name = "Exc. 1 solution"

#
# Start the main loop. Callback are done to AI_loop.
#

ai.start(AI_loop,["-name", name, 
                  "-join", 
                  "-turnSpeed", "64",
                  "-turnResistance", "0",
                  "-port", str(port)])
