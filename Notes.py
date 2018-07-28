import tkinter as tk
import time

class Notes():
    instances = []
    label = []
    counter = 0;
  
    def __init__(self, canvas, x0, x1, y0, y1,color):
        self.canvas = canvas
        
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.color = color
        
        self.minimum = 400
        self.maximum = 1000000
        self.xspeed = 1;
        self.yspeed = 2;
        
        if(not self.create()):

            del self
        
    @property
    def _x0(self):
        return self.x0
    
    @_x0.setter
    def _x0(self,value):
        self.x0 = value

    @property
    def _x1(self):
        return self.x1
    
    @_x1.setter
    def _x1(self,value):
        self.x1 = value

    @property
    def _y0(self):
        return self.y0
    
    @_y0.setter
    def _y0(self,value):
        self.y0 = value

    @property
    def _y1(self):
        return self.y1
    
    @_y1.setter
    def _y1(self,value):
        self.y1 = value

    @property
    def _color(self):
        return self.color
    
    @_color.setter
    def _color(self,value):
        self.color = value
        
    def _minimum(self,value):
        self.minimum = value

    def _maximum(self,value):
        self.maximum = value    
                        
    def create(self):
        #self.refractor()
        
        if(not self.border(self.area(),self.minimum,self.maximum)):
            print("Improper size")
            return False
        
        if(not self.collision(self.x0, self.x1, self.y0, self.y1, self.instances)):
            print("A rectangle already exists here")
            return False;

        Notes.counter = Notes.counter + 1;
        self.id = Notes.counter;
                
        self.data = self.canvas.create_rectangle(self.x0,self.y0,self.x1,self.y1, fill=self.color)
        self.label = self.canvas.create_text(((self.x0 + self.x1)/2, (self.y0 + self.y1)/2), text=self.id)
        
        self.instances.append(self) #Add instance to record
        
        return True;
            
    def refractor(self):
        if(self.x1 < self.x0):
            tempX = self.x0
            self.x0 = self.x1
            self.x1 = tempX
        if(self.y1 < self.y0):
            tempY = self.y0
            self.y0 = self.y1
            self.y1 = tempY
    
    def area(self):
        length = self.x1 - self.x0
        width = self.y1 - self.y0
        return length * width
    
    def border(self, area, minimum, maximum):
        
        if not (minimum < (area) < maximum):
            return False;
        
        return True;
    
    def collision(self, x0, x1, y0, y1, rectangles):
        
        for rects in rectangles:
            rX0 = rects.x0
            rX1 = rects.x1
            rY0 = rects.y0
            rY1 = rects.y1
            
            #Check overlapped corner with respect to the created rectangle and then existing rectangle
            if(((rX0 <= x0 <= rX1) & (rY0 <= y0 <= rY1)) | ((x0 <= rX0 <= x1) & (y0 <= rY0 <= y1))): #Top Left
                return False;
            elif(((rX0 <= x1 <= rX1) & (rY0 <= y1 <= rY1)) | ((x0 <= rX1 <= x1) & (y0 <= rY1 <= y1))): #Bottom Right
                return False;          
            elif(((rX0 <= x1 <= rX1) & (rY0 <= y0 <= rY1)) | ((x0 <= rX1 <= x1) & (y0 <= rY0 <= y1))): #Top Right  
                return False;
            elif(((rX0 <= x0 <= rX1) & (rY0 <= y1 <= rY1)) | ((x0 <= rX0 <= x1) & (y0 <= rY1 <= y1))): #Bottom Left
                return False;        

     
            #over lap without corners with respect to the created rectangle
            elif(((rX0 <= x0 <= rX1) & (y0 <= rY0 <= y1)) | ((x0 <= rX0 <= x1) & (rY0 <= y0 <= rY1))): #Top Left Intersection   
                return False; 
            elif(((rX0 <= x1 <= rX1) & (y0 <= rY0 <= y1)) | ((x0 <= rX1 <= x1) & (rY0  <= y1 <= rY1))): #Top Right Intersection 
                return False;
            elif(((rX0 <= x0 <= rX1) & (y0 <= rY1 <= y1)) | ((x0 <= rX0 <= x1) & (rY0  <= y0 <= rY1))): #Bottom Left Intersection  
                return False;
            elif(((rX0 <= x1 <= rX1) & (y0 <= rY1 <= y1)) | ((x0 <= rX1 <= x1) & (rY0  <= y1 <= rY1))): #Bottom Right Intersection   
                return False;
                         
        return True; #return of rectangles are not colliding
    
    
    def move(self):
        yspeed = 2
        xspeed = 1
        while(True):

            self.canvas.move(self.data, xspeed, yspeed)
            self.canvas.move(self.label, xspeed, yspeed)
            pos=self.canvas.coords(self.data)
            
            if(pos[3] >= 500 or pos[1] <= 0):
                yspeed = -yspeed
            if(pos[2] >= 800 or pos[0] <= 0):
                xspeed = -xspeed
                            
            self.canvas.update()
            self.x0 = pos[0]
            self.x1 = pos[1]
            self.y0 = pos[2]
            self.y1 = pos[3]
            
            Notes.instances[self.id - 1].x0 = self.x0
            Notes.instances[self.id - 1].x1 = self.x1
            Notes.instances[self.id - 1].y0 = self.y0
            Notes.instances[self.id - 1].y1 = self.y1
            
            time.sleep(0.01)
        return