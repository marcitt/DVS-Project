import cv2
import mediapipe as mp
import pyautogui
import sys
import os
import numpy as np

from gui import prepare_for_connected_components, extract_icons

"""
Original eye-controlled mouse framework adapted from:
ProgrammingHero1. (2023). eye_controlled_mouse [GitHub repository].
https://github.com/ProgrammingHero1/eye_controlled_mouse
I adapted this to integrate it with my GUI processing strategies + added the concept of "eye-snapping"
Eye snapping was inspired by this paper on "voice-snapping": https://dl.acm.org/doi/10.1145/3532106.3533452
Voice Snapping: Inclusive Speech Interaction Techniques for Creative Object Manipulation
"""

### GUI EXTRACTION CODE 

screen_w, screen_h = pyautogui.size()
screenshot = pyautogui.screenshot()

image = np.array(screenshot)
resized = cv2.resize(image, (screen_w, screen_h)) # this is because resolution doesn't automatically match up

bounding_boxes, centres = extract_icons(resized)

for p in centres:
    cv2.circle(resized,(int(p[0]),int(p[1])), 5, (255,0,0), -1)

cv2.imwrite("latest_screenshot.png", resized)
cv2.imwrite("bounding_boxes.png", bounding_boxes)

## EYE TRACKING CODE

pyautogui.FAILSAFE = True

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True) #using mediapipe

control_center_x = None
control_center_y = None
box_size = 0.25
xmin = None
ymin = None

try:
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape
        if landmark_points:
            landmarks = landmark_points[0].landmark
            
            """
            This is where I also added some adaptions to the original eye tracking framework.
            I adapted it to use the centre between the right and left eye.
            I found these coordinates from: https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker
            """
        
            # right eye 
            right_landmark = landmarks[473]
            rx = right_landmark.x 
            ry = right_landmark.y
            
            # left eye
            left_landmark = landmarks[468]
            lx = left_landmark.x 
            ly = left_landmark.y
            
            avg_x = (rx+lx)/2
            avg_y = (ry+ly)/2

            screen_x = avg_x * screen_w
            screen_y = avg_y * screen_h
            
            """
            Citation: Eye-tracking normalization logic below was generated with guidance from
            OpenAI ChatGPT (GPT-5). This code scales and clamps eye coordinates to a smaller control region
            to improve cursor sensitivity.
            """
            # START OF CITED CODE
            if control_center_x is None:
                control_center_x = avg_x
                control_center_y = avg_y
            xmin = control_center_x - box_size/2
            xmax = control_center_x + box_size/2
            ymin = control_center_y - box_size/2
            ymax = control_center_y + box_size/2
            nx = (avg_x - xmin) / (xmax - xmin)
            ny = (avg_y - ymin) / (ymax - ymin)
            nx = max(0, min(1, nx))
            ny = max(0, min(1, ny))
            # END OF CITED CODE

            cursor_position = pyautogui.position()
            x_c, y_c = cursor_position

            screen_x = nx * screen_w
            screen_y = ny * screen_h
            
            candidate = np.array((screen_x,screen_y))

            """
            Nearest-coordinate computation adapted from:
            # Stack Overflow. (2021). "How to find the closest coordinate from a list of points".
            # https://stackoverflow.com/questions/66238749/how-to-find-the-closest-coordinate-from-a-list-of-points 
            """
            # START OF CITED CODE
            distances = np.linalg.norm(centres-candidate, axis=1)
            min_index = np.argmin(distances)
        
            snap_x = int(centres[min_index][0])
            snap_y = int(centres[min_index][1])
            # END OF CITED CODE
            
            icon_distance = distances[min_index]
            print(f"the closest GUI icon is at {snap_x, snap_y}, at a distance of {icon_distance}")
            
            """
            INSIGHTS / NOTES
            If we are able to effectively upscale SIFT matching we can also get the command line to print the label of the currently focused GUI icon.
            
            I want to achieve 'eye-snapping' e.g. when the cursor approaches an icon - it will snap to the GUI icon.
            The goal here is to help users who may have difficulty with stable movement or precision.
            
            1. My initial approach was to use a simple snap rule where if the icon is less than a certain distance away the cursor will snap to it.            
            This itself works quite well once a good configuration is found

            """
            if icon_distance < 120:
                pyautogui.moveTo(snap_x, snap_y)
            else:
                pyautogui.moveTo(screen_x, screen_y)
            

except pyautogui.FailSafeException:
    print("Failsafe triggered")

except KeyboardInterrupt:
    print("Keyboard interrupt")

finally:
    cam.release()
    cv2.destroyAllWindows()
    sys.exit(0)