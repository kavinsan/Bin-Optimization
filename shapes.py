import tkinter as tk
from random import randint
import time
from Notes import *

              
class square(tk.Tk):

    colors = ["white", "#363636", "crimson", "#CCCCFF","#E3CF57","beige","#6bf98a"]

    
    def __init__(self):
        tk.Tk.__init__(self)
    
        self.x = self.y = 0
        self.canvas = tk.Canvas(self, width=1000, height=400, cursor="tcross", highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Button-3>", self.on_button_delete)
        self.canvas.bind("<Button-2>", self.on_button_data)
    
        self.canvas.focus_set()
        self.canvas.bind("<Return>", self.generate)
        self.canvas.bind("<BackSpace>", self.deleteAll)
        
        self.canvas.bind('<Motion>', self.position)
        self.resizable(False, False)
        
               
    def position(self, event):
        self.mouseX = event.x
        self.mouseY = event.y
        #print("{} - {}".format(self.mouseX, self.mouseY))
        
    def generate(self, event):

        while(True):
            x0 = randint(0,1000)
            y0 = randint(0,400)
            x1 = randint(0,1000)
            y1 = randint(0,400)
            
            if((x0 == x1) & (y0 == y1)):
                continue;
            
            #Limit the square size minium and/or maximum
            length = x1 - x0
            width = y1 - y0
            area = length * width
            if not (400 < (area) < 40000):
                continue;
    
            #Swap values based on cursor positive-negative position
            if(x1 < x0):
                tempX = x0
                x0 = x1
                x1 = tempX
            if(y1 < y0):
                tempY = y0
                y0 = y1
                y1 = tempY      
                  
            if Notes(self.canvas,x0,x1,y0,y1,self.colors[randint(0,6)]) == None:
                continue
            else:
                break;
        
    def on_button_data(self,event):
        
        rectangles = Notes.instances
        
        if(len(rectangles) == 0):
            print("No Rectangles Exist")
            return

        self.x = event.x
        self.y = event.y
        
        for rects in rectangles:
            if (((self.x > rects.x0) & (self.x < rects.x1)) & ((self.y > rects.y0) & (self.y < rects.y1))):

                print("[ID]: {}, [COLOR]: {}, [AREA]: {}, [x0]: {}, [y0]: {}, [x1]: {}, [y1]: {}".format(rects.id, rects.color, rects.area(), rects.x0, rects.y0, rects.x1, rects.y1))   
                return
        
        #If no rectangles are touched then print them all  
        for rects in rectangles:
            print("[ID]: {}, [COLOR]: {}, [AREA]: {}, [x0]: {}, [y0]: {}, [x1]: {}, [y1]: {}".format(rects.id, rects.color, rects.area(), rects.x0, rects.y0, rects.x1, rects.y1))   
            

    def deleteAll(self,event):
        for rects in Notes.instances:

            data = rects.data
            label = rects.label
            
            print("Deleted [ID]: {}, [COLOR]: {}".format(rects.id, "text"), rects.color)
            self.canvas.delete(data)
            self.canvas.delete(label)
            
        Notes.instances = []
        return
                  
    def on_button_delete(self,event):
        self.x = event.x
        self.y = event.y
        rectangles = Notes.instances
        for index, rects in enumerate(rectangles):
            if(self.x < rects.x0):
                continue
            if(self.x > rects.x1):
                continue
            if(self.y < rects.y0):
                continue
            if(self.y > rects.y1):
                continue

            else:
                data = rects.data
                label = rects.label
                Notes.instances = Notes.instances[:index] + Notes.instances[index+1:]
                print("Deleted [ID]: {}, [COLOR]: {}".format(rects.id, "text"), rects.color)
                self.canvas.delete(data)
                self.canvas.delete(label)
                return
            
    def on_button_press(self, event):
        self.x = event.x
        self.y = event.y
             
    def on_button_release(self, event):
        x0,y0 = (self.x, self.y)
        x1,y1 = (event.x, event.y)
        
        if((x0 == x1) & (y0 == y1)):
            return;
        
        #Swap values based on cursor positive-negative position
        if(x1 < x0):
            tempX = x0
            x0 = x1
            x1 = tempX
        if(y1 < y0):
            tempY = y0
            y0 = y1
            y1 = tempY

        
        Notes(self.canvas,x0,x1,y0,y1,self.colors[randint(0,6)])
        
if __name__ == "__main__":
    
    app = square()
    app.mainloop()