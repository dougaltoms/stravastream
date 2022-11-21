import streamlit as st
import requests
import pandas as pd
import polyline

client_id = st.secrets['client_id']
client_secret = st.secrets['client_secret']
redirect_url = st.secrets['redirect_url']

request_url = f'http://www.strava.com/oauth/authorize?client_id={client_id}' \
                  f'&response_type=code&redirect_uri={redirect_url}' \
                  f'&approval_prompt=force' \
                  f'&scope=profile:read_all,activity:read_all'

st.image('https://i2.wp.com/bikewalkwichita.org/wp-content/uploads/2020/03/strava-logo-png-4.png?fit=1200%2C1198&ssl=1'
        , width=250)
st.header('Custom Strava Dashboard')                  

link = f'[Click here to authorise]({request_url})'
st.markdown(link)

##################
## Show summary ##
##################

if st.button("Get Data"):

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

    if 'access_token' not in st.session_state:
        st.session_state['access_token'] = access_token

    if 'refresh_token' not in st.session_state:
        st.session_state['refresh_token'] = refresh_token

    if 'expires_at' not in st.session_state:
        st.session_state['expires_at'] = expires_at

    firstname = r.json()['athlete']['firstname']
    lastname = r.json()['athlete']['lastname']
    fullname = firstname + " " + lastname

    st.header(f"Hello, {fullname}")

    r = requests.get(f"http://www.strava.com/api/v3/athlete/activities?access_token={access_token}")

    df = pd.DataFrame(r.json())
    #df_display = df[['name', 'distance', 'moving_time', 'total_elevation_gain','sport_type']]
    df_display = df[['name', 'id']]
    df_display = df_display.set_index("name")

    selected = st.multiselect("Choose activity: ", list(df_display.index))

    display = df_display.loc[selected]
    st.dataframe(display)

    # if 'selected' not in st.session_state:
    #     st.session_state.selected = selected

    # # df_display['distance'] = round(df_display['distance']/1000,2)
    # # df_display['total_elevation_gain'] = round(df_display['total_elevation_gain'],2)
    # # df_display['moving_time'] = df_display['moving_time']/60

    # ########################
    # ## Display 1 activity ##
    # ########################
    # with st.form("activity_form"):

    #     submit = st.form_submit_button("Get activity data")

    #     if submit:

    #         activity = df_display.loc[st.session_state.selected]
    #         activity_id = df_display['id']

    #         r = requests.get(f"http://www.strava.com/api/v3/activities/{activity_id}?access_token={[st.session_state.access_token]}")
    #         map_polyline = r.json()['map']['polyline']
    #         map_coords = polyline.decode(map_polyline)
    #         map_df = pd.DataFrame(map_coords, columns =['lat', 'lon'])
    #         st.map(map_df)

