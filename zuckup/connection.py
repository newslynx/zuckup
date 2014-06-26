#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import facepy
from urlparse import parse_qs

import credentials

def connect(**kw):
  
  # parse kw's
  app_id = kw.get('app_id', credentials.FB_APP_ID)
  app_secret = kw.get('app_secret', credentials.FB_APP_SECRET)
  access_token = kw.get('access_token', None)

  # if no access token, create one
  if not access_token:
    access_token = generate_app_access_token(app_id, app_secret)

  # return api
  return facepy.GraphAPI(access_token)

def generate_app_access_token(app_id, app_secret):

  """
  Get an extended OAuth access token.

  :param access_token: A string describing an OAuth access token.
  :param application_id: An icdsnteger describing the Facebook application's ID.
  :param application_secret_key: A string describing the Facebook application's secret key.

  Returns a tuple with a string describing the extended access token and a datetime instance
  describing when it expires.
  """
  # access tokens
  default_access_token = facepy.get_application_access_token(
    application_id = app_id,  
    application_secret_key = app_secret
  )
  graph = facepy.GraphAPI(default_access_token)

  response = graph.get(
    path='oauth/access_token',
    client_id = app_id,
    client_secret = app_secret,
    grant_type = 'client_credentials'
  )
  components = parse_qs(response)
  token = components['access_token'][0]
  return token
