import cv2 as cv
import face_recognition as fr
import numpy as np
import pandas as pd
from datetime import datetime
import os

images = [] # creates an empty list to store loaded images
student_name = [] # creates an empty list to store student names
known_face_encoding = [] # creates an empty list to store face encodings

attendance_df = pd.DataFrame(columns=["Name", "Time", "Date"]) # initializes a pandas DataFrame to store attendance records
marked_today = set() # creates an empty set to track students who have already been marked present today

def load_known_faces():  # Loads student images and names from a folder
    path = 'student_images' # sets the path to the directory containing student images
    image_file = os.listdir(path) # gets a list of all files in the directory

    for file in image_file:
        img = cv.imread(f"{path}/{file}") # reads the image file
        images.append(img)
        student_name.append(os.path.splitext(file)[0]) # extracts the student's name from the filename and adds it to the student_name list

    print("Loading known faces completed.")

def encoded_faces(images_list):  # Converts faces into unique digital signatures
    for img in images:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB) # converts the image from BGR to RGB color space
        face_location = fr.face_locations(img) # finds all face locations in the image
        encodings = fr.face_encodings(img, face_location) # computes the face encoding for the detected face

        if encodings:
            known_face_encoding.append(encodings[0]) # adds the first face encoding found to the known_face_encoding list

    print("Encoding known faces complete.")
    return known_face_encoding

def compare_faces(face_encoding_to_check):  # Compares a new face to all known faces
    if not known_face_encoding:
        print("No known faces")

    matches = fr.compare_faces(known_face_encoding, face_encoding_to_check) # compares the new face encoding with all known face encodings
    name = "unknown"

    face_distance = fr.face_distance(known_face_encoding, face_encoding_to_check) # computes the distance between the new face and all known faces

    best_match_index = np.argmin(face_distance) # finds the index of the best matching face (the one with the smallest distance)

    if matches[best_match_index]:
        name = student_name[best_match_index] # retrieves the name of the best matching student

    return name

def mark_attendance(name):  # Records attendance for a recognized student
    global attendance_df # declares that we are using the global attendance_df variable
    global marked_today # declares that we are using the global marked_today variable

    if name == "unknown":
        return

    if name not in marked_today:
        now = datetime.now() # gets the current date and time
        current_time = now.strftime("%H:%M:%S") # formats the current time
        current_date = now.strftime("%Y-%m-%d") # formats the current date

        new_entry = pd.DataFrame([{"Name":name, "Time":current_time, "Date":current_date}]) # creates a new DataFrame entry for the student's attendance

        attendance_df = pd.concat([attendance_df, new_entry], ignore_index=True) # appends the new entry to the main attendance DataFrame
        marked_today.add(name) # adds the student's name to the marked_today set

        print(f"Attendance marked for {name} at {current_time} on {current_date}")

def save_attendance():  # Saves the day's attendance to an Excel file
    today_date = datetime.now().strftime("%Y-%m-%d") # gets today's date
    output_dir = "attendance" # sets the output directory
    os.makedirs(output_dir, exist_ok=True) # creates the directory if it doesn't already exist
    excel_file_path = os.path.join(output_dir, f"attendance_{today_date}.xlsx") # constructs the full path for the Excel file

    try:
        attendance_df.to_excel(excel_file_path, index=False) # saves the attendance DataFrame to an Excel file
    except Exception as e:
        print(f"Error saving attendance: {e}")

def detect_faces():  # Uses the webcam to find and recognize faces
    video_capture = cv.VideoCapture(0) # opens the default webcam
    if not video_capture.isOpened():
        print("Could not open webcam")

    while True:
        ret, frame = video_capture.read() # reads a frame from the webcam
        if not ret: # checks if the frame was read successfully
            print("Failed to grab frame")
            break

        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        face_location = fr.face_locations(rgb_frame) # finds all face locations in the current frame
        face_encoding_in_frame = fr.face_encodings(rgb_frame, face_location) # computes face encodings for detected faces

        for (top, right, bottom, left), face_encoding in zip(face_location, face_encoding_in_frame):
            recognized_face = compare_faces(face_encoding) # compares the face with known faces
            mark_attendance(recognized_face) # marks attendance for the recognized face

            cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2) # draws a rectangle around the detected face
            cv.putText(frame, recognized_face, (left+6, bottom-6), cv.FONT_HERSHEY_PLAIN, # displays the name of the recognized person
                       0.9, (255, 0, 255), 2)

        cv.imshow("Face Detection", frame) # displays the frame with the detected faces
        if cv.waitKey(1) & 0xff == ord('q'):
            break

    video_capture.release()
    cv.destroyAllWindows()
    print("Webcam shut down.")

    save_attendance() # saves the final attendance records
    print("Attendance saved successfully")


def main():
    load_known_faces()

    if images:
        encoded_faces(images)
    else:
        print("Faces were not loaded. Please check")

    if known_face_encoding:
        detect_faces()
    else:
        print("No faces were encoded. Please check")

if __name__ == '__main__':
    main() 