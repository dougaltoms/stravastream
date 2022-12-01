import urllib
import requests
import streamlit as st


def get_authorization_url():
    """Generate authorization URL"""
    
    params = {
        "client_id": st.secrets['client_id'],
        "response_type": "code",
        "redirect_uri": st.secrets['redirect_url'],
        "scope": "read,profile:read_all,activity:read",
        "approval_prompt": "force"
    }

    values_url = urllib.parse.urlencode(params)
    base_url = 'https://www.strava.com/oauth/authorize'
    url = base_url + '?' + values_url

    return url


def get_refresh_token_and_access_token(auth_code):
    """POST request to retrieve refresh_token and access_token"""
    params = {
        "client_id": st.secrets['client_id'],
        "client_secret": st.secrets['client_secret'],
        "code": auth_code,
        "grant_type": "authorization_code"
    }

    values_url = urllib.parse.urlencode(params)
    base_url = 'https://www.strava.com/oauth/token'
    url = base_url + '?' + values_url

    return requests.post(url).json()


def get_athlete_activities(access_token, per_page=200, before=""):

    """GET request to retrieve athlete activities"""
    if before == "":
        params = {
            "access_token": access_token,
            "per_page": per_page
        }
    else:
        params = {
            "access_token": access_token,
            "before": before,
            "per_page": per_page
        }

    values_url = urllib.parse.urlencode(params)
    base_url = 'https://www.strava.com/api/v3/athlete/activities'
    url = base_url + '?' + values_url

    return requests.get(url).json()