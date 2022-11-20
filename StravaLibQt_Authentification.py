from stravalib.client import Client

from PySide2.QtCore import QUrl
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtWebEngineWidgets import QWebEngineView
import pickle

import sys
from os import path
import time


class LogInStravaWindow(QMainWindow):
    def __init__(self, client_strava_class_id, client_class_secret):
        super(LogInStravaWindow, self).__init__()
        self.client = Client()
        self.client_strava_id = client_strava_class_id
        self.client_strava_secret = client_class_secret
        self.browser = QWebEngineView()
        url = self.get_authentification_url()
        self.browser.setUrl(QUrl(url))
        self.setCentralWidget(self.browser)
        self.browser.urlChanged.connect(self.url_changed)

    def url_changed(self):
        """Parse returned url after login and use code to get access token.."""
        if self.browser.url().toString().find('code=') != -1:
            code = self.browser.url().toString().split('&')[1].split('=')[1]

            access_token = self.client.exchange_code_for_token(client_id=self.client_strava_id,
                                                               client_secret=self.client_strava_secret, code=code)
            pickle.dump(access_token, open("access_token.acs", "wb"))
            # print(access_token)
            # print(code)
            self.close()

    def get_authentification_url(self):
        """Just to make sure you supplied access token ..."""
        if self.client_strava_id != 0:
            url = self.client.authorization_url(client_id=self.client_strava_id,
                                                redirect_uri='http://127.0.0.1:5000/authorization',
                                                scope=['read_all', 'profile:read_all', 'activity:read_all'])
        else:
            url = ''

        return url


def refresh_access_token(client_id, client_sec):
    """Refresh access token if necesary and return client"""
    if not path.exists("access_token.acs"):
        app = QApplication(sys.argv)
        window = LogInStravaWindow(client_id, client_sec)
        window.show()
        app.exec_()

    # start main app loop for activity monitoring ...
    my_access_token = pickle.load(open("access_token.acs", "rb"))
    #print(my_access_token)
    client = Client(access_token=my_access_token['access_token'])
    client.access_token = my_access_token['access_token']
    client.refresh_token = my_access_token['refresh_token']
    client.token_expires_at = my_access_token['expires_at']
    # refresh access token from strava ...
    if time.time() > client.token_expires_at:
        my_access_token = client.refresh_access_token(client_id=client_id, client_secret=client_sec,
                                                      refresh_token=my_access_token['refresh_token'])
        pickle.dump(my_access_token, open("access_token.acs", "wb"))
    return client