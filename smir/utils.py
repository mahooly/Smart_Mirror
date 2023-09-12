import os
import pickle

import httplib2
from django.contrib.auth.models import User
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client import client

from Smart_Mirror.settings import BASE_DIR
from smir.models import UserCredentials


def refresh_token(username):
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/tasks.readonly']
    creds = None
    client_id = '828422134130-bneqqft7mngj1be10i0j2ath0tl2hc9i.apps.googleusercontent.com'
    client_secret = 'ozBOZnvxR8vkoSOnh11kql0h'
    user_creds, created = UserCredentials.objects.get_or_create(user__username=username)
    if not created:
        credentials = os.path.join(BASE_DIR, 'tokens/{}_token.pickle'.format(user_creds.user.username))
        print(credentials)
        with open(credentials, 'rb') as token:
            creds = pickle.load(token)
            print(creds)
    else:
        credentials = os.path.join(BASE_DIR, 'tokens/{}_token.pickle'.format(username))
        user = User.objects.get(username=username)
        user_creds.user = user
        user_creds.credentials = credentials
        user_creds.save()
    if not creds:
        if creds and creds.expired and creds.refresh_token:
            creds = client.GoogleCredentials(None, client_id, client_secret,
                                             creds.refresh_token, creds.expiry,
                                             "https://accounts.google.com/o/oauth2/token", "Smart Mirror")
            http = creds.authorize(httplib2.Http())
            creds.refresh(http)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/mahooly/PycharmProjects/SMir/smir/client_secret.json', SCOPES)
            creds = flow.run_local_server()
        with open(credentials, 'wb') as token:
            pickle.dump(creds, token)
    return creds
