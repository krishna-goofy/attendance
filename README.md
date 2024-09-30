

# Attendance Management System

This project is an automated attendance management system using two devices, Device 1 (ESP8266) and Device 2 (Arduino Nano), which communicate through IR signals. The system validates students using fingerprint authentication and logs their attendance remotely on a Flask web server. It provides functionality for administrators to manage timetables, student batches, and track attendance, as well as for students to view their attendance records via a student dashboard.

## Features
- **Fingerprint-based Attendance**: Uses a fingerprint sensor to authenticate students and record their attendance.
- **ESP8266 & Arduino Communication**: Device 1 (ESP8266) broadcasts IR signals, and Device 2 (Arduino Nano) listens and responds after validating the student's fingerprint.
- **Remote Attendance Management**: Attendance data is sent to a Flask web server, where it is processed and stored in a database.
- **Timetable Management**: The admin can create timetables for classes, and assign batches of students to specific periods.
- **Batch Creation**: Admins can create batches of students, which are assigned to timetables.
- **Attendance Tracking**: Attendance is recorded with timestamps for each period, including arrival and departure times.
- **Student Dashboard**: Students can view their attendance records, including total time spent in class.
- **Proxy Elimination**: Ensures that only the authenticated student can mark their attendance, thus eliminating proxies.

## System Components

### Device 1: ESP8266
- **Function**: Broadcasts IR signals and sends attendance data to the server upon student validation.
- **Components**:
  - ESP8266 Microcontroller
  - IR Infrared Transmitter Module

### Device 2: Arduino Nano
- **Function**: Validates the student's fingerprint and sends signals back to Device 1.
- **Components**:
  - Arduino Nano
  - IR Infrared Receiver Module
  - HLK-FPM383C Capacitive Touch Fingerprint Sensor

### Server-Side: Flask Web Application
- **Features**:
  - Provides an admin panel for managing timetables, batches, and attendance records.
  - Allows real-time attendance tracking and viewing of past attendance data.
  - Displays student attendance statistics on a dedicated dashboard.

## Workflow

1. **Fingerprint Enrollment**: Students enroll their fingerprints in the HLK-FPM383C sensor.
2. **Device Communication**: Device 1 continuously broadcasts IR signals. Device 2 validates fingerprints and sends the result back to Device 1.
3. **Attendance Data Logging**: Upon successful validation, Device 1 sends attendance data to the server.
4. **Attendance Records**: The Flask server records attendance with timestamps and stores it in a database.
5. **Admin Features**:
    - **Timetable Creation**: Create timetables for different classes.
    - **Batch Creation**: Add student batches and assign them to classes.
    - **Attendance Monitoring**: Track attendance records for different periods.
6. **Student Features**:
    - **View Attendance**: Students can log in to view their attendance details and total class time.
   
## Database Models

- **Folder**: Stores the class or timetable folders.
- **Batch**: Stores student batches, including names of students in each batch.
- **Timetable**: Stores the timetable, including days, timeslots, and assigned student batches.
- **Attendance**: Logs student attendance, including coming-in and going-out times for each period.

## Web Pages

1. **Admin Pages**:
    - **Create Timetable**: Admin can create and manage timetables.
    - **Create Student Batches**: Admin can add batches of students.
    - **View Timetables**: Admin can view created timetables.
    - **Attendance Page**: Admin can take attendance remotely.
    - **View Attendance**: Admin can view attendance records for all students.

2. **Student Dashboard**:
    - **View Attendance**: Students can view their own attendance records and the total duration spent in class.
    - **Current Class Attendance**: Automatically finds and displays the ongoing class for the student.

## Setup Instructions

### Requirements
- ESP8266
- Arduino Nano
- HLK-FPM383C Capacitive Touch Fingerprint Sensor
- IR Infrared Transmitter and Receiver Modules
- Python 3.x
- Flask
- SQLAlchemy
- SQLite

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/krishna-goofy/attendance.git
   cd attendance-management-system
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Flask Migrations**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. **Run the Flask App**
   ```bash
   flask run
   ```

5. **Upload Arduino Code**
   - Program the Arduino Nano with the provided code.
   - Enroll fingerprints using the `Adafruit_Fingerprint` library.

### Running the Project

1. **Start the Server**: Start the Flask web server to handle attendance data.
2. **Power the Devices**: Power up the ESP8266 and Arduino Nano devices and ensure the communication is working.
3. **Log Attendance**: Students authenticate using fingerprints, and the system logs their attendance remotely.
4. **Admin Tasks**: Admins can manage timetables, view attendance, and create batches through the web portal.

## Benefits

- **Prevents Proxy Attendance**: Only authenticated students can mark their attendance using fingerprints.
- **Automated Attendance Tracking**: No manual intervention is required for tracking student presence.
- **Real-time Data**: Attendance records are updated in real-time on the server, accessible by admins and students.
- **Remote Access**: Admins can manage attendance, timetables, and batches remotely.
- **Improved Efficiency**: Reduces the administrative burden of manual attendance tracking.

## Future Enhancements

- Add notifications to inform students or teachers when attendance is marked.
- Implement facial recognition as an alternative to fingerprint authentication.
- Include support for multiple campuses or classrooms.
  
---

![image](https://github.com/user-attachments/assets/9571c8a1-f576-4c60-b062-1baaec29101d)
![image](https://github.com/user-attachments/assets/3983b13a-fdf8-4987-b325-a799db8d9b6e)
![image](https://github.com/user-attachments/assets/d4a51727-4c6f-4fc8-9bc3-26162505cc74)
![image](https://github.com/user-attachments/assets/0e7a0974-f88d-4e07-b0a8-73f469283e3d)
![image](https://github.com/user-attachments/assets/214dc049-e782-4980-a50b-c2f831874b76)
![image](https://github.com/user-attachments/assets/983d4053-b42f-4153-a561-d4bda16c5135)
