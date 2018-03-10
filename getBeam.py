from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))



# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

	
	image = frame.array
 	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


    lower = [63, 158, 91];
	upper = [86, 255, 255];



	lower = np.array(lower, 'uint8')
	upper = np.array(upper, 'uint8')

	mask = cv2.inRange(hsv, lower, upper)
	mask = cv2.dilate(mask, None, iterations=2)
	mask = cv2.erode(mask, None, iterations=2)


    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)[-2]


	roi = cv2.bitwise_and(image,image, mask=mask)
	blur = roi #cv2.blur(roi, (1,1))

    points = []

    for c in cnts:
        (x, y), radius = cv2.minEnclosingCircle(c)
        if(radius > 2):
            points.append([int(x), int(y)])

    if(len(points) == 4):

        points.sort(key=lambda x:x[1])
        top = points[:2]
        top.sort()
        bottom = points[2:]
        bottom.sort()
        pts = top + bottom
        transPoints = np.float32([[0,0], [300,0],[0,50],[300,50]])
        M = cv2.getPerspectiveTransform(np.float32(pts),transPoints)
        dst = cv2.warpPerspective(image,M,(300,50))
        blur = dst

	# show the frame
	cv2.imshow("image", blur)
	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
        # cv2.imwrite("rand.png",image)
		break
	if key == ord("b"):
            cv2.imwrite('blur.png', blur)
            cv2.imwrite("rand.png",image)
            break
