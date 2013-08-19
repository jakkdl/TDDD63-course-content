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

class myai:
    def __init__(self):
        self.count = 0
        self.mode = "init"
        self.turnLeft = (0)
        self.turnRight = (0)
        self.count = 0

    def tick(self):
        try:
          self.count += 1
          selfX = ai.selfX()
          selfY = ai.selfY()
          selfVelX = ai.selfVelX()
          selfVelY = ai.selfVelY()
          selfHeading = ai.selfHeadingDeg()
          enemyId=ai.closestShipId()
          if enemyId != -1:
            enemyX=ai.screenEnemyXId(enemyId)
            enemyY=ai.screenEnemyYId(enemyId)
            (enemyX,enemyY)=ClosestEnemy(selfX, selfY, enemyX, enemyY, 700)
            enemyVel = ai.enemySpeedId(enemyId)
            enemyTracking = ai.enemyTrackingRadId(enemyId)
            if enemyTracking == None or math.isnan(enemyTracking):
              enemyVelX = enemyVelY = 0
            else:
              enemyVelX = enemyVel*math.cos(enemyTracking)
              enemyVelY = enemyVel*math.sin(enemyTracking)
            aim = aimAt(selfX, selfY, selfVelX, selfVelY, enemyX, enemyY,
                enemyVelX, enemyVelY, 20)

            diff = selfHeading - aim

            if aim == -1:
              diff = 10 #so we don't shoot
              aim = selfHeading


            if diff > 180:
              diff -= 360
            elif diff < -180:
              diff += 360
            diff = round(diff/2.8125)
          else:
            diff = 0
            aim = ai.selfHeadingDeg()
          

          if self.count % 2 == 0:
            if abs(diff) >= 4:
              ai.setTurnSpeed(abs(diff))
              if diff > 0:
                self.turnLeft = 0
                self.turnRight = 1
              else:
                self.turnRight = 0
                self.turnLeft = 1
            elif abs(diff) > 0:
              ai.setTurnSpeed(64)
              ai.turn(-int(diff*3))

              self.turnRight = self.turnLeft = 0
          else:
            self.turnRight = self.turnLeft = 0


          if abs(diff) <= 1 and enemyId != -1:
            ai.fireShot()


          ai.turnLeft(self.turnLeft)
          ai.turnRight(self.turnRight)

        except:
            e = sys.exc_info()
            print ("ERROR: ", e[1], "in", traceback.extract_tb(e[2]))


def aimAt(selfX, selfY, selfVelX, selfVelY, enemyX, enemyY,
    enemyVelX, enemyVelY, bulletVel):
  relX = enemyX-selfX
  relY = enemyY-selfY
  relVelX = enemyVelX - selfVelX
  relVelY = enemyVelY - selfVelY
  time = timeOfImpact(relX, relY, relVelX, relVelY, bulletVel)
  if time == -1:
    return -1
  return ai.radToDeg(math.atan2(relY+relVelY*time,relX+relVelX*time))

def timeOfImpact(relPosX, relPosY, relVelX, relVelY, bulVel):
  a = bulVel ** 2 - (relVelX**2 + relVelY**2)
  b = relPosX * relVelX + relPosY * relVelY
  c = relPosX ** 2 + relPosY ** 2
  d = b ** 2 + a * c

  if a != 0 and d >= 0:
    t = (b + d ** 0.5) / a
    if t >= 0:
      return t

  return -1
  

def ClosestEnemy(selfX, selfY, enemyX, enemyY, mapConstant):
  minDistance = sys.maxsize
  for i in range(-1, 2): #-1, 0, 1
    for j in range(-1, 2):
      x = enemyX + mapConstant * i
      y = enemyY + mapConstant * j
      distance = Distance(selfX, selfY, x, y)
      if distance < minDistance:
        minX = x
        minY = y
        minDistance = distance
  return (minX, minY)

def Distance(x0, y0, x1, y1):
  return ((x1-x0)**2 + (y1-y0)**2)**0.5

bot = myai()

def AI_loop():
    bot.tick()

(options, args) = parser.parse_args()

port = 15345 + options.group
name = "Lucky Luke 2.0"

ai.start(AI_loop,["-name", name, 
                  "-join", 
                  "-showHUD", "no",
                  "-turnResistance", "0",
                  "-port", str(port)])
