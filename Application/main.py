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
        
        self.result=Result_Square(self,175,400)
        self.result.update_result(TRUE)
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
        
if __name__ == "__main__":
    app=App()
    app.window.mainloop()
    