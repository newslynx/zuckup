#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util import utc_now, strip_date

from siegfried import (
  prepare_url, is_short_url, unshorten_url, urls_from_string
  )

def parse_post(post, page_id=None):
  data = {}
  data['page_id'] = page_id
  data['post_id'] = post.get('id', None)
  data['urls'] = get_urls(post)
  data['img_url'] = get_img(post)
  data['datetime'] = get_datetime(post)
  data['message'] = post.get('message', None)
  data['description'] = post.get('description', None)
  data['status_type'] = post.get('status_type', None)
  data['type'] = post.get('type', None)
  return data

def parse_page_stats(page, page_id=None):
  data = {}
  data['page_id'] = page_id
  data['page_talking_about_count'] = int(page['talking_about_count'])
  data['page_likes'] = int(page['likes'])
  data['datetime'] = utc_now()
  return data

def parse_insights(data, page_id=None, post_id=None):
  """
  Get insights data if indicated so by the config file
  """
  
  # add metadata
  insights = {}
  insights['page_id'] = page_id
  insights['post_id'] = post_id
  insights['datetime'] = utc_now()

  # flatten dict
  for d in data:
    val = d['values'][0]['value']
    if isinstance(val, dict):
      for k, v in val.iteritems():
        insights[k] = v

    else:
      insights[d['name']] = val

  return insights

def get_url_candidates(post):
  
  urls = set()
  
  if post.has_key('link'):
    urls.add(post['link'])

  if post.has_key('source'):
    urls.add(post['source'])

  if post.has_key('message'):
    msg_urls = parse_message_urls(post['message'])
    for u in msg_urls: urls.add(u)

  return list(urls)

def parse_message_urls(message):
  urls = urls_from_string(message)
  return urls

# TODO: improve this
def get_img(post):
  return post.get('picture', None)

def get_urls(post):
  candidates = get_url_candidates(post)
  urls = set()
  for u in candidates:
    if 'facebook' not in u:
      if is_short_url(u):
        u = unshorten_url(u)
      urls.add(prepare_url(u))
  return list(urls)

def get_datetime(post):
  if post.has_key('updated_time'):
    return strip_date(post['updated_time'])
  else:
    return utc_now()



