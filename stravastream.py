import streamlit as st
import pandas as pd
import requests

st.set_page_config("Your Strava Analysis",
                    "🚴‍♂️",
                    "wide")

# ###################
# ## Authorisation ##
# ###################

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

def main():
    
    # set up side menu
    st.sidebar.title("Strava Analysis")
    get_data = st.button("Get data")

    if get_data:
        stravastream()
        get_data = False

def stravastream():

    # Load athlete data as DF using Strava API V3
    @st.experimental_memo
    def load_data():

        code = st.experimental_get_query_params()["code"][0]

        url = 'https://www.strava.com/oauth/token'
        r = requests.post(url,  data={'client_id': client_id,
                                    'client_secret': client_secret,
                                    'code': code,
                                    'grant_type': 'authorization_code'})

        access_token = r.json()['access_token']
        
        r = requests.get(f"http://www.strava.com/api/v3/athlete/activities?access_token={access_token}")

        df = pd.json_normalize(r.json())

        return df

    # Create DF to display
    st.experimental_memo
    def create_summary(df):

        try:
            df = df[['name', 'distance', 'moving_time', 'total_elevation_gain','sport_type','id']]
            df = df.set_index("name")
            df['distance'] = round(df['distance']/1000,2)
            df['total_elevation_gain'] = round(df['total_elevation_gain'],2)
            df['moving_time'] = df['moving_time'].astype('float64') 
            df['moving_time'] = pd.to_datetime(df["moving_time"], unit='m')
            df['Average Speed (kmh)'] = df['distance']/df['moving_time']

            return df
        
        except:

            return df

    df = load_data()
    summary = create_summary(df)

    st.dataframe(summary)

if __name__ == "__main__":
    main()