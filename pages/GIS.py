#make the necessary imports 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st 
import plotly.graph_objects as go
from PIL import Image

#look for extreme outliers in the data, not just small outliers 
#compare one site in the lake with other sites in the lake, why is the pH in one site vastly different to another 
#compare changes in metrics (like pH) over time, how does it change from one month to another 
#for example, if DO drastically drops from Dec to Jan, why is this changing? Maybe it's bc the lake froze over and there's no
#gaseous exchange

#for swimming you would want to look for turbidity of less than 50
#for swimming the temp would also have to be high



#we will 

APP_TITLE = 'Canadian WQI GIS'
APP_SUB_TITLE = 'Source: ACAP St. John'

#st.set_page_config(APP_TITLE)
st.title(APP_TITLE)
st.caption(APP_SUB_TITLE)


#DATA CLEANING PART
values_df = ['All',
             'Community-Based Water Monitoring Program',
             'Nutrients in the Lower Wolastoq Watershed',
             'Sediment PAHs']

#we'll set the nutrients dataset as the default one because it has less missing values
choose_df = st.sidebar.selectbox('Choose a dataset to Analyse: ',
                                 values_df,
                                 index=values_df.index('Community-Based Water Monitoring Program')
                                 )

if choose_df == values_df[0]:
    df = pd.read_csv('Concatenated_master_dataset.csv')

elif choose_df == values_df[1]:
    df = pd.read_csv('ACAP_Saint_John_Community-Based_Water_Monitoring_Program.csv') #not gonna use parse dates for now
    
elif choose_df == values_df[2]:
    df = pd.read_csv('ACAP_Saint_John_Nutrients_in_the_lower_Wolastoq_watershed.csv')

elif choose_df == values_df[3]:
    df = pd.read_csv('ACAP_Saint_John_Sediment_PAHs.csv')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1000)

st.sidebar.title('SIDEBAR:')
pitch_value = st.sidebar.slider('Pitch value: ', 0, 60)
st.sidebar.selectbox('Choose different classes:',
                     ('Recreational',
                      'Acquatic',
                      'Drinking')
                     )

st.markdown(
    "Tip 💡: You can use the filters in the sidebar 👈 to display different visuals!"
)


#df = pd.read_csv('ACAP_Saint_John_Community-Based_Water_Monitoring_Program.csv')


#df
map_df = df.groupby('MonitoringLocationName').mean()[['MonitoringLocationLatitude', 'MonitoringLocationLongitude']].reset_index()
map_df

nme = list(map_df.MonitoringLocationName)
lati = list(map_df.MonitoringLocationLatitude)
longi = list(map_df.MonitoringLocationLongitude)

mapbox_access_token = 'pk.eyJ1IjoiYWp1bWEiLCJhIjoiY2xvZXVrNDc1MGhqbjJ2bXBtNzA0NGl3ZiJ9.s0bInsWqbaE52py5z_wepg'
fig = go.Figure(go.Scattermapbox(
        lat=lati,
        lon=longi,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            symbol='harbor'
        ),
        text=nme,
    ))

fig.update_layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=45.3,
            lon=-66.2
        ),
        pitch=pitch_value,
        zoom=8
    ),
)

st.plotly_chart(fig)
















# st.map(folium.Map(location=[56.1304, 106.3468]))
