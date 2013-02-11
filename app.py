import os
import psycopg2
import urlparse
import json
import datetime
from dateutil import tz
from flask import Flask, render_template, Response
from flask.ext.bootstrap import Bootstrap


# Get environement variables
db_url = urlparse.urlparse(os.environ['DATABASE_URL'])
debug_app = os.environ['DEBUG_APP']

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


# Routes for app
@app.route('/')
def index():
	return render_template('index.html')


# Routes for API
@app.route('/api/license/<license>', methods=['GET'])
def api_license(license):
  query = "SELECT * FROM mpd_lpt_records WHERE plate = '%s' LIMIT 500" % (license)
  data = db_query_simple(query)
  return output_json(data)


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