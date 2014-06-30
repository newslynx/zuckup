#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime 
import pytz
import logging 
import time

from defaults import default_kws
from connection import connect
import facepy

try:
  import gevent
  from gevent.pool import Pool

  # patch everything except for thread.
  import gevent.monkey
  gevent.monkey.patch_socket()
  gevent.monkey.patch_ssl()
  gevent.monkey.patch_os()
  gevent.monkey.patch_time()
  gevent.monkey.patch_select()
  gevent.monkey.patch_subprocess()

except ImportError:
  imported_gevent = False
else:
  imported_gevent = True

FB_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S+0000"

logging.basicConfig()
logger = logging.getLogger("zuckup")

def concurrent_yield(func, iterartor, **kw):
  if imported_gevent:
    p = Pool(kw.get('num_workers'))
    for result in p.imap_unordered(func, iterartor):
      yield result
  else:
    logger.warn('Cannot run concurrently without importing gevent')
    for args in iterartor:
      yield func(*args)

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
  Catch Facebook API Errors, backoff, and timeout.
  """
  
  # get timing kwargs
  wait = kw.get('wait')
  backoff = kw.get('backoff')
  timeout = kw.get('timeout')

  # try until we timeout
  t0 = time.time()
  while True:
    try:
      results = func(api, **kw)
      break
    
    # backoff from errors
    except facepy.FacepyError as e:
      time.sleep(wait)
      wait *= backoff

      # timeout
      now = time.time()
      if now - t0 > timeout:
        logger.warn("Timing out beacause of {0}".format(e))
        results = []
        break

  return results