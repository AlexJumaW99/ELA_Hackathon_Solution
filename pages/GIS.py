#make the necessary imports 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import streamlit as st 
import plotly.graph_objects as go
from PIL import Image
from streamlit_folium import st_folium

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
values_df = ['Community-Based Water Monitoring Program',
             'Nutrients in the Lower Wolastoq Watershed',
             'Sediment PAHs']

#we'll set the nutrients dataset as the default one because it has less missing values
choose_df = st.sidebar.selectbox('Choose a dataset to Analyse: ',
                                 values_df,
                                 index=values_df.index('Community-Based Water Monitoring Program')
                                 )

# if choose_df == values_df[0]:
#     df = pd.read_csv('Concatenated_master_dataset.csv')

if choose_df == values_df[0]:
    df = pd.read_csv('ACAP_Saint_John_Community-Based_Water_Monitoring_Program.csv') #not gonna use parse dates for now
    
elif choose_df == values_df[1]:
    df = pd.read_csv('ACAP_Saint_John_Nutrients_in_the_lower_Wolastoq_watershed.csv')

elif choose_df == values_df[2]:
    df = pd.read_csv('ACAP_Saint_John_Sediment_PAHs.csv')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1000)

st.sidebar.title('SIDEBAR:')
# pitch_value = st.sidebar.slider('Pitch value: ', 0, 60)
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
map_df = df.pivot_table(index=['MonitoringLocationName',
                               'ActivityStartDate',
                               'MonitoringLocationLatitude',
                               'MonitoringLocationLongitude'],
                        
        columns='CharacteristicName',
        values='ResultValue')

# df_pvt.fillna(0, inplace=True)
# df_pvt.reset_index()
map_df = map_df.reset_index()
# map_df

final_dict_cols = {
    'ActivityStartDate':'max',
}

dict_cols_2 = {
    k:'mean' for k in map_df.columns[2:]
}

final_dict_cols.update(dict_cols_2)

map_df_grouped = map_df.groupby(['MonitoringLocationName']).agg(final_dict_cols)
map_df_grouped = map_df_grouped.reset_index()
# map_df_grouped


safe_df = map_df_grouped[(map_df_grouped['Escherichia coli']<200) & (map_df_grouped['Escherichia coli'].notnull())]
# safe_df

unsafe_df = map_df_grouped[(map_df_grouped['Escherichia coli']>=200) & (map_df_grouped['Escherichia coli'].notnull())]
# unsafe_df

no_data = map_df_grouped[map_df_grouped['Escherichia coli'].isnull()]
# no_data

m = folium.Map(location=(45.3,-66.2), zoom_start=12)

group_1 = folium.FeatureGroup('Safe to Swim').add_to(m)
for loc, lat, lon, ecoli in zip(safe_df.MonitoringLocationName, safe_df.MonitoringLocationLatitude, safe_df.MonitoringLocationLongitude, safe_df['Escherichia coli']):
    folium.Marker(
        location = [lat, lon],
        tooltip = 'Safe to Swim! Click for details',
        popup = f'{loc} has a SAFE Ecoli value of {round(ecoli, 2)}',   
        icon = folium.Icon(icon="cloud", prefix='fa', color='green') 
    ).add_to(group_1)

group_2 = folium.FeatureGroup('Closed for Swimmers').add_to(m)
for loc, lat, lon, ecoli in zip(unsafe_df.MonitoringLocationName, unsafe_df.MonitoringLocationLatitude, unsafe_df.MonitoringLocationLongitude, unsafe_df['Escherichia coli']):
    folium.Marker(
        location = [lat, lon],
        tooltip = 'Dangerous to Swim in! Click for details',
        popup = f'{loc} has a UNSAFE Ecoli value of {round(ecoli, 2)}',   
        icon = folium.Icon(icon="cloud", prefix='fa', color='red') 
    ).add_to(group_2)
    
group_3 = folium.FeatureGroup('No data available').add_to(m)
for loc, lat, lon in zip(no_data.MonitoringLocationName, no_data.MonitoringLocationLatitude, no_data.MonitoringLocationLongitude):
    folium.Marker(
        location = [lat, lon],
        tooltip = 'No data availabel',
        popup = f'{loc} has no ecoli data. Swim with caution.',   
        icon = folium.Icon(icon="cloud", prefix='fa', color='black') 
    ).add_to(group_3)
    

st_map = st_folium(m, width=700, height=450)