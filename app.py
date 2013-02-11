import os
import psycopg2
import urlparse
import json
import datetime
import re
from dateutil import tz
from flask import Flask, render_template, Response
from flask.ext.bootstrap import Bootstrap
from flask.ext.cache import Cache


# Get environement variables
db_url = urlparse.urlparse(os.environ['DATABASE_URL'])
debug_app = 'DEBUG_APP' in os.environ

# Set up database connection
urlparse.uses_netloc.append('postgres')
conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % 
  (db_url.path[1:], db_url.username, db_url.password, db_url.hostname))
db = conn.cursor()


# Set up Flask app
app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_USE_MINIFIED'] = True

if debug_app:
  app.debug = True

# Set up cache
cache_config = {
  'CACHE_TYPE': 'filesystem',
  'CACHE_THRESHOLD': 1000,
  'CACHE_DIR': 'cache'
}
cache = Cache(config = cache_config)
cache.init_app(app, config = cache_config)


# Routes for app
@app.route('/')
@cache.cached(timeout=50)
def index():
	return render_template('index.html')


# Routes for API
@app.route('/api/license/<license>', methods=['GET'])
@cache.cached(timeout=5000)
def api_license(license):
  license = re.sub('[\W_]+', '', license)
  query = "SELECT * FROM mpd_lpt_records WHERE LOWER(plate) = LOWER('%s') ORDER BY  timestamp_parsed ASC LIMIT 500" % (license)
  data = db_query_simple(query)
  response = output_json(data)
  
  response.headers['Cache-Control'] = 'public,max-age=2592000';
  return response


# Helper functions
def output_json(data):
  return Response(json.dumps(data, default=json_date_handler), mimetype = 'application/json')
  
def db_query_simple(query, args=(), one=False):
  db.execute(query, args)
  r = [dict((db.description[i][0], value) for i, value in enumerate(row)) for row in db.fetchall()]
  return (r[0] if r else None) if one else r

def json_date_handler(obj):
  if hasattr(obj, 'isoformat'):
    return obj.isoformat()
  else:
    return str(obj)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)