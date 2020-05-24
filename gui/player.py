#!/usr/bin/python3

from PIL import Image

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
        #print(self.toString())

    @property
    def height(self):
        im=Image.open(self.imageUrl)
        width, height = im.size
        return height
    
    @property
    def width(self):
        im=Image.open(self.imageUrl)
        width, height = im.size
        return width

    def toString(self):
        return "type:{};x:{};y:{};width:{};height:{};imageUrl:{};".format(type(self).__name__, self.position.x, self.position.y, self.width, self.height, self.imageUrl)

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

class logicPlayer(player): 
    def __init__(self, imageUrl, position, plType, _width, _height):
        self._width = _width
        self._height = _height
        self.plType = plType
        super().__init__(imageUrl, position)

    @property
    def height(self):
        return self._height
    
    @property
    def width(self):
        return self._width

class toiletRoll(player): 
    def __init__(self, imageUrl = "images/toiletRoll_100x100.png", position = Cartesian2D(150,50)):
        super().__init__(imageUrl, position)


class virus(player):    
    def __init__(self, imageUrl = "images/virus.png", position = Cartesian2D(900,50)):
        super().__init__(imageUrl, position)


class cart(player):    
    def __init__(self, imageUrl = "images/greenShoppingCart.png", position = Cartesian2D(500, 400)):
        super().__init__(imageUrl, position)        
