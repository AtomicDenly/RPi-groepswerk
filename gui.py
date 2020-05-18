#!/usr/bin/python3

import tkinter as tk
from time import sleep
import paho.mqtt.client as paho
from threading import Thread
from PIL import Image
import player as p


window = tk.Tk()
window.geometry("1024x768")
window.title("Corona Hamster Game")

text = tk.Label(window, text="Corona Hamster Game", fg = 'green', bg = 'black', font=("Roboto", 24, "bold"))
text.pack(fill="x")
#text.place(x=100, y=100)
#text.grid(row=1,column=1)

canvas = tk.Canvas(window)
canvas.pack(fill=tk.BOTH, expand = tk.YES,)

players = [p.toiletRoll(), p.virus(), p.cart(), p.toiletRoll(position=p.Cartesian2D(400,200))]
photo1 = tk.PhotoImage(file=players[0].imageUrl)
photo2 = tk.PhotoImage(file=players[1].imageUrl)
photo3 = tk.PhotoImage(file=players[2].imageUrl)

images = [canvas.create_image(players[0].position.x,players[0].position.y, anchor = tk.NW, image=photo1)]
images.append(canvas.create_image(players[1].position.x,players[1].position.y, anchor = tk.NW, image=photo2))
images.append(canvas.create_image(players[2].position.x,players[2].position.y, anchor = tk.NW, image=photo3))


for pl in players:
    photo = tk.PhotoImage(file=pl.imageUrl)
    x = pl.position.x
    y = pl.position.y
    images.append(canvas.create_image(x, y, anchor=tk.NW, image=photo))


#images.append(canvas.create_image(players[0].position.x,players[0].position.y, anchor = tk.NW, image=tk.PhotoImage(file="toiletRoll_100x100.png")))
window.mainloop()