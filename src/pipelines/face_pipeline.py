import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st
from src.database.db import get_all_students


@st.cache_resource #models heavy hote h baar baar load krega toh memory lega
def load_dlib_models():
    detector = dlib.get_frontal_face_detector() #how many faces and in what coordinate

    sp=dlib.shape_predictor( #shape predictor
        face_recognition_models.pose_predictor_model_location()
    )

    facerec= dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    return detector,sp,facerec

def get_face_embeddings(image_np):
    detector,sp,facerec =load_dlib_models()
    faces = detector(image_np,1) #jitna jyada no. utna jyada baar preprocess krega image ko

    encoding=[]

    for face in faces:
        shape=sp(image_np,face)
        face_descriptor = facerec.compute_face_descriptor(image_np,shape,1)
        encoding.append(np.array(face_descriptor))
    return encoding

@st.cache_resource
def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get("face_embedding")

        if embedding is not None:
            X.append(np.array(embedding))
            y.append(student.get("student_id"))

    # No students
    if len(X) == 0:
        return None

    # IMPORTANT:
    # If there is only ONE student, don't train SVM.
    if len(set(y)) == 1:
        return {
            "clf": None,
            "X": X,
            "y": y
        }

    # Two or more students -> train SVM
    clf = SVC(
        kernel="linear",
        probability=True,
        class_weight="balanced"
    )

    try:
        clf.fit(X, y)

    except ValueError as e:
        st.error(f"Face model training failed: {e}")
        return None

    return {
        "clf": clf,
        "X": X,
        "y": y
    }

def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np):

    encodings = get_face_embeddings(class_image_np)

    detected_student = {}

    model_data = get_trained_model()

    # No registered students
    if not model_data:
        return detected_student, [], len(encodings)

    clf = model_data["clf"]
    X_train = model_data["X"]
    y_train = model_data["y"]

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:

        # --------------------------------
        # CASE 1: Only one student exists
        # --------------------------------
        if clf is None:

            predicted_id = int(all_students[0])

        # --------------------------------
        # CASE 2: Multiple students exist
        # --------------------------------
        else:

            predicted_id = int(
                clf.predict([encoding])[0]
            )

        # Get embedding of predicted student
        student_index = y_train.index(predicted_id)

        student_embedding = X_train[student_index]

        # Euclidean distance
        best_match_score = np.linalg.norm(
            student_embedding - encoding
        )

        resemblance_threshold = 0.6

        if best_match_score <= resemblance_threshold:

            detected_student[predicted_id] = True

    return (
        detected_student,
        all_students,
        len(encodings)
    )




    





