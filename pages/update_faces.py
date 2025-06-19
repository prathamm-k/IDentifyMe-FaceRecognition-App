import streamlit as st 
import cv2
import yaml 
import pickle 
from face_utils import submit_new, get_info_from_id, delete_one
import numpy as np

st.set_page_config(layout="wide")
st.title("IDentifyMe - Face Recognition App")
st.write("This page is used to add new faces to the dataset")

#sidebar menu for selecting operation
menu = ["Adding","Deleting", "Adjusting"]
choice = st.sidebar.selectbox("Options",menu)

if choice == "Adding":
    #section for adding a new face
    name = st.text_input("Name",placeholder='Enter name')
    id = st.text_input("ID",placeholder='Enter id')
    #choose between uploading an image or using the webcam
    upload = st.radio("Upload image or use webcam",("Upload","Webcam"))
    if upload == "Upload":
        uploaded_image = st.file_uploader("Upload",type=['jpg','png','jpeg'])
        if uploaded_image is not None:
            st.image(uploaded_image)
            submit_btn = st.button("Submit",key="submit_btn")
            if submit_btn:
                if name == "" or id == "":
                    st.error("Please enter name and ID")
                else:
                    #add new face from uploaded image
                    ret = submit_new(name, id, uploaded_image)
                    if ret == 1: 
                        st.success("Student Added")
                    elif ret == 0: 
                        st.error("Student ID already exists")
                    elif ret == -1: 
                        st.error("There is no face in the picture")
    elif upload == "Webcam":
        img_file_buffer = st.camera_input("Take a picture")
        submit_btn = st.button("Submit",key="submit_btn")
        if img_file_buffer is not None:
            #convert webcam image to OpenCV format
            bytes_data = img_file_buffer.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            if submit_btn: 
                if name == "" or id == "":
                    st.error("Please enter name and ID")
                else:
                    #add new face from webcam image
                    ret = submit_new(name, id, cv2_img)
                    if ret == 1: 
                        st.success("Student Added")
                    elif ret == 0: 
                        st.error("Student ID already exists")
                    elif ret == -1: 
                        st.error("There is no face in the picture")

elif choice == "Deleting":
    #section for deleting a face by ID
    def del_btn_callback(id):
        delete_one(id)
        st.success("Student deleted")
        
    id = st.text_input("ID",placeholder='Enter id')
    submit_btn = st.button("Submit",key="submit_btn")
    if submit_btn:
        name, image,_ = get_info_from_id(id)
        if name == None and image == None:
            st.error("Student ID does not exist")
        else:
            st.success(f"Name of student with ID {id} is: {name}")
            st.warning("Please check the image below to make sure you are deleting the right student")
            st.image(image)
            #button to confirm deletion
            del_btn = st.button("Delete",key="del_btn",on_click=del_btn_callback, args=(id,)) 
        
elif choice == "Adjusting":
    #function for adjusting or editing an existing face entry
    def form_callback(old_name, old_id, old_image, old_idx):
        #callback to update student info
        new_name = st.session_state['new_name']
        new_id = st.session_state['new_id']
        new_image = st.session_state['new_image']
        name = old_name
        id = old_id
        image = old_image
        #updates fields if changed
        if new_image is not None:
            image = cv2.imdecode(np.frombuffer(new_image.read(), np.uint8), cv2.IMREAD_COLOR)
        if new_name != old_name:
            name = new_name
        if new_id != old_id:
            id = new_id
        #updates the entry in the database
        ret = submit_new(name, id, image, old_idx=old_idx)
        if ret == 1: 
            st.success("Student Added")
        elif ret == 0: 
            st.error("Student ID already exists")
        elif ret == -1: 
            st.error("There is no face in the picture")
    id = st.text_input("ID",placeholder='Enter id')
    submit_btn = st.button("Submit",key="submit_btn")
    if submit_btn:
        old_name, old_image, old_idx = get_info_from_id(id)
        if old_name == None and old_image == None:
            st.error("Student ID does not exist")
        else:
            #form for editing student info
            with st.form(key='my_form'):
                st.title("Adjusting student info")
                col1, col2 = st.columns(2)
                new_name = col1.text_input("Name",key='new_name', value=old_name, placeholder='Enter new name')
                new_id  = col1.text_input("ID",key='new_id',value=id,placeholder='Enter new id')
                new_image = col1.file_uploader("Upload new image",key='new_image',type=['jpg','png','jpeg'])
                col2.image(old_image,caption='Current image',width=400)
                #submit button for the form
                st.form_submit_button(label='Submit',on_click=form_callback, args=(old_name, id, old_image, old_idx))