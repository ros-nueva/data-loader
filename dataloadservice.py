#!/usr/bin/env python2
import urllib2
import rospy
import json
from pubnub import Pubnub
from std_msgs.msg import String

serverURI = "ros-nueva@appspot.com"

pubnub = Pubnub(subscribe_key="sub-c-056c9aec-d84b-11e6-b9cf-02ee2ddab7fe", publish_key="sub-c-056c9aec-d84b-11e6-b9cf-02ee2ddab7fe")

pub = rospy.Publisher('initialization', String)
r = rospy.Rate(10)
current_journey=''

def pub_callback(message, channel):
    data = json.loads(urrlib2.urlopen('%s/journey/%s/get' % (serverURI, message.journeyid)).read()).latest_trip
    trip = json.loads(urllib2.urlopen('%s/trip/%s/get' % (serverURI, data)).read())
    urllib2.urlopen('%s/trip/%s/start' % (serverURI, data))
    trip.start = json.loads(urrlib2.urlopen('%s/room/%s/get' % (serverURI, trip.start)).read())
    trip.dest = json.loads(urrlib2.urlopen('%s/room/%s/get' % (serverURI, trip.dest)).read())
    pub.publish(json.dumps(trip))
    global current_journey
    current_journey=message.journey_id

def pub_error(message):
    print("PUBNUB ERROR: "+ str(message))

def pub_connect(message):
    print("PUBNUB CONNECTED")

def pub_reconnect(message):
    print("PUBNUB RECONNECTED")

def pub_disconnect(message):
    print("PUBNUB DISCONNECTED")

def handle_complete_trip():
    data = json.loads(urrlib2.urlopen('%s/journey/%s/get' % (serverURI, current_journey)).read()).latest_trip
    urllib2.urlopen('%s/trip/%s/complete' % (serverURI, data))
    urllib2.urlopen('%s/trip/%s/start' % (serverURI, data))
    data = json.loads(urrlib2.urlopen('%s/journey/%s/get' % (serverURI, current_journey)).read()).latest_trip
    return CompleteTripResponse(urllib2.urlopen('%s/trip/%s/get' % (serverURI, data)).read())

def data_loader_server():
    rospy.init_node('data_loader_server')
    pubnub.subscribe(channels="unicub", callback=pub_callback, error=pub_error, connect=pub_connect, reconnect=pub_reconnect, disconnect=pub_disconnect)
    complete_trip_service = rospy.Service('complete_trip', CompleteTrip, handle_complete_trip)
    rospy.spin()

if __name__ == "__main__":
    data_loader_server()
