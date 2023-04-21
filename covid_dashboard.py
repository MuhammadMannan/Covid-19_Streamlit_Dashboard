import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="COVID-19 World Wide Dashboard 🦠")
st.markdown("# Covid-19 World Wide Dashboard 🦠")
st.markdown("### Created by Muhammad Mannan")
st.markdown("### CSSE Major at The Univeristy of Washington Bothell")
st.write("This is a web-based dashboard that provides a visual representation of COVID-19 data worldwide. It is built using Streamlit, a Python library for creating interactive web applications, and Plotly, a Python graphing library for creating interactive plots and charts.")
# Load data from CSV file
df = pd.read_csv('covid_data.csv')  # Replace 'covid_data.csv' with your own CSV file name

# Assuming the CSV file has the following columns: 'Country/Region', 'Confirmed', 'Deaths', 'Recovered'
# Create sidebar element for country filtering with default value set to "All Countries"
selected_regions = st.sidebar.multiselect('Select Region(s)', ['All Regions'] + list(df['WHO Region'].unique()), default='All Regions')

# Create sidebar element for country filtering with default value set to "All Countries"
selected_countries = st.sidebar.multiselect('Select Countries', ['All Countries'] + list(df['Country/Region'].unique()), default='All Countries')

# Filter data based on selected countries
if 'All Countries' in selected_countries and 'All Regions' in selected_regions:
    filtered_df = df
elif 'All Countries' in selected_countries:
    filtered_df = df[df['WHO Region'].isin(selected_regions)]
elif 'All Regions' in selected_regions:
    filtered_df = df[df['Country/Region'].isin(selected_countries)]
else:
    filtered_df = df[df['Country/Region'].isin(selected_countries) & df['WHO Region'].isin(selected_regions)]

# Calculate total cases, deaths, and recoveries
total_cases = filtered_df['Confirmed'].sum()
total_deaths = filtered_df['Deaths'].sum()
total_recovered = filtered_df['Recovered'].sum()

# Calculate percentages
percent_deaths = (total_deaths / total_cases) * 100
percent_recovered = (total_recovered / total_cases) * 100
percent_unknown = ((total_cases - (total_deaths +total_recovered)) / total_cases) * 100

# Create donut chart for percentage representation of deaths and recoveries
fig_donut = go.Figure(go.Pie(
    labels=['Deaths', 'Recovered', 'Uknown'],
    values=[percent_deaths, percent_recovered, percent_unknown],
    hole=0.5,
    marker_colors=['#d62728', '#2ca02c']
))

# Create a two-column layout for table and bar chart
col1, col2 = st.columns(2)

# Create table to display country-wise data with scrollbar
with col1:
    st.write('**Country-wise COVID-19 Data**')
    table_height = min(500, filtered_df.shape[0] * 25 + 25)  # Set max height of table to 500 pixels
    filtered_df_table = filtered_df[['Country/Region', 'Confirmed', 'Deaths', 'Recovered','WHO Region']]
    st.write(filtered_df_table.style.set_properties(**{'max-height': f'{table_height}px' ,'overflow-y': 'scroll'}))

# Create a bar chart for confirmed cases by country
with col2:
    fig_donut = go.Figure(go.Pie(
    labels=['Deaths', 'Recovered', 'Uknown'],
    values=[percent_deaths, percent_recovered, percent_unknown],
    hole=0.5,
    marker_colors=['#d62728', '#2ca02c']
))

    fig_donut.update_traces(textinfo='percent+label')

    st.plotly_chart(fig_donut, use_container_width=True)

# Create a two-column layout for heatmap and donut chart
col3, col4 = st.columns(2)
# Create map figure using Plotly
fig = px.choropleth(df, 
                    locations='Country/Region', 
                    locationmode='country names', 
                    color='Confirmed', 
                    hover_name='Country/Region', 
                    hover_data=['Confirmed', 'Deaths', 'Recovered'],
                    color_continuous_scale='YlOrRd', 
                    title='COVID-19 Confirmed Cases by Country')

# Update the layout of the map
fig.update_geos(projection_type='natural earth', 
               showcountries=True, 
               countrycolor='black', 
               showcoastlines=True, 
               coastlinecolor='white', 
               showland=True, 
               landcolor='lightgray', 
               showocean=True, 
               oceancolor='lightblue')
st.plotly_chart(fig, use_container_width=True)

fig_bar_confirmed = go.Figure(go.Bar(
        x=filtered_df['Country/Region'],
        y=filtered_df['Confirmed'],
        text=filtered_df['Confirmed'],
        textposition='inside',
        marker_color='#1f77b4',
        hovertemplate='Country: %{x}<br>' +
                      'Confirmed Cases: %{y}<br>' +
                      '<extra></extra>',
    ))
fig_bar_confirmed.update_xaxes(title='Country')
fig_bar_confirmed.update_yaxes(title='Confirmed Cases')
fig_bar_confirmed.update_layout(title='COVID-19 Confirmed Cases by Country (Bar Chart)', height=500)

st.plotly_chart(fig_bar_confirmed, use_container_width=True)

# Create a heatmap for confirmed cases by country
fig_heatmap = go.Figure(go.Heatmap(
    x=filtered_df['Country/Region'],
    y=['Confirmed Cases'],
    z=[filtered_df['Confirmed']],
    colorscale='YlOrRd',
    hovertemplate='Country: %{x}<br>' +
                  'Confirmed Cases: %{z}<br>' +
                  '<extra></extra>',
))
fig_heatmap.update_xaxes(title='Country')
fig_heatmap.update_yaxes(visible=True)
fig_heatmap.update_layout(title='COVID-19 Confirmed Cases by Country (Heatmap)', height=600)

fig_bar_deaths = go.Figure(go.Bar(
        x=filtered_df['Country/Region'],
        y=filtered_df['Deaths'],
        text=filtered_df['Deaths'],
        textposition='inside',
        marker_color='red',
        hovertemplate='Country: %{x}<br>' +
                      'Confirmed Cases: %{y}<br>' +
                      '<extra></extra>',
    ))
fig_bar_deaths.update_xaxes(title='Country')
fig_bar_deaths.update_yaxes(title='Deaths')
fig_bar_deaths.update_layout(title='COVID-19 Death Cases by Country (Bar Chart)', height=500)

fig_bar_recovered = go.Figure(go.Bar(
        x=filtered_df['Country/Region'],
        y=filtered_df['Recovered'],
        text=filtered_df['Recovered'],
        textposition='inside',
        marker_color='green',
        hovertemplate='Country: %{x}<br>' +
                      'Recovered Cases: %{y}<br>' +
                      '<extra></extra>',
    ))
fig_bar_recovered.update_xaxes(title='Country')
fig_bar_recovered.update_yaxes(title='Recovered Cases')
fig_bar_recovered.update_layout(title='COVID-19 Recovered Cases by Country (Bar Chart)', height=500)

# Create a grid layout with 2 columns and 3 rows
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# Add the visualizations to the grid layout
col3.plotly_chart(fig_bar_deaths, use_container_width=True)
col4.plotly_chart(fig_bar_recovered, use_container_width=True)
