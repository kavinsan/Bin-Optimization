
class Optimize():
    
    def __init__(self, canvas, notes):
        self.canvas = canvas
        self.notes = notes
        
    @property
    def _notes(self):
        return self.notes
    
    @_notes.setter
    def _notes(self,value):
        self.notes = value
        
    def sort(self):
        
        list = []
        x0 = 5;
        y0 = 20;
        x1 = 0
        y1 = 0
        
        padX = 4
        padY = 4
        
        count = -1;
        
        for note in self.notes:
            note.moveable = True
            count = count + 1
            if(count == len(self.notes)):
                break;
            if(count == 0):
                x1 = x0 + note.width() + padX
                y1 = y0 + note.height() + padY
                
                #print(("x0: {}, y0: {}, x1: {}, y1: {}").format(x0,y0,x1,y1))
                list.append([x0,y0,x1,y1])
                continue
                
            x0 = x1
            y0 = y0
            x1 = x0 + note.width() + padX
            y1 = y0 + note.height() + padY
                       
            #print(("x0: {}, y0: {}, x1: {}, y1: {}").format(x0,y0,x1,y1))
            list.append([x0,y0,x1,y1])
        
        return list