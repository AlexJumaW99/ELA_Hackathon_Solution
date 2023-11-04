import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  
import base64
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

#read in cleaned and formatted datasets

#FIND A WAY TO CONCATENATE DATASETS!!!

#ADD A PLUS BUTTON FOR THE LINE GRAPH TO OVERLAY ANOTHER BODY OF WATER FOR COMPARISON PURPOSES

@st.cache_data
def get_img_as_base64(file):
    with open(file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# img = get_img_as_base64('mo-hs2PaEGb6r8-unsplash.jpg')


# page_bg_image = """
# <style>
# [data-testid="stAppViewContainer"] {
#     background-image: url("https://images.unsplash.com/photo-1698414786771-0fa24cabcd0b?auto=format&fit=crop&q=80&w=3024&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
#     background-size: cover;
# }

# [data-testid="stHeader"] {
#     background-color: rgba(0, 0, 0, 0);
# }

# [data-testid="stToolbar"] {
#     right: 2rem;
# }

# [data-testid="stSidebar"] {
#     background-image: url("https://images.unsplash.com/photo-1698414786771-0fa24cabcd0b?auto=format&fit=crop&q=80&w=3024&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
#     background-position: center;
# }
# </style>

# """


#inject CSS tag and add unsafe_allow_html
# st.markdown(page_bg_image, unsafe_allow_html=True)

#DATA CLEANING PART
values_df = ['All',
             'Community-Based Water Monitoring Program',
             'Nutrients in the Lower Wolastoq Watershed',
             'Sediment PAHs']

#we'll set the nutrients dataset as the default one because it has less missing values
choose_df = st.sidebar.selectbox('Choose an ACAP St. John dataset to Analyse: ',
                                 values_df
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

#check out how many missing values each 
df.info()

#keep only the columns that contain at least 5000 values out of the possible 30282
df = df.dropna(axis=1, thresh=5000)
df.sort_values('MonitoringLocationName', ascending=False).head(11)

#add a year, month and day column to assist with further aggregation in future
df['Year'] = df['ActivityStartDate'].str.split('-').str[0]
df['Month'] = df['ActivityStartDate'].str.split('-').str[1]
df['Day'] = df['ActivityStartDate'].str.split('-').str[2]

df_pvt = df.pivot_table(index=['MonitoringLocationName', 'ActivityStartDate'],
        columns='CharacteristicName',
        values='ResultValue')

# df_pvt.fillna(0, inplace=True)
# df_pvt.reset_index()
df_pvt = df_pvt.reset_index()

df_pvt.info()

#create year, month and day columns for pivot table as well bc info was lost
df_pvt['Year'] = df_pvt['ActivityStartDate'].str.split('-').str[0]
df_pvt['Month'] = df_pvt['ActivityStartDate'].str.split('-').str[1]
df_pvt['Day'] = df_pvt['ActivityStartDate'].str.split('-').str[2]
#df_pvt

yr_bar = df_pvt.groupby(['MonitoringLocationName', 'Year']).mean()
yr_bar.reset_index()

len(df['MonitoringLocationName'].unique())

df.info()


# df = pd.read_csv('cleaned_df.csv')
# df_pvt = pd.read_csv('cleaned_df_pivot.csv')
# unit = {'mg/L':['Dissolved oxygen (DO)','Ammonia','Escherichia coli','Fecal Coliform','Orthophosphate','Total Coliform','Total dissolved solids','Total suspended solids','Dissolved oxygen saturation'],'ppt':[],'°C':['Temperature, water','Temperature, air'],'NTU':['Turbidity'],'uS/cm':['Conductivity']}
unit = {
    'Dissolved oxygen (DO)':'mg/L',
    'Ammonia':'mg/L',
    'Escherichia coli':'mg/L',
    'Fecal Coliform':'mg/L',
    'Orthophosphate':'mg/L',
    'Total Coliform':'mg/L',
    'Total dissolved solids':'mg/L',
    'Total suspended solids':'mg/L',
    'Dissolved oxygen saturation':'mg/L',
    'Salinity':'ppt',
    'Temperature, water':'°C',
    'Temperature, air':'°C',
    'Turbidity':'NTU',
    'Conductivity':'uS/cm',
    }
#title of the main page
st.title('ELA DASHBOARD')
st.caption('Source: ACAP St. John')

# creating the sidebar which contains diff filters
# --- SIDEBAR ---
st.sidebar.title("SIDEBAR")
st.sidebar.header("Please Filter here: ")
choose_visual = st.sidebar.selectbox(
    'Visuals:',
    (
        'Line Graph',
        'Bar Graph',
        'Scatter Plot',
        'Pie Chart',
        'Histogram',
    )
) 

if choose_visual == 'Line Graph':
    values_body = list(df_pvt.MonitoringLocationName.unique())
    choose_body = st.sidebar.selectbox('Choose a body of water:',
                                    values_body
    )

    for w in list(df_pvt.MonitoringLocationName.unique()):
        if w == choose_body:
            df_line = df_pvt[df_pvt.MonitoringLocationName == w]
    
    values_measure = list(df_pvt.columns[2:-3])
    choose_measure = st.sidebar.selectbox('Choose the trend you would like to look at:',
                                          values_measure
    )
    
    
        
    choose_timeline = st.sidebar.selectbox('Choose timeline:',
                                           (
                                               'All-Time',
                                               'Year, Month, Day'
                                           )                                      
    )
    
    if choose_timeline == 'All-Time':
        
        #create streamlit columns that we will use later
        col1, col2 = st.columns([2,2])
        
        #display the dataframe used to make the line graphs
        
        # with col1:
        #     st.metric(f'Max {choose_measure}: ', round(df_line[choose_measure].max(),4))
        #     st.metric(f'Min {choose_measure}: ', round(df_line[choose_measure].min(),4))
        #     # st.subheader('Table: ')
        #     # df_line[['MonitoringLocationName', 'ActivityStartDate', choose_measure]]
            
        # with col2:
        #     st.markdown(f'Name of water body: ')
        #     st.text(str(df_line.MonitoringLocationName.unique()[0]))
            
        #     st.metric(f'Mean {choose_measure}: ', round(df_line[choose_measure].mean(),4))
        #     st.metric(f'Median {choose_measure}: ', round(df_line[choose_measure].median(),4))
              # col3, col4 = st.columns([2,2])
        with col1:
            for x in unit:
                if x == choose_measure:
                    choose_unit =  unit[x]
            gauge_graph = go.Figure(go.Indicator(
                mode = 'gauge+number',
                value = round(df_line[choose_measure].mean(),4),
                
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': f'{choose_measure} ({choose_unit})'},
                gauge = {
                    'axis':{'range':[round(df_line[choose_measure].min(),4),round(df_line[choose_measure].max(),4)]},
                    'bar': {'color': 'white'},
                    # 'steps': [
                    #     {'range': [round(df_line[choose_measure].min(),4), round(df_line[choose_measure].median(),4)], 'color': 'green'},
                    #     {'range': [round(df_line[choose_measure].median(),4), round(df_line[choose_measure].max(),4)], 'color': 'red'}],
                        }
                    ))
            st.plotly_chart(gauge_graph, use_container_width=True)

        # Create a Plotly figure
        fig = px.line(df_line, x='ActivityStartDate', y=choose_measure, labels={choose_measure: f'{choose_measure}'}, title=f'Trend of {choose_measure} over the years')
        fig.update_layout(
            xaxis_title='Time',
            yaxis_title=f'{choose_measure}',
            legend_title='Legend'
        )

        # Add horizontal lines for 'Dissolved oxygen (DO)'
        if choose_measure == 'Dissolved oxygen (DO)':
            fig.add_shape(
                dict(
                    type='line',
                    x0=df_line['ActivityStartDate'].min(),
                    x1=df_line['ActivityStartDate'].max(),
                    y0=4,
                    y1=4,
                    line=dict(color='orange', width=2, dash='solid'),
                    name='Stress Zone'
                )
            )

            fig.add_shape(
                dict(
                    type='line',
                    x0=df_line['ActivityStartDate'].min(),
                    x1=df_line['ActivityStartDate'].max(),
                    y0=1,
                    y1=1,
                    line=dict(color='red', width=2, dash='dashdot'),
                    name='Danger Zone'
                )
            )

        # Rotate x-axis labels
        fig.update_xaxes(tickangle=90)

        # Show the plot
        st.plotly_chart(fig)

        #old matplotlib line graph for comparison purposes
        fig, ax = plt.subplots(figsize=(20,8), dpi=150)
        ax.plot(df_line.ActivityStartDate, df_line[choose_measure], label=f'{choose_measure}')
        
        if choose_measure == 'Dissolved oxygen (DO)':
            plt.axhline(y=4, color='orange', linestyle='-', label='Stress Zone')
            plt.axhline(y=1, color='red', linestyle='-.', label='Danger Zone')
        
        ax.set_title(f'Trend of {choose_measure} over the years',
                    fontsize=20,
                    fontweight=700,
                    color='blue')
        
        ax.set_xlabel('Time',
                    fontsize=20,
                    fontweight=400)
        
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)  
        
        ax.set_ylabel(f'{choose_measure}',
                    fontsize=20,
                    fontweight=400)
        
        plt.legend(title='Legend:', loc=[1.01,0.5])
        
        st.pyplot(fig)
    
    elif choose_timeline == 'Year, Month, Day':
        choose_year = st.sidebar.selectbox('Year:',
            tuple(df_line['Year'].unique())
        )
        df_line_year = df_line.groupby('Year').mean()
        df_line_year = df_line_year.reset_index()
        df_line_year.Year = df_line_year.Year.astype('int32') 
        df_line_year.Year = pd.to_datetime(df_line_year.Year, format='%Y')
        #df_line_year.Year = df_line_year.strftime('%Y')
        df_line_year[['Year', choose_measure]]
        
        '''
        for y in df_line['Year'].unique():
            if choose_year == y:
                df_line_one_year = df_line_year[df_line_year.index == ]
        '''
    
if choose_visual == 'Bar Graph':
    choose_bar_measure = st.sidebar.selectbox('Choose the trend you would like to look at on the bar graph:',
                                          tuple(df_pvt.columns[2:-3])
    )
    
    choose_year = st.sidebar.selectbox('Please select the year: ',
                                       tuple(df_pvt.sort_values('Year', ascending=True).Year.unique()))
    
    choose_rank = st.sidebar.selectbox('Please choose the order: ',
                                       (
                                           'Ascending',
                                           'Descending'
                                       ))
    
    for yr in list(tuple(df_pvt.sort_values('Year', ascending=True).Year.unique())):
        if yr == choose_year:
            df_bar = df_pvt[df_pvt['Year'] == yr]
    
    df_bar
    
    descending = df_bar.groupby('MonitoringLocationName').mean().sort_values(choose_bar_measure, ascending=False)[:20]
    ascending = df_bar.groupby('MonitoringLocationName').mean().sort_values(choose_bar_measure, ascending=True)[:20]
    
    #count = len(df[])
    if choose_rank == 'Ascending':
        df_plotly_bar = ascending
    else:
        df_plotly_bar = descending

    # Create a Plotly figure for the bar plot
    fig = px.bar(df_plotly_bar,
                 y=df_plotly_bar.index,
                 x=choose_bar_measure,
                 labels={choose_bar_measure: f'{choose_bar_measure}'},
                 orientation='h')
    
    fig.update_layout(
        yaxis_title='Water Body',
        xaxis_title=f'{choose_bar_measure}',
        title=f'How {choose_bar_measure} compares in the different water bodies in {choose_year}',
        xaxis=dict(tickangle=45),
        title_font=dict(size=20, color='red'),
        yaxis_title_font=dict(size=20),
        xaxis_title_font=dict(size=20)
    )

    # Show the plot
    st.plotly_chart(fig)

    
    
    # if choose_rank == 'Ascending':
    #     ascending
        
    #     fig, ax = plt.subplots(figsize=(12,5), dpi=150)
    #     sns.barplot(data=ascending,
    #                 x=ascending.index,
    #                 y=ascending[choose_bar_measure])
        
    # elif choose_rank == 'Descending':
    #     descending
        
    #     fig, ax = plt.subplots(figsize=(12,5), dpi=150)
    #     sns.barplot(data=descending,
    #                 x=descending.index,
    #                 y=descending[choose_bar_measure])
    
    # ax.set_xticklabels(labels=ax.get_xticklabels(), rotation=90) 
    # ax.set_title(f'How {choose_bar_measure} compares in the different water bodies in {choose_year}',
    #              fontsize=20,
    #              fontweight=700,
    #              color='blue')
    
    # ax.set_xlabel('Water Body',
    #                 fontsize=20,
    #                 fontweight=400)
    
    # ax.set_ylabel(f'{choose_bar_measure}',
    #                 fontsize=20,
    #                 fontweight=400)
    
    # st.pyplot(fig)

    #df_bar = df_pvt.groupby('MonitoringLocationName')
    
if choose_visual == 'Scatter Plot':
    df_pvt
    
    choose_scope = st.sidebar.selectbox('Choose the scope: ',
                                       ('All bodies of water', 'Specify')
                                       )
    
    choose_x = st.sidebar.selectbox('Choose the x value: ',
        tuple(df_pvt.columns[2:-3])
              )
    
    choose_y = st.sidebar.selectbox('Choose the y value: ',
        tuple(df_pvt.columns[2:-3])
              )
    
    
    if choose_scope == 'All bodies of water':
        fig, ax  = plt.subplots(figsize=(12,5), dpi=150)
        sns.scatterplot(data = df_pvt,
                            x=df_pvt[choose_x],
                            y=df_pvt[choose_y])
        
        st.pyplot(fig)
    
    else:
        choose_body = st.sidebar.selectbox('Choose the body of water: ',
                                           tuple(df_pvt.MonitoringLocationName.unique())
                                           )
        
        fig, ax  = plt.subplots(figsize=(12,5), dpi=150)
        sns.scatterplot(data = df_pvt[df_pvt.MonitoringLocationName == choose_body],
                            x=choose_x,
                            y=choose_y)
        
        ax.set_title(f'Scatterplot showing correlation between {choose_x} and {choose_y} in {choose_body}',
                     fontsize=15)
        
        ax.set_xlabel(f'{choose_x}',
                      fontsize=15)
        
        ax.set_ylabel(f'{choose_y}',
                      fontsize=15)
        
        st.pyplot(fig)
        
        # fig2 = sns.heatmap(df_pvt[df_pvt.MonitoringLocationName == choose_body].corr())
        # st.pyplot(fig2)
        
        
    
    
    
    






