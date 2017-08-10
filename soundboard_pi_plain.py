#!/usr/bin/python3

"""
This function is to expected to be running on the host machine and will listen
to an mqtt in AWS IoT and when a message is received it will play that message
"""

import paho.mqtt.client as mqtt
import ssl
import json, time
import slackweb
import pygame.mixer
from time import sleep
from sys import exit

slack = slackweb.Slack(url="https://hooks.slack.com/services/xxx/xxx/xxx")

#pygame settings and variables to support the wave files.
pygame.mixer.init(48000, -16, 1, 1024)
pygame.init()

sndA = pygame.mixer.Sound("woohoo.wav")
sndB = pygame.mixer.Sound("mmmbeer.wav")

soundChannelA = pygame.mixer.Channel(1)
soundChannelB = pygame.mixer.Channel(2)


#connection function used to read data from AWS IOT
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("$aws/things/piTractor/shadow/update/accepted")


#Listen for JSON message with tractor function requested
def on_message(client, userdata, msg):
    message_json = json.loads(msg.payload.decode())
    try:

        if message_json['state']['desired']['function'] == "woohoo":
             print("woohoo")
             soundChannelA.play(sndA)
             slack.notify(text=":woohoo:")

        elif message_json['state']['desired']['function'] == "mmmbeer":
             print("mmmbeer")
             soundChannelB.play(sndB)
             slack.notify(text=":beer:")


    except KeyboardInterrupt:
        exit()


#Connect to AWS IoT
client = mqtt.Client(client_id="tractorRasp")
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(ca_certs='/home/pi/soundboard/root-CA.pem',
               certfile='/home/pi/soundboard/xxx-certificate.pem.crt',
               keyfile='/home/pi/soundboard/xxx-private.pem.key',
               tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("xxx.iot.us-west-2.amazonaws.com", 8883, 30)
client.loop_forever()
