import os
import threading
import serial.tools.list_ports
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import serial.tools.list_ports
ser = 0
nnn = 0
print('Search...')
ports = serial.tools.list_ports.comports(include_links=False)
for port in ports :
	print('Find port '+ port.device)
mycom = serial.Serial(port.device)
if mycom.isOpen():
	mycom.close()
mycom = serial.Serial(port.device, 115200, timeout=1,)
print('Connect ' + mycom.name)
time.sleep(1.0)
#mycom = serial.Serial(('COM28'), 38400)

def read_from_port(mycom):
	while mycom.isOpen():
		reading = mycom.readline().decode()
		handle_data(reading)
def handle_data(data):
	global nnn
	nnn = data.split(',')


thread = threading.Thread(target=read_from_port, args=(mycom,))
thread.daemon = True
thread.start()

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
				help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="csrt", help="nothing"
						"")
args = vars(ap.parse_args())
# extract the OpenCV version info
(major, minor) = cv2.__version__.split(".")[:2]
# if we are using OpenCV 3.2 OR BEFORE, we can use a special factory
# function to create our object tracker
if int(major) == 3 and int(minor) < 3:
	tracker = cv2.Tracker_create(args["tracker"].upper())
# otherwise, for OpenCV 3.3 OR NEWER, we need to explicity call the
# approrpiate object tracker constructor:
else:
	# initialize a dictionary that maps strings to their corresponding
	# OpenCV object tracker implementations
	OPENCV_OBJECT_TRACKERS = {
		"csrt": cv2.TrackerCSRT_create,
		"kcf": cv2.TrackerKCF_create,
		"boosting": cv2.TrackerBoosting_create,
		"mil": cv2.TrackerMIL_create,
		"tld": cv2.TrackerTLD_create,
		"medianflow": cv2.TrackerMedianFlow_create,
		"mosse": cv2.TrackerMOSSE_create
	}
	# grab the appropriate object tracker using our dictionary of
	# OpenCV object tracker objects
	tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
# initialize the bounding box coordinates of the object we are going
# to track
initBB = None
# if a video path was not supplied, grab the reference to the web cam
if not args.get("video", False):
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()

	time.sleep(1.0)
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])
# initialize the FPS throughput estimator
#fps = None
# loop over frames from the video stream
while True:
	# grab the current frame, then handle if we are using a
	# VideoStream or VideoCapture object
	frame = vs.read()
	frame = frame[1] if args.get("video", False) else frame
	# check to see if we have reached the end of the stream
	if frame is None:
		break
	# resize the frame (so we can process it faster) and grab the
	# frame dimensions
	ligne, gaga, gaga2 = [int(s) for s in nnn]

	if gaga2 == 10:
		ilgis = 640
		plotis = 480

	if gaga2 == 20:
		ilgis = 800
		plotis = 600

	if gaga2 == 30:
		ilgis = 1024
		plotis = 768

	if gaga2 == 40:
		ilgis = 1280
		plotis = 720

	if gaga2 == 50:
		ilgis = 1360
		plotis = 768

	if gaga2 == 60:
		ilgis = 1366
		plotis = 768

	if gaga2 == 70:
		ilgis = 1440
		plotis = 900

	if gaga2 == 80:
		ilgis = 1536
		plotis = 864

	if gaga2 == 90:
		ilgis = 1600
		plotis = 900

	if gaga2 == 100:
		ilgis = 1920
		plotis = 1080

	frame = cv2.resize(frame, (ilgis, plotis))
	#frame = frame[0:480, 0:640]
	#frame = imutils.resize(frame, width=640)
	#frame = cv2.resize(frame, (640, 480))
	(H, W) = (plotis, ilgis)
	# check to see if we are currently tracking an object
	if initBB is not None:
		# grab the new bounding box coordinates of the object
		(success, box) = tracker.update(frame)
		if success:
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(frame, (x, y), (x + w, y + h),
						(0, 255, 0), 0)
			roi_color = frame[y:y + h, x:x + w]
			arr = {y: y + h, x: x + w}
			xx = int(x + (x + h)) / 2
			yy = int(y + (y + w)) / 2
			center = (xx, yy)
			#print("Center of Rectangle is :", center)
			data = "X{0: .0f}Y{1: .0f}Z".format(xx, yy)
			#print("output = '" + data + "'")

			mycom.write(data.encode())
		# update the FPS counter
		#fps.update()
		#fps.
		# the frame
		#info = [
			#("Trackeris", args["tracker"]),
			#("Sekimas", "Taip" if success else "Ne"),
			#("KPS", "{:.2f}".format(fps.fps())),
		#]
		# loop over the info tuples and draw them on our frame
		#for (i, (k, v)) in enumerate(info):
			#text = "{}: {}".format(k, v)
			#cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
						#cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if  gaga == 10:
		kvadratas = W/50
	if  gaga == 20:
		kvadratas = W/45
	if  gaga == 30:
		kvadratas = W/40
	if gaga == 40:
		kvadratas = W/35
	if  gaga == 50:
		kvadratas = W/30
	if gaga == 60:
		kvadratas = W/25
	if gaga == 70:
		kvadratas = W/20
	if gaga == 80:
		kvadratas = W/15
	if gaga == 90:
		kvadratas = W/10
	if  gaga == 100:
		 kvadratas = W/5

	if  ligne == 1:
		initBB = (W/2-kvadratas/2, H/2-kvadratas/2, kvadratas, kvadratas)
		# initBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
		tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
		tracker.init(frame, initBB)
		#fps = FPS().start()
	if ligne == 3:
		tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
		#        tracker.init(frame, initBB)
		#        fps = FPS().start()
	elif key == ord("q"):
		break

if not args.get("video", False):
	vs.stop()
# otherwise, release the file pointer
else:
	vs.release()
cv2.destroyAllWindows()
