import streamlit as st
import pandas as pd
import json
from code.data_reader import transform_data
from code.viz import *

st.set_page_config(layout='wide', page_title='Data Cleaner', page_icon='app/static/hlogo.png')

# Title
st.title("Hinge Data Analyzer")

# File uploader
uploaded_file = st.file_uploader("Upload Your Matches File Here", type=['json'])

# Check if a file has been uploaded
if uploaded_file:
    # Load the json file from the uploaded file object
    data = json.load(uploaded_file)

    # Call transform data which converts loaded data into clean dataframe
    df = transform_data(data)
      
    # Subheader
    st.subheader('Data Visualizations')

    # Graph selection dropdown
    graph_selection = st.selectbox('Filter Graphs', ['Main', 'Likes and Matches', 'Messages', 'Voice Notes', 'All'])

    # Create two columns for better viewing
    col1, col2 = st.columns(2)

    # Display graphs based on selection 
    if graph_selection == 'Main':
        with col1:
            main_stats(df)
        with col2:
            plot_sankey(df)
            plot_matches_over_time(df)

    if graph_selection == 'All' or graph_selection == 'Messages':
        with col1:
            plot_message_distribution(df)
            plot_avg_time_between_messages(df)
            plot_corr_messages_and_avg_time(df)

        with col2:
            plot_avg_message_length(df)
            plot_time_between_first_and_last_message(df)
        
    if graph_selection == 'All' or graph_selection == 'Likes and Matches':
        with col1:
            plot_time_between_like_and_match(df)
            plot_matches_by_weekday(df)

        with col2:
            plot_matches_over_time(df)
            plot_matches_by_time(df)
            plot_sankey(df)
            
    if graph_selection == 'All' or graph_selection == 'Voice Notes':
        with col1:
            plot_voice_notes_sent(df)

    if graph_selection == 'All':
        main_stats(df)

    # Allow users to view dataframe with dropdown
    with st.expander("Data"):
        st.write("Note: Data provided for a received like is limited.")
        st.dataframe(df)


