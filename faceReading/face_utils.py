import face_recognition
import numpy as np

def get_face_encoding(frame):
    rgb = frame[:, :, ::-1]  # BGR → RGB

    encodings = face_recognition.face_encodings(rgb)
    if len(encodings) != 1:
        return None

    return encodings[0]

def identify_user(frame, users, tolerance=0.45):
    encoding = get_face_encoding(frame)
    if encoding is None:
        return None

    known_encodings = [u["encoding"] for u in users]
    distances = face_recognition.face_distance(known_encodings, encoding)

    if len(distances) == 0:
        return None

    best_match = np.argmin(distances)
    if distances[best_match] < tolerance:
        return users[best_match]

    return None
