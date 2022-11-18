# Streamlit app

import streamlit as st
import pandas as pd
import requests
import polyline


st.image('https://i2.wp.com/bikewalkwichita.org/wp-content/uploads/2020/03/strava-logo-png-4.png?fit=1200%2C1198&ssl=1'
        , width=250)
st.header('Analyse your Strava activity')

###################
## Authorisation ##
###################

client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]
redirect_uri = r'https://stravastream.streamlit.app/'

request_url = f'http://www.strava.com/oauth/authorize?client_id={client_id}' \
                  f'&response_type=code&redirect_uri={redirect_uri}' \
                  f'&approval_prompt=force' \
                  f'&scope=profile:read_all,activity:read_all'

link = f'[Click here to authorise]({request_url})'
st.markdown(link, unsafe_allow_html=True)

#################
## get_request ##
#################

# def get_request(endpoint):

#     import requests

#     url = f"https://www.strava.com/api/v3/{endpoint}"
#     r = requests.get(url + '?access_token=' + access_token)

#     r = r.json()

#     return r

with st.form("my_form"):
   url = st.text_input("Paste url here:")
   link = f'[Click here to authorise]({request_url})'
   st.markdown(link, unsafe_allow_html=True)

   # Every form must have a submit button.
   submitted = st.form_submit_button("Get data")

   if submitted:

        code = url.split('https://stravastream.streamlit.app/?state=&code=')
        code = code[1]
        code = code[0:40]

        st.text(code)

        tokens = requests.post(url='https://www.strava.com/oauth/token',
                       data={'client_id': client_id,
                             'client_secret': client_secret,
                             'code': code,
                             'grant_type': 'authorization_code'})

        strava_tokens = tokens.json()
        st.json(strava_tokens)

        ###################
        ## Get User Info ##
        ###################

        firstname = strava_tokens['athlete']['firstname']
        lastname = strava_tokens['athlete']['lastname']
        name = firstname + " " + lastname

        profile_pic = strava_tokens['athlete']['profile']

        st.write("Hello, ", name), st.image(profile_pic, width=250)

        # r = get_request(f'activities/{activity_id}')

        # df = pd.DataFrame.from_dict(r, orient="index")
        # df=df.transpose()
        # df=df.loc[:,"name":"sport_type"]
        # df['distance'] = df['distance']/1000
        # df['moving_time'] = df['moving_time']/60
        # df['elapsed_time'] = df['elapsed_time']/60

        # pline = r['map']['polyline']
        # map_coords = polyline.decode(pline)
        # map_df = pd.DataFrame(map_coords, columns =['lat', 'lon'])

        # title = r["name"]
        # distance = str(round((r['distance']/1000),2))
        # speed = str(round((r['distance']/1000)/((r['elapsed_time']/60)/60)))
        # st.header(title)
        # st.text('Distance: '+ distance)
        # st.text('Average speed (km/h): '+ speed)
        # st.map(map_df)
        # st.dataframe(df)
