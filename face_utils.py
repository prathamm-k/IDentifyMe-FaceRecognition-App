#Contains core functions for face detection, recognition, and database management for the entire app

from typing import Dict, List, Tuple, Optional, Union
import face_recognition as frg
import pickle as pkl
import os
import cv2
import numpy as np
import yaml
from collections import defaultdict
from pathlib import Path

Image = np.ndarray
Database = Dict[int, Dict[str, Union[str, Image, np.ndarray]]]
FaceLocation = Tuple[int, int, int, int]

# Load configuration from YAML file
with open('config.yaml', 'r') as f:
    cfg = yaml.safe_load(f)

DATASET_DIR = Path(cfg['PATH']['DATASET_DIR'])
PKL_PATH = Path(cfg['PATH']['PKL_PATH'])

#Load the face recognition database from pickle file
def get_database() -> Database:
    with open(PKL_PATH, 'rb') as f:
        return pkl.load(f)

#Detect and recognize faces in an image using the database
def recognize(image: Image, tolerance: float) -> Tuple[Image, str, str]:
    database = get_database()
    known_encodings = [database[id]['encoding'] for id in database.keys()]
    face_locations = frg.face_locations(image)
    face_encodings = frg.face_encodings(image, face_locations)
    name = 'Unknown'
    id = 'Unknown'
    # Loop through detected faces and compare with known encodings
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = frg.compare_faces(known_encodings, face_encoding, tolerance=tolerance)
        distance = frg.face_distance(known_encodings, face_encoding)
        if True in matches:
            match_index = matches.index(True)
            name = database[match_index]['name']
            id = database[match_index]['id']
            distance = round(distance[match_index], 2)
            # Annotate image with distance
            cv2.putText(image, str(distance), (left, top-30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        # Draw rectangle and label for each face
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(image, name, (left, top-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    return image, name, id

#Returns True if at least one face is detected in the image
def is_face_exists(image: Image) -> bool:
    return len(frg.face_locations(image)) > 0

#Add or update a person in the database, this handles both upload and webcam images
def submit_new(name: str, id: str, image: Union[Image, bytes], old_idx: Optional[int] = None) -> Union[bool, int]:
    database = get_database()
    #Convert uploaded file to numpy array if needed
    if not isinstance(image, np.ndarray):
        image = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
    if not is_face_exists(image):
        return -1  #flag for no face found
    encoding = frg.face_encodings(image)[0]
    existing_ids = [database[i]['id'] for i in database.keys()]
    #Update existing entry or add new entry
    if old_idx is not None:
        new_idx = old_idx
    else:
        if id in existing_ids:
            return 0  #flag for ID already exists
        new_idx = len(database)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  #store as RGB
    database[new_idx] = {
        'image': image,
        'id': id,
        'name': name,
        'encoding': encoding
    }
    #Save updated database
    with open(PKL_PATH, 'wb') as f:
        pkl.dump(database, f)
    return True

#Look up a person by ID and return their name, image, and index number
def get_info_from_id(id: str) -> Tuple[Optional[str], Optional[Image], Optional[int]]:
    database = get_database()
    for idx, person in database.items():
        if person['id'] == id:
            return person['name'], person['image'], idx
    return None, None, None

#Remove a person from the database by their ID
def delete_one(id: str) -> bool:
    database = get_database()
    for key, person in database.items():
        if person['id'] == id:
            del database[key]
            with open(PKL_PATH, 'wb') as f:
                pkl.dump(database, f)
            return True
    return False

#Rebuild the face database from all images in the dataset directory
def build_dataset() -> None:
    information = defaultdict(dict)
    counter = 0
    #process each image in the dataset directory
    for image_path in DATASET_DIR.glob('*.jpg'):
        image_name = image_path.stem
        parsed_name = image_name.split('_')
        person_id = parsed_name[0]
        person_name = ' '.join(parsed_name[1:])
        image = frg.load_image_file(str(image_path))
        information[counter] = {
            'image': image,
            'id': person_id,
            'name': person_name,
            'encoding': frg.face_encodings(image)[0]
        }
        counter += 1
    #save the rebuilt database
    with open(PKL_PATH, 'wb') as f:
        pkl.dump(information, f)