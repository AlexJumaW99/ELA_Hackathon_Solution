import streamlit as st 
from PIL import Image

st.title('Dataset Explainer')

#we're going to upload the images containing the Dataset Explainer from the DataStream website
image = Image.open('Temperature_pages-to-jpg-0001.jpg')
image2 = Image.open('Temperature_pages-to-jpg-0002.jpg')
image3 = Image.open('Temperature_pages-to-jpg-0003.jpg')

#display the image on streamlit
st.image(image, caption='Explainer: Page 1')

#display the second image 
st.image(image2, caption='Explainer: Page 2')

#third image
st.image(image3, caption='Explainer: Page 3')
