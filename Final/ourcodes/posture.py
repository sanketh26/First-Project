from naoqi import ALProxy
import sys

posture = sys.argv[1]
postureProxy = ALProxy('ALRobotPosture','localhost',9559)

postureProxy.goToPosture(posture, 1.0)

print postureProxy.getPostureFamily()