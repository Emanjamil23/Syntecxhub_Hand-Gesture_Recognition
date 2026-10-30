
Hand Gesture Recognition

Syntecxhub Internship - Project 2

A simple Python project that detects a hand through the webcam, recognizes a few gestures, and links each gesture to an action like play/pause or volume control.

Features
Detects hand landmarks in real time using MediaPipe
Recognizes 4 simple gestures: Open Palm, Fist, Thumbs Up, Peace
Maps each gesture to a media action
Shows the detected gesture and action on the webcam window
Cooldown and frame check so one gesture does not trigger many times by mistake
Gestures and Actions
Gesture	Action
Open Palm	Play / Pause
Fist	Volume Down
Thumbs Up	Volume Up
Peace (two fingers)	Next Track
Requirements
Python 3.8 to 3.11
A working webcam

Libraries:

pip install opencv-python mediapipe pyautogui
How to Run
python hand_gesture_recognition.py

Press q to close the window.

How It Works
OpenCV reads each frame from the webcam.
MediaPipe finds 21 landmark points on the hand.
The code checks if each finger is up or folded by comparing the fingertip position with the finger joint.
Based on which fingers are up, the gesture is decided.
If the same gesture stays for a few frames, its action runs using pyautogui (keyboard media keys).
Tips
Keep your hand upright and facing the camera.
Use good lighting and a plain background.
If pyautogui is not installed, the program only prints the action.
Project Files
hand_gesture_recognition.py - main script
README.md - project description
Author

Eman Jamil
