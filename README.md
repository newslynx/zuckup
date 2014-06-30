![travis-img](https://travis-ci.org/newslynx/zuckup.svg)
zuckup
======
_simple facebook parsing_

## Install
```
pip install zuckup
```

## Test
Requires `nose`
```
nosetests
```

## Usage
`zuckup` comes with three utilities: `insights`, `page`, and `page_stats`

### Insights

*NOTE*: To get facebook insights data you must first have an access token that has necessary credentials to view this data.
```python
import zuckup

for post_stats in zuckup.insights(page_id='authenticated_page'):
  print post_stats
```

### Page Posts

```python
import zuckup

for post in zuckup.page(page_id='nytimes')
  print post 
```

### Page Stats

```python
import zuckup

page_stats = zuckup.page_stats(page_id='nytimes')
print page_stats
```

## Authentication
`zuckup` will automatically connect to the facebook api via `facepy` if you have `FB_APP_ID` and `FB_APP_SECRET` set as environmental variables.

Alternatively, you can connect beforehand and pass in this connection via the kwarg `conn`:

```python
import zuckup

conn = zuckup.connect(app_id='12345', app_secret='678910')

page_stats = zuckup.page_stats(page_id='nytimes', conn=conn)
print page_stats
```

Finally, if you want to connect with just an access token, say one acquired from a user authenticating to your app, pass in `access_token` to any of the methods:

```python
import zuckup

page_stats = zuckup.page_stats(page_id='nytimes', access_token='a-users-access-token')
print page_stats
```

## Pagination
paginate through results using `paginate` with `insights` and  `page`:
```
for post in zuckup.page(page_id='nytimes', paginate=True)
  print post 
```

## Concurrency
optional concurrency for `insights` and `page` via `gevent`:
```
import zuckup

for post in zuckup.page(page_id='nytimes', concurrent=True)
  print post 
```

