import urllib

print 'Download 01'
urllib.urlretrieve('https://s3.amazonaws.com/data.minnpost/projects/minnpost-mpd-license-plates/data/Aug+30+to+9-20+REDACTED.csv', '/tmp/mpd-lpt-20120830-20120920.csv')

print 'Download 02'
urllib.urlretrieve('https://s3.amazonaws.com/data.minnpost/projects/minnpost-mpd-license-plates/data/Sept+21+to+Oct+12+LPR+Redacted.csv', '/tmp/mpd-lpt-20120921-20121013.csv')

print 'Download 03'
urllib.urlretrieve('https://s3.amazonaws.com/data.minnpost/projects/minnpost-mpd-license-plates/data/Oct+13+to+November+3+Redacted.csv', '/tmp/mpd-lpt-20121013-20121103.csv')

print 'Download 04'
urllib.urlretrieve('https://s3.amazonaws.com/data.minnpost/projects/minnpost-mpd-license-plates/data/November+4+to+November+29+LPR+Redacted.csv', '/tmp/mpd-lpt-20121104-20121129.csv')