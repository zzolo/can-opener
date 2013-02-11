/**
 * Main JS for cano opener.
 */

// Utility stuff
if (!String.prototype.trim) {
  String.prototype.trim = function() {
    return this.replace(/^\s+|\s+$/g,'');
  };
}


// The real stuff
(function($, w, undefined) {
  // Helper functions
  var help = {};
  
  help.parseRecords = function(data) {
    return _.map(data, function(d) {
      d.lat = (!_.isNaN(parseFloat(d.lat))) ? parseFloat(d.lat) : '';
      d.lon = (!_.isNaN(parseFloat(d.lon))) ? parseFloat(d.lon) : '';
      d.date = moment(d.timestamp_parsed);
      return d;
    });
  };

  help.makeMarker = function(layer, record, template) {
    layer.add_feature({
      geometry: {
        coordinates: [record.lon, record.lat]
      },
      properties: {
        'marker-size': 'medium',
        'marker-color': '#222222',
        'marker-symbol': 'rail',
        description: template({ d: record })
      }
    });
  };
  
  help.makeList = function(records, template) {
    records = _.sortBy(records, function(r) {
      return r.date.unix();
    });
    $('.results-list').html(template({ records: records }));
  };

  // When page is loaded.
  $(document).ready(function() {
    // Get templates
    var templates = {
      popup: _.template($('#template-marker-popup').html()),
      list: _.template($('#template-records-list').html())
    };
  
    // Show explaning modal
    var $explainModal = $('.inital-explanantion-modal');
    $explainModal.modal('show')
      .on('hidden', function() {
      
      });
  
    // Load map
    mapbox.auto('map-container', 'zzolo.map-906px3yv', function(map, tiledata) {
      // Add custom attribution
      map.ui.attribution.add()
        .content('<a href="http://mapbox.com/about/maps" target="_blank">Mapbox Terms &amp; Feedback</a>');
    
      // Add marker layer
      var markerLayer = mapbox.markers.layer();
      mapbox.markers.interaction(markerLayer);
      map.addLayer(markerLayer);
      
    
      // Handle getting license query
      $('.license-plate-query-form').on('submit', function(e) {
        e.preventDefault();
        var license = $('.license-plate-query').val().trim();
        
        // Close modal if its open
        $explainModal.modal('hide');
        
        // Get license plate data
        $.getJSON('/api/license/' + license, function(data) {
          data = help.parseRecords(data);
          
          _.each(data, function(r) {
            if (r.lat && r.lon) {
              // Add markers to map
              help.makeMarker(markerLayer, r, templates.popup);
            }
          });
          
          // Make list of non-location records and count of found
          help.makeList(data, templates.list);
        });
      });
    });
  });
})(jQuery, window);