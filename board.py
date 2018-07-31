import tkinter as tk
from random import randint
import time
from Notes import *
from msilib.schema import RadioButton
from Optimize import *
              
class board(tk.Tk):

    colors = ["white", "#363636", "crimson", "#CCCCFF","#E3CF57","beige","#6bf98a"]
    toggle = True;
    translate = False;
    speed = 0.0025
    WIDTH = 500
    HEIGHT = 800
    
    def __init__(self):
        tk.Tk.__init__(self)
        
        #Properties
        self.protocol("WM_DELETE_WINDOW",  self.on_close)
        self.title("Bin Optimization Simulator")
        self.resizable(False, False)
        self.canvas = tk.Canvas(self, width = self.WIDTH, height = self.HEIGHT, cursor="tcross", highlightthickness=2, bg='white', highlightbackground="#585858")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.x = self.y = 0
        
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Button-3>", self.on_button_delete)
        self.canvas.bind("<Button-2>", self.on_button_data)
        self.canvas.bind("<MouseWheel>", self.changeSpeed)
            
        self.canvas.focus_set()
        self.canvas.bind("<Return>", self.generate)
        self.canvas.bind("<BackSpace>", self.deleteAll)
        self.canvas.bind("<p>", self.pause)
        self.canvas.bind("<o>", self.algorithm)
             
        self.canvas.bind('<Motion>', self.position)
        
        #Header labels
        self.countLabel = self.canvas.create_text((self.WIDTH / 2, 10), text="Count: 0",  font='bold')
        self.posLabel = self.canvas.create_text((self.WIDTH - 30, 10), text="0,0",  font='bold')
        self.pauseLabel = self.canvas.create_text((20, 10), text="OFF",  font='bold', fill="red")
    
    def algorithm(self, event):
        optimize = Optimize(self.canvas,Notes.instances)
        list = optimize.sort()
        
        
    def on_close(self): #On close ensure motion functions are closed
        self.translate = False;
        self.destroy()
        
    def changeSpeed(self,event):
        nos = int((event.delta/120)) * 0.0005 * -1
        if((self.speed + nos) <= 0):
            return
        if((self.speed + nos) >= 0.01):
            return
        
        self.speed += nos
            
    def pause(self, event):

        self.translate = not self.translate; 
        if(self.translate):
            self.canvas.itemconfig(self.pauseLabel, fill="green", text="ON")
        else:
            self.canvas.itemconfig(self.pauseLabel, fill="red", text="OFF")
               
        self.canvas.update()
                
        while(self.translate):
            self.move(self.mouseX,self.mouseY)
        
    def move(self, desX0, desY0):
        
        optimize = Optimize(self.canvas,Notes.instances)
        list = optimize.sort()
        count = 0
        
        for rects in Notes.instances:
            desX0 = list[count][0]
            desY0 = list[count][1]
            count = count + 1
            if(not rects.moveable):
                continue
                
            if((rects.x0 == desX0) & (rects.y0 == desY0)):
                rects.moveable = False;
                continue
                
            pos=self.canvas.coords(rects.data)
            x0 = pos[0]
            y0 = pos[1]
            x1 = pos[2]
            y1 = pos[3]

                                
            if(x0 > desX0):
                self.canvas.move(rects.data, -rects.xspeed, 0)
                self.canvas.move(rects.label, -rects.xspeed, 0)
 
            elif(x0 < desX0):
                self.canvas.move(rects.data, rects.xspeed, 0)
                self.canvas.move(rects.label, rects.xspeed, 0)
                    
            if(y0 > desY0):
                self.canvas.move(rects.data, 0, -rects.yspeed)
                self.canvas.move(rects.label, 0, -rects.yspeed)
 
            elif(y0 < desY0):
                self.canvas.move(rects.data, 0, rects.yspeed)
                self.canvas.move(rects.label, 0, rects.yspeed)

            rects.x0 = x0
            rects.y0 = y0
            rects.x1 = x1
            rects.y1 = y1
                                 
        self.canvas.update()
        time.sleep(self.speed)
        
    def position(self, event): #Get the current position of the mouse
        self.mouseX = event.x
        self.mouseY = event.y
        
        text = str(self.mouseX) + "," + str(self.mouseY)
        
        self.canvas.itemconfig(self.posLabel, text=text)
        self.canvas.tag_raise(self.posLabel)
        self.canvas.update()
          
    def generate(self, event): #Generate a random sized and positioned note
        
        while(True):
            x0 = randint(0,self.WIDTH)
            y0 = randint(0,self.HEIGHT)
            x1 = randint(0,self.WIDTH)
            y1 = randint(0,self.HEIGHT)
            
            if((x0 == x1) & (y0 == y1)):
                continue;
            
            #Limit the square size minimize and/or maximum
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
                text = "Count: " + str(len(Notes.instances))
                self.canvas.itemconfig(self.countLabel, text=text)
                self.canvas.tag_raise(self.countLabel)
                self.canvas.update()
                break;

    def deleteAll(self,event):
        for rects in Notes.instances:

            data = rects.data
            label = rects.label
            
            print("Deleted [ID]: {}, [COLOR]: {}".format(rects.id, "text"), rects.color)
            self.canvas.delete(data)
            self.canvas.delete(label)
            
        Notes.instances = []
        text = "Count: " + str(len(Notes.instances))
        self.canvas.itemconfig(self.countLabel, text=text)
        self.canvas.tag_raise(self.countLabel)
        self.canvas.update()
        return
        
    def generateColor(self): #Generate a random color in hex value
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
                
                text = "Count: " + str(len(Notes.instances))
                self.canvas.itemconfig(self.countLabel, text=text)
                self.canvas.tag_raise(self.countLabel)
                self.canvas.update()
                return
            
    def on_button_press(self, event):
        self.x = event.x
        self.y = event.y
        self.x1 = self.x + 1
        self.y1 = self.y + 1
        self.toggle = True;
        
        self.color = self.generateColor()
        #data = self.canvas.create_rectangle(self.x,self.y,self.x1,self.y1, fill="#d9ebf7", outline="#f7feff", width="2") 
        data = self.canvas.create_rectangle(self.x,self.y,self.x1,self.y1, fill=self.color, outline="#f7feff", width="2") 
        
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
        Notes(self.canvas,x0,x1,y0,y1,self.color)
        text = "Count: " + str(len(Notes.instances))
        self.canvas.itemconfig(self.countLabel, text=text)
        self.canvas.tag_raise(self.countLabel)
        self.canvas.update()
        
        
if __name__ == "__main__":
    
    app = board()
    app.mainloop()