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
        self.targetId = -1

    def tick(self):
        try:

            #
            # If we die then restart the state machine in the state "init"
            #
            if not ai.selfAlive():
                self.count = 0
                self.mode = "wait"
                return

            self.count += 1

            #
            # Read the "sensors"
            #

            heading = ai.selfHeadingRad() 
            tracking = ai.selfTrackingRad()
            # 0-2pi, 0 in x direction, positive toward y

            speed = ai.selfSpeed()
            mass = ai.selfMass()
            x = ai.selfX()
            y = ai.selfY()
            vx = ai.selfVelX()
            vy = ai.selfVelY()

            # Add more sensors readings here if they are needed

            print (self.mode, round(speed))



            # avoid strange sensor values when starting by waiting
            # three ticks until we go to ready
            if self.mode == "wait":
              if ai.selfAlive():
                self.mode = "acquire target"
            elif self.mode == "acquire target":
              ai.setPower(55)
              self.targetId = ai.nextCheckPoint()
              self.mode = "travel"
            elif self.mode == "travel":
              checkX = ai.checkPointX(self.targetId)*ai.blockSize()
              checkY = ai.checkPointY(self.targetId)*ai.blockSize()

              dist = ( (checkX-x)**2 + (checkY-y)**2 ) ** 0.5

              if dist < speed*mass*0.7:
                self.mode = "stop"
                return

              if self.count % 2 == 0:
                wantedHeading = math.atan2(checkY-y, checkX-x)
                ai.turnToRad(wantedHeading)
                if speed < 25 and ai.angleDiffRad(wantedHeading, heading) < 0.1:
                  ai.thrust()

            elif self.mode == "stop":
              if speed > 5:
                if self.count % 2 == 0:
                  ai.turnToRad(tracking + math.pi)
                if ai.angleDiffRad(heading, tracking + math.pi) < 0.1:
                  ai.thrust()
              else:
                self.mode = "acquire target"
                


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
name = "exc2 solution"

#
# Start the main loop. Callback are done to AI_loop.
#

ai.start(AI_loop,["-name", name, 
                  "-join",
                  "-turnSpeed", "64",
                  "-turnResistance", "0",
                  "-port", str(port)])
