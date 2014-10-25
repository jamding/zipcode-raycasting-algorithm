import sys
import pycurl
import io
import re

#detect if found within relevant polygon, linear examination
def point_in_poly(x,y,poly):

	n = len(poly)
	inside = False

	p1x,p1y = poly[0]
	for i in range(n+1):
		p2x,p2y = poly[i % n]
		if y > min(p1y,p2y):
			if y <= max(p1y,p2y):
				if x <= max(p1x,p2x):
					if p1y != p2y:
						xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
					if p1x == p2x or x <= xints:
						inside = not inside
		p1x,p1y = p2x,p2y

	return inside

#iterate through each source file
def find_zip_code(latitude, longitude):
	for x in range(10):
		i = 9 - x
		rc = find_in_file(str(i), float(latitude), float(longitude))
		if rc is not False:
			return rc
		print("Doesn't start with " + str(i))

#read line by line through file block
def find_in_file(filename, latitude, longitude):
	with open(filename, 'r') as f:
		for line in f:
			line_zip = zip_list = re.match('@@@(\d*)===', line).group(1)
			coord_string = line.split("===")
			coord_string = coord_string[1]
			
			points = coord_string.split(";")
			poly = []
			for point in points:
				temp = point.split(",")
				if len(temp) < 2:
					continue
				poly.append((float(temp[0]), float(temp[1])))
			if point_in_poly(latitude, longitude, poly):
				return line_zip
	return False
	
def write_coordinates_for_zip_prefix(first_digit, output_filename, target_list):
	with open(first_digit, 'r') as f:
		for line in f:
			#check if zipcode is in here
			#write its contents if it is
			line_zip = zip_list = re.match('@@@(\d*)===', line).group(1)
			#print("Matching " + line_zip)
			if line_zip in target_list:
				coord_string = line.split("===")
				output_filename.write(coord_string[1])
	
def main():
	#usage validation
	if len(sys.argv) != 4:
		print("Usage: python zipify <latitude> <longitude> <mile-search-radius>")
		sys.exit(1)
	
	#input sanitation
	lat = str(float(sys.argv[1]))
	lon = str(float(sys.argv[2]))
	zipcode = find_zip_code(lat, lon)
	radius = str(int(sys.argv[3]))
	
	#curl cString buffering
	buf = io.BytesIO()

	#curl this handy external API
	url = "http://zipcodedistanceapi.redline13.com/rest/2odywUYrQJOEEO0vJdlcH5Qd8Lf6EGKG4YfBTd2JXQoCFo7pBsBiysvGdLNSsyzw/radius.json/"+zipcode+"/"+radius+"/mile"

	c = pycurl.Curl()
	c.setopt(c.URL, url)
	c.setopt(c.WRITEFUNCTION, buf.write)
	c.setopt(c.CONNECTTIMEOUT, 5)
	c.setopt(c.TIMEOUT, 8)
	c.perform()

	#print(buf.getvalue())
	raw_curl = str(buf.getvalue())
	buf.close()
	
	#regex to parse string
	zip_list = re.findall('"zip_code":"(\d*)","distance":', raw_curl)
	zip_list.sort()
	print(zip_list)
	
	#now let's read in the generated files, look for coordinates and write them to a file
	target_output = open("C:\wamp\www\homejoy\OUTPUT", 'w')
	prefixes = []
	for x in zip_list:
		if x[0] in prefixes:
			pass
		else:
			prefixes.append(x[0])
	
	for prefix in prefixes:
		write_coordinates_for_zip_prefix(prefix, target_output, zip_list)
		
	meta_output = open("C:\wamp\www\homejoy\META", 'w')
	meta_output.write("Searching in " + radius + " mile radius around " + zipcode)
	meta_output.write("\n")
	meta_output.write(", ".join(zip_list))
	
	
main()