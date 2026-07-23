#code to add check for the deepfake images for proxy attendance . 
import cv2
import face_recognition
import numpy as np
import datetime
import os
import dlib
from scipy.spatial import distance

# Load dlib's face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Ensure correct path

# Eye landmarks
LEFT_EYE = list(range(42, 48))
RIGHT_EYE = list(range(36, 42))

# Function to calculate Eye Aspect Ratio (EAR)
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Function to mark attendance
def mark_attendance(name, attendance_record):
    if name not in attendance_record:
        with open("attendance.csv", "a") as f:
            today = datetime.date.today()
            now = datetime.datetime.now().strftime("%H:%M:%S")
            f.write(f"{today},{now},{name}\n")
        attendance_record.append(name)

# Load images and encode faces
def load_images_and_encode():
    known_faces_encodings = []
    known_faces_names = []

    # DataSet
    image_paths = ["suraj.jpg", "surajjpg.jpg"]

    for path in image_paths:
        if os.path.exists(path):
            image = face_recognition.load_image_file(path)
            face_encodings = face_recognition.face_encodings(image)
            if face_encodings:
                known_faces_encodings.append(face_encodings[0])
                known_faces_names.append(os.path.splitext(os.path.basename(path))[0])
            else:
                print(f"No face detected in {path}")
        else:
            print(f"File not found: {path}")

    return known_faces_encodings, known_faces_names

# Main function for face recognition and blink detection
def recognize_faces():
    EAR_THRESHOLD = 0.21  # Eye aspect ratio below which eye is considered closed
    CONSEC_FRAMES = 3     # Number of consecutive frames with blink

    blink_counter = 0

    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not video_capture.isOpened():
        print("Error opening video capture device.")
        return

    attendance_record = []
    known_faces_encodings, known_faces_names = load_images_and_encode()

    while True:
        ret, frame = video_capture.read()

        if not ret:
            print("Error reading frame from camera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_faces_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_faces_names[first_match_index]

                # Blink Detection using dlib
                rect = dlib.rectangle(left, top, right, bottom)
                landmarks = predictor(gray, rect)

                left_eye = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in LEFT_EYE])
                right_eye = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in RIGHT_EYE])

                left_EAR = eye_aspect_ratio(left_eye)
                right_EAR = eye_aspect_ratio(right_eye)
                avg_EAR = (left_EAR + right_EAR) / 2.0

                # Draw eye contours
                cv2.polylines(frame, [left_eye], True, (0, 255, 0), 1)
                cv2.polylines(frame, [right_eye], True, (0, 255, 0), 1)

                if avg_EAR < EAR_THRESHOLD:
                    blink_counter += 1
                else:
                    if blink_counter >= CONSEC_FRAMES:
                        print(f"Blink Detected for {name}")
                        mark_attendance(name, attendance_record)
                    blink_counter = 0

            # Draw face box and name
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow("Attendance Monitoring with Anti-Spoofing", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_faces()
