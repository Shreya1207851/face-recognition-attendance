import cv2
import face_recognition
import numpy as np
import datetime
import os

# Function to mark attendance
def mark_attendance(name, attendance_record):
    if name not in attendance_record:
        with open("attendance.csv", "a") as f:
            today = datetime.date.today()
            now = datetime.datetime.now().strftime("%H:%M:%S")
            f.write(f"{today},{now},{name}\n")
        attendance_record.append(name)  

# Load images and encode faces
def load_images_and_encode(tolerance=0.4):
    known_faces_encodings = []
    known_faces_names = []

    # DataSet
    image_paths = [
        "suraj.jpg",
        "Amanjeet_Kumar.jpg",
        "Ankit_Kumar.jpg",
    ]

    for path in image_paths:
        if os.path.exists(path):
            image = face_recognition.load_image_file(path)
            face_encodings = face_recognition.face_encodings(image)
            if face_encodings:
                face_encoding = face_encodings[0]
                known_faces_encodings.append(face_encoding)
                known_faces_names.append(os.path.splitext(os.path.basename(path))[0])
            else:
                print(f"No face detected in {path}")
        else:
            print(f"File not found: {path}")

    return known_faces_encodings, known_faces_names

# Main function for face recognition
def recognize_faces():
   
    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  

    if not video_capture.isOpened():
        print("Error opening video capture device. Check your camera connection or permissions.")
        exit()

    attendance_record = []

    known_faces_encodings, known_faces_names = load_images_and_encode()

    while True:
        ret, frame = video_capture.read()

        if not ret:
            print("Error reading frame from camera.")
            break

        # Convert color (improves face_recognition accuracy)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_faces_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_faces_names[first_match_index]

            # Draw rectangle and name
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (0, 255, 0), 1)

            if name != "Unknown":
                mark_attendance(name, attendance_record)

        cv2.imshow("Attendance Monitoring", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_faces()


