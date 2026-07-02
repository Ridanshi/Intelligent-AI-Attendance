# SnapClass — Intelligent AI Attendance System

An ML-powered attendance system that uses **face recognition** and **voice recognition** to automatically mark student attendance from a single classroom photo or audio recording.

---

## Features

### Teacher Portal
- Register / Login with username & password
- Create and manage subjects with unique join codes
- Share enrollment link via **QR code** or WhatsApp
- **Take attendance from group photos** — upload multiple classroom photos and AI detects every face
- **Voice attendance** — record classroom audio and AI identifies students by voice
- View attendance records with session-wise stats and live search

### Student Portal
- Register with **face enrollment** (webcam photo)
- Optional **voice enrollment** for voice-based attendance
- Login using face recognition (no passwords)
- Enroll in subjects via QR code or join link
- View personal attendance stats per subject
- Unenroll from subjects anytime

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend / DB | Supabase (PostgreSQL) |
| Face Detection | dlib + face_recognition_models |
| Face Classification | Scikit-learn SVM (SVC) |
| Voice Recognition | Resemblyzer (VoiceEncoder) |
| Audio Processing | librosa |
| QR Code | segno |
| Auth | bcrypt |

---

## Project Structure

```
├── app.py                        # Entry point, routing
├── requirements.txt
├── .streamlit/
│   └── config.toml               # Theme config
├── src/
│   ├── screens/
│   │   ├── home_screen.py
│   │   ├── teacher_screen.py
│   │   └── student_screen.py
│   ├── components/
│   │   ├── header.py
│   │   ├── footer.py
│   │   ├── subject_card.py
│   │   ├── dialog_create_subject.py
│   │   ├── dialog_share_subject.py
│   │   ├── dialog_add_photo.py
│   │   ├── dialog_attendance_results.py
│   │   ├── dialog_voice_attendance.py
│   │   ├── dialog_enroll.py
│   │   └── dialog_auto_enroll.py
│   ├── pipelines/
│   │   ├── face_pipeline.py      # dlib face embeddings + SVM classifier
│   │   └── voice_pipeline.py     # Resemblyzer voice embeddings
│   ├── database/
│   │   ├── config.py             # Supabase client
│   │   └── db.py                 # All DB queries
│   └── ui/
│       └── base_layout.py        # Global CSS / theming
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/Ridanshi/Intelligent-AI-Attendance.git
cd Intelligent-AI-Attendance
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies

> **Windows users:** `resemblyzer` requires `webrtcvad` which needs a C++ build workaround:
```bash
pip install webrtcvad-wheels
pip install resemblyzer --no-deps
pip install -r requirements.txt
```

> **macOS/Linux:**
```bash
pip install -r requirements.txt
```

### 4. Configure Supabase

Create `.streamlit/secrets.toml`:
```toml
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-anon-key"
```

### 5. Set up Supabase tables

Run in the Supabase SQL Editor:

```sql
CREATE TABLE teachers (
  teacher_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  password_hash TEXT NOT NULL
);

CREATE TABLE subjects (
  subject_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  teacher_id BIGINT REFERENCES teachers(teacher_id),
  name TEXT NOT NULL,
  subject_code TEXT UNIQUE NOT NULL,
  section TEXT
);

CREATE TABLE students (
  student_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name TEXT NOT NULL,
  face_embedding JSONB,
  voice_embedding JSONB
);

CREATE TABLE subject_students (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  subject_id BIGINT REFERENCES subjects(subject_id),
  student_id BIGINT REFERENCES students(student_id),
  UNIQUE(subject_id, student_id)
);

CREATE TABLE attendance_logs (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  student_id BIGINT REFERENCES students(student_id),
  subject_id BIGINT REFERENCES subjects(subject_id),
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  is_present BOOLEAN DEFAULT FALSE
);

-- Enable RLS and allow all (adjust for production)
ALTER TABLE teachers ENABLE ROW LEVEL SECURITY;
ALTER TABLE subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE subject_students ENABLE ROW LEVEL SECURITY;
ALTER TABLE attendance_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "allow all" ON teachers FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "allow all" ON subjects FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "allow all" ON students FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "allow all" ON subject_students FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "allow all" ON attendance_logs FOR ALL USING (true) WITH CHECK (true);
```

### 6. Run the app
```bash
streamlit run app.py
```

---

## How It Works

1. **Teacher** creates a subject → shares QR code with students
2. **Students** scan QR → register face (+ optional voice) → enrolled automatically
3. **Teacher** uploads classroom photos → AI detects and matches faces against enrolled students → attendance marked
4. Alternatively, **teacher** records classroom audio → AI identifies voices → attendance marked
5. Both teacher and students can view attendance records anytime

---

## Author

**Ridanshi Agarwal**
