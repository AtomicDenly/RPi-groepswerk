#!/usr/bin/python3

import tkinter as tk
from time import sleep
import paho.mqtt.client as paho
from threading import Thread
from PIL import Image


window = tk.Tk()
window.geometry("1024x768")
window.title("Corona Hamster Game")

text = tk.Label(window, text="Corona Hamster Game", fg = 'green', bg = 'black', font=("Roboto", 24, "bold"))
text.pack(fill="x")
#text.place(x=100, y=100)
#text.grid(row=1,column=1)

canvas = tk.Canvas(window)
canvas.pack(fill=tk.BOTH, expand = tk.YES,)

toiletRollPhotos = [tk.PhotoImage(file="toiletRoll_100x100.png")]
#photos.append(tk.PhotoImage(file="toiletRoll_50x50.png"))

cartPhotos = [tk.PhotoImage(file="greenShoppingCart.png")]

virusPhotos = [tk.PhotoImage(file="virus.png")]

images = [canvas.create_image( 150, 50, anchor=tk.NW, image=toiletRollPhotos[0])]
images.append(canvas.create_image( 500, 400, anchor=tk.NW, image=cartPhotos[0]))
images.append(canvas.create_image( 900, 50, anchor=tk.NW, image=virusPhotos[0]))

window.mainloop()