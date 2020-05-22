#!/usr/bin/python3

import tkinter as tk
from PIL import Image
import player as p 
from threading import Thread  

players = [p.toiletRoll(), p.virus(), p.cart(), p.toiletRoll(position=p.Cartesian2D(400,200))]
resolution = "1024x768"
update = True
photos=[]
images=[]

def gui():
    window = tk.Tk()
    window.title("Corona Hamster Game")  
    while True:
        global update
        if update:
            global resolution
            window.geometry(resolution)  
            canvas = tk.Canvas(window)
            canvas.pack(fill=tk.BOTH, expand = tk.YES,)
            canvas.delete("all")

            global players
            global photos
            global images
            i = 0
            for pl in players:
                photos.append(tk.PhotoImage(file=pl.imageUrl))
                x = pl.position.x
                y = pl.position.y
                images.append(canvas.create_image(x, y, anchor=tk.NW, image=photos[i]))
                i += 1 
        update = False
        window.update()

    window.mainloop()


import paho.mqtt.client as paho

def mqqtClient():

        def find_between(s, first, last):
            try:
                start = s.index(first) + len(first)
                end = s.index(last, start)
                return s[start:end]
            except ValueError:
                return ""
        
        def on_connect(host, port, keepalive):
            print("Connected")

        def on_subscribe(client, userdata, mid, granted_qos):
            print("subscribed")

        def on_publish(client, userdata, mid):
            print("published")

        def on_message(client, userdata, msg):
            mqttmsg = str(msg.payload)
            print("Mqqt msg = " + mqttmsg + " -------------------------------------------")
        
        def on_message_setting(client, userdata, msg):
            global resolution
            global update
            temp = str(msg.payload)
            resolution = temp[2:-1]
            #check if string has right format
            update = True

        def on_message_p1(client, userdata, msg):
            #message format: "x:788;y:366;"
            global players
            global update
            x = find_between(str(msg.payload), "x:", ";")
            y = find_between(str(msg.payload), "y:", ";")
            
            print(players[1].toString())
            players[1].moveTo(x=float(x), y=float(y))
            print(players[1].toString())
            update = True


        client = paho.Client(client_id="clientId-xslliid1ns", clean_session=True, userdata=None, protocol=paho.MQTTv31)
        client.on_connect = on_connect
        client.on_subscribe = on_subscribe
        client.on_message = on_message
        client.on_publish = on_publish

        client.message_callback_add('coronahamstergame/settings', on_message_setting)
        client.message_callback_add('coronahamstergame/players/1', on_message_p1)
        # client.message_callback_add('coronahamstergame/players/2', on_message_pubip)
        # client.message_callback_add('coronahamstergame/players/3', on_message_temp)
        # client.message_callback_add('coronahamstergame/players/4', on_message_humi)

        client.connect("broker.mqttdashboard.com", port=1883, keepalive=60)
        client.subscribe("coronahamstergame/#", qos=1)
        client.loop_start()

        input("press enter\n")
    
#mqqtClient()
task1 = Thread(target=gui)
task2 = Thread(target=mqqtClient)

task1.start()
task2.start()

#gui()



