#!/usr/bin/python3

class Cartesian2D:
    def __init__(self, x = 0.0, y = 0.0):
        self.x = x
        self.y = y

    def toString(self):
        return "{},{}".format(self.x, self.y)


class player:
    def __init__(self, imageUrl, position = Cartesian2D(0,0)):
        self.position = position
        self.imageUrl = imageUrl

    def toString(self):
        return "{} on position {} with imageUrl '{}'".format(type(self).__name__, self.position.toString(), self.imageUrl)

    def moveTo(self,x,y):
        self.position = Cartesian2D(x=x,y=y)


class toiletRoll(player): 
    def __init__(self, imageUrl = "toiletRoll_100x100.png", position = Cartesian2D(150,50)):
        super().__init__(imageUrl, position)


class virus(player):    
    def __init__(self, imageUrl = "virus.png", position = Cartesian2D(900,50)):
        super().__init__(imageUrl, position)


class cart(player):    
    def __init__(self, imageUrl = "greenShoppingCart.png", position = Cartesian2D(500, 400)):
        super().__init__(imageUrl, position)        