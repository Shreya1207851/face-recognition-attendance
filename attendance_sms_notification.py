import cv2
import face_recognition
import datetime
import os
from twilio.rest import Client

# Twilio credentials
account_sid = "YOUR_ACCOUNT_SID"
auth_token = "YOUR_AUTH_TOKEN"
twilio_phone_number = "YOUR_TWILIO_NUMBER"
recipient_phone_number = "YOUR_RECIPIENT_NUMBER"

client = Client(account_sid, auth_token)


# Function to send SMS
def send_sms(name):
    message = client.messages.create(
        body=f"Alert: {name} missed attendance today.",
        from_=twilio_phone_number,
        to=recipient_phone_number
    )
    print(f"SMS sent: {message.sid}")


# Function to mark attendance
def mark_attendance(name, attendance_record):
    if name not in attendance_record:
        with open("attendance.csv", "a") as f:
            today = datetime.date.today()
            now = datetime.datetime.now().strftime("%H:%M:%S")
            f.write(f"{today},{now},{name}\n")

        attendance_record.append(name)
        print(f"Attendance marked: {name}")


# Load images and encode faces
def load_images_and_encode():
    known_faces_encodings = []
    known_faces_names = []

    image_paths = ["Shreya.jpg"]

    for path in image_paths:
        image = face_recognition.load_image_file(path)
        face_encodings = face_recognition.face_encodings(image)

        if face_encodings:
            face_encoding = face_encodings[0]
            known_faces_encodings.append(face_encoding)
            known_faces_names.append("Shreya")
        else:
            print(f"No face detected in {path}")

    return known_faces_encodings, known_faces_names


# Main face recognition function
def recognize_faces():
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("Error opening video capture device.")
        return

    attendance_record = []

    known_faces_encodings, known_faces_names = load_images_and_encode()

    print("Camera started. Press Q to quit.")

    while True:
        ret, frame = video_capture.read()

        if not ret:
            print("Error reading frame from camera.")
            break

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(
            frame,
            face_locations
        )

        for (top, right, bottom, left), face_encoding in zip(
            face_locations,
            face_encodings
        ):
            matches = face_recognition.compare_faces(
                known_faces_encodings,
                face_encoding,
                tolerance=0.6
            )

            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_faces_names[first_match_index]

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                name,
                (left + 6, bottom - 6),
                cv2.FONT_HERSHEY_DUPLEX,
                0.5,
                (0, 255, 0),
                1
            )

            if name != "Unknown":
                mark_attendance(name, attendance_record)

        cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video_capture.release()
    cv2.destroyAllWindows()


# Start program
if __name__ == "__main__":
    recognize_faces()