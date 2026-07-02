import streamlit as st
import numpy as np
import time
from PIL import Image

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.components.dialog_enroll import enroll_dialog
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    if 'student_mode' not in st.session_state:
        st.session_state.student_mode = 'login'

    mode_col1, mode_col2 = st.columns(2)
    with mode_col1:
        t = 'primary' if st.session_state.student_mode == 'login' else 'tertiary'
        if st.button('Login with FaceID', type=t, width='stretch', icon=':material/face:'):
            st.session_state.student_mode = 'login'
            st.rerun()
    with mode_col2:
        t = 'primary' if st.session_state.student_mode == 'register' else 'tertiary'
        if st.button('New Student? Register', type=t, width='stretch', icon=':material/person_add:'):
            st.session_state.student_mode = 'register'
            st.rerun()

    st.divider()

    if st.session_state.student_mode == 'login':
        _login_flow()
    else:
        _register_flow(photo_source=None)

    footer_dashboard()


def _login_flow():
    st.markdown("<h2 style='text-align:center; color:#1e1b4b;'>Login with FaceID</h2>", unsafe_allow_html=True)
    st.space()

    photo_source = st.camera_input("Position your face in the center")

    if photo_source:
        img = np.array(Image.open(photo_source))
        with st.spinner('AI is scanning...'):
            try:
                detected, all_ids, num_faces = predict_attendance(img)
            except Exception as e:
                st.error(f"Connection error: {e}\n\nCheck your internet / Supabase project status.")
                return

            if num_faces == 0:
                st.warning('No face detected!')
            elif num_faces > 1:
                st.warning('Multiple faces detected. Please be alone in frame.')
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    try:
                        all_students = get_all_students()
                    except Exception:
                        st.error('Could not reach database. Check connection.')
                        return
                    student = next((s for s in all_students if s['student_id'] == student_id), None)
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome back, {student['name']}!")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('Face not recognized. Switch to **New Student? Register** above.')


def _register_flow(photo_source=None):
    st.markdown("<h2 style='text-align:center; color:#1e1b4b;'>Register New Profile</h2>", unsafe_allow_html=True)
    st.space()

    photo_source = st.camera_input("Take your photo for face registration")

    new_name = st.text_input("Enter your full name", placeholder='E.g. Hamza Rizvi')

    st.subheader('Optional: Voice Enrollment')
    st.info("Record a short phrase for voice-only attendance.")

    st.space()
    audio_data = None
    try:
        audio_data = st.audio_input("Record a short phrase (e.g., 'Hello, this is my voice. Speak for 20-30 seconds')")
    except Exception:
        st.caption('Audio recording not available on this browser')

    if st.button('Create Account', type='primary', width='stretch'):
        if not new_name:
            st.warning('Please enter your name!')
            return
        if not photo_source:
            st.warning('Please take your photo first!')
            return
        with st.spinner('Creating profile...'):
            img = np.array(Image.open(photo_source))
            encodings = get_face_embeddings(img)
            if encodings:
                face_emb = encodings[0].tolist()
                voice_emb = None
                if audio_data:
                    voice_emb = get_voice_embedding(audio_data.read())
                try:
                    response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)
                except Exception as e:
                    st.error(f'Database error: {e}')
                    return
                if response_data:
                    train_classifier()
                    st.session_state.is_logged_in = True
                    st.session_state.user_role = 'student'
                    st.session_state.student_data = response_data[0]
                    st.toast(f"Profile created! Hi {new_name}!")
                    time.sleep(1)
                    st.rerun()
            else:
                st.error("Couldn't detect your face. Make sure face is clearly visible and retake photo.")


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {student_data['name']}!")
        if st.button("Logout", type='secondary', key='student_logout_btn', shortcut="control+l"):
            st.session_state['is_logged_in'] = False
            st.session_state.student_mode = 'login'
            del st.session_state.student_data
            st.rerun()

    st.space()

    c1, c2 = st.columns(2)
    with c1:
        st.header('Your Enrolled Subjects')
    with c2:
        if st.button('Enroll in Subject', type='primary', width='stretch'):
            enroll_dialog()

    st.divider()

    try:
        with st.spinner('Loading your subjects...'):
            subjects = get_student_subjects(student_id)
            logs = get_student_attendance(student_id)
    except Exception:
        st.error('Could not load data. Check your connection.')
        return

    stats_map = {}
    for log in logs:
        sid = log['subject_id']
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]['total'] += 1
        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    if not subjects:
        st.info("Not enrolled in any subjects yet. Click 'Enroll in Subject' to join one.")
    else:
        cols = st.columns(2)
        for i, sub_node in enumerate(subjects):
            sub = sub_node['subjects']
            sid = sub['subject_id']
            stats = stats_map.get(sid, {"total": 0, "attended": 0})

            def unenroll_button(s=sub):
                if st.button(f"Unenroll from {s['name']}", key=f"unenroll_{s['subject_id']}", type='tertiary', width='stretch', icon=':material/delete_forever:'):
                    unenroll_student_to_subject(student_id, s['subject_id'])
                    st.toast(f"Unenrolled from {s['name']}")
                    st.rerun()

            with cols[i % 2]:
                subject_card(
                    name=sub['name'],
                    code=sub['subject_code'],
                    section=sub['section'],
                    stats=[
                        ('📅', 'Total', stats['total']),
                        ('✅', 'Attended', stats['attended']),
                    ],
                    footer_callback=unenroll_button
                )

    footer_dashboard()
