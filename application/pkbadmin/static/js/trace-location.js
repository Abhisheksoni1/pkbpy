    var source, destination;
    var directionsDisplay;
    var directionsService;
    source =get_source();

      var destination='';
      options = { componentRestrictions: { country: 'IN'} };

    $(function(){
    $(window).load(function(){
       directionsService = new google.maps.DirectionsService();
      google.maps.event.addDomListener(window, 'load', function () {
          new google.maps.places.Autocomplete(source, options);
          new google.maps.places.Autocomplete(destination, options);
         // directionsDisplay = new google.maps.DirectionsRenderer({ 'draggable': true });
      });
      });
    });

      function GetRoute() {

          destination= get_address();
          console.log(destination)
          source =get_source();

          $('#dvMap').height(400);
          $('#dvMap').show().html('');
          $('#dvPanel').show().html('');
          var PKB = new google.maps.LatLng(28.6501764, 77.3716896);
          var mapOptions = {
              zoom: 7,
              center: PKB
          };
          directionsDisplay = new google.maps.DirectionsRenderer({ 'draggable': true });
          map = new google.maps.Map(document.getElementById('dvMap'), mapOptions);
          directionsDisplay.setMap(map);
          directionsDisplay.setPanel(document.getElementById('dvPanel'));

          //*********DIRECTIONS AND ROUTE**********************//
          source = source //document.getElementById("txtSource").value;
          destination = destination //document.getElementById("txtDestination").value;

          var request = {
              origin: source,
              destination: destination,
              travelMode: google.maps.TravelMode.DRIVING
          };
          directionsService = new google.maps.DirectionsService();
          directionsService.route(request, function (response, status) {
              if (status == google.maps.DirectionsStatus.OK) {
                  directionsDisplay.setDirections(response);
              }
          });

          //*********DISTANCE AND DURATION**********************//
          var service = new google.maps.DistanceMatrixService();
          service.getDistanceMatrix({
              origins: [source],
              destinations: [destination],
              travelMode: google.maps.TravelMode.DRIVING,
              unitSystem: google.maps.UnitSystem.METRIC,
              avoidHighways: false,
              avoidTolls: false
          }, function (response, status) {
              console.log(response, status)
              if(response.destinationAddresses!=''){
              if (status == google.maps.DistanceMatrixStatus.OK && response.rows[0].elements[0].status != "ZERO_RESULTS") {
                 // var distance = response.rows[0].elements[0].distance.text;
                  var distance = response.rows[0].elements[0].distance.text;
                  var duration = response.rows[0].elements[0].duration.text;
                  document.getElementById("lblDistance").innerHTML = distance+'~';
                  document.getElementById("duration").innerHTML = duration;
              } else {
                  bootbox.alert("Unable to find the distance via road.");
              }
          }
          else{
              bootbox.alert("Address not found");
          }
          });
      }


    $("#mapbtn").click(function(){
        $(this).hide()
      $("#closebtn").show();
    });
    $('#closebtn').click(function(){
      $('#dvMap').hide('');
      $('#dvPanel').hide('');
      $(this).hide('');
      $('#mapbtn').show();
    });

    $('#go_back').click(function goBack() {
    window.history.back();
    });

    function get_source(){

        kitchen_address = $('input[name=kitchen_address]').val();
        return kitchen_address
    }