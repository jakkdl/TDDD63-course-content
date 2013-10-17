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
        global tickCount
        global mode
        global targetId

        #
        # If we die then restart the state machine in the state "init"
        #
        if not ai.selfAlive():
            tickCount = 0
            mode = "aim"
            return

        #tickCount += 1

        #
        # Read some "sensors"
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


        #print (self.count, self.mode, self.targetId, numTargetsAlive)


        if mode == "wait":
          if numTargetsAlive > 0:
            mode = "aim"
        elif mode == "aim":
          if numTargetsAlive == 0:
            mode = "wait"
            return

          for i in range(numTargets):
            if ai.targetAlive(i):
              targetId = i
              break

          targetX = ai.targetX(targetId)
          targetY = ai.targetY(targetId)

          wantedHeading = math.atan2(targetY-y, targetX-x)
          
          if tickCount % 2 == 0:
            ai.turnToRad(wantedHeading)

          if ai.angleDiffRad(wantedHeading, heading) < ai.xdegToRad(2):
            mode = "shoot"

        elif mode == "shoot":
          targetX = ai.targetX(targetId)
          targetY = ai.targetY(targetId)
          wantedHeading = math.atan2(targetY-y, targetX-x)
          if ai.angleDiffRad(wantedHeading, heading) > ai.xdegToRad(2):
            mode = "aim"
            return

          if ai.targetAlive(targetId):
            ai.fireShot()
          else:
            mode = "aim"
    except:
        print(traceback.print_exc())
        print(sys.exc_info())

#
# Create an instace of the bot class myai.
#

#bot = myai()

#
# Connect the bot instance with the AI loop
#

#def AI_loop():
    #bot.tick()

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

ai.start(tick,["-name", name, 
                  "-join", 
                  "-turnSpeed", "64",
                  "-turnResistance", "0",
                  "-port", str(port)])
