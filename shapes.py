import tkinter as tk
from random import randint
import time

class square(tk.Tk):
    rectangles = [];
    colors = ["white", "#363636", "crimson", "#CCCCFF","#E3CF57","beige","#6bf98a"]
    counter = 0;
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0
        self.canvas = tk.Canvas(self, width=1000, height=400, cursor="tcross")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Button-3>", self.on_button_delete)
        self.canvas.bind("<Button-2>", self.on_button_data)
    
        self.canvas.focus_set()
        self.canvas.bind("<Return>", self.generate)
        self.canvas.bind("<BackSpace>", self.deleteAll)
        
        self.canvas.bind('<Motion>', self.position)
    
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
                  
            if not self.create(x0, x1, y0, y1):
                continue
            else:
                break;
        
    def on_button_data(self,event):
        
        if(len(self.rectangles) == 0):
            print("No Rectangles Exist")
            return

        self.x = event.x
        self.y = event.y
        
        for rects in self.rectangles:
            if (((self.x > rects[1]) & (self.x < rects[3])) & ((self.y > rects[2]) & (self.y < rects[4]))):
                
                print("[ID]: {}, [COLOR]: {}, [AREA]: {}, [x0]: {}, [y0]: {}, [x1]: {}, [y1]: {}".format(self.canvas.itemcget(rects[7], "text"), rects[6], rects[5], rects[1], rects[2], rects[3], rects[4]))   
                return
        
        #If no rectangles are touched then print them all  
        for rects in self.rectangles:
            print("[ID]: {}, [COLOR]: {}, [AREA]: {}, [x0]: {}, [y0]: {}, [x1]: {}, [y1]: {}".format(self.canvas.itemcget(rects[7], "text"), rects[6], rects[5], rects[1], rects[2], rects[3], rects[4]))   
            

    def deleteAll(self,event):
        for index, rects in enumerate(self.rectangles):

            data = rects[0]
            label = rects[7]
            
            print("Deleted [ID]: {}, [COLOR]: {}".format(self.canvas.itemcget(rects[7], "text"), rects[6]))
            self.canvas.delete(data)
            self.canvas.delete(label)
            
        self.rectangles = []
        return
                  
    def on_button_delete(self,event):
        self.x = event.x
        self.y = event.y
        
        for index, rects in enumerate(self.rectangles):
            if(self.x < rects[1]):
                continue
            if(self.x > rects[3]):
                continue
            if(self.y < rects[2]):
                continue
            if(self.y > rects[4]):
                continue

            else:
                data = rects[0]
                label = rects[7]
                self.rectangles = self.rectangles[:index] + self.rectangles[index+1:]
                print("Deleted [ID]: {}, [COLOR]: {}".format(self.canvas.itemcget(rects[7], "text"), rects[6]))
                self.canvas.delete(data)
                self.canvas.delete(label)
                return
            
    def on_button_press(self, event):
        self.x = event.x
        self.y = event.y
        if(len(self.rectangles) <= 0):
            return;
             
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
        
        #Limit the square size minimum and/or maximum
  
        self.create(x0,x1,y0,y1)
        
    def move(self, data, label, id, x0, y0, x1, y1):
        yspeed = 2
        xspeed = 1
        while(True):

            self.canvas.move(data, xspeed, yspeed)
            self.canvas.move(label, xspeed, yspeed)
            pos=self.canvas.coords(data)
            
            if(pos[3] >= 400 or pos[1] <= 0):
                yspeed = -yspeed
            if(pos[2] >= 1000 or pos[0] <= 0):
                xspeed = -xspeed
                            
            self.canvas.update()
            self.rectangles[id][1] = pos[0]
            self.rectangles[id][2] = pos[1]
            self.rectangles[id][3] = pos[2]
            self.rectangles[id][4] = pos[3]
    

            time.sleep(0.01)
        return
    def border(self, area, minimum, maximum):
        if not (minimum < (area) < maximum):
            return False;
        
        return True;
    
    def area(self, x0, x1, y0, y1):
        length = x1 - x0
        width = y1 - y0
        return length * width
        
    def create(self, x0, x1, y0, y1):
        
        area = self.area(x0,x1,y0,y1)
        
        if(not self.border(area, 400,40000)):
            return False
        
        if(not self.collision(x0, x1, y0, y1)):
            print("A rectangle already exists here")
            return False;
        
        #Assign a color  
        newColor = self.colors[randint(0,6)]
        #Create the rectangle
        data = self.canvas.create_rectangle(x0,y0,x1,y1, fill=newColor)
        #Assign a label
        self.counter = self.counter + 1
        text = "[" + str(self.counter) + "]"
        label = self.canvas.create_text(((x0 + x1)/2, (y0+y1)/2), text=text)       
        #Register the rectangle to our array to keep track for events
        #x0 = 1, y0 = 2, x1 = 3, y1 = 4
        self.rectangles.append([data, int(self.canvas.coords(data)[0]),int(self.canvas.coords(data)[1]),x1,y1, area,newColor,label])       
        #self.move(data,label, self.counter - 1, x0,y0,x1,y1)
        return True;
    
    def collision(self, x0, x1, y0, y1):
        
        for rects in self.rectangles:
            rX0 = rects[1]
            rX1 = rects[3]
            rY0 = rects[2]
            rY1 = rects[4]
            
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

if __name__ == "__main__":
    app = square()
    app.mainloop()