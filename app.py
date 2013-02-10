import os
import psycopg2
import urlparse
from flask import Flask, render_template
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
@app.route('/api/license', methods=['GET'])
def api_license():
  return output_json()

# Helper functions
def output_json(data):
  return Response(json.dumps(data), mimetype = 'application/json')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)