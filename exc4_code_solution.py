#
# This is the file stub.py that can be used as a starting point for the bots
#

import libpyAI as ai

import sys
import traceback
import math
import os
import random

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
        self.mode = "travel"
        self.destructing = 0

    def tick(self):
        try:

            #
            # If we die then restart the state machine in the state "init"
            #
            if not ai.selfAlive():
                self.count = 0
                self.mode = "travel"
                self.destructing = 0
                return

            self.count += 1
            if self.count == 3:
              ai.getOption("shotspeed")
              return

            #
            # Read the "sensors"
            #

            heading = ai.selfHeadingRad() 
            tracking = ai.selfTrackingRad()
            # 0-2pi, 0 in x direction, positive toward y

            x = ai.selfX()
            y = ai.selfY()
            vx = (ai.selfVelX() + 0.5)*1.1
            vy = (ai.selfVelY() + 0.5)*1.1
            speed = (vx**2 + vy**2)**0.5

            rh = ai.radarHeight()
            rw = ai.radarWidth()

            mapWidth = ai.mapWidthPixels()
            mapHeight = ai.mapHeightPixels()

            radarToScreenY = ai.mapHeightPixels() / rh
            radarToScreenX = ai.mapWidthPixels() / rw

            # Add more sensors readings here if they are needed

            #os.system('clear')
            for i in range(0):#range(ai.asteroidCountScreen()):
              fresh = ai.asteroidFresh(i)
              print(ai.asteroidX(i))
              print(ai.asteroidY(i))
              print("size: ", ai.asteroidSize(i))
              print("type: ", ai.asteroidType(i))
              print("rotation: ", ai.asteroidRotation(i))
              print("freshness: ", fresh)
              if fresh:
                print(ai.asteroidSpeed(i))
                print(ai.asteroidTrackingRad(i))
                print("velX: ", ai.asteroidVelX(i))
                print("velY: ", ai.asteroidVelY(i))
                print("alert: ", ai.asteroidAlert(i))
              print("-------------------")
            print(ai.asteroidCountScreen())
            #print (self.mode, ai.numAsteroidScreen(), ai.numShipRadar())

            numAsteroids = ai.asteroidCountScreen()
            #print(numAsteroids, ai.asteroidTrackX(0), ai.asteroidX(0))
            #return
            if ai.selfFuel() <= 10 and not self.destructing:
              ai.selfDestruct()
              self.destructing = 1


            if numAsteroids == 0:
              self.mode = "travel"
            else:
              self.mode = "shoot"

            if self.mode == "travel":
              id = ai.closestRadarId()
              asteroidX = ai.radarX(id) * radarToScreenX
              asteroidY = ai.radarY(id) * radarToScreenY

              asteroidX = wrap(x, asteroidX, mapWidth)
              asteroidY = wrap(y, asteroidY, mapHeight)

              wantedHeading = math.atan2(asteroidY-y,asteroidX-x)
              
              if self.count % 2 == 0:
                ai.turnToRad(wantedHeading)
              
              if ai.radToXdeg(ai.angleDiffRad(heading,wantedHeading)) < 2 and speed < 5:
                ai.thrust()
              
              if ai.angleDiffRad(tracking, wantedHeading) > math.pi/2:
                ai.thrust()

            elif self.mode == "shoot":
              shotspeed = ai.getOption("shotspeed")
              if shotspeed == "queued":
                return
              dist = -1
              id = -1
              for i in range(numAsteroids):
                if not ai.asteroidFresh(i):
                  continue
                tempDist = ai.asteroidAlert(i);
                if dist == -1 or tempDist < dist:
                  dist = tempDist
                  id = i
              if id == -1:
                return
              astX        = wrap(x, ai.asteroidX(id), mapWidth)
              astY        = wrap(y, ai.asteroidY(id), mapHeight)
              astTracking = ai.asteroidTrackingRad(id)
              astVelX = ai.asteroidVelX(id)
              astVelY = ai.asteroidVelY(id)

              wantedHeading = aim(x, y, vx, vy, astX, astY, astVelX, astVelY, ai.getOption("shotspeed"))

              wantedHeading += random.randint(-4,4)*ai.xdegToRad(1)

              if self.count % 2 == 0:
                ai.turnToRad(wantedHeading)

              ai.fireShot()


        except:
            print(traceback.print_exc())
            print(sys.exc_info())


def wrap(self, target, size):
  if abs(target-self) < size/2:
    return target
  elif target-self > size/2:
    return target-size
  else:
    return target+size

def aim(selfX, selfY, selfVelX, selfVelY, targetX, targetY, targetVelX, targetVelY, bulletSpeed):
  x = targetX - selfX
  y = targetY - selfY
  vx = targetVelX - selfVelX
  vy = targetVelY - selfVelY

  time = timeOfImpact(x, y, vx, vy, bulletSpeed)


  return math.atan2(y+vy*time, x+vx*time)

def timeOfImpact(x, y, vx, vy, bulletSpeed):
  a = bulletSpeed ** 2 - (vx**2 + vy**2)
  b = x * vx + y * vy
  c = x**2 + y**2
  d = b ** 2 + a * c

  if a == 0 or d < 0:
    return 0
  time = ( b + d**0.5 ) / a
  if time < 0:
    return 0
  return time



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
