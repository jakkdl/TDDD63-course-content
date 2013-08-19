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
        self.mode = "acquire target"

    def tick(self):
        try:

            #
            # If we die then restart the state machine in the state "init"
            #
            if not ai.selfAlive():
                self.count = 0
                self.mode = "acquire target"
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
            mass = ai.selfMass()
            block = ai.blockSize()
            tracking = ai.selfTrackingRad()

            shotDist = ai.getOption("shotlife") * ai.getOption("shotspeed")

            print (self.mode, x, y, vx, vy, speed, heading)


            # avoid strange sensor values when starting by waiting
            # three ticks until we go to ready
            if self.mode == "acquire target":
              for i in range(ai.numTargetServer()):
                if ai.targetAlive(i):
                  self.targetId = i
                  self.mode = "travel"
                  return
            elif self.mode == "travel":
              tx = ai.targetX(self.targetId)
              ty = ai.targetY(self.targetId)
              if ( (x - tx)**2 + (y - ty)**2 )**0.5 < 500:
                self.mode = "stop"
              ai.setPower(55)
              if self.count % 2 == 0:
                ai.turnToRad(math.atan2(ty-y,tx-x))
              if speed < 20:
                ai.thrust()
              elif ai.angleDiffRad(tracking, math.atan2(ty-y, tx-x)) > math.pi/4:
                self.mode = "stop"

            elif self.mode == "stop":
              if self.count % 2 == 0:
                ai.turnToRad(tracking + math.pi)
              if speed < 1:
                self.mode = "shoot"
              if ai.angleDiffRad(heading, tracking + math.pi) < 0.1:
                ai.thrust()

            elif self.mode == "shoot":
              if not ai.targetAlive(self.targetId):
                self.mode = "acquire target"
              tx = ai.targetX(self.targetId)
              ty = ai.targetY(self.targetId)
              if ( (x - tx)**2 + (y - ty)**2 )**0.5 > shotDist:
                self.mode = "travel"

              if self.count % 2 == 0:
                ai.turnToRad(math.atan2(ty-y,tx-x))
              if ai.angleDiffRad(heading, math.atan2(ty-y, tx-x)) < 0.3:
                ai.fireShot()


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
name = "Exc3 solution"

#
# Start the main loop. Callback are done to AI_loop.
#

ai.start(AI_loop,["-name", name, 
                  "-join",
                  "-turnSpeed", "64",
                  "-turnResistance", "0",
                  "-port", str(port)])
