import cv2
import numpy as np

class BallProcessing:

    def __init__(self):

        #self.greenLower = (16, 70, 90)# dark
	#self.greenUpper = (57, 200, 200) # light
        #  30 180 170
        # ball [[[ 24 254 243]]]
        # self.greenLower = (22, 234, 163)# dark
        # self.greenUpper = (53, 255, 240) # light
        # self.greenLower = (14, 200, 163)# dark
        # self.greenUpper = (34, 255, 240) # light
        # self.greenLower = (14, 130, 150)# dark
        # self.greenUpper = (34, 255, 240) # light
        self.yellowLower = (14, 180, 200)# dark
        self.yellowUpper = (34, 255, 255) # light

        self.font                   = cv2.FONT_HERSHEY_SIMPLEX
        self.bottomLeftCornerOfText = (30,50)
        self.fontScale              = 0.5
        self.fontColor              = (255,255,255)
        self.lineType               = 1
        self.current_data           = {"obj_x":0,"obj_y":0, "obj_r":0}

    def process(self, frame):
    	# resize the frame, blur it, and convert it to the HSV
        # color space
        #frame = imutils.resize(frame, width=600)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, self.yellowLower, self.yellowUpper)

        # cv2.imshow("Frame2", mask)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        self.current_data = {"obj_x":0,"obj_y":0, "obj_r":0}
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 10:
                self.current_data = {"obj_x": int(x),"obj_y": int(y), "obj_r": int(radius)}
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

                cv2.putText(frame,"({:d},{:d},{:d})".format(int(x),int(y),int(radius)),
                    (int(x), int(y)),
                    self.font,
                    self.fontScale,
                    self.fontColor,
                    self.lineType)

        return mask, frame

    def get_current_data(self):
        return self.current_data
