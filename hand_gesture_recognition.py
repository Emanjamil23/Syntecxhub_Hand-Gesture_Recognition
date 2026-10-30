"""
Project 2 - Hand Gesture Recognition
Syntecxhub Internship

What this script does:
1. Opens the webcam
2. Finds the hand landmarks using MediaPipe
3. Recognizes simple gestures (open palm, fist, thumbs up, peace sign)
4. Maps each gesture to an action (play/pause, volume, next track)

Install:
    pip install opencv-python mediapipe pyautogui

Run:
    python hand_gesture_recognition.py

Press 'q' to quit.
"""

import time
import cv2
import mediapipe as mp

# pyautogui is used to press keyboard media keys.
# If it is not installed, the program will only print the action.
try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# landmark numbers (from the MediaPipe hand model)
THUMB_TIP = 4
THUMB_IP = 3
INDEX_MCP = 5
FINGER_TIPS = [8, 12, 16, 20]   # index, middle, ring, pinky
FINGER_PIPS = [6, 10, 14, 18]   # the middle joint of each finger


def fingers_up(landmarks):
    """Return a list [index, middle, ring, pinky] with 1 if finger is up, else 0."""
    result = []
    for tip, pip in zip(FINGER_TIPS, FINGER_PIPS):
        # in the image, smaller y means higher up
        if landmarks[tip].y < landmarks[pip].y:
            result.append(1)
        else:
            result.append(0)
    return result


def thumb_is_up(landmarks):
    """Thumb is pointing up if its tip is above the thumb joint and the index knuckle."""
    tip_y = landmarks[THUMB_TIP].y
    ip_y = landmarks[THUMB_IP].y
    mcp_y = landmarks[INDEX_MCP].y
    return tip_y < ip_y and tip_y < mcp_y


def thumb_is_out(landmarks):
    """Thumb is stretched sideways (used for open palm)."""
    thumb_x = landmarks[THUMB_TIP].x
    index_x = landmarks[INDEX_MCP].x
    return abs(thumb_x - index_x) > 0.05


def classify_gesture(landmarks):
    """Look at the hand and decide which gesture it is."""
    fingers = fingers_up(landmarks)
    total = sum(fingers)

    # all four fingers up + thumb out = open palm
    if total == 4 and thumb_is_out(landmarks):
        return "Open Palm"

    # all fingers folded
    if total == 0:
        if thumb_is_up(landmarks):
            return "Thumbs Up"
        return "Fist"

    # index and middle up, others folded = peace sign
    if fingers == [1, 1, 0, 0]:
        return "Peace"

    return "Unknown"


# gesture -> action name
ACTIONS = {
    "Open Palm": "Play / Pause",
    "Fist": "Volume Down",
    "Thumbs Up": "Volume Up",
    "Peace": "Next Track",
}

# gesture -> keyboard key
KEYS = {
    "Open Palm": "playpause",
    "Fist": "volumedown",
    "Thumbs Up": "volumeup",
    "Peace": "nexttrack",
}

# how many seconds to wait before the same gesture can trigger again
COOLDOWN = {
    "Open Palm": 1.5,
    "Fist": 0.4,
    "Thumbs Up": 0.4,
    "Peace": 1.5,
}


def do_action(gesture):
    """Run the action linked to the gesture."""
    action = ACTIONS.get(gesture)
    if action is None:
        return
    print("Gesture:", gesture, "->", action)
    if HAS_PYAUTOGUI:
        pyautogui.press(KEYS[gesture])


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open the webcam.")
        return

    last_time = {}           # when each gesture last triggered
    current = "Unknown"      # gesture seen in the last frame
    same_count = 0           # how many frames in a row we saw the same gesture
    FRAMES_NEEDED = 5        # gesture must stay for 5 frames to count (avoids flicker)

    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
    ) as hands:

        while True:
            ok, frame = cap.read()
            if not ok:
                break

            frame = cv2.flip(frame, 1)   # mirror view so it feels natural
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            gesture = "No Hand"

            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
                gesture = classify_gesture(hand.landmark)

            # count how long the same gesture stays
            if gesture == current:
                same_count += 1
            else:
                current = gesture
                same_count = 1

            # trigger the action if gesture is stable and cooldown is over
            if same_count >= FRAMES_NEEDED and gesture in ACTIONS:
                now = time.time()
                if now - last_time.get(gesture, 0) > COOLDOWN[gesture]:
                    do_action(gesture)
                    last_time[gesture] = now

            # show text on screen
            cv2.putText(frame, "Gesture: " + gesture, (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            action_text = ACTIONS.get(gesture, "-")
            cv2.putText(frame, "Action: " + action_text, (10, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 200, 0), 2)

            cv2.imshow("Hand Gesture Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
