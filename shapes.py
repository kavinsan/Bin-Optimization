import tkinter as tk
from random import randint
import time
from Notes import *

              
class square(tk.Tk):

    colors = ["white", "#363636", "crimson", "#CCCCFF","#E3CF57","beige","#6bf98a"]
    toggle = True;
    translate = False;
    speed = 0.0025
    WIDTH = 500
    HEIGHT = 800
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.protocol("WM_DELETE_WINDOW",  self.on_close)
        self.title("Bin Optimization Simulator")
  
        self.x = self.y = 0
        self.canvas = tk.Canvas(self, width = self.WIDTH, height = self.HEIGHT, cursor="tcross", highlightthickness=0)
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
        
        self.posLabel = self.canvas.create_text((self.WIDTH - 30, 10), text="",  font='bold')
        self.pauseLabel = self.canvas.create_text((20, 10), text="OFF",  font='bold', fill="red")

        self.canvas.bind("<p>", self.go)
        self.canvas.bind("<MouseWheel>", self.changeSpeed)
    
    def on_close(self):
        self.translate = False;
        self.destroy()
        
    def changeSpeed(self,event):
        nos = int((event.delta/120)) * 0.0005 * -1
        if((self.speed + nos) <= 0):
            return
        if((self.speed + nos) >= 0.01):
            return
        
        self.speed += nos
        
    def go(self, event):
        yspeed = 2
        xspeed = 1
        self.translate = not self.translate; 
        if(self.translate):
            self.canvas.itemconfig(self.pauseLabel, fill="green", text="ON")
        else:
            self.canvas.itemconfig(self.pauseLabel, fill="red", text="OFF")
               
        self.canvas.update()
        
        while(self.translate):
            for rects in Notes.instances:

                pos=self.canvas.coords(rects.data)
                    
                if(pos[3] >= 800 or pos[1] <= 0):
                    rects.yspeed = -rects.yspeed

                if(pos[2] >= 500 or pos[0] <= 0):
                    rects.xspeed = -rects.xspeed
                    
                self.canvas.move(rects.data, rects.xspeed, rects.yspeed)
                self.canvas.move(rects.label, rects.xspeed, rects.yspeed)
                
                rects.x0 = pos[0]
                rects.y0 = pos[1]
                rects.x1 = pos[2]
                rects.y1 = pos[3]
                                 
            self.canvas.update()
            time.sleep(self.speed)

                 
    def position(self, event):
        self.mouseX = event.x
        self.mouseY = event.y
        #print("{} - {}".format(self.mouseX, self.mouseY))
        text = str(self.mouseX) + "," + str(self.mouseY)
        
        self.canvas.itemconfig(self.posLabel, text=text)
        self.canvas.tag_raise(self.posLabel)
        self.canvas.update()
          
    def generate(self, event):

        while(True):
            x0 = randint(0,self.WIDTH)
            y0 = randint(0,self.HEIGHT)
            x1 = randint(0,self.WIDTH)
            y1 = randint(0,self.HEIGHT)
            
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
                  
            if Notes(self.canvas,x0,x0 + 50,y0,y0 + 50,self.generateColor()) == None:
                continue
            else:
                break;
    
    def generateColor(self):
        count = 0;
        color = "#"
        while(count < 3):
            val = hex(randint(0,255))[2:]
            if(len(val) <= 1):
                color += str(0) + val
                count = count + 1;
            else:
                color += val
                count = count + 1;
        
        return color
        
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
        self.x1 = self.x + 1
        self.y1 = self.y + 1
        self.toggle = True;
        
        
        data = self.canvas.create_rectangle(self.x,self.y,self.x1,self.y1, fill=None, outline="#fcaf62", width="2") 
        
        while(self.toggle == True):
            self.canvas.coords(data, self.x, self.y, self.mouseX,self.mouseY)
            self.canvas.update()
            
        self.canvas.delete(data)
        
    def on_button_release(self, event):
        
        self.toggle = False;
        
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
            
        if((x1 > self.WIDTH) | (x0 < 0) | (y0 < 0) | (y1 > self.HEIGHT)):
            return
                   
        #Notes(self.canvas,x0,x1,y0,y1,self.colors[randint(0,6)])
        Notes(self.canvas,x0,x1,y0,y1,self.generateColor())
        
if __name__ == "__main__":
    
    app = square()
    app.mainloop()