import json
import tweepy
import socket
import re
import requests

ACCESS_TOKEN = '2257758242-bGEWDiMgjqJ0diinLosmjzlFgBeTF2bj40VoumB'
ACCESS_SECRET = 'e1wHHXF0IzU6UHeCawCLE4l7eCYTBJClRACTPc5gILbgg'
CONSUMER_KEY = 'e93ZIf2SOnrwKyVwqPQ1eMUWS'
CONSUMER_SECRET = 'nTCIMxTUe0oLKt9MYiK78Xgj6Ip8ocXNgrLBytc9cMJ7tYMyJP'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

hashtag = '#trump'

TCP_IP = 'localhost'
TCP_PORT = 9001

# https://maps.googleapis.com/maps/api/geocode/json?address=Dallas&key=%20AIzaSyC60BTMhJOp5Q_xrt6MOmIKo6wI-8irhYo

# create sockets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((TCP_IP, TCP_PORT))
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.user.location is not None:
            cleanTweet = self.clean_tweet(status.text)
            # print self.clean_tweet(status.text)
            # print cleanTweet
            # print status.user.location
            URl = "https://maps.googleapis.com/maps/api/geocode/json"+"?address='"+status.user.location+"'&key=%20AIzaSyC60BTMhJOp5Q_xrt6MOmIKo6wI-8irhYo"
            # print URl
            results = requests.get(url= URl)
            data = results.json()
            if len(data['results']) == 0:
                return
            if len(data['results'][0]['address_components']) > 0:
                for x in data['results'][0]['address_components']:
                    latitude = data['results'][0]['geometry']['location']['lat']
                    longitude = data['results'][0]['geometry']['location']['lng']
                    dict = {'text': cleanTweet, 'location': status.user.location, 'coordinates': [latitude, longitude]}
                    finalOutput = json.dumps(dict)
                    print(finalOutput)
                    finalOutput = finalOutput + "\n"
                    conn.send(finalOutput.encode('utf-8'))
                    # if x['long_name'] == 'United States':
                    #     latitude = data['results'][0]['geometry']['location']['lat']
                    #     longitude = data['results'][0]['geometry']['location']['lng']
                    #     dict = {'text': cleanTweet, 'location': status.user.location, 'coordinates': [latitude, longitude]}
                    #     finalOutput = json.dumps(dict)
                    #     print(finalOutput)
                    #     finalOutput = finalOutput + "\n"
                    #     conn.send(finalOutput.encode('utf-8'))

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def on_error(self, status_code):
        if status_code == 420:
            return False
        else:
            print(status_code)

myStream = tweepy.Stream(auth=auth, listener=MyStreamListener())

myStream.filter(track=[hashtag])
