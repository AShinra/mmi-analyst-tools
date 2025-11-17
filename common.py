import streamlit as st
from pymongo import MongoClient
from PIL import Image
import requests
from io import BytesIO
import random
from openpyxl import Workbook
import pandas as pd

# font list
font_list = ['Arial', 'Segoe UI', 'Helvetica', 'Times New Roman', 'Comic Sans MS', 'Fira Code', 'Verdana', 'Source Code Pro', 'Calibri', 'Playfair']
font_list = sorted(font_list)

@st.cache_resource
def get_client():
    client = MongoClient(st.secrets["mongo"]["uri"])
    return client

@st.cache_resource
def connect_mongodb():
    client = get_client()
    return client['mars']

@st.cache_resource
def get_collection(collection_name):
    db = connect_mongodb()
    return db[collection_name]

@st.cache_resource
def get_tier_collection():
    client = get_client()
    db = client['histo']
    return db['tier']

@st.cache_resource
def get_logo():
    url = "https://i.ibb.co/JRW19H4Y/AShinra-Logo.png"
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

def gradient_line():
    st.markdown("""
    <div style='height: 4px; 
                background: linear-gradient(90deg, #5f27cd, #48dbfb, #10ac84);
                border-radius: 10px; 
                margin-bottom: 20px;'>
    </div>
    """,
    unsafe_allow_html=True)

def bible_verse(num):

    bible_dict = {
        1:['Whatever you do, work at it with all your heart, as working for the Lord, not for human masters..', 'Colossians 3:23'],
        2:['For the Lord gives wisdom; from His mouth come knowledge and understanding.', 'Proverbs 2:6'],
        3:['If any of you lacks wisdom, you should ask God, who gives generously to all without finding fault, and it will be given to you.', 'James 1:5'],
        4:['Trust in the Lord with all your heart and lean not on your own understanding; in all your ways submit to Him, and He will make your paths straight.', 'Proverbs 3:5–6'],
        5:['I will instruct you and teach you in the way you should go; I will counsel you with My loving eye on you.', 'Psalm 32:8'],
        6:['So whether you eat or drink or whatever you do, do it all for the glory of God.', '1 Corinthians 10:31']
    }

    return bible_dict[num]


def create_workbook(output_filename:str):
    '''
    output_filename ==>> filename to be used in creating an excel file
    '''

    wb = Workbook()    
    wb.save(f'{output_filename}.xlsx')


def header_settings():
    '''
    Formatting of sheet headers\n\n
    0 ==>> header font name (default Arial)\n
    1 ==>> header font size (default 24)\n
    2 ==>> header font color (default #0066cc)\n
    3 ==>> bold (default True)\n
    4 ==>> itallic (default False)
    '''
    header_settings = []
    st.markdown('#### Headers (Font Defaults)')
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        header_font_name = st.selectbox(
             label='Name',
             options=font_list,
             placeholder='Arial',
             key='header_font_name')
        
        default_value = 24
        header_font_size = st.selectbox(
            label='Size',
            options=[i for i in range(1, 100)],
            index=default_value - 1,
            key='header_font_size')

    with col2:
        header_font_color = st.color_picker(
             label='Color',
             value='#0066cc',
             key='header_font_color')
        header_font_color = header_font_color.split('#')[1]
        
    with col3:
        header_bold = st.checkbox(
              label='Bold',
              key='header_bold',
              value=True)
        header_italic = st.checkbox(
            label='Italic',
            key='header_italic')
        
    header_settings.append(header_font_name)
    header_settings.append(header_font_size)
    header_settings.append(header_font_color)
    header_settings.append(header_bold)
    header_settings.append(header_italic)
    
    return header_settings
        

def subheader_settings():
    '''
    Formatting of sheet subheaders\n\n
    0 ==>> subheader font name (default Arial)\n
    1 ==>> subheader font size (default 11)\n
    2 ==>> subheader font color (default #0066cc)\n
    3 ==>> bold (default True)\n
    4 ==>> itallic (default False)
    '''
    subheader_settings = []

    st.markdown('#### Sub Headers (Defaults)')
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        subheader_font_name = st.selectbox(
             label='Name',
             options=font_list,
             placeholder='Arial',
             key='subheader_font_name')
        
        default_value = 11
        subheader_font_size = st.selectbox(
            label='Size',
            options=[i for i in range(1, 100)],
            index=default_value - 1,
            key='subheader_font_size')
        
    with col2:
        subheader_font_color = st.color_picker(
             label='Color',
             value='#0066cc',
             key='subheader_font_color')
        subheader_font_color = subheader_font_color.split('#')[1]
        
    with col3:
        subheader_bold = st.checkbox(
            label='Bold',
            value=True,
            key='subheader_bold')
        
        subheader_italic = st.checkbox(
            label='Italic',
            value=False,
            key='subheader_italic')
        
    subheader_settings.append(subheader_font_name)
    subheader_settings.append(subheader_font_size)
    subheader_settings.append(subheader_font_color)
    subheader_settings.append(subheader_bold)
    subheader_settings.append(subheader_italic)
    
    return subheader_settings


def sheet_title_settings():
    '''
    Formatting of sheet subheaders\n\n
    0 ==>> sheet title font name (default Arial)\n
    1 ==>> sheet title font size (default 11)\n
    2 ==>> sheet title font color (default #0066cc)\n
    3 ==>> bold (default True)\n
    4 ==>> itallic (default False)
    '''
    sheettitle_settings = []

    st.markdown('#### Sub Headers (Defaults)')
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        sheettitle_font_name = st.selectbox(
             label='Name',
             options=font_list,
             placeholder='Arial',
             key='sheettitle_font_name')
        
        default_value = 11
        sheettitle_font_size = st.selectbox(
            label='Size',
            options=[i for i in range(1, 100)],
            index=default_value - 1,
            key='sheettitle_font_size')
        
    with col2:
        sheettitle_font_color = st.color_picker(
             label='Color',
             value='#0066cc',
             key='sheettitle_font_color')
        sheetitle_font_color = sheettitle_font_color.split('#')[1]
        
    with col3:
        sheettitle_bold = st.checkbox(
            label='Bold',
            value=True,
            key='sheettitle_bold')
        
        sheettitle_italic = st.checkbox(
            label='Italic',
            value=False,
            key='sheettitle_italic')
        
    sheettitle_settings.append(sheettitle_font_name)
    sheettitle_settings.append(sheettitle_font_size)
    sheettitle_settings.append(sheetitle_font_color)
    sheettitle_settings.append(sheettitle_bold)
    sheettitle_settings.append(sheettitle_italic)
    
    return sheettitle_settings