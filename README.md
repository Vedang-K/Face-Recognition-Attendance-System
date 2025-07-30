# 🎓 Face Recognition Attendance System

This project is a **Face Recognition Attendance System** built using **Python**, **OpenCV**, and the **face_recognition** library. It uses your webcam to detect and recognize faces in real-time and automatically records attendance in an Excel file.

---

## 📸 What It Does

- Detects faces in real-time using your webcam.
- Recognizes known student faces by comparing with preloaded images.
- Automatically marks attendance with **name**, **time**, and **date**.
- Prevents duplicate attendance entries during a single session.
- Saves all attendance records in organized Excel files.

---

## 🧰 Technologies Used

- Python 3.8+
- OpenCV (`cv2`)
- face_recognition
- NumPy
- pandas
- datetime
- os

---

## 📁 Folder Structure

FaceRecognitionAttendance/
│
├── ```student_images/ # Folder containing student face images (used for training)
├── attendance/ # Folder where attendance Excel sheets are saved
├── face_attendance.py # Main Python script
└── README.md # Project documentation```


---

## 🖼️ How to Add Students

1. Create a folder named **`student_images`** in the project directory.
2. Add one image per student inside the folder.
3. Rename each image to the student’s name. Example:
student_images/
├──``` Aaryan.jpg
├── Sharvil.png
└── Vedang.jpeg```


> 📷 Make sure the faces in the images are clearly visible and front-facing.


---

## ✅ Output Example

A file like `attendance_2025-07-30.xlsx` will be generated with the following format:

| Name     | Time     | Date       |
|----------|----------|------------|
| Vedang   | 09:45:32 | 2025-07-30 |
| Sharvil  | 10:03:21 | 2025-07-30 |


---

## 🚀 How to Run

1. Make sure Python 3.8+ is installed.
2. Install dependencies:
   ```bash
   pip install opencv-python face_recognition numpy pandas
