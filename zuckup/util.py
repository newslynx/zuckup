#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime 
import pytz

from defaults import default_kws
from connection import connect
import facepy

FB_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S+0000"

def utc_now():
  dt = datetime.utcnow()
  dt = dt.replace(tzinfo = pytz.utc)
  return dt

def strip_date(ds):
  dt = datetime.strptime(ds, FB_DATE_FORMAT)
  dt = dt.replace(tzinfo = pytz.utc)
  return dt

def validate_kw(kw, requires):
  """
  Validate kw.
  """
  # check required kwargs
  for r in requires:
    if r not in kw:
      raise Exception(
        "Missing required kwarg: %s" % r
        )

  # insert defaults 
  for k,v in default_kws.items():
    if k not in kw:
      kw[k] = v

  return kw

def opt_connect(**kw):
  """
  Connect to api if we havent passed a `conn` 
  argument in.
  """
  if 'conn' in kw:
    return conn 
  else:
    return connect(**kw)

def catch_err(func, api, **kw):
  """
  Catch Twitter API Errors, backoff, and timeout.
  """
  
  # get timing kwargs
  wait = kw.get('wait')
  backoff = kw.get('backoff')
  timeout = kw.get('timeout')

  # try until we timeout
  while True:
    try:
      results = func(api, **kw)
      break
    
    # backoff from errors
    except facepy.FacepyError as e:
      t0 = time.time()
      time.sleep(wait)
      wait *= backoff

      # timeout
      now = time.time()
      if now - t0 > timeout:
        logger.warn("Timing out beacause of {0}".format(e))
        results = []
        break

  return results