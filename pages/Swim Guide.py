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


APP_TITLE = 'SWIM GUIDE'
APP_SUB_TITLE = 'Source: ACAP St. John'

#st.set_page_config(APP_TITLE)
st.title(APP_TITLE)
st.caption(APP_SUB_TITLE)


#DATA CLEANING PART

# if choose_df == values_df[0]:
#     df = pd.read_csv('Concatenated_master_dataset.csv')

df = pd.read_csv('datasets/ACAP_Saint_John_Community-Based_Water_Monitoring_Program.csv') #not gonna use parse dates for now

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1000)

# st.sidebar.title('SIDEBAR:')
# pitch_value = st.sidebar.slider('Pitch value: ', 0, 60)

# st.sidebar.selectbox('Choose different classes:',
#                      ('Recreational',
#                       'Acquatic',
#                       'Drinking')
#                      )

# st.markdown(
#     "Tip 💡: You can use the filters in the sidebar 👈 to display different visuals!"
# )

st.markdown("""
            If the geometric mean of E. coli samples exceeds the recreational
            water quality objective of 200 bacteria/100 mL and/or when a single sample
            contains more than 400 bacteria/100 mL the beach is re-sampled.
            """)

st.markdown("""
            A beach is marked Green when the geometric mean of E. coli samples is below the recreational water
            quality objective of 200 bacteria/100 mL.
            """)

st.markdown("""
            A beach is marked Red when the geometric mean
            of E. coli samples is above therecreational water quality objective of  200 bacteria/100 mL.
            """)

st.markdown("""
           A beach is marked Grey when reliable or up-to-date information is not available. 
            """)




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
        icon = folium.Icon(icon="cloud", prefix='fa', color='lightgray') 
    ).add_to(group_3)
    

st_map = st_folium(m, width=700, height=450)