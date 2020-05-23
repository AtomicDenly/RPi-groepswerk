#!/usr/bin/python3

#
# ToDo: -send player status or image on request
#       -split up in different files + main function
#       -setup broker connection
#       -terminate program when clicking 'x'
#       -testing
#

import tkinter as tk
from PIL import Image
import player as p 
from threading import Thread  

players = [p.toiletRoll(), p.virus(), p.cart()]
resolution = "1024x768"
update = True
photos=[]
images=[]

def gui():
    window = tk.Tk()
    window.title("Corona Hamster Game")
    window.resizable(False,False)
    canvas = tk.Canvas(window)

    while True:
        global update
        if update:
            global resolution
            window.geometry(resolution)  
            #canvas.configure(width= 1024, height=768)
            canvas.pack(fill=tk.BOTH, expand = tk.YES)
            # canvas.delete("all")
             

            global players
            global photos
            global images
            images = []
            photos = []
            i = 0
            for pl in players:
                print(pl.toString())
                photos.append(tk.PhotoImage(file=pl.imageUrl))
                # x = pl.position.x
                # y = pl.position.y
                # images.append(canvas.create_image(pl.position.x, pl.position.y, anchor=tk.NW, image=photos[i]))
                canvas.create_image(pl.position.x, pl.position.y, anchor=tk.NW, image=photos[i])
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
            #print("Connected")
            pass

        def on_subscribe(client, userdata, mid, granted_qos):
            #print("subscribed")
            pass

        def on_publish(client, userdata, mid):
            print("published")

        def on_message(client, userdata, msg):
            mqttmsg = str(msg.payload)
            print("Mqqt msg = " + mqttmsg)
        
        def on_message_setting(client, userdata, msg):
            #message format: "1024x768"
            global resolution
            global update
            temp = str(msg.payload)
            resolution = temp[2:-1]
            update = True

        def on_message_players_m(client, userdata, msg):
            #message format: "i:1;x:788;y:366;" i=player index, x= x position, y = y position,
            global players
            global update
            pIndex = find_between(str(msg.payload), "i:", ";")
            x = find_between(str(msg.payload), "x:", ";")
            y = find_between(str(msg.payload), "y:", ";")
            players[int(pIndex)].moveTo(x=float(x), y=float(y))
            update = True
        
        def on_message_players_d(client, userdata, msg):
            #message format: "i:1;" or "i:all;" i=player index or "all"
            global players
            global update
            pIndex = find_between(str(msg.payload), "i:", ";")
            if pIndex == "all":
                players = []
            else:
                players.remove(int(pIndex))
            
            update = True
        
        def on_message_players_a(client, userdata, msg):
            #message format: "i:1;t:t;" options for i = index or "last" 
            #                           options for t: t = toiletroll, v=virus, c=cart, options for p = index or "last"
            global players
            global update
            pIndex = find_between(str(msg.payload), "i:", ";")
            playerType = find_between(str(msg.payload), "t:", ";")
            
            if playerType == "t":
                player = p.toiletRoll()
            elif playerType == "v":
                player = p.virus()
            elif playerType == "c":
                player = p.cart
                
            if pIndex == "last":
                    players.append(player)
            else:
                players.index(int(pIndex),player)
            
            update = True
        
        def on_message_players_url(client, userdata, msg):
            #message format: "i:1;url:"existingImageurl";" 
            #                           options for i: index 
            #                           options for url: url for image
            global players
            global update
            pIndex = find_between(str(msg.payload), "i:", ";")
            url = find_between(str(msg.payload), "url:", ";")
            
            players[int(pIndex)].imageUrl = url
            
            update = True

        def on_message_status(client, userdata, msg):
            #message format: "request:image_sizes;" or "request:player_status;"
            global players
            global update
            pIndex = find_between(str(msg.payload), "p:", ";")
            playerType = find_between(str(msg.payload), "t:", ";")
            
            if playerType == "t":
                player = p.toiletRoll()
            elif playerType == "v":
                player = p.virus()
            elif playerType == "c":
                player = p.cart
                
            if pIndex == "last":
                    players.append(player)
            else:
                players.index(int(pIndex),player)
            
            update = True

        client = paho.Client(client_id="clientId-gui2ea", clean_session=True, userdata=None, protocol=paho.MQTTv31)
        client.on_connect = on_connect
        client.on_subscribe = on_subscribe
        client.on_message = on_message
        client.on_publish = on_publish

        client.message_callback_add('coronahamstergame/gui/settings', on_message_setting)
        client.message_callback_add('coronahamstergame/gui/players/move', on_message_players_m)
        client.message_callback_add('coronahamstergame/gui/players/delete', on_message_players_d)
        client.message_callback_add('coronahamstergame/gui/players/add', on_message_players_a)
        client.message_callback_add('coronahamstergame/gui/players/changeurl', on_message_players_url)
        client.message_callback_add('coronahamstergame/gui/status', on_message_status)

        client.connect("broker.mqttdashboard.com", port=1883, keepalive=60)
        client.subscribe("coronahamstergame/gui/#", qos=1)
        client.loop_start()

        input("press enter\n")
    
#mqqtClient()
task1 = Thread(target=gui)
task2 = Thread(target=mqqtClient)

task1.start()
task2.start()

#gui()



