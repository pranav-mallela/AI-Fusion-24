import numpy as np
import cv2
import time
import os
import threading
import requests

# Local imports
from utils import Tracker, Command, Capture, start_node, rescale_frame

# Variables initialization
mutex = 0 
debug = True
UDP = 'udp://192.138.10.1:11111'

# Thread creation for starting ROS node
node_thread = threading.Thread(target=start_node) 
node_thread.deamon = True
node_thread.start()

# Load COCO class labels
labelsPath = "tello/req_files/coco.names"
LABELS = open(labelsPath).read().strip().split("\n")

# Initialize colors for class labels
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

# Derive paths to YOLO weights and configuration
weightsPath = "tello/req_files/yolov3.weights"
if not os.path.exists(weightsPath):
    print(f"[INFO] Weights not found in the following path: {weightsPath}, Downloading now ...")
    os.system('cmd /c "curl -o tello/req_files/yolov3.weights https://pjreddie.com/media/files/yolov3.weights')
configPath = "tello/req_files/yolov3.cfg"

# Load YOLO object detector
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Check debug mode and set up video capture accordingly
if not debug:
    isStreamOn = requests.get("http://localhost:4000/test/streamon")
    print(isStreamOn.text)
    time.sleep(2)
    udp = UDP
    capture = Capture(udp)
    command = Command()
    print("[INFO] Starting video from Tello")
else:
    capture = Capture(0)
    command = Command(debug=True)
    print("[INFO] Starting video from webcam")

# Check if Tello drone should takeoff
if not debug:
    isTakeoff = requests.get('http://localhost:4000/test/takeoff')
    print(isTakeoff.status_code)

# Create Tracker object
tracker = Tracker(720/2, 960/2)
capture.startCaptureThread()
countOfFrames = 0

# Main loop for processing video frames
while True:
    frame = capture.read()
    
    if mutex == 0 and not debug:
        command.startCmdThread()
        mutex = 1

    H = 720/2 
    W = 960/2
    frame = rescale_frame(frame, percent=50)
    
    # Convert frame to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Construct blob and perform forward pass through YOLO
    blob = cv2.dnn.blobFromImage(rgb, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    end = time.time()

    # Initialize lists for detected bounding boxes, confidences, and class IDs
    boxes = []
    confidences = []
    classIDs = []

    # Loop over each of the layer outputs
    for output in layerOutputs:
        # Loop over each detection
        for detection in output:
            # Extract class ID and confidence
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            # Filter out weak predictions
            if confidence > 0.5:
                # Scale bounding box coordinates
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # Derive top-left corner of bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # Update lists of bounding box coordinates, confidences, and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
                
    # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.6)

    # Ensure at least one detection exists
    if len(idxs) > 0:
        # Loop over the indexes we are keeping
        for i in idxs.flatten():
            # Extract bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            
            # Draw bounding box rectangle and label on the frame
            color = [int(c) for c in COLORS[classIDs[i]]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 1)
            text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            check = text.split(':')
            if check[0] == 'person':
                # Determine direction of movement
                direction, value = tracker.getDirection(x, y, w, h, end - start)
                command.putInQue(direction)
                countOfFrames = 0
            else:
                countOfFrames += 1
                if countOfFrames == 4:
                    direction = [0, 0, 0, 20]
                    command.putInQue(direction)
                    countOfFrames = 0
                continue
            
            # Output time elapsed for processing single frame
            elap = (end - start)
            print("[INFO] single frame took {:.4f} seconds".format(elap))
    
    # Display frame
    cv2.imshow("frame", frame)
    
    # Exit loop if 'q' is pressed
    if cv2.waitKey(300) & 0xFF == ord('q'):
            break

# Free resources and stop program
print('[INFO] Freeing resources and stopping program')
capture.stopCaptureThread()
capture.release()
command.stopCmdThread()
cv2.destroyAllWindows()
