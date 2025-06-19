# IDentifyMe-FaceRecognition-App

## Project Motivation
I wanted to build a project that combines face recognition, and practical image data management. My goal was to create a tool that could be used for attendance, security, or any scenario where quick and reliable face identification is needed. Through this project, I learned how to:
- Integrate Python libraries for face recognition and image processing
- Manage and serialize image data
- Write cross-platform setup scripts and automate environment setup
- Structure a project for clarity and maintainability

## Project Overview
**IDentifyMe-FaceRecognition-App** is a face recognition web application built with Python and Streamlit. It allows users to:
- Recognize faces from images or webcam
- Add, delete, and update face entries in a database
- View the face database in a user-friendly table

**Technologies Used:**
- **Python 3.11.13**: Core programming language
- **Streamlit**: For building the interactive web UI
- **face_recognition**: For face detection and recognition (built on dlib)
- **OpenCV**: For image processing and webcam integration
- **PyYAML**: For configuration management
- **Pickle**: For database serialization
- **PowerShell/Bash**: For cross-platform setup scripts

These technologies were chosen for their reliability, ease of use, and strong community support. Streamlit makes it easy to build and deploy data apps, while face_recognition and OpenCV provide robust face detection and image handling.

## Setup Instructions

### 1. Windows (PowerShell)
```powershell
# Open PowerShell in the project directory
./setup.ps1
# To activate the environment later:
./facerec-venv/Scripts/Activate.ps1
# To run the app:
streamlit run app.py
```

### 2. Arch Linux (or any Linux/macOS with Bash)
```bash
# In the project directory
bash setup.sh
# To activate the environment later:
source facerec-venv/bin/activate
# To run the app:
streamlit run app.py
```

### 3. Manual Setup (without any script usage)
```bash
# Clone the repository
 git clone https://github.com/prathamm-k/IDentifyMe-FaceRecognition-App.git
 cd IDentifyMe-FaceRecognition-App

# Create and activate a virtual environment
 python -m venv facerec-venv
 # On Linux/macOS:
 source facerec-venv/bin/activate
 # On Windows (cmd):
 facerec-venv\Scripts\activate
 # On Windows (PowerShell):
 .\facerec-venv\Scripts\Activate.ps1

# Install dependencies
 pip install --upgrade pip
 pip install -r requirements.txt

# Run the app
 streamlit run app.py
```

## Project Structure
```
IDentifyMe-FaceRecognition-App/
├── config.yaml            # App configuration (paths, prompts)
├── dataset/               # Face images and serialized database
│   ├── <ID>_<Name>.jpg    # Example: 1_Pratham.jpg
│   └── database.pkl       # Pickled face database
├── facerec-venv/          # Python virtual environment (created after setup)
├── pages/                 # Streamlit multipage scripts
│   ├── update_faces.py    # Add, delete, and adjust faces
│   └── view_database.py   # View the face database
├── app.py                 # Main Streamlit app (face recognition)
├── face_utils.py          # Face recognition and core functionalities and utilities
├── requirements.txt       # Python dependencies
├── setup.sh               # Bash setup script
├── setup.ps1              # PowerShell setup script
└── README.md              # Project documentation
```

## Function-by-Function Explanation

### app.py (Main Application)
- **initialize_sidebar()**: Sets up sidebar controls for input type, tolerance, and info display.
- **handle_picture_input(name_container, id_container, tolerance)**: Handles image uploads, runs recognition, and displays results.
- **handle_webcam_input(name_container, id_container, tolerance)**: Handles webcam input, runs real-time recognition, and displays results.
- **main()**: Orchestrates the app, calling the above functions and providing a developer section to rebuild the dataset.

### face_utils.py (Core Face Recognition Utilities/Functionalities)
- **get_database()**: Loads the face database (a pickle file) into memory.
- **recognize(image, tolerance)**: Detects and recognizes faces in an image, returning the image with annotations, the recognized name, and ID.
- **is_face_exists(image)**: Checks if there is at least one face in the image.
- **submit_new(name, id, image, old_idx=None)**: Adds a new face to the database or updates an existing one. Handles both file uploads and webcam images.
- **get_info_from_id(id)**: Retrieves a person's name, image, and index from the database using their ID.
- **delete_one(id)**: Removes a person from the database by their ID.
- **build_dataset()**: Rebuilds the database from all images in the dataset directory, encoding each face and storing the results.

### pages/update_faces.py (Add, Delete, Adjust Faces)
- **Adding section**: Lets users add a new face by uploading an image or using the webcam. Calls `submit_new` from `face_utils.py`.
- **Deleting section**: Lets users delete a face by ID. Calls `delete_one` from `face_utils.py`.
- **Adjusting section**: Lets users update an existing face entry (name, ID, or image). Calls `submit_new` with the old index for updating.
- **del_btn_callback(id)**: Callback to delete a student by ID.
- **form_callback(old_name, old_id, old_image, old_idx)**: Callback to update student info.

### pages/view_database.py (View Database)
- Loads the face database and displays it in a table with columns for index, ID, name, and image. Each row is aligned under the correct header for clarity.

### config.yaml
- Stores paths for the dataset and database, as well as prompt messages for the UI.

## Repository
GitHub: [prathamm-k/IDentifyMe-FaceRecognition-App](https://github.com/prathamm-k/IDentifyMe-FaceRecognition-App)

## Extra Details
- **Easy setup**: Use the provided scripts for quick environment setup.
- **Extensible**: Add more pages or features by creating new scripts in the `pages/` directory.
- **Dataset format**: Images should be named `<ID>_<Name>.jpg` for easy parsing.
- **Contact**: For questions or contributions, open an issue or pull request on GitHub.

## Troubleshooting
- If you encounter issues with dlib or face_recognition installation, ensure you are using a compatible Python version (3.9–3.11 recommended).
- If the webcam is not detected, make sure no other application is using it and that your browser/OS has granted permission.
- For Windows users, always use PowerShell to run `setup.ps1` and activate the environment.
- For Linux/macOS, ensure you have Python and pip installed and available in your PATH.

## Contributing
Contributions are welcome! If you have ideas for new features, bug fixes, or improvements, feel free to open an issue or submit a pull request. Please follow best practices and write clear commit messages.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [face_recognition](https://github.com/ageitgey/face_recognition) by Adam Geitgey
- [Streamlit](https://streamlit.io/)
- [OpenCV](https://opencv.org/)
- [dlib](http://dlib.net/)
- Inspiration from open-source face recognition and attendance systems

## Contact
Created by [prathamm-k](https://github.com/prathamm-k) — feel free to reach out via GitHub for questions, suggestions, or collaboration.

---
Enjoy using and extending IDentifyMe-FaceRecognition-App!