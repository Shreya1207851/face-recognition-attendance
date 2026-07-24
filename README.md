# Face Recognition Attendance System

A real-time face recognition-based attendance system built using Python and OpenCV. This project uses a webcam to recognize registered faces and automatically marks attendance in a CSV file.

---

## 📌 About the Project

The Face Recognition Attendance System is a Python-based computer vision project that uses face recognition technology to identify registered individuals through a webcam.

When a registered face is recognized, the system automatically records the person's attendance along with the date and time.

The project also includes SMS notification functionality for attendance updates.

---

## ✨ Features

- Real-time face recognition using a webcam
- Automatic attendance marking
- Attendance records stored in CSV format
- Face detection and recognition
- SMS notification support
- Easy-to-use Python implementation
- Automatic date and time recording

---

## 🛠️ Technologies Used

- Python
- OpenCV
- face_recognition
- NumPy
- Pandas

---

## Project Structure

```text
face-recognition-attendance/
│
├── attendance_sms_notification.py
├── frs.py
├── deepfake.py
├── check.py
├── attendance.csv
├── Shreya.jpg
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Command to Run the Code

Run the main attendance system using:

```bash
python attendance_sms_notification.py
```

Press **Q** to quit the camera.

---

## Attendance Records

Attendance records are stored in:

`attendance.csv`

The CSV file contains attendance information recorded by the face recognition system.

---

## SMS Notification

The project includes SMS notification functionality for sending attendance updates.

For security reasons, API keys, passwords, and other sensitive credentials should not be uploaded to GitHub.

---

## Author

**Shreya Kaushal**

GitHub: https://github.com/Shreya1207851

---

## Future Improvements

- Add a web-based dashboard
- Add multiple user registration
- Add database integration
- Add email notifications
- Improve face recognition accuracy
- Add an admin panel
- Generate attendance reports
- Add monthly and yearly attendance analytics
- Add support for multiple cameras

  ---
  Note: Add your registered face image as Shreya.jpg in the project folder before running the application.
