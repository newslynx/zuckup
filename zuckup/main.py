#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps 

from parsers import parse_insights, parse_post, parse_page_stats
from util import opt_connect, validate_kw, catch_err

def fb(requires=[], default={}):
  def fb_func(func, **kw):  
    @wraps(func)
    def f(*args, **kw):
      
      # check kw's
      kw = validate_kw(kw, requires)

      # optionally connect to the api
      api = opt_connect(**kw)

      # add defautls to kw's
      kw = dict(kw.items() + default.items())
        
      # get results
      return catch_err(func, api, **kw)

    return f
  return fb_func

@fb(requires=['page_id'])
def insights(api, **kw):
  
  # get the page id
  page_id = kw.get('page_id')
  
  # if paginate, double iterate
  if kw.get('page'):
    pages = api.get(page_id + "/posts", **kw)
    for page in pages:
      for post in page['data']:
        post_id = post['id']
        insights = api.get(post_id + "/insights", **kw)
        yield parse_insights(insights, page_id, post_id)

  # if not, simple yield
  else:
    page = api.get(page_id + "/posts", **kw)
    for post in page['data']:
      post_id = post['id']
      insights = api.get(post_id + "/insights", **kw)
      yield parse_insights(insights, page_id, post_id)


@fb(requires=['page_id'])
def page(api, **kw):
  # get the page id
  page_id = kw.get('page_id')
  
  # if paginate, double iterate
  if kw.get('page'):
    pages = api.get(page_id + "/posts", **kw)
    for page in pages:
      for post in page['data']:
        yield parse_post(post, page_id)

  # if not, simple yield
  else:
    page = api.get(page_id + "/posts", **kw)
    for post in page['data']:
      yield parse_post(post, page_id)


@fb(requires=['page_id'])
def page_stats(api, **kw):
  page_id = kw.get('page_id')
  page = api.get(page_id, **kw)
  return parse_page_stats(page, page_id)

if __name__ == '__main__':
  print page_stats(page_id="nytimes")

