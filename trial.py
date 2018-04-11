# importing the requests library
import requests
URl = "https://maps.googleapis.com/maps/api/geocode/json"
# ?address=Toledo&key=YOUR_API_KEY
# URL = "http://maps.googleapis.com/maps/api/geocode/json"
location = "Dallas"
# PARAMS = {'address':location}
# r = requests.get(url = URL, params = PARAMS)
# data = r.json()
# print data
# https://maps.googleapis.com/maps/api/geocode/json?address=Dallas&key=%20AIzaSyC60BTMhJOp5Q_xrt6MOmIKo6wI-8irhYo
print URl+"?address="+location+"&key=%20AIzaSyC60BTMhJOp5Q_xrt6MOmIKo6wI-8irhYo"


# extracting latitude, longitude and formatted address
# of the first matching location
# latitude = data['results'][0]['geometry']['location']['lat']
# longitude = data['results'][0]['geometry']['location']['lng']
# formatted_address = data['results'][0]['formatted_address']
#
# # printing the output
# print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
#       %(latitude, longitude,formatted_address))
