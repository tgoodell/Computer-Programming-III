import time

from Phidget22.Net import *
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.DistanceSensor import *

Net.addServer("", "192.168.100.1", 5661, "", 0)

leftMotors = DCMotor()
rightMotors = DCMotor()
sonar = DistanceSensor()

leftMotors.setChannel(0)
rightMotors.setChannel(1)

leftMotors.openWaitForAttachment(2000)
rightMotors.openWaitForAttachment(2000)
sonar.openWaitForAttachment(2000)


leftMotors.setTargetVelocity(0.5)
rightMotors.setTargetVelocity(0.5)

while sonar.getDistance() > 500:
    time.sleep(0.1)

lStops = 0

lStart = time.time()
while sonar.getDistance() < 500:
    time.sleep(0.1)
    lStops+=1

lEnd = time.time()-lStart

leftMotors.setTargetVelocity(0)
rightMotors.setTargetVelocity(0)

time.sleep(1.5)

leftMotors.setTargetVelocity(-0.8)
rightMotors.setTargetVelocity(1)

time.sleep(0.64)

leftMotors.setTargetVelocity(0)
rightMotors.setTargetVelocity(0)

time.sleep(1.5)

leftMotors.setTargetVelocity(-1)
rightMotors.setTargetVelocity(-1)

time.sleep(1)

leftMotors.setTargetVelocity(0.5)
rightMotors.setTargetVelocity(0.5)

while sonar.getDistance() > 500:
    time.sleep(0.1)

wStart = time.time()
wStops = 0
while sonar.getDistance() < 500:
    time.sleep(0.1)
    wStops+=1

wEnd = time.time()-wStart

length = lEnd*12.5*0.683
width = wEnd*12.5*0.683

print(length)
print(width)
