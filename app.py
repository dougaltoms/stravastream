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
api_url = r'https:www.strava.com/api/v3/'

request_url = f'http://www.strava.com/oauth/authorize?client_id={client_id}' \
                  f'&response_type=code&redirect_uri={redirect_uri}' \
                  f'&approval_prompt=force' \
                  f'&scope=profile:read_all,activity:read_all'

# with st.form("authorise_form"):

#     link = f'[Click here to authorise]({request_url})'
#     authorise = st.form_submit_button(link)

#     authorisation_code = '7e5eb812c34ab7351ff68c75b3a0833cfbb3599c'

#     if authorise:
#         response = requests.post(
#         url="https://www.strava.com/oauth/token",
#         json={
#             "client_id": client_id,
#             "client_secret": client_secret,
#             "code": authorisation_code,
#             "grant_type": "authorization_code",
#         }
#     )
#         # r = requests.post('request_url
#         #     )

    


# st.markdown(link, unsafe_allow_html=True)


code = '7e5eb812c34ab7351ff68c75b3a0833cfbb3599c'

tokens = requests.post(url='https://www.strava.com/oauth/token',
               data={'client_id': client_id,
                     'client_secret': client_secret,
                     'code': code,
                     'grant_type': 'authorization_code'})

strava_tokens = tokens.json()

with st.form("my_form"):
   #url = st.text_input("Paste authorisation url here:")
   activity= st.text_input("Paste activity url here:")
   # Every form must have a submit button.
   submitted = st.form_submit_button("Get data")

   if submitted:

        # code = url.split('https://stravastream.streamlit.app/?state=&code=')[1]
        # code = code[0:40]

        # tokens = requests.post(url='https://www.strava.com/oauth/token',
        #                data={'client_id': client_id,
        #                      'client_secret': client_secret,
        #                      'code': code,
        #                      'grant_type': 'authorization_code'})

        # strava_tokens = tokens.json()
        requests.get

        ###################
        ## Get User Info ##
        ###################

        firstname = strava_tokens['athlete']['firstname']
        lastname = strava_tokens['athlete']['lastname']
        name = firstname + " " + lastname

        profile_pic = strava_tokens['athlete']['profile']

        st.write("Hello, ", name), st.image(profile_pic, width=250)

        ######################
        ## Display Activity ##
        #####################

        activity_id = activity.split("https://www.strava.com/activities/")[1]
        r = requests.get(f"{api_url}activities/{activity_id}")
        df = pd.DataFrame.from_dict(r, orient="index")
        df=df.transpose()
        df=df.loc[:,"name":"sport_type"]
        df['distance'] = df['distance']/1000
        df['moving_time'] = df['moving_time']/60
        df['elapsed_time'] = df['elapsed_time']/60

        pline = r['map']['polyline']
        map_coords = polyline.decode(pline)
        map_df = pd.DataFrame(map_coords, columns =['lat', 'lon'])

        title = r["name"]
        distance = str(round((r['distance']/1000),2))
        speed = str(round((r['distance']/1000)/((r['elapsed_time']/60)/60)))
        st.header(title)
        st.text('Distance: '+ distance)
        st.text('Average speed (km/h): '+ speed)
        st.map(map_df)
        st.dataframe(df)
