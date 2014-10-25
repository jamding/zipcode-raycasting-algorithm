
import shapefile

def convert():
	sf = shapefile.Reader("tl_2014_us_zcta510/tl_2014_us_zcta510.shp")
	
	shapeRec = sf.shapeRecord(0)
	print(shapeRec.record)
	#print(shapeRec.shape.points)
	files = []
	for i in range(10):
		files.append(open(str(i), 'w'))

	i = 0
	while(True):
		shapeRec = sf.shapeRecord(i)
		if shapeRec is None:
			break
		
		zipcode = shapeRec.record[0]
		first_dig = int(zipcode[0])
		file = files[first_dig]
		file.write("@@@")
		file.write(zipcode)
		file.write("===")
		points = shapeRec.shape.points
		#file.write("\n")
		output = ""
		for point in points:
			output = output + str(point[0]) + "," + str(point[1]) + ";"
		file.write(output)
		file.write("\n")
		i += 1
		if i % 1000 == 0:
			print(i)
	
convert()