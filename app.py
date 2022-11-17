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

auth_url = "https://www.strava.com/oauth/token"
payload = {
    "client_id":st.secrets["client_id"],
    "client_secret":st.secrets["client_secret"],
    "refresh_token":st.secrets["refresh_token"],
    "grant_type":"refresh_token",
    "f":"json"
}

r = requests.post(auth_url, data=payload, verify=False)
access_token = r.json()['access_token']

#################
## get_request ##
#################

def get_request(endpoint):

    import requests

    url = f"https://www.strava.com/api/v3/{endpoint}"
    r = requests.get(url + '?access_token=' + access_token)

    r = r.json()

    return r

def get_name(activity_id):

    r = get_request(f'activities/{activity_id}')
    athlete = r['athlete']

    r = get_request(athlete)
    firstname = r['firstname']
    lastname = r['lastname']
    name = firstname + " " + lastname

    return name


with st.form("my_form"):
   activity = st.text_input("Paste Strava activity URL here:")

   # Every form must have a submit button.
   submitted = st.form_submit_button("Get data")

   if submitted:
        url_list = activity.split('https://www.strava.com/activities/')
        activity_id = url_list[1]

        st.write("Hello, ", get_name(activity_id))

        r = get_request(f'activities/{activity_id}')

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
