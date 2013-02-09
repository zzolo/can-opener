"""
File to handle importing MPD LPT data.
"""
import csv
import os
import psycopg2
import sys
from datetime import *
import dateutil.parser
import ppygis


def ct(value):
  """
  Custom trim function for cleaning up strings
  """
  if value == "''" or value == '""' or value == '' or value == 'NULL':
    return None
  else:
    return value.strip()
  

def dt(value, return_type):
  """
  Custom date handler function for cleaning up strings
  """
  if value == 'NULL' or value == '':
    return None
  else:
    if return_type == 'date':
      return dateutil.parser.parse(value).date()
    else:
      return dateutil.parser.parse(value)


def pp(value):
  """
  Wrapper for printing to the screen without a buffer.
  """
  sys.stdout.write(value)
  sys.stdout.flush()


# Paths
path = os.path.dirname(__file__)

# Connect to database
conn = psycopg2.connect('dbname=minnpost_mpd_lpt user=postgres host=localhost')
db = conn.cursor()

# First, let's clear or create the DB table
query = """
DROP INDEX IF EXISTS mpd_lpt_records_timestamp_parsed;
DROP INDEX IF EXISTS mpd_lpt_records_plate;
DROP INDEX IF EXISTS mpd_lpt_records_reader;
DROP TABLE IF EXISTS mpd_lpt_records;

CREATE TABLE mpd_lpt_records
(
  id bigserial NOT NULL,
  plate character varying(16),
  reader character varying(32),
  timestamp_text character varying(64),
  timestamp_parsed timestamp without time zone,
  lat numeric,
  lon numeric,
  CONSTRAINT mpd_lpt_records_id PRIMARY KEY (id )
)
WITH (
  OIDS=FALSE
);
SELECT AddGeometryColumn('mpd_lpt_records', 'location', 4326, 'POINT', 2);
CREATE INDEX mpd_lpt_records_timestamp_parsed ON mpd_lpt_records (timestamp_parsed);
CREATE INDEX mpd_lpt_records_plate ON mpd_lpt_records (plate);
CREATE INDEX mpd_lpt_records_reader ON mpd_lpt_records (reader);
"""

pp("\n[table] (re)Creating table.")
db.execute(query)
committed = conn.commit()

# Import in each file
files = [ 'mpd-lpt-20120830-20120920.csv', 'mpd-lpt-20120921-20121013.csv', 'mpd-lpt-20121013-20121103.csv', 'mpd-lpt-20121104-20121129.csv' ];
for f in files:
  pp("\n[%s] Reading file: %s." % (f, f))
  committed = conn.commit()
  
  # Read file
  input_file = os.path.join(path, '../data/%s' % f)
  reader = csv.reader(open(input_file, 'rU'), delimiter=',', dialect=csv.excel_tab)
  
  # Import into DB
  pp("\n[%s] Importing..." % (f))
  row_count = 0
  insert_count = 0
  
  for row in reader:
    # Ensure no row and a license plate.  There
    # are also rows with labels
    if row_count > 0 and row[0] != '0' and row[0] != 'Plate' and row[0] != '':
      try:
        # Some values don't have lat/lon
        if ct(row[1]) != '' and ct(row[1]) != None:
          db.execute("""
            INSERT INTO mpd_lpt_records 
            (plate, reader, timestamp_text, timestamp_parsed, lat, lon, location) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
          """,
            (ct(row[0]), ct(row[4]), ct(row[3]), dt(row[3], ''), float(row[1]), float(row[2]),
            ppygis.Point(float(row[2]), float(row[1]), srid=4326)))
        else:
          db.execute("""
            INSERT INTO mpd_lpt_records 
            (plate, reader, timestamp_text, timestamp_parsed) 
            VALUES (%s, %s, %s, %s)
          """,
            (ct(row[0]), ct(row[4]), ct(row[3]), dt(row[3], '')))
        
        committed = conn.commit()
      except Exception, err:
        print '[%s] Error thrown while saving to database: %s' % (f, row)
        raise
      
      # Make a mark to help show progress
      insert_count += 1
      if insert_count % 1000 == 0:
        pp('.')
        
    row_count += 1
    
  pp("\n[%s] Commited %s rows.\n" % (f, insert_count))
  


pp("\n\n.")