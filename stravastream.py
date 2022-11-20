import streamlit as st
import requests
import pandas as pd
import polyline

client_id = st.secrets('client_id')
client_secret = st.secrets('client_secret')
redirect_url = st.secrets('redirect_url')

request_url = f'http://www.strava.com/oauth/authorize?client_id={client_id}' \
                  f'&response_type=code&redirect_uri={redirect_url}' \
                  f'&approval_prompt=force' \
                  f'&scope=profile:read_all,activity:read_all'

link = f'[Click here to authorise]({request_url})'
st.markdown(link)

with st.form("We need your access token"):

    code = st.text_input('Copy & Paste auth token here')
    authorise = st.form_submit_button('Submit')

    if authorise:

        url = 'https://www.strava.com/oauth/token'
        r = requests.post(url,  data={'client_id': client_id,
                             'client_secret': client_secret,
                             'code': code,
                             'grant_type': 'authorization_code'})

        token = r.json()['access_token']

        st.text('Successfully Authorised')

#####################
## Generate Client ##
#####################
