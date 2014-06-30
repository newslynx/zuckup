#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps 

from parsers import (
  parse_insights, parse_post, parse_page_stats, get_datetime
  )
from util import (
  opt_connect, validate_kw, catch_err, concurrent_yield
  )

def fb(parser=parse_post,requires=[], default={}, gen=True):
  def fb_func(func, **kw):  
    @wraps(func)
    def f(*args, **kw):
      
      # check kw's
      kw = validate_kw(kw, requires)

      # optionally connect to the api
      api = opt_connect(**kw)

      # add defautls to kw's
      kw = dict(kw.items() + default.items())
        
      # get args
      args = catch_err(func, api, **kw)

      if gen:
        if kw.get('concurrent'):
          return concurrent_yield(parser, args, **kw)

        else:
          return (parser(a) for a in args)

      else:
        return parser(args)


    return f
  return fb_func

@fb(parser=parse_insights, requires=['page_id'])
def insights(api, **kw):
  
  # get the page id
  page_id = kw.get('page_id')
  
  # if paginate, double iterate
  if kw.get('page') or kw.get('paginate'):
    pages = api.get(page_id + "/posts", **kw)
    for page in pages:
      for post in page['data']:
        post_id = post['id']
        pub_datetime = get_datetime(post)
        insights = api.get(post_id + "/insights", **kw)
        yield insights, page_id, post_id, pub_datetime

  # if not, simple yield
  else:
    page = api.get(page_id + "/posts", **kw)
    for post in page['data']:
      post_id = post['id']
      pub_datetime = get_datetime(post)
      insights = api.get(post_id + "/insights", **kw)
      yield insights, page_id, post_id, pub_datetime


@fb(requires=['page_id'])
def page(api, **kw):
  # get the page id
  page_id = kw.get('page_id')
  
  # if paginate, double iterate
  if kw.get('page'):
    pages = api.get(page_id + "/posts", **kw)
    for page in pages:
      for post in page['data']:
        yield post, page_id

  # if not, simple yield
  else:
    page = api.get(page_id + "/posts", **kw)
    for post in page['data']:
      yield post, page_id


@fb(parser=parse_page_stats, requires=['page_id'], gen=False)
def page_stats(api, **kw):
  page_id = kw.get('page_id')
  page = api.get(page_id, **kw)
  return page, page_id

if __name__ == '__main__':
  for p in page(page_id="nytimes", concurrent=True):
    print p


