/**
 * Main JS for cano opener.
 */

(function($, w, undefined) {
  $(document).ready(function() {
    // Show explaning modal
    $('.inital-explanantion-modal').modal('show')
      .on('hidden', function() {
      
      });
  
    // Load map
    mapbox.auto('map-container', 'zzolo.map-906px3yv', function(map, tiledata) {
    
    });
  
  });
})(jQuery, window);