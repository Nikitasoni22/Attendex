import streamlit as st
from src.components.footer import footer
from src.components.header import header_dashboard
from src.ui.base_layout import style_background_dashboard
from src.ui.base_layout import style_base_layout
from PIL import Image
import numpy as np
from src.components.dialog_enroll import enroll_dialog
from src.pipelines.face_pipeline import (
    predict_attendance,
    get_face_embeddings,
    train_classifier
)
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student,get_student_subjects,get_student_attendance,unenroll_student_to_subject,enroll_student_to_subject
import time
from src.components.subject_card import subject_card


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    c1,c2 = st.columns(2, vertical_alignment="center",gap ='xxlarge')
    with c1:
        header_dashboard()

    with c2:
        st.subheader(f""" Welcome!{student_data['name']}""")
        if st.button("Logout",type="secondary",key="loginbackbtn",shortcut="ctrl+backspace"):
            st.session_state['is_logged_in']=False
            del st.session_state.student_data
            st.rerun()
    st.space()
    c1,c2 = st.columns(2)
    with c1:
        st.header("Your Enrolled subjects")
    with c2:
        if st.button("Enroll in subject",type='primary',width='stretch'):
            enroll_dialog()
    st.divider()
    with st.spinner('Loading your subjects..'):
        subjects=get_student_subjects(student_id)
        logs= get_student_attendance(student_id)
    stats_map={}
    for log in logs:
        sid=log['subject_id']

        if sid not in stats_map:
            stats_map[sid]={"total":0,"attended":0}
        stats_map[sid]['total'] += 1
        if log.get('is_present'):
            stats_map[sid]['attended'] += 1
    cols =st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid =sub['subject_id']
        stats =stats_map.get(sid,{"total":0,"attended":0})
        def unenroll_button():
                if st.button('Unenroll from this course',type="tertiary",width='stretch',icon=':material/delete_forever:'):
                    unenroll_student_to_subject(student_id,sid)
                    st.toast(f'Unenrolled from{sub['name']} successfully!')

        with cols[i %2]:
            subject_card(
                name = sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ('🗓️','Total',stats['total']),
                    ('✅','Attended',stats['attended']),
                ],
                footer_callback = unenroll_button
            )



    footer()


def student_screen():

    # Initialize registration state
    if "show_registration" not in st.session_state:
        st.session_state.show_registration = False

    style_background_dashboard()
    style_base_layout()

    # If student is already logged in
    if "student_data" in st.session_state:
        student_dashboard()
        return

    # Header + Back button
    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back to home",
            type="secondary",
            key="loginbackbtn",
            shortcut="ctrl+backspace"
        ):
            st.session_state["login_type"] = None
            st.session_state.show_registration = False
            st.rerun()

    st.header(
        "Login using FaceID",
        text_alignment="center"
    )

    st.space()

    # Camera button styling
    st.markdown(
        """
        <style>
        div[data-testid="stCameraInput"] button {
            background-color: #2EC4B6 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Face capture
    photo_source = st.camera_input(
        "Place your face in the center"
    )

    if photo_source:

        img = np.array(Image.open(photo_source))

        with st.spinner("AI is scanning...."):

            detected, all_ids, num_faces = predict_attendance(img)

            # No face
            if num_faces == 0:
                st.warning("Faces not found")

            # Multiple faces
            elif num_faces > 1:
                st.warning("Multiple faces found")

            # Exactly one face
            else:

                # Face recognized
                if detected:

                    student_id = list(detected.keys())[0]

                    all_students = get_all_students()

                    student = next(
                        (
                            s
                            for s in all_students
                            if s["student_id"] == student_id
                        ),
                        None
                    )

                    if student:

                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.student_data = student

                        st.toast(
                            f"Welcome back {student['name']}"
                        )

                        time.sleep(1)
                        st.rerun()

                # Face not recognized
                else:

                    st.info(
                        "Face not recognized! "
                        "You might be a new student!"
                    )

                    st.session_state.show_registration = True

    # Registration section
    if st.session_state.show_registration:

        with st.container(border=True):

            st.header("Register New Profile")

            new_name = st.text_input(
                "Enter your name",
                placeholder="E.g. Nikita Soni"
            )

            st.subheader("Optional: Voice Enrollment")

            st.info(
                "Enroll your voice for voice-only attendance."
            )

            audio_data = None

            try:

                audio_data = st.audio_input(
                    "Record a short phrase like "
                    "'Hello! I am present, my name is Nikita.'"
                )

            except Exception:

                st.error("Audio data failed!")

            # Create account
            if st.button(
                "Create account",
                type="primary"
            ):

                if new_name:

                    with st.spinner("Creating profile..."):

                        # Reuse captured face image
                        if photo_source is None:
                            st.error(
                                "Please capture your face first."
                            )
                            return

                        img = np.array(
                            Image.open(photo_source)
                        )

                        # Generate face embedding
                        encodings = get_face_embeddings(img)

                        if encodings:

                            face_emb = encodings[0].tolist()

                            # Generate voice embedding
                            voice_emb = None

                            if audio_data:
                                voice_emb = get_voice_embedding(
                                    audio_data.read()
                                )

                            # Create student
                            response_data = create_student(
                                new_name,
                                face_embedding=face_emb,
                                voice_embedding=voice_emb
                            )

                            if response_data:

                                # Retrain face classifier
                                train_classifier()

                                # Login newly created student
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = response_data[0]

                                st.toast(
                                    f"Profile created! "
                                    f"Hi {response_data[0]['name']}"
                                )

                                time.sleep(1)
                                st.rerun()

                            else:

                                st.error(
                                    "Could not create student profile."
                                )

                        else:

                            st.error(
                                "Couldn't capture your facial "
                                "features for registration."
                            )

                else:

                    st.warning("Please enter your name.")

    footer()