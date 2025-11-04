import streamlit as st
from pymongo import MongoClient
from PIL import Image
import requests
from io import BytesIO

@st.cache_resource
def get_client():
    client = MongoClient(st.secrets["mongo"]["uri"])
    return client

@st.cache_resource
def connect_mongodb():
    client = get_client()
    return client['jfm_ims']

@st.cache_resource
def get_collection(collection_name):
    db = connect_mongodb()
    return db[collection_name]

@st.cache_resource
def get_logo():
    url = "https://i.ibb.co/RpzG1R1d/JFM-Logo.jpg"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return Image.open(BytesIO(response.content))

@st.cache_resource
def get_bgimage():
    background_image = """
    <style>
    [data-testid="stAppViewContainer"] > .main {
    background-image: url("https://i.ibb.co/8D4hLbSX/natural-light-white-background.jpg");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;
    background-repeat: no-repeat;}</style>"""
    st.markdown(background_image, unsafe_allow_html=True)


def has_upper_and_number(text: str) -> bool:
    has_upper = any(c.isupper() for c in text)
    has_digit = any(c.isdigit() for c in text)
    if len(text)>=8:
        text_length = True
    else:
        text_length = False
    return has_upper, has_digit, text_length

def page_title(title):
    st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem; /* Adjust this value as needed (e.g., 0rem for minimal padding) */
        padding-bottom: 0rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }    
    </style>
    """,
    unsafe_allow_html=True
    )
    
    # st.markdown(
    #     """<style>h1{color: blue !important;}</style>""", unsafe_allow_html=True)
    
    st.title(f":blue[{title}]")


