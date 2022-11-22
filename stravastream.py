##########################################
######### TEST DASHBOARD #################
##########################################

import time
import polyline
import numpy as np
import pandas as pd
import streamlit as st

df = pd.read_csv("https://raw.githubusercontent.com/dougaltoms/stravastream/main/test.csv")

st.set_page_config("Your Strava Analysis",
                    "🚴‍♂️",
                    "wide")

# read csv from url and store in st memory
# @st.experimental_memo
# def get_data():
#      return pd.read_csv(data_link)

# df = get_data()

# dashboard title
st.title("Real-time Strava Analysis")

# set filter
name_filter = st.selectbox("Select activity", df['name'])

# create empty container for the dashboard
placeholder = st.empty()

# df where 'name' == chosen name
df = df[df["name"] == name_filter]

# create key metric from chosen activity
with placeholder.container():
    
    col1, col2 = st.columns(2)

    col1.metric(
        label="Distance (km)",
        value = round(df['distance'].loc[df.index[0]]/1000,2),
        delta = 100-round(df['distance'].loc[df.index[0]]/1000,2)
    )

    col2.metric(
        label="Time (mins)",
        value = round(df['moving_time'].loc[df.index[0]]/60,2),
        delta = 100-round(df['moving_time'].loc[df.index[0]]/1000,2)
    )

    # some basic plots
    fig_col1 = st.columns(1)

    # with fig_col1:
    #     st.markdown("## Map")
    #     pline=df['map'][1]['summary_polyline']
    #     map_coords = polyline.decode(pline)
    #     map_df = pd.DataFrame(map_coords, columns =['lat', 'lon'])
    #     st.map(map_df)

# # real-time (ish) updates using for loop
# for seconds in range(200):

