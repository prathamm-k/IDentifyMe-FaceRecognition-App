import streamlit as st 
import pickle 
import yaml 
import pandas as pd 

#load configuration and database
cfg = yaml.load(open("config.yaml", "r"), Loader=yaml.FullLoader)
PKL_PATH = cfg['PATH']["PKL_PATH"]
st.set_page_config(layout="wide")

#load the face database from pickle file
with open(PKL_PATH, 'rb') as file:
    database = pickle.load(file)

#display table header
header_cols = st.columns([0.7, 0.9, 3, 3])
header_cols[0].markdown("**Index**")
header_cols[1].markdown("**ID**")
header_cols[2].markdown("**Name**")
header_cols[3].markdown("**Image**")

#display each entry in a new row, aligned under the correct header
for idx, person in database.items():
    row_cols = st.columns([0.7, 0.9, 3, 3])
    row_cols[0].write(idx)
    row_cols[1].write(person['id'])
    row_cols[2].write(person['name'])
    row_cols[3].image(person['image'], width=200)