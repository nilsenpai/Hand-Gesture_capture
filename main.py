import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

WRIST, THUMB_TIP, INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP = 0, 4, 8, 12, 16, 20
INDEX_PIP, MIDDLE_PIP, RING_PIP, PINKY_PIP = 6, 10, 14, 18
INDEX_MCP, MIDDLE_MCP, RING_MCP, PINKY_MCP = 5, 9, 13, 17
THUMB_IP, THUMB_MCP = 3, 2

def dist(a, b): return math.hypot(a.x - b.x, a.y - b.y)

def angle(p1, p2, p3):
    v1, v2 = (p1.x - p2.x, p1.y - p2.y), (p3.x - p2.x, p3.y - p2.y)
    dot = v1[0]*v2[0] + v1[1]*v2[1]
    n1, n2 = math.hypot(*v1), math.hypot(*v2)
    if not n1 or not n2: return 0
    return math.degrees(math.acos(max(-1,min(1,dot/(n1*n2)))))

def finger_up(lms, tip, pip, mcp):
    return dist(lms[tip], lms[WRIST]) > dist(lms[pip], lms[WRIST]) and angle(lms[mcp], lms[pip], lms[tip]) > 160

def thumb_up(lms):
    return lms[THUMB_TIP].y < lms[THUMB_IP].y < lms[THUMB_MCP].y and lms[THUMB_TIP].y < lms[WRIST].y

def get_gesture(lms):
    fingers = {
        "thumb": dist(lms[THUMB_TIP], lms[WRIST]) > dist(lms[THUMB_IP], lms[WRIST]),
        "index": finger_up(lms, INDEX_TIP, INDEX_PIP, INDEX_MCP),
        "middle": finger_up(lms, MIDDLE_TIP, MIDDLE_PIP, MIDDLE_MCP),
        "ring": finger_up(lms, RING_TIP, RING_PIP, RING_MCP),
        "pinky": finger_up(lms, PINKY_TIP, PINKY_PIP, PINKY_MCP)
    }

    up = [f for f,v in fingers.items() if v]

    if not up: return "Fist"
    if fingers["index"] and fingers["middle"] and not fingers["ring"] and not fingers["pinky"]:
        return "Peace"
    if len(up) >= 4: return "Open Palm"
    if fingers["thumb"] and not any(fingers[f] for f in ["index","middle","ring","pinky"]) and thumb_up(lms):
        return "Thumbs Up"
    return "Unknown"

def main():
    cap = cv2.VideoCapture(0)
    prev_gesture = None  # remember last gesture

    with mp_hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.6) as hands:
        while True:
            ret, frame = cap.read()
            if not ret: break
            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]
            res = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            gesture = "No Hand"

            if res.multi_hand_landmarks:
                lms = res.multi_hand_landmarks[0].landmark
                mp_draw.draw_landmarks(frame, res.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
                gesture = get_gesture(lms)
                xs, ys = [int(pt.x*w) for pt in lms], [int(pt.y*h) for pt in lms]
                cv2.rectangle(frame,(min(xs)-10,min(ys)-10),(max(xs)+10,max(ys)+10),(0,255,0),2)

            # only print when gesture changes
            if gesture != prev_gesture:
                print("Detected:", gesture)
                prev_gesture = gesture

            cv2.putText(frame, f"Gesture: {gesture}", (20,40), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            cv2.imshow("Hand Gestures", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release(); cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

