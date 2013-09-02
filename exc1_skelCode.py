#
# This file can be used as a starting point for the bot in exercise 1
#

import sys
import traceback
import math
import os
import libpyAI as ai
from optparse import OptionParser


#
# Create variables that persist between ticks.
#

tickCount = 0
mode = "wait"
targetId = -1

def tick(self):
    #
    # The API won't print out exceptions, so we have to catch and print them ourselves
    #
    try:

        #
        # If we die then restart the state machine in the "aim" state
        #
        if not ai.selfAlive():
            self.count = 0
            self.mode = "aim"
            return

        self.count += 1

        #
        # Read some "sensors" into local variable to avoid excessive calls to the API.
        #
        selfX = ai.selfX()
        selfY = ai.selfY()
        selfHeading = ai.selfHeadingRad() 
        # 0-2pi, 0 in x direction, positive toward y

        targetCount = ai.targetCountServer()
        targetCountAlive = 0

        for i in range(targetCount):
          if ai.targetAlive(i):
            targetCountAlive += 1

        # Use print statements for debugging, either here or further down in the code.
        # useful functions: round(), ai.radToDeg, ai.degToRad, etc.
        # os.system('clear') clears the terminal screen, which can be useful.

        print("tick count:", tickCount, "mode:", mode, "heading:",
                round(ai.radToDeg(heading)), "targets alive:", targetCountAlive)


        if self.mode == "wait":
          if numTargetsAlive > 0:
            self.mode = "aim"

        elif self.mode == "aim":
          if numTargetsAlive == 0:
            self.mode = "wait"
            return

          # Find a target that is alive and save the index in targetId.
          # useful variables: targetCount, targetId
          # useful functions: ai.targetAlive

          """your code here"""

          # Calculate what direction the target is in and save in
          # the variable targetDirection
          # useful variables: selfX, selfY
          # useful functions: math.atan2, ai.targetX, ai.targetY

          """your code here"""

          # Turn to the direction of the target
          # useful variables: targetDirection
          # useful functions: turnRad, turnToRad

          """your code here"""

          # If the ship keeps oscillating between a few angles
          # it may be due to latency. Only turning every second
          # or third tick is a simple solution (use self.count and %)


          # If you are finished aiming change mode to shoot
          # useful variables: selfHeading, targetDirection, mode
          # useful functions: ai.angleDiffRad, ai.angleDiffDeg, ai.radToDeg, ai.degToRad

          """your code here"""

        elif self.mode == "shoot":

          # Shoot the target
          # useful functions: ai.fireShot

          """your code here"""

          # if the target is destroyed, change state to aim
          # useful variables: targetId, mode
          # useful functions: ai.targetAlive

          """your code here"""

    except:
        print(traceback.print_exc())
        print(sys.exc_info())


#
# Parse the command line arguments
#
parser = OptionParser()

parser.add_option ("-p", "-port", action="store", type="int", 
                   dest="port", default=15345, 
                   help="The port to use. Used to avoid port collisions when" 
                   " connecting to the server.")

(options, args) = parser.parse_args()

port = options.port
name = "Exc. 1 skeleton" #Feel free to change this

#
# Start the main loop. Callback are done to tick.
#

ai.start(tick, ["-name", name, 
                "-join", 
                "-turnSpeed", "64",
                "-turnResistance", "0",
                "-port", str(port)])
