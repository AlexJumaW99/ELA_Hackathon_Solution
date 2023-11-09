import streamlit as st 
from PIL import Image

page_bg_image = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1516132006923-6cf348e5dee2?auto=format&fit=crop&q=80&w=3774&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: cover;
    color: white;
}

[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
}

[data-testid="stToolbar"] {
    right: 2rem;
}

[data-testid="stSidebar"] {
    background-image: url("https://images.unsplash.com/photo-1698414786771-0fa24cabcd0b?auto=format&fit=crop&q=80&w=3024&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-position: center;
}
</style>

"""


#inject CSS tag and add unsafe_allow_html
st.markdown(page_bg_image, unsafe_allow_html=True)

st.title('Dataset Explainer')
st.caption('Source: ACAP St. John')

#we're going to upload the images containing the Dataset Explainer from the DataStream website
image = Image.open('images/Temperature_pages-to-jpg-0001.jpg')
image2 = Image.open('images/Temperature_pages-to-jpg-0002.jpg')
image3 = Image.open('images/Temperature_pages-to-jpg-0003.jpg')

#display the image on streamlit
st.image(image, caption='Explainer: Page 1')

#display the second image 
st.image(image2, caption='Explainer: Page 2')

#third image
st.image(image3, caption='Explainer: Page 3')
