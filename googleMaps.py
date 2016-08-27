#pip install -U googlemaps

import json
import re

import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyAOHs5bYxYRWtFkBCOHAFkcS3-nrMd91BE')

# Geocoding an address
#geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
#reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
#now = datetime.now()
#directions_result = gmaps.directions("Sydney Town Hall",
#					"Parramatta, NSW",
#					mode="transit",
#					departure_time=now)

#print reverse_geocode_result

#print directions_result

def latLngToString(latLng):
	return str(latLng[0])+", "+str(latLng[1])

def textToLatLng(inputText, region="us"):
	reverse_geocode_result = gmaps.geocode(inputText, region=region)
	return reverse_geocode_result[0]["geometry"]["location"]["lat"], reverse_geocode_result[0]["geometry"]["location"]["lng"]

def getDirectionLatLng(fromLatLng, toLatLng, mode="driving", departure_time=datetime.now()):
	fromLatLngString = latLngToString(fromLatLng)
	toLatLngString = latLngToString(toLatLng)
	directions_result = gmaps.directions(fromLatLngString, toLatLngString, mode=mode, departure_time=departure_time)
	return getStepsArrayFromJson(directions_result)

def getDirection(origin, destination, mode="driving", departure_time=datetime.now()):
	directions_result = gmaps.directions(origin, destination, mode=mode, departure_time=departure_time)
	return getStepsArrayFromJson(directions_result)

def getStepsArrayFromJson(directions_result):
	directions_steps = directions_result[0]["legs"][0]["steps"]
	numberOfSteps = len(directions_steps)

	returnArray = []
	for i in range(0, numberOfSteps):
		instructionString = re.sub(r"[ ]*<[^>]*>[ ]*", r' ', str(directions_steps[i]["html_instructions"]))
		returnArray.append(instructionString)

	return returnArray


def closestFromGroup(origin, destinationArray):
	distanceMatrix = gmaps.distance_matrix(origin, destinationArray)

	numberOfIndexes = len(distanceMatrix['rows'][0]['elements'])
	smallestDistance = 999999999999 #int max
	smallestIndex = -1
	# fill the first address
	for i in range(0, numberOfIndexes):
		if (distanceMatrix['rows'][0]['elements'][i]['status'].find("OK") != -1):
			smallestDistance = distanceMatrix['rows'][0]['elements'][0]['distance']['value']
			smallestIndex = 0

	for i in range(1, numberOfIndexes):
		if (distanceMatrix['rows'][0]['elements'][i]['status'].find("OK") != -1):
			distanceTmp = distanceMatrix['rows'][0]['elements'][i]['distance']['value']
			if (distanceTmp < smallestDistance):
				smallestDistance = distanceTmp
				smallestIndex = i

	#print smallestIndex
	#print destinationArray[smallestIndex]
	return distanceMatrix['destination_addresses'][smallestIndex]




#print textToLatLng('1600 Amphitheatre Parkway, Mountain View, CA')

#print getDirectionLatLng(textToLatLng("Microsoft, redmond"), textToLatLng("Google, Kirkland") )

#print closestFromGroup("Microsoft, redmond", ["Google Seattle" ,"Google, Kirkland","Google Mountain View"])

#print getDirection("Microsoft, redmond","Google, Kirkland")


myLocation = "1100 NE Campus Pkwy #200, Seattle, WA 98105"
listOfStarbucks = ["4555 University Way NE, Seattle, WA 98105", "First Starbucks Pike Place, Seattle WA", "1124 Pike St, Seattle, WA 98101"] 

listOfStarbucks.append("starbucks near University District Seattle WA")

print listOfStarbucks
print closestFromGroup(myLocation, listOfStarbucks)

print getDirection(myLocation, closestFromGroup(myLocation, listOfStarbucks))