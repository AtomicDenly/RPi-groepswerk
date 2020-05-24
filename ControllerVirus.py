#!/usr/bin/python3

import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
segments = (11,4,23,8,7,10,18)

for segment in segments:
  GPIO.setup(segment, GPIO.OUT)
  GPIO.output(segment, False)

score=0

GPIO.add_event_detect(14,GPIO.FALLING, callback=Post, bouncetime=20)
GPIO.add_event_detect(15,GPIO.FALLING, callback=Post, bouncetime=20)

num = {
    (1,1,1,1,1,1,0),
    (0,1,1,0,0,0,0),
    (1,1,0,1,1,0,1),
    (1,1,1,1,0,0,1),
    (0,1,1,0,0,1,1),
    (1,0,1,1,0,1,1),
    (1,0,1,1,1,1,1),
    (1,1,1,0,0,0,0),
    (1,1,1,1,1,1,1),
    (1,1,1,1,0,1,1)}


def on_connect(client, userdata, flags, rc):
  client.subscribe("coronahamstergame/gamelogic/#")

def on_message(client, userdata, msg)
  global score

  if msg.payload[3:5] == b'UP' :
    score+=1
  if msg.payload[3:5] == b'DN' :
    score-=1
  if msg.payload[3:5] == b'RS' :
    score=0
  
  if score<0
    score=0  
  if score>9
    score=9

  if score==0
    for loop in range(0,6)
      GPIO.output(segments[loop],num[0][loop])
  elif score==1
    for loop in range(0,6)
      GPIO.output(segments[loop],num[1][loop])
  elif score==2
    for loop in range(0,6)
      GPIO.output(segments[loop],num[2][loop])
  elif score==3
    for loop in range(0,6)
      GPIO.output(segments[loop],num[3][loop])
  elif score==4
    for loop in range(0,6)
      GPIO.output(segments[loop],num[4][loop])
  elif score==5
    for loop in range(0,6)
      GPIO.output(segments[loop],num[5][loop])
  elif score==6
    for loop in range(0,6)
      GPIO.output(segments[loop],num[6][loop])
  elif score==7
    for loop in range(0,6)
      GPIO.output(segments[loop],num[7][loop])
  elif score==8
    for loop in range(0,6)
      GPIO.output(segments[loop],num[8][loop])
  elif score==9
    for loop in range(0,6)
      GPIO.output(segments[loop],num[9][loop])



def Post(channnel)
  if channel==14 :
    (rc,mid)=client.publish("coronahamstergame/player/virus", "VAR=DN; NAAM=VIR")
    time.sleep(0.2)
  if channel==15 :
    (rc,mid)=client.publish("coronahamstergame/player/virus", "VAR=UP; NAAM=VIR")
    time.sleep(0.2)


client=paho.Client()
client.on_connect=on_connect
client.on_message=on_message
client.connect("broker.mqttdashboard.com",1883,60)


try:
  while True:
    GPIO.output(27 , True)
    client.loop_forever()

finally:
  GPIO.output(27 , False)
  client.loop_stop()
  client.disconnect()
  GPIO.remove_event_detect(14)
  GPIO.remove_event_detect(15)
  GPIO.cleanup()
