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
        self.recordTime = 0
        self.start = 0

        #record: 55mines with 0.0698 mines/second

    def tick(self):
        try:

            #
            # If we die then restart the state machine in the state "init"
            #
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
            if speed == 0:
              speed = 0.5
            x = ai.selfX()
            y = ai.selfY()
            vx = ai.selfVelX()
            vy = ai.selfVelY()
            itemCount = ai.itemCountScreen()
            wallDist = ai.wallFeelerDeg(10000, ai.radToDeg(tracking))
            speedConst = 30
            maxSpeed = 3
            selfMines = ai.selfItem(8)
            time = self.start - ai.timeLeftSec()

            if time == 0:
              time = 1

            if selfMines > self.record:
              self.record = selfMines
              self.recordTime = selfMines / time
            os.system('clear')
            print(self.record, self.recordTime)
            print(selfMines, selfMines / time)
            print(self.mode, speed)
            
            if wallDist < speed*speedConst:
              self.mode = "stop"
              self.wallDir = tracking

            if self.mode == "wait":
              if itemCount > 0:
                self.mode = "move"
                return
              wantedHeading = math.atan2(ai.mapHeightPixels()/2-y, ai.mapWidthPixels()/2-x)
              if self.count % 2 == 0:
                ai.turnToRad(wantedHeading)

              if speed < maxSpeed and ai.angleDiffRad(wantedHeading, heading) < 0.018:
                ai.thrust()

              if ai.radToDeg(ai.angleDiffRad(tracking, heading)) > 45:
                ai.thrust()

            elif self.mode == "stop":
              wantedHeading = ai.angleAddRad(self.wallDir, math.pi)
              if self.count % 2 == 0:
                ai.turnToRad(wantedHeading)
              if ai.angleDiffRad(wantedHeading, heading) < ai.xdegToRad(2):
                ai.thrust()
              else:
                print("not thrusting")
              if wallDist > speed*speedConst:
                self.mode = "move"




            elif self.mode == "move":
              if itemCount == 0:
                self.mode = "wait"
                return
              itemId = 0
              for i in range(itemCount):
                if ai.itemAge(i) > 0:
                  itemId = i
                  break
              itemX = ai.itemX(itemId)
              itemY = ai.itemY(itemId)
              itemVelX = ai.itemVelX(itemId)
              itemVelY = ai.itemVelY(itemId)
              wantedHeading = math.atan2(itemY-y, itemX-x)


              if self.count % 2 == 0:
                ai.turnToRad(wantedHeading)

              if speed < maxSpeed and ai.angleDiffRad(wantedHeading, heading) < 0.018:
                ai.thrust()

              if ai.radToDeg(ai.angleDiffRad(tracking, heading)) > 45:
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
