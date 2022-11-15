# Streamlit app

import streamlit as st
import pandas as pd
import requests
#import polyline


st.image('https://i2.wp.com/bikewalkwichita.org/wp-content/uploads/2020/03/strava-logo-png-4.png?fit=1200%2C1198&ssl=1'
        , width=250)
st.header('Analyse your Strava activity')

with st.form("my_form"):
   activity = st.text_input("Paste Strava activity URL here:")

   # Every form must have a submit button.
   submitted = st.form_submit_button("Get data")

   if submitted:
        url_list = activity.split('https://www.strava.com/activities/')
        activity_id = url_list[1]
        st.write("Activity ID: ", activity_id)

        # response = requests.post(
        #                 url = 'https://www.strava.com/oauth/token',
        #                 data = {
        #                         'client_id': st.secrets['client_id'],
        #                         'client_secret': st.secrets['client_secret'],
        #                         'code': st.secrets['code'], 
        #                         'grant_type': 'authorization_code'
        #                         }
        #             )
                    
        # st.text(response)

        # strava_tokens = response.json()
        # access_token = strava_tokens['access_token']

        #def get_request()

        access_token = '65208a2306120b7ddc30a0486f43dcfb2177d3ff'
        url = f"https://www.strava.com/api/v3/activities/{activity_id}"
        r = requests.get(url + '?access_token=' + access_token)
        r = r.json()

        df = pd.DataFrame.from_dict(r, orient="index")
        df=df.transpose()
        df=df.loc[:,"name":"sport_type"]
        df['distance'] = df['distance']/1000
        df['moving_time'] = df['moving_time']/60
        df['elapsed_time'] = df['elapsed_time']/60
        st.dataframe(df)
