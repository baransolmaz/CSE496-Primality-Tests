import math
from tkinter import *

class App:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("350x500")  # Screen Size(yatay x dikey)
        self.window.resizable(0, 0)
        self.window.title("Primality Tests")  # Pencere ismi
        self.window.iconname("Primality Tests")
        self.window.config(background="gray")
        
        self.input_label = Text_Label(self, "Enter Number",175,25)
        self.entry_box =Entry_Box(self,175,60)

        self.result=Result_Square(self,175,400)
        
        
        # self.result.update_result(False)
class Result_Square:
    def __init__(self,obj,center_x,center_y):
        self.canvas = Canvas(obj.window, height=50, width=100,
                             background="white", highlightthickness=3,highlightbackground="black")
        self.text = self.canvas.create_text(
            52,28, fill="black", text="??", font=('Helvetica 10 bold'))
        self.canvas.place(x=center_x,y=center_y,anchor=CENTER)
        
    
    def get_result(self,bool):
        if bool:
            return "green","Prime"
        else:
            return "red","Not Prime"
         
    def update_result(self,result):
        self.canvas["bg"] , txt = self.get_result(result)
        self.canvas.delete(self.text)
        self.text = self.canvas.create_text(
            52, 28, fill="black", text=txt, font=('Helvetica 10 bold'), anchor=CENTER)
   
   
class Text_Label:
    def __init__(self,obj,txt,_x_,_y_):
        self.label=Label(
            obj.window, background=obj.window["bg"], text=txt, font=('Helvetica 20 bold'))
        self.label.place(x=_x_,y=_y_,anchor=CENTER) 
        

class Entry_Box:
    def __init__(self, obj, _x_, _y_):
        validation = obj.window.register(self.only_numbers)
        self.entry_box = Entry(
            obj.window, background="white", width=20,validate="key",validatecommand=(validation,'%S'), font=('Helvetica 20 normal'))
        self.entry_box.place(x=_x_,y=_y_,anchor=CENTER)
        
        self.submit_button = Button(obj.window, text='Submit', command=self.submit)
        self.submit_button.place(x=_x_-75,y=_y_+40,anchor=CENTER) 
        
        self.clear_button = Button(
            obj.window, text='Clear', command=self.clear)
        self.clear_button.place(x=_x_+75, y=_y_+40, anchor=CENTER)
        

    def only_numbers(self,char):
        return char.isdigit()

    def submit(self):
        value=self.entry_box.get()
        self.entry_box.delete(0,END)
        print(value)
        
    def clear(self):
        self.entry_box.delete(0,END)

if __name__ == "__main__":
    app=App()
    app.window.mainloop()
    