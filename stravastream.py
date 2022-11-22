##########################################
######### TEST DASHBOARD #################
##########################################

import polyline
import numpy as np
import pandas as pd
import streamlit as st
import requests

st.set_page_config("Your Strava Analysis",
                    "🚴‍♂️",
                    "wide")

###################
## Authorisation ##
###################

client_id = st.secrets['client_id']
client_secret = st.secrets['client_secret']
redirect_url = st.secrets['redirect_url']

request_url = f'http://www.strava.com/oauth/authorize?client_id={client_id}' \
                  f'&response_type=code&redirect_uri={redirect_url}' \
                  f'&approval_prompt=force' \
                  f'&scope=profile:read_all,activity:read_all'

st.image('https://i2.wp.com/bikewalkwichita.org/wp-content/uploads/2020/03/strava-logo-png-4.png?fit=1200%2C1198&ssl=1'
        , width=200)
st.header('Custom Strava Dashboard')                  

link = f'[Click here to authorise]({request_url})'
st.markdown(link)

##############
## Get Data ##
##############

if st.button("Get Data"):

    # create empty container for the dashboard
    placeholder = st.empty()

    with placeholder.container():

        code = st.experimental_get_query_params()["code"][0]

        if 'code' not in st.session_state:
            st.session_state['code'] = code

        url = 'https://www.strava.com/oauth/token'
        r = requests.post(url,  data={'client_id': client_id,
                                'client_secret': client_secret,
                                'code': code,
                                'grant_type': 'authorization_code'})

        access_token = r.json()['access_token']
        refresh_token = r.json()['refresh_token']
        expires_at = r.json()['expires_at']

        r = requests.get(f"http://www.strava.com/api/v3/athlete/activities?access_token={access_token}")

        df = pd.json_normalize(r.json())
        #df = pd.read_csv("https://raw.githubusercontent.com/dougaltoms/stravastream/main/test.csv")

        # dashboard title
        st.title("Real-time Strava Analysis")

        # set filter
        name_filter = st.selectbox("Select activity", df['name'], key='name_filter')

        if 'name_filter' not in st.session_state:
            st.session_state.name_filter = name_filter

        # create empty container for the dashboard
        placeholder = st.empty()

        # df where 'name' == chosen name
        df = df[df["name"] == st.session_state.name_filter]

        # create key metric from chosen activity
    
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

        # # some basic plots
        # fig_col1 = st.columns(1)

        # with fig_col1:
        #     st.markdown("## Map")
        #     pline=df['map'][1]['summary_polyline']
        #     map_coords = polyline.decode(pline)
        #     map_df = pd.DataFrame(map_coords, columns =['lat', 'lon'])
        #     st.map(map_df)

 
