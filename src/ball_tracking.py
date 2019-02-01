#!/usr/bin/env python
from __future__ import print_function

import roslib
import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image, CompressedImage
from geometry_msgs.msg import Twist, Point, Quaternion
from ball_processing import BallProcessing
# from cv_bridge import CvBridge, CvBridgeError

roslib.load_manifest('turtlebro_examples')

angular_speed = 0.4

rospy.init_node('demo_ball_tracking')
image_pub = rospy.Publisher("image/compressed", CompressedImage, queue_size=1)
mask_pub  = rospy.Publisher("mask/compressed", CompressedImage, queue_size=1)
cmd_vel = rospy.Publisher('cmd_vel', Twist, queue_size=5)
bp = BallProcessing()

r = rospy.Rate(20) # 30 Hz
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

# bridge = CvBridge()

while not rospy.is_shutdown():

    ret,im = cap.read()
    #blur = cv2.GaussianBlur(im,(0,0),5)
    #cv2.imshow('camra blur', blur)
    #image_pub.publish(bridge.cv2_to_imgmsg(im, encoding="bgr8")) #

    mask, frame = bp.process(im)

    frame_msg = CompressedImage()
    frame_msg.header.stamp = rospy.Time.now()
    frame_msg.format = "jpeg"
    frame_msg.data = np.array(cv2.imencode('.jpg', frame)[1]).tostring()
    image_pub.publish(frame_msg)

    mask_msg = CompressedImage()
    mask_msg.header.stamp = rospy.Time.now()
    mask_msg.format = "jpeg"
    mask_msg.data = np.array(cv2.imencode('.jpg', mask)[1]).tostring()
    mask_pub.publish(mask_msg)
    # r.sleep()

    params = bp.get_current_data()

    move_cmd = Twist()
    if(params['obj_x'] > 0 and params['obj_y'] > 0 and params['obj_r'] > 5):
        if(params['obj_x'] > 400):
            move_cmd.angular.z = -angular_speed
            # if(params['obj_x'] > 500):
            #     move_cmd.angular.z = angular_speed*2

            # print('go right')

        if(params['obj_x'] < 240):
            move_cmd.angular.z = angular_speed
            # if(params['obj_x'] < 140):
            #     move_cmd.angular.z = -angular_speed*2
            # print('go left')

#        if(params['obj_x'] >=240 and params['obj_x'] <= 400):
            # print('stop')

    cmd_vel.publish(move_cmd)

    if cv2.waitKey(10) == '27':
        break
