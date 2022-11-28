import streamlit as st
import pandas as pd
import time
from stravalib.client import Client

st.set_page_config("Your Strava Analysis",
                    "🚴‍♂️",
                    "wide")

st.image('https://i2.wp.com/bikewalkwichita.org/wp-content/uploads/2020/03/strava-logo-png-4.png?fit=1200%2C1198&ssl=1'
        , width=200)
st.header('Custom Strava Dashboard')     

# ###################
# ## Authorisation ##
# ###################

CLIENT_ID = st.secrets['client_id']
CLIENT_SECRET = st.secrets['client_secret']
REDIRECT_URL = st.secrets['redirect_url']

client = Client()

def auth_url():

    auth_url = client.authorization_url(client_id=CLIENT_ID,
                            redirect_uri=REDIRECT_URL,
                            scope=["read_all", "profile:read_all", "activity:read_all"])

    return auth_url

auth_url = auth_url()
  
link = f'[Click here to authorise]({auth_url})'
st.markdown(link)

def main():
    
    get_data = st.button("Get data")

    if get_data:
        stravastream()
        get_data = False

def stravastream():

    @st.experimental_memo
    def get_access_token():

        code = st.experimental_get_query_params()["code"][0]
        access_token = client.exchange_code_for_token(CLIENT_ID, CLIENT_SECRET, code)

        return access_token

    access_token = get_access_token()

    @st.experimental_memo
    def check_expiry(access_token):

        if time.time() > access_token['expires_at']:
            refresh_response = client.refresh_access_token(CLIENT_ID, CLIENT_SECRET, access_token['refresh_token'])
            access_token = refresh_response

            client.access_token = refresh_response['acess_token']
            client.refresh_token = refresh_response['refresh_token']
            client.token_expires_at = refresh_response['expires_at']

            if 'access_token' not in st.session_state:
                st.session_state['access_token'] = client.access_token
            if 'refresh_token' not in st.session_state:
                st.session_state['refresh_token'] = client.refresh_token
            if 'token_expires_at' not in st.session_state:
                st.session_state['token_expires_at'] = client.token_expires_at

        else:
            client.access_token = access_token['access_token']
            client.refresh_token = access_token['refresh_token']
            client.token_expires_at = access_token['expires_at'] 

            if 'access_token' not in st.session_state:
                st.session_state['access_token'] = client.access_token
            if 'refresh_token' not in st.session_state:
                st.session_state['refresh_token'] = client.refresh_token
            if 'token_expires_at' not in st.session_state:
                st.session_state['token_expires_at'] = client.token_expires_at

    check_expiry(access_token)

    @st.experimental_singleton
    def athlete():
        athlete = client.get_athlete()
        return "Hello, {} {}".format(athlete.firstname, athlete.lastname)

    greeting = athlete()
    st.write(greeting)

if __name__ == "__main__":
    main()




