#!/usr/bin/python3                                                                                           

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
        
        def on_message_players_status(client, userdata, msg):
            pass
        
        def on_message_images_status(client, userdata, msg):
           pass


        client = paho.Client(client_id="clientId-logic2ea", clean_session=True, userdata=None, protocol=paho.MQTTv31)
        client.on_connect = on_connect
        client.on_subscribe = on_subscribe
        client.on_message = on_message
        client.on_publish = on_publish

        client.message_callback_add('coronahamstergame/gamelogic/gui/player_status', on_message_players_status)
        client.message_callback_add('coronahamstergame/gamelogic/gui/images_status', on_message_images_status)

        client.connect("broker.mqttdashboard.com", port=1883, keepalive=60)
        # client.connect("rasplabo.hopto.org", port=1883, keepalive=60)
        client.subscribe("coronahamstergame/gamelogic/#", qos=1)
        client.loop_start()

        #setup
        client.publish("coronahamstergame/gui/players/delete", "i:all;", qos=1)
        client.publish("coronahamstergame/gui/players/add", "i:last;t:t;", qos=1)
        client.publish("coronahamstergame/gui/players/add", "i:last;t:v;", qos=1)
        client.publish("coronahamstergame/gui/players/add", "i:last;t:c;", qos=1)
            #get player properties for collision

        #gameloop moet in thread
        xOffset, x1, x2 = 1, 0, 1024
        while True:
            x1 += xOffset
            x2 -= xOffset
            client.publish("coronahamstergame/gui/players/move", "i:0;x:{};y:350;".format(x1), qos=1)
            client.publish("coronahamstergame/gui/players/move", "i:1;x:{};y:350;".format(x2), qos=1)


mqqtClient()