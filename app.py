import streamlit as st
import cv2
import face_recognition as frg
import yaml
from face_utils import recognize, build_dataset

# Load configuration from YAML file
with open('config.yaml', 'r') as f:
    cfg = yaml.safe_load(f)

PICTURE_PROMPT = cfg['INFO']['PICTURE_PROMPT']
WEBCAM_PROMPT = cfg['INFO']['WEBCAM_PROMPT']

#Set up sidebar controls and info containers
def initialize_sidebar():

    st.sidebar.title("Settings")
    # Select input type (Picture or Webcam)
    menu = ["Picture", "Webcam"]
    choice = st.sidebar.selectbox("Input type", menu)
    # Slider for face recognition tolerance
    tolerance = st.sidebar.slider(
        "Tolerance",
        0.0, 1.0, 0.5, 0.01,
        help="Threshold for face recognition. Lower values are more strict, higher values are more lenient."
    )
    # Info containers for recognized name and ID
    st.sidebar.title("Student Information")
    name_container = st.sidebar.empty()
    id_container = st.sidebar.empty()
    name_container.info('Name: Unknown')
    id_container.success('ID: Unknown')
    return choice, tolerance, name_container, id_container

#Handles image upload, run recognition function, and display results
def handle_picture_input(name_container, id_container, tolerance):
    
    st.title("IDentifyMe - Face Recognition App")
    st.write(PICTURE_PROMPT)
    # Allow multiple image uploads
    uploaded_images = st.file_uploader(
        "Upload",
        type=['jpg', 'png', 'jpeg'],
        accept_multiple_files=True
    )
    if uploaded_images:
        for image in uploaded_images:
            # Load and process each uploaded image
            image = frg.load_image_file(image)
            image, name, id = recognize(image, tolerance)
            name_container.info(f"Name: {name}")
            id_container.success(f"ID: {id}")
            st.image(image)
    else:
        st.info("Please upload an image")

#Handle webcam input, run real-time recognition, and display results
def handle_webcam_input(name_container, id_container, tolerance):

    st.title("IDentifyMe - Face Recognition App")
    st.write(WEBCAM_PROMPT)
    # Open webcam
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    frame_window = st.image([])
    while True:
        ret, frame = cam.read()
        if not ret:
            st.error("Failed to capture frame from camera")
            st.info("Please turn off the other apps that are using the camera and restart IDentifyMe app")
            st.stop()
        # Run recognition on each frame
        image, name, id = recognize(frame, tolerance)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        name_container.info(f"Name: {name}")
        id_container.success(f"ID: {id}")
        frame_window.image(image)

#sets up database management tools, layout and UI of the app
def main():
    st.set_page_config(layout="wide")
    # Set up sidebar and get user choices
    choice, tolerance, name_container, id_container = initialize_sidebar()
    # Handle input based on user choice
    if choice == "Picture":
        handle_picture_input(name_container, id_container, tolerance)
    else:
        handle_webcam_input(name_container, id_container, tolerance)
    # Developer section: allows rebuilding the dataset
    with st.sidebar.form(key='developer_form'):
        st.title("Database Management")
        if st.form_submit_button(label='RECONFIGURE DATASET'):
            with st.spinner("Reconfiguring dataset..."):
                build_dataset()
            st.success("Dataset has been reconfigured/rebuilt")

if __name__ == "__main__":
    main()