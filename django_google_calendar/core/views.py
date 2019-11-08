import httplib2
import logging
import os
import pickle
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from googleapiclient.discovery import build
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets


CLIENT_SECRETS = os.path.join(
    settings.BASE_DIR,
    'credentials.json')

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri='http://localhost:8000/oauth2callback')


class Index(View):
    def get(self, request):
        credential = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                credential = pickle.load(token)

        if credential is None or credential.invalid is True:
            chave = settings.SECRET_KEY
            user = request.user
            token = xsrfutil.generate_token(settings.GOOGLE_OAUTH2_CLIENT_SECRET, settings.GOOGLE_OAUTH2_CLIENT_ID)
            FLOW.params['state'] = token
            authorize_url = FLOW.step1_get_authorize_url()
            return HttpResponseRedirect(authorize_url)

        http = httplib2.Http()
        http = credential.authorize(http)
        service = build('calendar', 'v3', http=http)
        events = service.events()
        event_list = events.list(calendarId='primary').execute()
        logging.info(event_list)
        return render(request, 'core/events.html', {'events': event_list})


class AuthHandler(View):
    def get(self, request):
        chave = settings.SECRET_KEY
        state = bytes(request.GET.get('state'), 'utf-8')
        user = request.user
        if not xsrfutil.validate_token(
            settings.GOOGLE_OAUTH2_CLIENT_SECRET, 
            state, 
            settings.GOOGLE_OAUTH2_CLIENT_ID):
            return HttpResponseBadRequest()
        credential = FLOW.step2_exchange(request.REQUEST)
        with open('token.pickle', 'wb') as token:
            pickle.dump(credential, token)
        return HttpResponseRedirect("/")
