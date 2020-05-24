#!/usr/bin/python3

#
# ToDo: - [Done] send player status or image on request
#       - [Done] make list of local images and their sizes + maybe safe them in dedicated folder
#       - [unsuccesfull] split up in different files + main function
#       - [Done] terminate program when clicking 'x'
#       - [Done] give player width and height
#       - [Done] als afbeelding veranderd dan moet height en width ook veranderen bij player 
#       - [Done] setup broker connection
#       - [done] testing
#

import tkinter as tk
from PIL import Image
import player as p 
from threading import Thread 
import glob 
from findBetween import find_between

players = [] #[p.toiletRoll(), p.virus(), p.cart()]
resolution = ""
update = True
photos, images= [], []
score = [0,0]

def getImageSizesAsString():
    imageInfo = ""
    i = 0
    for filename in glob.glob('images/*.png'): 
        im=Image.open(filename)
        width, height = im.size
        imageInfo += "i:{};filename:{};width:{};height:{};\n".format(i,filename, width, height)
        i += 1
    return imageInfo

def gui():
    window = tk.Tk()
    window.title("Corona Hamster Game")
    window.resizable(False,False)
    canvas = tk.Canvas(window)

    while True:
        global update
        if update:
            canvas.delete("all")
            global resolution
            window.geometry(resolution)  
            canvas.pack(fill=tk.BOTH, expand = tk.YES)
 
            global players, photos, images, score
            photos, images= [], []
            i = 0
            for pl in players:
                #print(pl.toString())
                canvas.create_text(pl.position.x-10, pl.position.y+10, text= str(i+1))
                photos.append(tk.PhotoImage(file=pl.imageUrl))
                canvas.create_image(pl.position.x, pl.position.y, anchor=tk.NW, image=photos[i])
                canvas.create_text(50, 30, text= "Score\nHamsteraars: {}\nVirus: {}".format(score[0], score[1]))
                i += 1 
        update = False
        window.update()
    window.mainloop()

import paho.mqtt.client as paho

def mqqtClient():
        
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
            #message format: "res:1024x768";
            global resolution
            global update
            resolution = find_between(str(msg.payload), "res:", ";")
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
                players.pop(int(pIndex))
            
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
                player = p.cart()   
                
            if pIndex == "last":
                    players.append(player)
            else:
                players.insert(int(pIndex),player)
            
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
        
        def on_message_score(client, userdata, msg):
            #message format: "score0:2;score1:4;
            global score
            global update
            sc0 = find_between(str(msg.payload), "score0:", ";")
            sc1 = find_between(str(msg.payload), "score1:", ";")
            
            score = [int(sc0), int(sc1)]
            
            update = True

        def on_message_status(client, userdata, msg):
            #message format: "req:images;" for image sizes or "req:players;" for player status
            global players
            global update
            command  = find_between(str(msg.payload), "req:", ";")
            
            if command == "images":
                client.publish("coronahamstergame/gamelogic/gui/images_status", getImageSizesAsString(),qos=1)
            elif command == "players":
                playerstats = ""
                i = 0
                for p in players:
                    playerstats += "i:{};".format(i) + p.toString() + "\n"
                    i += 1
                client.publish("coronahamstergame/gamelogic/gui/player_status", playerstats,qos=1)

        client = paho.Client(client_id="clientId-gui2ea", clean_session=True, userdata=None, protocol=paho.MQTTv31)#unique client_id is required
        client.on_connect = on_connect
        client.on_subscribe = on_subscribe
        client.on_message = on_message
        client.on_publish = on_publish

        client.message_callback_add('coronahamstergame/gui/settings', on_message_setting)
        client.message_callback_add('coronahamstergame/gui/players/move', on_message_players_m)
        client.message_callback_add('coronahamstergame/gui/players/delete', on_message_players_d)
        client.message_callback_add('coronahamstergame/gui/players/add', on_message_players_a)
        client.message_callback_add('coronahamstergame/gui/players/changeurl', on_message_players_url)
        client.message_callback_add('coronahamstergame/gui/score', on_message_score)
        client.message_callback_add('coronahamstergame/gui/status', on_message_status)

        client.connect("broker.mqttdashboard.com", port=1883, keepalive=60)
        # client.connect("rasplabo.hopto.org", port=1883, keepalive=60)
        client.subscribe("coronahamstergame/gui/#", qos=1)
        client.loop_start()


task1 = Thread(target=gui)
# task2 = Thread(target=mqqtClient)

task1.start()
# task2.start()

mqqtClient()

