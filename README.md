<div align="center">

<img src="attendex_logo_v2.png" alt="Attendex Logo" width="160"/>

# Attendex

### AI-Powered Attendance Management System

</div>

Attendex is an AI-powered attendance management system that automates student identification and attendance tracking using **Face Recognition and Voice Recognition**.

The application provides separate workflows for **Students and Teachers**, with Supabase handling persistent data such as users, subjects, enrollments, biometric embeddings, and attendance records.

---

## 🚀 Features

### 👨‍🎓 Student Features

- Face-based student authentication
- New student registration
- Face embedding generation
- Optional voice enrollment
- Enroll in subjects using subject code
- Quick enrollment through shared QR/link
- View enrolled subjects
- View attendance statistics
- Unenroll from subjects

### 👨‍🏫 Teacher Features

- Teacher registration and login
- Create and manage subjects
- Share subjects using QR code and enrollment link
- Add classroom photos using:
  - Camera
  - Image upload
- Analyze classroom images for attendance
- Voice-based attendance
- Review attendance before saving
- Confirm or discard attendance results
- View attendance records
- View subject/student information

---

## 🧠 AI / ML Pipelines

Attendex currently uses two biometric pipelines:

```text
                 Attendex
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
    Face Pipeline       Voice Pipeline
          │                   │
          ▼                   ▼
    Face Embedding      Voice Embedding
          │                   │
          ▼                   ▼
       SVM /             Similarity
     Distance              Check
          │                   │
          └─────────┬─────────┘
                    ▼
             Student Identity
                    │
                    ▼
              Attendance
```

### 👁️ Face Recognition Pipeline

The face pipeline uses Dlib to detect faces and generate facial embeddings.

```text
Camera / Classroom Image
          │
          ▼
    Face Detection
          │
          ▼
 Facial Landmark Detection
          │
          ▼
   Face Embedding
          │
          ▼
    Linear SVM Classifier
          │
          ▼
   Predicted Student ID
          │
          ▼
 Euclidean Distance Check
          │
          ▼
     Verified Identity
```

**Technologies:** Dlib, NumPy, Scikit-learn, SVM, Face embeddings, Euclidean distance

The SVM is used to classify a face embedding into a registered student identity, while the distance check provides an additional verification layer before accepting the match.

### 🎙️ Voice Recognition Pipeline

Attendex also supports voice-based attendance. The teacher can record classroom audio containing students saying a predefined phrase.

```text
Classroom Audio
       │
       ▼
  Audio Input
       │
       ▼
Librosa Processing
       │
       ▼
Audio Preprocessing
       │
       ▼
   Resemblyzer
       │
       ▼
 Voice Embedding
       │
       ▼
Similarity Comparison
       │
       ▼
Student Identification
       │
       ▼
Attendance Result
```

The voice pipeline uses Resemblyzer to generate speaker embeddings and compares them against stored voice embeddings of enrolled students.

---

## 📸 Classroom Photo Attendance

Teachers can capture or upload classroom photographs. The application supports both:

```text
Camera → Take Snapshot
Upload Photos → Multiple Images
```

The photo dialog stores multiple classroom images before analysis.

### Attendance Workflow

```text
Teacher selects subject
        │
        ▼
Capture / Upload photos
        │
        ▼
   Detect faces
        │
        ▼
Generate embeddings
        │
        ▼
Predict student identities
        │
        ▼
 Verify predictions
        │
        ▼
Compare with enrolled students
        │
        ▼
  Present / Absent
        │
        ▼
  Review Results
        │
        ▼
 Confirm & Save
```

## 🎙️ Voice Attendance

Teachers can also start a voice attendance session. The teacher records classroom audio and clicks **Analyze Audio**.

The system:

1. Retrieves students enrolled in the selected subject.
2. Retrieves available voice embeddings.
3. Processes the recorded audio.
4. Generates detected student scores.
5. Creates a Present/Absent result for each enrolled student.
6. Shows the results for review.
7. Allows the teacher to confirm and save the attendance.

The current implementation uses `process_bulk_audio()` and stores the generated attendance data in Streamlit session state before confirmation.

## ✅ Attendance Result Review

Attendex does not immediately commit the generated attendance result. The teacher first sees a result table:

| Student Name | Student ID | Status  |
|--------------|------------|---------|
| Student A    | ST001      | Present |
| Student B    | ST002      | Absent  |
| Student C    | ST003      | Present |

The teacher can then choose to discard the result or confirm and save it:

```text
        Attendance Result
               │
        ┌──────┴──────┐
        ▼             ▼
     Discard      Confirm & Save
                      │
                      ▼
                Supabase DB
```

---

## 📚 Subject Management

Teachers can create subjects and manage their classes. A subject contains:

- Subject name
- Subject code
- Section
- Teacher association

Students can join subjects using the subject code.

## 🔗 QR-Based Subject Enrollment

Teachers can share a subject using a generated QR code. The system generates a URL containing the subject code:

```text
http://localhost:8501/?join-code=CS101
```

The QR code can then be scanned/shared with students. Students can also enter the subject code manually.

## ⚡ Quick / Automatic Enrollment

Attendex provides a Quick Enrollment flow. When a student opens a shared subject link:

```text
Join Link
    │
    ▼
Extract Subject Code
    │
    ▼
Find Subject
    │
    ▼
Check Existing Enrollment
    │
    ├── Already enrolled
    │       ↓
    │    Show message
    │
    └── Not enrolled
            ↓
       Confirm enrollment
            ↓
       Add student
```

The quick enrollment component checks whether the subject exists and whether the student is already enrolled before inserting the enrollment.

## 👨‍🎓 Student Authentication

Students can authenticate using their face.

```text
Camera
  │
  ▼
Face Detection
  │
  ▼
Face Embedding
  │
  ▼
SVM Prediction
  │
  ▼
Distance Verification
  │
  ▼
Student Identified
  │
  ▼
Student Dashboard
```

If the system cannot confidently identify the student, the application can guide the user toward registration.

## 📝 Student Registration

A new student can register by providing:

- Name
- Face image
- Optional voice sample

The system generates and stores biometric embeddings associated with the student's identity. After registration, the face classifier can be refreshed to include the new student.

## 🔐 Teacher Authentication

Teachers authenticate using username and password. Passwords are hashed using **bcrypt** before being stored, and the entered password is verified against the stored hash during login.

---

## 🗄️ Database

Attendex uses Supabase as the backend database. The application stores information related to:

- Students
- Teachers
- Subjects
- Subject enrollments
- Face embeddings
- Voice embeddings
- Attendance records

### Simplified Relationship

```text
             Teachers
                 │
                 │ creates
                 ▼
              Subjects
                 │
          ┌──────┴──────┐
          │             │
          ▼             ▼
   Subject Students   Attendance
          │             │
          ▼             ▼
       Students ◄───────┘
```

A student can enroll in multiple subjects, while each subject can contain multiple students.

---

## 🖥️ Application Structure

The project is organized into screens, reusable UI components, database functions, and AI pipelines.

```text
Attendex/
│
├── app.py
├── requirements.txt
│
├── attendex_logo_v2.png
├── search_image.png
├── thinking_image.png
│
└── src/
    │
    ├── components/
    │   ├── dialog_add_photo.py
    │   ├── dialog_attendance_results.py
    │   ├── dialog_auto_enroll.py
    │   ├── dialog_create_subject.py
    │   ├── dialog_enroll.py
    │   ├── dialog_share_subject.py
    │   ├── dialog_voice_attendance.py
    │   ├── footer.py
    │   ├── header.py
    │   └── subject_card.py
    │
    ├── database/
    │   ├── config.py
    │   └── db.py
    │
    ├── pipelines/
    │   ├── face_pipeline.py
    │   └── voice_pipeline.py
    │
    ├── screens/
    │   ├── home_screen.py
    │   ├── student_screen.py
    │   └── teacher_screen.py
    │
    └── ui/
        └── base_layout.py
```

### 🧩 Components

| File | Responsibility |
|------|----------------|
| `dialog_add_photo.py` | Camera capture, multiple image upload, classroom photo collection |
| `dialog_attendance_results.py` | Attendance result preview, discarding results, confirming and saving attendance |
| `dialog_auto_enroll.py` | QR/link-based quick enrollment, subject-code lookup, duplicate enrollment checking |
| `dialog_create_subject.py` | Subject creation |
| `dialog_enroll.py` | Manual subject enrollment, subject-code validation, duplicate enrollment checking |
| `dialog_share_subject.py` | Subject-code sharing, enrollment URL generation, QR-code generation |
| `dialog_voice_attendance.py` | Classroom audio recording, voice recognition, attendance result generation, attendance session preparation |
| `header.py` | Reusable application header |
| `footer.py` | Reusable application footer |
| `subject_card.py` | Displays subject information and student subject actions |

### 🧠 AI Pipelines

| File | Responsibility |
|------|----------------|
| `face_pipeline.py` | Face detection, face embedding generation, SVM training, student prediction, distance-based verification |
| `voice_pipeline.py` | Audio preprocessing, voice embedding generation, voice similarity comparison, bulk audio processing |

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| UI | Streamlit |
| Database | Supabase |
| Computer Vision | Dlib |
| Face Recognition | Dlib Face Recognition Model |
| Classification | Scikit-learn SVM |
| Voice Recognition | Resemblyzer |
| Audio Processing | Librosa |
| Image Processing | Pillow |
| Numerical Computing | NumPy |
| Authentication | bcrypt |
| QR Generation | Segno |

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Nikitasoni22/Attendex.git
cd Attendex
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Supabase

Create the following file:

```text
.streamlit/
└── secrets.toml
```

Add your Supabase credentials:

```toml
SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_supabase_key"
```

> ⚠️ Do not commit credentials to GitHub.

### 5. Run Attendex

```bash
streamlit run app.py
```

The application will normally be available at `http://localhost:8501`.

---

## 🔄 Complete System Flow

```text
                       ATTENDEX
                           │
                  ┌────────┴────────┐
                  │                 │
                  ▼                 ▼
              STUDENT             TEACHER
                  │                 │
            Face Login        Password Login
                  │                 │
                  ▼                 ▼
          Student Dashboard   Teacher Dashboard
                  │                 │
          ┌───────┴──────┐   ┌──────┴───────────┐
          │              │   │                  │
          ▼              ▼   ▼                  ▼
       Subjects       Profile  Subjects      Attendance
          │                      │               │
          ▼                      ▼          ┌────┴────┐
       Enroll                Share QR       │         │
          │                      │          ▼         ▼
          ▼                      ▼        Face      Voice
       Dashboard             Students     Photos    Audio
                                               │         │
                                               └────┬────┘
                                                    ▼
                                             Review Results
                                                    │
                                                    ▼
                                              Confirm & Save
                                                    │
                                                    ▼
                                               Supabase
```

---

## 🔒 Security & Reliability Considerations

Attendex is currently a project/educational implementation. For production deployment, the following improvements would be important:

- Liveness / anti-spoofing detection
- Secure biometric-data storage
- Stronger role-based authorization
- HTTPS
- Secure secret management
- Face-quality validation
- Multiple enrollment samples per student
- Threshold calibration
- False Acceptance Rate evaluation
- False Rejection Rate evaluation
- Audit logging
- Duplicate attendance prevention
- Database constraints
- Automated tests

## 🔮 Future Improvements

- Real-time liveness detection
- Better anti-spoofing
- Multiple face samples per student
- Face-quality checks
- Advanced voice anti-spoofing
- Attendance analytics dashboard
- Attendance export to CSV/PDF
- Email notifications
- Mobile-friendly interface
- Production deployment
- Automated testing
- Improved biometric threshold calibration

---

## 👨‍💻 Author

**Nikita Soni**

GitHub: [@Nikitasoni22](https://github.com/Nikitasoni22)
