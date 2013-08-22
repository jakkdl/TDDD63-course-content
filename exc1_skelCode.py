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
        self.mode = "wait"
        self.targetId = -1

    def tick(self):
        try:

            #
            # If we die then restart the state machine in the state "aim"
            #
            if not ai.selfAlive():
                self.count = 0
                self.mode = "wait"
                return

            self.count += 1

            #
            # Read the "sensors"
            #
            x = ai.selfX()
            y = ai.selfY()
            heading = ai.selfHeadingRad() 
            # 0-2pi, 0 in x direction, positive toward y

            targetCount = ai.targetCountServer()
            targetCountAlive = 0

            for i in range(targetCount):
              if ai.targetAlive(i):
                targetCountAlive += 1

            # For debugging use print statements, either here or further down in the code.
            # useful functions: round(), ai.radToDeg, ai.degToRad, etc.
            # os.system('clear') clears the terminal screen, which can be useful.

            print(self.count, self.mode, round(ai.radToDeg(heading)), targetCountAlive)


            if self.mode == "wait":
              if numTargetsAlive > 0:
                self.mode = "aim"

            elif self.mode == "aim":
              if numTargetsAlive == 0:
                self.mode = "wait"
                return

              # Find a target that is alive and save it's index in self.targetId.
              # useful function ai.targetAlive

              """your code here"""

              # Calculate the direction the target is in
              # useful functions: math.atan2, ai.targetX, ai.targetY

              """your code here"""

              # Turn to the direction of the target
              # useful functions: turnRad, turnToRad

              """your code here"""

              # If the ship keeps oscillating between a few angles
              # it may be due to latency. Only turning every second
              # or third tick is a simple solution (use self.count and %)


              # If you are finished aiming change mode to shoot
              # useful functions: ai.angleDiffRad, ai.angleDiffDeg, ai.radToDeg, ai.degToRad

              """your code here"""

            elif self.mode == "shoot":

              # Shoot the target
              # useful functions: ai.fireShot

              """your code here"""

              # if the target is destroyed, change state
              # useful functions: ai.targetAlive

              """your code here"""

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
name = "Exc. 1 skeleton" #Feel free to change this

#
# Start the main loop. Callback are done to AI_loop.
#

ai.start(AI_loop,["-name", name, 
                  "-join", 
                  "-turnSpeed", "64",
                  "-turnResistance", "0",
                  "-port", str(port)])
