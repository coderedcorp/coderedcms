  // Initialize the map on the gooogle maps api js callback.
  function initMap() {
    // Set defaults
    const map = new google.maps.Map(document.querySelector('#cr-map'), {
      zoom: parseInt($("#cr-map").data( "zoom" )),
      center: {
        lat: parseFloat($("#cr-map").data( "latitude" )),
        lng: parseFloat($("#cr-map").data( "longitude" )),
      }
    });
    // Create an infowindow object.
    var infowindow = new google.maps.InfoWindow({  });

    // Listener to update the map markers when the map is idling.
    google.maps.event.addListener(map, 'idle', () => {
      const sw = map.getBounds().getSouthWest();
      const ne = map.getBounds().getNorthEast();
      let locationDataFeatures = [];
      map.data.loadGeoJson(
        $("#cr-map").data( "geojson-url" ) + `&viewport=${sw.lat()},${sw.lng()}|${ne.lat()},${ne.lng()}`,
        null,
        features => {
          locationDataFeatures.forEach(dataFeature => {
            map.data.remove(dataFeature);
          });
          locationDataFeatures = features;
          if ($("#cr-map").data( "show-list" ) == "True"){
            update_list(locationDataFeatures);
          }
        }
      );
    });

    // Listener to update the info window when a marker is clicked.
    map.data.addListener('click', ev => {
      const f = ev.feature;
      const title = f.getProperty('name');
      const description = f.getProperty('description');

      infowindow.setContent(`<b>${title}</b><br/> ${description}`);
      infowindow.setPosition(f.getGeometry().get());
      infowindow.setOptions({
        pixelOffset: new google.maps.Size(0, -30)
      });
      infowindow.open(map);
    });


    // Logic to create a search box and move the map on successful search.

    if ($("#cr-map").data( "show-search" ) == "True"){
      var input = document.getElementById('pac-input');
      var searchBox = new google.maps.places.SearchBox(input);
      map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
      map.addListener('bounds_changed', function() {
              searchBox.setBounds(map.getBounds());
            });
      searchBox.addListener('places_changed', function() {
        var places = searchBox.getPlaces();
        if (places.length == 0) {
          return;
        }
        // For each place, get the icon, name and location.
        var bounds = new google.maps.LatLngBounds();
        places.forEach(function(place) {
          if (!place.geometry) {
            return;
          }
          if (place.geometry.viewport) {
            // Only geocodes have viewport.
            bounds.union(place.geometry.viewport);
          } else {
            bounds.extend(place.geometry.location);
          }
        });
        map.fitBounds(bounds);
      });
    }

  // Updates the list to the side of the map with markers that are in the viewport.
  function update_list(features) {
      new_html = "";
      if(features.length == 0){
        new_html = "<h5>Sorry, there are no locations in this area.</h5>";
      } else {
        for (i=0; i < features.length; i++){
            new_list_item = "";
            new_list_item += "<div class='list-group-item flex-column align-items'>";
            new_list_item += "<div class='d-flex w-100 justify-content-between'>";
            new_list_item += "<a href='" + features[i].l.url + "'><h5 class='mb-1'>" + features[i].l.name + "</h5></a>";
            new_list_item += "</div>";
            new_list_item += "<p class='mb-1'>" + features[i].l.description + "</p>";
            new_list_item += "</div>";
            new_html += new_list_item;
        }
      }
      $("#LocationList").html(new_html);
    }
  }