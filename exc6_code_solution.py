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
        self.record = 0
        self.start = 0


    def tick(self):
        try:

            if not ai.selfAlive():
                self.count = 0
                self.mode = "wait"
                return

            if self.count == 0 or self.start == -1:
              self.start = ai.timeLeftSec()
            
            self.count += 1

            #
            # Read the "sensors"
            #

            heading = ai.selfHeadingRad() 
            tracking = ai.selfTrackingRad()
            # 0-2pi, 0 in x direction, positive toward y

            speed = ai.selfSpeed()
            x = ai.selfX()
            y = ai.selfY()
            vx = ai.selfVelX()
            vy = ai.selfVelY()
            itemCount = ai.itemCountScreen()
            wallDist = ai.wallFeelerRad(10000, tracking)
            
            block = ai.blockSize()
            speedConst = 30
            maxSpeed = 3
            selfMines = ai.selfItem(8)
            time = self.start - ai.timeLeftSec()

            cannonDist = ( (ai.cannonX(0)-x)**2 + (ai.cannonY(0)-y)**2 )**0.5

            if time == 0:
              time = 1

            if time > self.record:
              self.record = time

            os.system('clear')
            print(self.record)
            print(time)
            print(self.mode)
            
            if wallDist < speed*speedConst:
              self.mode = "stop"
              self.wallDir = tracking
            elif cannonDist < 200:
              self.mode = "away from cannon"

            danger = 99999
            shotId = -1
            for i in range(ai.shotCountScreen()):
              if ai.shotAge(i) > 1:
                if ai.shotAlert(i) < danger:
                  shotId = i


            if self.mode == "wait":
              if shotId != -1:
                self.mode = "dodge"
                return

            elif self.mode == "stop":
              wantedHeading = ai.angleAddRad(self.wallDir, math.pi)
              if self.count % 2 == 0:
                ai.turnToRad(wantedHeading)
              if ai.angleDiffRad(wantedHeading, heading) < ai.degToRad(30):
                ai.thrust()
              if wallDist > speed*speedConst:
                self.mode = "dodge"

            elif self.mode == "away from cannon":
              cannonDir = math.atan2(ai.cannonY(0)-y,ai.cannonX(0))
              if self.count % 2 == 0:
                ai.turnToRad(cannonDir + math.pi)

              if ai.angleDiffRad(cannonDir+math.pi, heading) < 0.036:
                ai.thrust()
              if cannonDist > 200:
                self.mode = "dodge"

            elif self.mode == "dodge":
              if shotId == -1:
                self.mode = "wait"
                return
              
              print(ai.shotAlert(shotId))
              if ai.shotAlert(shotId) > 200:
                return
              shotX = ai.shotX(shotId)
              shotY = ai.shotY(shotId)
              shotVelX = ai.shotVelX(shotId)
              shotVelY = ai.shotVelY(shotId)

              shotApproachAngle = math.atan2(shotY-y, shotX-x)
              wantedHeading1 = shotApproachAngle + ai.degToRad(90)
              wantedHeading2 = shotApproachAngle + ai.degToRad(-90)

              if ai.wallFeelerRad(10000, wantedHeading1) > ai.wallFeelerRad(10000, wantedHeading2):
                wantedHeading = wantedHeading1
              else:
                wantedHeading = wantedHeading2


              if self.count % 2 == 0:
                ai.turnToRad(wantedHeading)

              ai.thrust()


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
