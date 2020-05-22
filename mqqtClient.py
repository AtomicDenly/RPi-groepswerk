#!/usr/bin/python3

import paho.mqtt.client as paho

def on_connect(host, port, keepalive):
    print("Connected")

def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed")

def on_publish(client, userdata, mid):
    print("published")

def on_message(client, userdata, msg):
    mqttmsg = str(msg.payload)
    print("Mqqt msg = " + mqttmsg)

client = paho.Client(client_id="clientId-PizzaHawai", clean_session=True, userdata=None, protocol=paho.MQTTv31)
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

client.connect("broker.mqttdashboard.com", port=1883, keepalive=60)
client.subscribe("testtopic/gui26", qos=1)

client.loop_start()

input("press enter to quit\n")