Reverse Zipcode Lookup & Visualizing Neighboring Areas via Raycasting Algorithm from CENSUS DATA
========================================

![Alt text](/screenshot.jpg?raw=true "RAYCASTING ALGORITHM")

Here's the scenario: as a services company contracting independent professionals, you need to map out what is a potentially serviceable area based on the professional's current location. You decide the best way to do this is to figure out what the professional's current zip code is, as well as zip codes of areas within a certain radius from the professional's location.

===========================================
This project functions in 2 parts:

1. 	PYTHON calculations

2. 	PHP & JS visualization
	
================================
SETUP

1. Given a spacefile from the US Census for zip code boundaries among other data, the script convert.py looks for a shapefile in ~/tl_2014_us_zcta510/tl_2014_us_zcta510.shp"

2. convert.py isolates relevant boundary data, and indexes it by zip code in 10 files (named 0 - 9), each containing zip codes starting with the filename

3. copy the WWW directory to a PHP-enabled webserver

4. change line 100 & 111 in zipify.py to your own appropriate web-facing directory (& append appropriate filename, either META or OUTPUT)

5. (todo) change 5 in WWW/index.php to reflect python path & deploy directory


================================
DEPENDENCIES:

	1. GIS web service is used to find zip codes adjacent to the zipcode returned by raycasting algorithm

	2. Google Maps v3 JS APi used to overlay polygons on map

================================
USAGE:

	1. run zipify.py to precalculate boundaries for the given position (longitude, latitude)

	2. open /path/to/index.php in a browser to visualize the geo boundaries
	
================================
TODO:

	1. executing zipify from within WWW/index.php via exec currently does not work 
		despite lines 1-13 of WWW/index.php because it is not blocking
		I suspect there is some configuration of PHP's exec or variant that works

	2. Add a form which executes the above scenario on WWW/index.php

	3. Use great circles rather than linear approximation for raycasting algorithm

	4. REMOVE hotlinks to bootstrap (from another one of my websites)

	5. Separate JS and CSS into linked sources instead of on index.php