from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2

def nothing(arg):
        pass

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))

cv2.namedWindow('image')

cv2.createTrackbar('HL','image',0,180,nothing)
cv2.createTrackbar('SL','image',0,255,nothing)
cv2.createTrackbar('VL','image',0,255,nothing)
cv2.createTrackbar('HH','image',0,180,nothing)
cv2.createTrackbar('SH','image',0,255,nothing)
cv2.createTrackbar('VH','image',0,255,nothing)
# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    image = frame.array
 	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


    lower = [45, 83, 122];
	upper = [80, 255, 255];


 	lower = [cv2.getTrackbarPos('HL','image'), cv2.getTrackbarPos('SL','image'), cv2.getTrackbarPos('VL','image')]
 	upper = [cv2.getTrackbarPos('HH','image'), cv2.getTrackbarPos('SH','image'), cv2.getTrackbarPos('VH','image')]

	lower = np.array(lower, 'uint8')
	upper = np.array(upper, 'uint8')

	mask = cv2.inRange(hsv, lower, upper)
	mask = cv2.dilate(mask, None, iterations=2)
	mask = cv2.erode(mask, None, iterations=2)



	roi = cv2.bitwise_and(image,image, mask=mask)
	blur = roi
	# cv2.blur(roi, (1,1))

	# show the frame
	cv2.imshow("image", blur)
	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
        # cv2.imwrite("rand.png",image)
		break
