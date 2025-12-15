import cv2
import time

from storage import load_users, save_users
from face_utils import get_face_encoding, identify_user


# ---------- UI BUTTONS ----------
buttons = {
    "register": (100, 200, 400, 260),
    "identify": (100, 300, 400, 360)
}

current_action = None


def draw_button(img, text, rect):
    x1, y1, x2, y2 = rect
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), -1)
    cv2.putText(img, text, (x1 + 30, y1 + 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)


def mouse_click(event, x, y, flags, param):
    global current_action
    if event == cv2.EVENT_LBUTTONDOWN:
        for key, (x1, y1, x2, y2) in buttons.items():
            if x1 < x < x2 and y1 < y < y2:
                current_action = key


# ---------- REGISTER ----------
def register_flow():
    name = input("Enter Name: ")
    age = input("Enter Age: ")
    email = input("Enter Email: ")

    cap = cv2.VideoCapture(0)
    start = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        remaining = 10 - int(time.time() - start)

        cv2.putText(frame, f"Capturing in {remaining}s",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2)

        cv2.imshow("Register User", frame)

        if remaining <= 0:
            encoding = get_face_encoding(frame)
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            encoding = None
            break

    cap.release()
    cv2.destroyAllWindows()

    if encoding is None:
        print("❌ Face not detected properly")
        return

    users = load_users()
    users.append({
        "name": name,
        "age": age,
        "email": email,
        "encoding": encoding
    })
    save_users(users)

    print("✅ User Registered Successfully")


# ---------- IDENTIFY ----------
def identify_flow():
    users = load_users()
    if not users:
        print("❌ No users registered")
        return

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        user = identify_user(frame, users)

        if user:
            cv2.putText(frame, f"Name: {user['name']}",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)
            cv2.putText(frame, f"Email: {user['email']}",
                        (20, 80), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)
            cv2.imshow("Identify User", frame)
            cv2.waitKey(3000)
            break

        cv2.imshow("Identify User", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# ---------- MAIN ----------
cap = cv2.VideoCapture(0)
cv2.namedWindow("Face App")
cv2.setMouseCallback("Face App", mouse_click)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.putText(frame, "FACE RECOGNITION SYSTEM",
                (80, 100), cv2.FONT_HERSHEY_SIMPLEX,
                1.2, (255, 255, 255), 2)

    draw_button(frame, "REGISTER USER", buttons["register"])
    draw_button(frame, "IDENTIFY USER", buttons["identify"])

    cv2.imshow("Face App", frame)

    if current_action == "register":
        cap.release()
        cv2.destroyAllWindows()
        register_flow()
        cap = cv2.VideoCapture(0)
        current_action = None

    elif current_action == "identify":
        cap.release()
        cv2.destroyAllWindows()
        identify_flow()
        cap = cv2.VideoCapture(0)
        current_action = None

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
