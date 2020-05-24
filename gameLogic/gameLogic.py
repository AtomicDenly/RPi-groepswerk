#!/usr/bin/python3                                                                                           

import player as p
from findBetween import find_between
import paho.mqtt.client as paho

def mqqtClient():
        toiletRolls, viruses, carts, players = [], [], [], []
        screenW = 1024
        screenH = 728

        def on_connect(host, port, keepalive):
            #print("Connected")
            pass

        def on_subscribe(client, userdata, mid, granted_qos):
            #print("subscribed")
            pass

        def on_publish(client, userdata, mid):
            #print("published")
            pass

        def on_message(client, userdata, msg):
            mqttmsg = str(msg.payload)
            print("Mqqt msg = " + mqttmsg)
        
        def on_message_players_status(client, userdata, msg):
            strings = msg.payload.splitlines()
            global toiletRolls, viruses, carts
            toiletRolls, viruses, carts = [], [], []
            for s in strings:
                plType = find_between(str(s), "type:", ";")
                x = find_between(str(s), "x:", ";")
                y = find_between(str(s), "y:", ";")
                width = find_between(str(s), "width:", ";")
                height = find_between(str(s), "height:", ";")
                imageUrl = find_between(str(s), "imageUrl:", ";")
                pl = p.logicPlayer(plType= plType,position= p.Cartesian2D(x=float(x), y=float(y)), _width= float(width), _height= float(height), imageUrl=imageUrl)
                players.append(pl)
                if(pl.plType == "toiletRoll"):
                    toiletRolls.append(pl)
                elif(pl.plType == "virus"):
                    viruses.append(pl)
                elif(pl.plType == "cart"):
                    carts.append(pl)
            
        
        def on_message_images_status(client, userdata, msg):
            # mqttmsg = str(msg.payload)
            # print("Mqqt msg = " + mqttmsg)
            pass


        client = paho.Client(client_id="clientId-logic2ea", clean_session=True, userdata=None, protocol=paho.MQTTv31)
        client.on_connect = on_connect
        client.on_subscribe = on_subscribe
        client.on_message = on_message
        client.on_publish = on_publish

        client.message_callback_add('coronahamstergame/gamelogic/gui/player_status', on_message_players_status)
        client.message_callback_add('coronahamstergame/gamelogic/gui/images_status', on_message_images_status)

        # client.connect("broker.mqttdashboard.com", port=1883, keepalive=60)
        client.connect("rasplabo.hopto.org", port=1883, keepalive=60)
        client.subscribe("coronahamstergame/gamelogic/#", qos=1)
        client.loop_start()

        #setup
        client.publish("coronahamstergame/gui/settings", "res:{}x{};".format(screenW, screenH), qos=1)
        client.publish("coronahamstergame/gui/players/delete", "i:all;", qos=1)
        client.publish("coronahamstergame/gui/players/add", "i:last;t:t;", qos=1)
        client.publish("coronahamstergame/gui/players/add", "i:last;t:v;", qos=1)
        client.publish("coronahamstergame/gui/players/add", "i:last;t:c;", qos=1)
        client.publish("coronahamstergame/gui/status", "req:players;", qos=1)
            #get player properties for collision

        def move():
            for p in players:
                if p.plType == "toiletRoll":
                    p.position.x += 1 if p.position.x < screenW else -screenW
                elif p.plType == "virus":
                    p.position.x -= 1 if p.position.x > 0 else -screenW

        def updateGUI():
            for p in players:
                client.publish("coronahamstergame/gui/players/move", "i:{};x:{};y:{};".format(players.index(p), p.position.x, p.position.y), qos=1)

        def collision():
            for t in players:
                if t.plType == "toiletRoll":
                    for v in players:
                        if v.plType == "virus":
                            if t.position.x <= v.position.x <= (t.position.x + t.width) or t.position.x <= (v.position.x + v.width) <= (t.position.x + t.width):
                                if t.position.y <= v.position.y <= (t.position.y + t.height) or t.position.y <= (v.position.y + v.height) <= (t.position.y + t.height):
                                    print("collision")      

        #gameloop
        while True:
            move()
            #collision()
            updateGUI()


mqqtClient()