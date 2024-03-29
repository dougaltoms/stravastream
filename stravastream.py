# import streamlit as st
# import pandas as pd
# import time
# from stravalib.client import Client

# st.set_page_config("Your Strava Analysis",
#                     "🚴‍♂️",
#                     "wide")

# st.image('https://i2.wp.com/bikewalkwichita.org/wp-content/uploads/2020/03/strava-logo-png-4.png?fit=1200%2C1198&ssl=1'
#         , width=200)
# st.header('Custom Strava Dashboard')     

# # ###################
# # ## Authorisation ##
# # ###################

# CLIENT_ID = st.secrets['client_id']
# CLIENT_SECRET = st.secrets['client_secret']
# REDIRECT_URL = st.secrets['redirect_url']

# client = Client()

# def auth_url():

#     auth_url = client.authorization_url(client_id=CLIENT_ID,
#                             redirect_uri=REDIRECT_URL,
#                             scope=["read_all", "profile:read_all", "activity:read_all"])

#     return auth_url

# auth_url = auth_url()
  
# link = f'[Click here to authorise]({auth_url})'
# st.markdown(link)

# def main():
    
#     get_data = st.button("Get data")

#     if get_data:
#         stravastream()
#         get_data = False

# def stravastream():

#     ## ============================= ##
#     ## Define functions to build app ##
#     ## ============================= ##

#     @st.cache
#     def get_access_token():

#         code = st.experimental_get_query_params()["code"][0]
#         access_token = client.exchange_code_for_token(CLIENT_ID, CLIENT_SECRET, code)

#         return access_token

#     @st.cache
#     def check_expiry(access_token):

#         if time.time() > access_token['expires_at']:

#             refresh_response = client.refresh_access_token(CLIENT_ID, CLIENT_SECRET, access_token['refresh_token'])
#             access_token = refresh_response

#             client.access_token = refresh_response['acess_token']
#             client.refresh_token = refresh_response['refresh_token']
#             client.token_expires_at = refresh_response['expires_at']

#             # if 'access_token' not in st.session_state:
#             #     st.session_state['access_token'] = client.access_token
#             # if 'refresh_token' not in st.session_state:
#             #     st.session_state['refresh_token'] = client.refresh_token
#             # if 'token_expires_at' not in st.session_state:
#             #     st.session_state['token_expires_at'] = client.token_expires_at

#         else:
#             client.access_token = access_token['access_token']
#             client.refresh_token = access_token['refresh_token']
#             client.token_expires_at = access_token['expires_at'] 

#             # if 'access_token' not in st.session_state:
#             #     st.session_state['access_token'] = client.access_token
#             # if 'refresh_token' not in st.session_state:
#             #     st.session_state['refresh_token'] = client.refresh_token
#             # if 'token_expires_at' not in st.session_state:
#             #     st.session_state['token_expires_at'] = client.token_expires_at

#     @st.experimental_singleton
#     def athlete():
#         athlete = client.get_athlete()
#         return "Hello, {} {}".format(athlete.firstname, athlete.lastname)

#     @st.experimental_singleton
#     def ftp():
#         athlete = client.get_athlete()
#         ftp = athlete.ftp

#         try:

#             if int(ftp) < 300:
#                 return f"{ftp}W FTP?! Slow."

#             else:
#                 return f"{ftp}W FTP! Ok big man"
        
#         except:
#             return "Too shy to post your ftp?"


#     @st.experimental_memo
#     def activities(limit):

#         activities = client.get_activities(limit=limit)

#         cols = ['name', 'start_date_local','type', 'distance', 'moving_time', 'elapsed_time',
#          'total_elevation_gain', 'average_speed','start_latitude', 'start_longitude']
        
#         data = []

#         for activity in activities:
#             activity_dict = activity.to_dict()
#             data.append([activity.id]+[activity_dict.get(x) for x in cols])

#         cols.insert(0, 'id')

#         df = pd.DataFrame(data, columns=cols)
        
#         return df

#     ## =================================== ##
#     ## =========== Run the App =========== ##
#     ## =================================== ##

#     access_token = get_access_token()
#     st.write(access_token)
#     check_expiry(access_token)
    
#     greeting = athlete()
#     ftp_ = ftp()

#     st.header(greeting)
#     st.write(ftp_)

#     check_expiry(access_token)

#     activities_ = activities(100)
#     st.dataframe(activities_)

# if __name__ == "__main__":
#     main()

##########################################
##########################################
## ----------- WE GO AGAIN ------------ ##
##########################################
##########################################

import streamlit as st
import pandas as pd
from auth.auth import get_authorization_url, get_athlete_activities, get_refresh_token_and_access_token

st.set_page_config("Your Strava Analysis",
                    "🚴‍♂️",
                    "wide")

st.image('https://i2.wp.com/bikewalkwichita.org/wp-content/uploads/2020/03/strava-logo-png-4.png?fit=1200%2C1198&ssl=1'
        , width=200)

url = get_authorization_url()
link = f'[Click here to authorise]({url})'
st.markdown(link)

st.markdown(f'''
  <button onclick="window.location.href='{url}';">Click Here to Authorise</button>
    ''')

if "code" in st.experimental_get_query_params():

    if "df" in st.session_state:
        df = st.session_state["df"]

    else:
        code = st.experimental_get_query_params()["code"][0]
        st.experimental_set_query_params()

        if "refresh_token" in st.session_state and "access_token" in st.session_state:
            refresh_token = st.session_state["refresh_token"]
            access_token = st.session_state["access_token"]
            athlete_id = st.session_state["athlete_id"]
            athlete_fname = st.session_state["athlete_fname"]
            athlete_lname = st.session_state["athlete_lname"]
            athlete_image_url = st.session_state["athlete_image_url"]

        else:
                
            tokens = get_refresh_token_and_access_token(code)


            athlete_id = tokens["athlete"]["id"]
            athlete_fname = tokens["athlete"]["firstname"]
            athlete_lname = tokens["athlete"]["lastname"]
            athlete_image_url = tokens["athlete"]["profile"]
            refresh_token = tokens["refresh_token"]
            access_token = tokens["access_token"]

            st.session_state["athlete_id"] = athlete_id
            st.session_state["athlete_fname"] = athlete_fname
            st.session_state["athlete_lname"] = athlete_lname
            st.session_state["athlete_image_url"] = athlete_image_url
            st.session_state["refresh_token"] = refresh_token
            st.session_state["access_token"] = access_token

        st.header("Hello, {} {}!".format(athlete_fname, athlete_lname))
        st.image(athlete_image_url)
    

        with st.spinner("Please wait, retrieving your data"):

            activities = get_athlete_activities(access_token)
            st.json(activities)
