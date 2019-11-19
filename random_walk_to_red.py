#!/usr/bin/env python
import rospy

# Imports Color message structure for monitoring if
# turtle is over red square

from turtlesim.srv import SetPen
from turtlesim.msg import Color
from geometry_msgs.msg import Twist
import random

droprate = 30
droppacket = 0
def colour_update(msg):
    global droprate
    global droppacket
    if(((msg.r == 0) and(msg.g == 255) and(msg.b == 0))):
        droppacket = 1
        backup = Twist()
        backup.angular.z = 3.14
        backup.linear.x = -3
        twist_pub.publish(backup)
        return
    print('Colour: %d %d %d ' % (msg.r, msg.g, msg.b))
    if((msg.r == 255) and (msg.g == 0) and (msg.b == 0)):
        dead_stop = Twist()
        twist_pub.publish(dead_stop)
        return
    droppacket = (droppacket + 1)%droprate
    if(droppacket != 0):
        return
    next_move = Twist() 
    # initialises to zero motion
    if(random.randint(0,1) == 0):
        next_move.linear.x = 3
    else:
        next_move.angular.z =3.14* random.uniform(-1,1)
        # Publish the next_move
    twist_pub.publish(next_move)

if __name__=='__main__':
     # Initialise node
        rospy.init_node('random_walker',anonymous=True)


        # Create Color subscriber and attach to colour_update() callback

        colour_sub = rospy.Subscriber("turtle1/color_sensor",Color,\
                              colour_update, queue_size=1)
        twist_pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=1)
        # This try / except block uses the service interface of the 
        # turtlesim node to instruct it not to draw its path
        try:
            rospy.wait_for_service('turtle1/set_pen')
            set_pen = rospy.ServiceProxy('turtle1/set_pen', SetPen)
            set_pen(0,0,0,0,1)
        except rospy.ServiceException, e:
            print"Service call failed: %s"%e
        # Here we enter into the ros spin loop which hands control
        # to ROS. This results in execution of the colour_update()
        # callback whenever a Color message is received.
        try:
            rospy.spin()
        except KeyboardInterrupt:
            print("Keyboard input")
                

