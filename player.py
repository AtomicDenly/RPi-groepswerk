#!/usr/bin/python3

class Cartesian2D:
    def __init__(self, x = 0.0, y = 0.0):
        self.x = x
        self.y = y

    def toString(self):
        return "{},{}".format(self.x, self.y)


class player:
    def __init__(self, imageUrl ="", position = Cartesian2D(0,0)):
        self.position = position
        self.imageUrl = imageUrl
        #print(self.toString())

    def toString(self):
        return "{} on position {} with imageUrl '{}'".format(type(self).__name__, self.position.toString(), self.imageUrl)

    def moveTo(self,x :float,y :float):
        self.position = Cartesian2D(x=x,y=y)
    
    def moveAmount(self, x=0, y=0):
        self.position.x += x
        self.position.y += y
    
    # def drawOnCanvas(self, canvas):
    #     print("drawing: " + type(self).__name__)
    #     print(canvas.__repr__())
    #     photoP = tk.PhotoImage(file=self.imageUrl)
    #     return canvas.create_image(self.position.x, self.position.y, anchor = tk.NW, image=photoP)


class toiletRoll(player): 
    def __init__(self, imageUrl = "toiletRoll_100x100.png", position = Cartesian2D(150,50)):
        super().__init__(imageUrl, position)


class virus(player):    
    def __init__(self, imageUrl = "virus.png", position = Cartesian2D(900,50)):
        super().__init__(imageUrl, position)


class cart(player):    
    def __init__(self, imageUrl = "greenShoppingCart.png", position = Cartesian2D(500, 400)):
        super().__init__(imageUrl, position)        