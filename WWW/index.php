<?php


if(isset($_GET['lat']) and isset($_GET['long']) and isset($_GET['radius'])) {
$cmd = "C:\Python34\python.exe C:\Users\jamdi_000\Desktop\homejoy\zipify.py ".$_GET['lat']." ".$_GET['long']." ".$_GET['radius'];
echo $cmd;
$result = exec($cmd);
//$output = exec("python C:\Users\jamdi_000\Desktop\homejoy\zipify.py ");
var_dump($result);


}
?>

<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
	<link rel="icon" href="http://ts1.mm.bing.net/th?id=HN.608019321878086093&amp;pid=1.7">
	<link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="http://fonts.googleapis.com/css?family=Montserrat:400,700|Crimson+Text:400,400italic,600,600italic,700,700italic" rel="stylesheet" type="text/css">
    <title>Simple Polygon</title>
<style>
  body {
	font-family: Montserrat, sans-serif;
  }
  </style>
    <style>
      html, body, #map-canvas {
        height: 100%;
        margin: 0px;
        padding: 0px;
      }
      #map-canvas {
        height: 90vh;
        margin: 0px;
        padding: 0px;
      }
	  #blurb {

		margin: 20px;
		padding:0px;
	  }
    </style>
	

    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp"></script>
  	<?php
	
	function isEmpty($var) {
		return (strlen($var) > 0) ? true : false;
	}
		$data = file_get_contents('./OUTPUT');
		$polygons = explode("\n", $data);
		$polygons = array_filter($polygons, "isEmpty");
		//var_dump($polygons);
		$polygon = explode(";", $polygons[0]);
		$temp = explode(",", $polygon[0]);
		$center = $temp[1].', '.$temp[0];
		/*
		$polygon = explode(";", $polygons[0]);
		$printout = array();
		foreach($polygon as $coordinates) {
			$temp = explode(",", $coordinates);
			if(count($temp) < 2) {
			continue;
			}
			array_push($printout, "new google.maps.LatLng(".$temp[1].', '.$temp[0].")");
		}
		$temp = explode(",", $polygon[0]);
		array_push($printout, "new google.maps.LatLng(".$temp[1].', '.$temp[0].")");
		*/
		
	?>
    <script>
// This example creates a simple polygon representing the Bermuda Triangle.

function initialize() {
  var mapOptions = {
    zoom: 9,
    center: new google.maps.LatLng(<?php echo $center; ?>),
    mapTypeId: google.maps.MapTypeId.TERRAIN
  };


  var map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);

  // Define the LatLng coordinates for the polygon's path.
  
  <?php 
  $i = 0;
  foreach($polygons as $entry) { 
	
  		$polygon = explode(";", $polygons[$i]);
		$i++;
		$printout = array();
		foreach($polygon as $coordinates) {
			$temp = explode(",", $coordinates);
			if(count($temp) < 2) {
			continue;
			}
			array_push($printout, "new google.maps.LatLng(".$temp[1].', '.$temp[0].")");
		}
		//$temp = explode(",", $polygon[]);
		//array_push($printout, "new google.maps.LatLng(".$temp[1].', '.$temp[0].")");

  ?>
  
	  var triangle<?php echo $i; ?> = [
	  <?php echo join(", ", $printout); ?>
	  ];
	  
	  // Construct the polygon.
	  var bermuda<?php echo $i; ?> = new google.maps.Polygon({
		paths: triangle<?php echo $i; ?>,
		strokeColor: '#FF0000',
		strokeOpacity: 0.8,
		strokeWeight: 2,
		fillColor: '#FF0000',
		fillOpacity: 0.35
	  });

	  bermuda<?php echo $i; ?>.setMap(map);
  <?php
  }
  ?>



}

google.maps.event.addDomListener(window, 'load', initialize);

    </script>
  </head>
  <body>

  
  <div id="blurb" >
  <h2>  	
	<?php
		$data = file_get_contents('./META');
		$split_data = explode("\n", $data);
		echo( $split_data[0]);

	?>
  </h2>
  <p>
  INCLUDED ZIPCODES: 
	<?php
		echo $split_data[1];
	?>

  </p>
  </div>
    <div id="map-canvas"></div>
  </body>
</html>