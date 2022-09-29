import streamlit as st
import requests
import json
import numpy as np

from helperFunctions import *

# Title
st.title("BB Annotation Viewer !!!")

name = st.text_input("Enter the sourceImageId", "Enter the sourceImageId")

if(st.button('Submit')):
    result = name.title()
    imgRetrieved = retrieveImageFromS3(result.lower())
    st.image(imgRetrieved)

    st.success(result)
 