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

# @st.cache_data
# def get_img_as_base64(file):
#     with open(file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# img = get_img_as_base64('mo-hs2PaEGb6r8-unsplash.jpg')

#background-image: url("https://images.unsplash.com/photo-1516132006923-6cf348e5dee2?auto=format&fit=crop&q=80&w=3774&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");


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

#DATA CLEANING PART
values_df = ['Community-Based Water Monitoring Program',
             'Nutrients in the Lower Wolastoq Watershed',
             'Sediment PAHs']

st.sidebar.title('SIDEBAR')

#we'll set the nutrients dataset as the default one because it has less missing values
st.sidebar.subheader('Please choose a dataset to Analyse 📈')
choose_df = st.sidebar.selectbox('Choose dataset: ',
                                 values_df
                                 )

# if choose_df == values_df[0]:
#     df = pd.read_csv('Concatenated_master_dataset.csv')

if choose_df == values_df[0]:
    df = pd.read_csv('datasets/ACAP_Saint_John_Community-Based_Water_Monitoring_Program.csv') #not gonna use parse dates for now
    
elif choose_df == values_df[1]:
    df = pd.read_csv('datasets/ACAP_Saint_John_Nutrients_in_the_lower_Wolastoq_watershed.csv')

elif choose_df == values_df[2]:
    df = pd.read_csv('datasets/ACAP_Saint_John_Sediment_PAHs.csv')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1000)

#check out how many missing values each 
df.info()

#keep only the columns that contain at least 5000 values out of the possible 30282
# df = df.dropna(axis=1, thresh=5000)
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


#let's create a dictionary that we will need later in the program 
#we're going to create a dictionary, where the key is the metric 
#and the value is a list that will have a bunch of items 
#the first index will be the subheader which will be the metric name 
#the second index will be the upper_descr before the graph 
#the third index will be the lower_descr after the graph

metric_names = ['Ammonia', 'Dissolved oxygen (DO)', 'Escherichia coli', 'Orthophosphate', 'Temperature, water', 'pH']
subheader_names = ['Ammonia', 'Dissolved oxygen (DO)', 'Escherichia coli', 'Orthophosphate', 'Temperature of water (°C)', 'pH']
upper_descr = [
    '''
    How Does Ammonia Affect Water Quality? Ammonia in drinking water can sometimes create an
    unpleasant taste and smell, which is caused by the formation of chloramines, which the addition of ammonia helps promote.
    Chloramines form when both chlorine and ammonia are added to drinking water to disinfect it.
    '''
    ,
    '''
    Why is dissolved oxygen important for water quality?
    Dissolved oxygen is the amount of gaseous oxygen dissolved in the water.
    Oxygen gets into the water in various ways, including absorbing it from the atmosphere,
    by rapid movement of the water, or as a product of photosynthesis. Oxygen is what gives the water life!
    Fish and plants depend on certain levels of oxygen to survive.
    '''
    ,
    '''
    E. coli in water is a strong indicator of sewage or animal waste contamination.
    Sewage and animal waste can contain many types of disease causing organisms.
    Consumption may result in severe illness; children under five years of age,
    those with compromised immune systems, and the elderly are particularly susceptible.
    '''
    ,
    '''
    Phosphorus is an essential nutrient for plants and animals.
    However, excessive phosphorus in surface water can cause explosive growth of aquatic plants and algae.
    This can lead to a variety of water-quality problems, including low dissolved oxygen concentrations,
    which can cause fish kills and harm other aquatic life.
    '''
    ,
    '''
    Why is water temperature important? Water temperature is a key feature of any water body.
    It changes the water’s density, the water’s ability to support life, as well as its ability to absorb gases (like CO₂), and nutrients.
    Increases in water temperature can cause some chemicals to become “soluble”:
    think how quickly salt dissolves in hot water versus cold water.
    Algae blooms and other vegetation can also grow more quickly in warmer water.
    When these blooms decompose, they reduce the total amount of dissolved oxygen in the water,
    making it difficult for fish and other aquatic critters to breath.
    '''
    ,
    '''
    Why is pH important for water quality? 
    pH stands for “potential for Hydrogen”. It is the measure of the acidity or alkalinity of water soluble substances.
    pH sets up the conditions for how easy it is for nutrients to be available and how easily things like heavy metals (toxicity for aquatic life) can dissolve in the water.
    Rivers and lakes generally range between 5 (acidic) and 9 (basic) on the pH scale.
    Whereas ocean water averages closer to 8.2 (slightly basic).
    Low pH can reduce how many fish eggs hatch and can make life difficult for fish and macroinvertebrates (the backbone of our water ecosystems).
    '''    
]

lower_subheader_names = ['How is it measured?'] * len(metric_names)
# print(lower_subheader_names)

lower_descr = [
    '''
    Ammonia is analyzed by chemical titration.
    The method used in most test kits is called the salicylate method.
    Always measure pH and temperature when you measure ammonia.
    '''
    ,
    '''
    Dissolved oxygen is measured as a concentration, in units of milligrams per litre (mg/L).
    We use the Chemetrics dissolved oxygen testkit because it is the most user friendly to conduct
    (no measuring chemicals) and easier to interpret than other tests we have tried.
    This device has been compared to professional probes with very good results.
    Full study by Carleton University to compare our kits to professional probes. 
    The inexpensive probes that we have tried were finicky and inaccurate (even with proper calibration).
    Professional probes will give you more fine-grain results, but they are thousands of dollars and require calibration really often.
    '''
    ,
    '''
    E. coli levels are measured by analyzing bacterial growth in laboratory analyses.
    This is commonly done by the membrane filter procedure, although color test kits have also been EPA-approved.
    Care must be taken when collecting water samples because all of the sampling containers must be sterile.
    '''
    ,
    '''
    The EPA-approved method for measuring total orthophosphate is known as the ascorbic acid method.
    Briefly, a reagent (either liquid or powder) containing ascorbic acid and ammonium molybdate
    reacts with orthophosphate in the sample to form a blue compound.
    '''
    ,
    '''
    Water temperature is measured in degrees with a digital or analog thermometer.
    Make sure the thermometer is submerged at least 10 cm from the surface of the water.
    Hold under the water for 5 minutes. You will know it is ready when the temperature has remained
    the same for at least 30 seconds.
    '''
    ,
    '''
    pH is measured on a logarithmic scale from 0-14, with 7 indicating neutral water.
    There are many tools for measuring pH, from expensive digital probes to easy to use test strips.
    We use test strips for pH. We have compared 15 types of test strips, and those made by Taylor have been shown to be the most accurate.
    For those looking for more accuracy, inexpensive pen-style meters have proven to be very accurate,
    but they need to be calibrated at least once a week. We have tried this one and it works well
    (however, you need to be careful not to dunk it too far in the water).
    '''
]

display_dict_upper = {}
display_dict_lower = {}

for m, t, descr in  zip(metric_names, subheader_names, upper_descr):
    display_dict_upper[m] = [t, descr]

for m, t, descr in zip(metric_names, lower_subheader_names, lower_descr):
    display_dict_lower[m] = [t, descr]


#title of the main page
st.title('ELA DASHBOARD 📊')
st.caption('Source: ACAP St. John')

# creating the sidebar which contains diff filters
# --- SIDEBAR ---
# st.sidebar.title("Visualization Filters 👇🏾")
st.sidebar.header("Please Filter here 👇🏾")
choose_visual = st.sidebar.selectbox(
    'Visuals:',
    (
        'Line Graph',
        'Bar Graph',
        'Scatter Plot'
    )
) 

if choose_visual == 'Line Graph':
    values_body = list(df_pvt.MonitoringLocationName.unique())
    
    choose_body = st.sidebar.multiselect('Choose water bodies:',
                                 values_body,
                                 df_pvt.MonitoringLocationName.unique()[2:5])
    
    df_pvt_filtered = df_pvt['MonitoringLocationName'].isin(choose_body)
    df_line = df_pvt[df_pvt_filtered]
    
    values_measure = list(df_pvt.columns[2:-3])
    choose_measure = st.sidebar.selectbox('Choose the trend you would like to look at:',
                                          values_measure
    )

    for k, v in display_dict_upper.items():
        if choose_measure == k:
            st.subheader(v[0])
            st.markdown(v[1])
    
    
    
        
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
        
        with col1:
            st.metric(f'Max {choose_measure}: ', round(df_line[choose_measure].max(),4))
            st.metric(f'Min {choose_measure}: ', round(df_line[choose_measure].min(),4))
            # st.subheader('Table: ')
            # df_line[['MonitoringLocationName', 'ActivityStartDate', choose_measure]]
            
        with col2:
            st.markdown(f'Name of water body: ')
            try:
                if len(choose_body) <= 3:
                    for w in choose_body:
                        st.text(w)
                
                else:
                    st.text('Check legend below ⬇️')
            except IndexError:
                st.text('Please pick a water body!')
            
            st.metric(f'Mean {choose_measure}: ', round(df_line[choose_measure].mean(),4))
            st.metric(f'Median {choose_measure}: ', round(df_line[choose_measure].median(),4))
            
        
        fig = px.line(df_line,
            x="ActivityStartDate",
            y=choose_measure,
            color='MonitoringLocationName',
            title=f'Trend of {choose_measure} over the years')
        
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
        
        st.plotly_chart(fig)
        
        
    
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
    
#     if choose_measure == 'Temperature, water':
#         st.subheader('How do you measure water temperature?')
#         st.markdown("""
# Water temperature is measured in degrees with a digital or analog thermometer. Make sure the thermometer is submerged at least 10 cm from the surface of the water. Hold under the water for 5 minutes. You’ll know it’s ready when the temperature has remained the same for at least 30 seconds.
#                     """)

    for k, v in display_dict_lower.items():
        if choose_measure == k:
            st.subheader(v[0])
            st.markdown(v[1])
    
if choose_visual == 'Bar Graph':
    choose_bar_measure = st.sidebar.selectbox('Choose the trend you would like to look at on the bar graph:',
                                          tuple(df_pvt.columns[2:-3])
    )
    
    for k, v in display_dict_upper.items():
        if choose_bar_measure == k:
            st.subheader(v[0])
            st.markdown(v[1])
    
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
    
    # df_bar
    
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
        title_font=dict(size=20),
        yaxis_title_font=dict(size=20),
        xaxis_title_font=dict(size=20)
    )

    # Show the plot
    st.plotly_chart(fig)
    
    for k, v in display_dict_lower.items():
        if choose_bar_measure == k:
            st.subheader(v[0])
            st.markdown(v[1])
    
if choose_visual == 'Scatter Plot':
    st.header('What are Scatter Plots for?')
    st.markdown(
    """
    The primary use of Scatter Plots are to observe and show relationships between two numeric variables. 
    The dots in a scatter plot not only report the values of individual data points,
    but also patterns when the data are taken as a whole. Identification of correlational relationships
    are common with scatter plots. In these cases, we want to know, if we were given a particular horizontal value,
    what a good prediction would be for the vertical value. You will often see the variable on the horizontal axis denoted
    an independent variable, and the variable on the vertical axis the dependent variable. Relationships between variables
    can be described in many ways: positive or negative, strong or weak, linear or nonlinear.
    """
        
    )
    # df_pvt
    
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
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df_pvt[choose_x],
                y=df_pvt[choose_y],
                mode='markers',
                marker=dict(symbol='diamond')
            )
        )

        fig.update_layout(
            title=f'Correlation between {choose_x} and {choose_y}',
            width=800,
            height=500,
            xaxis_title=choose_x,
            yaxis_title=choose_y,
            font=dict(size=15),
        )

        st.plotly_chart(fig)
        
        # fig, ax  = plt.subplots(figsize=(12,5), dpi=150)
        # sns.scatterplot(data = df_pvt,
        #                     x=df_pvt[choose_x],
        #                     y=df_pvt[choose_y])
        
        # st.pyplot(fig)
        
    
    else:
        choose_body = st.sidebar.selectbox('Choose the body of water: ',
                                           tuple(df_pvt.MonitoringLocationName.unique())
                                           )
        
        # fig, ax  = plt.subplots(figsize=(12,5), dpi=150)
        # sns.scatterplot(data = df_pvt[df_pvt.MonitoringLocationName == choose_body],
        #                     x=choose_x,
        #                     y=choose_y)
        
        # ax.set_title(f'Scatterplot showing correlation between {choose_x} and {choose_y} in {choose_body}',
        #              fontsize=15)
        
        # ax.set_xlabel(f'{choose_x}',
        #               fontsize=15)
        
        # ax.set_ylabel(f'{choose_y}',
        #               fontsize=15)
        
        # st.pyplot(fig)
        # Assuming you have a DataFrame df_pvt and variables choose_x, choose_y, choose_body
        filtered_df = df_pvt[df_pvt['MonitoringLocationName'] == choose_body]

        fig = px.scatter(
            filtered_df,
            x=choose_x,
            y=choose_y,
            title=f'Scatterplot showing correlation between {choose_x} and {choose_y} in {choose_body}',
        )

        fig.update_layout(
            xaxis_title=choose_x,
            yaxis_title=choose_y,
            font=dict(size=15),
            width=800,
            height=500,
        )

        st.plotly_chart(fig)
        
        # fig2 = sns.heatmap(df_pvt[df_pvt.MonitoringLocationName == choose_body].corr())
        # st.pyplot(fig2)
        
        
    
    
    
    






