#
# This file can be used as a starting point for the bot in exercise 1.
#


import sys
import traceback
import math
import os
import libpyAI as ai
from optparse import OptionParser


#
# Create global variables that persist between calls to tick.
#
tickCount = 0
mode = "aim"
targetId = -1

def tick():
    #
    # The API won't print out exceptions, so we have to catch and print them ourselves.
    #
    try:

        #
        # If we die then restart the state machine in the state "init"
        #
        if not ai.selfAlive():
            tickCount = 0
            mode = "aim"
            return

        tickCount += 1

        #
        # Read some "sensors"
        #
        selfX = ai.selfX()
        selfY = ai.selfY()
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
parser = OptionParser()

parser.add_option ("-g", "--group", action="store", type="int", 
                   dest="group", default=0, 
                   help="The group number. Used to avoid port collisions when" 
                   " connecting to the server.")

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
