import math
from tkinter import *
import random

class App:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("350x500")  # Screen Size(yatay x dikey)
        self.window.resizable(0, 0)
        self.window.title("Primality Tests")  # Pencere ismi
        self.window.iconname("Primality Tests")
        self.window.config(background="gray")
        
        self.input_label = Text_Label(self, "Enter Number",175,25)
        self.previous_number = Text_Label(self,"",175,300,30)
        
        self.result_box=Result_Square(self,175,400)
        self.divisor_text = Text_Label(self, "", 175,460)
        
        self.entry_box =Entry_Box(self,175,60)

class Result_Square:
    def __init__(self,obj,center_x,center_y):
        self.canvas = Canvas(obj.window, height=50, width=100,
                             background="white", highlightthickness=3,highlightbackground="black")
        self.text = self.canvas.create_text(
            52,28, fill="black", text="??", font=('Helvetica 10 bold'))
        self.canvas.place(x=center_x,y=center_y,anchor=CENTER)
        
    
    def get_result(self,bool):
        if bool==True:
            return "green","Prime"
        elif bool==False:
            return "red","Not Prime"
        else:
            return "white","??"
             
    def update_result(self,result):
        self.canvas["bg"] , txt = self.get_result(result)
        self.canvas.itemconfigure(self.text,text=txt)  
   
class Text_Label:
    def __init__(self,obj,txt,_x_,_y_,font=20):
        self.label=Label(
            obj.window, background=obj.window["bg"], text=txt, font=('Helvetica '+str(font)+' bold'))
        self.label.place(x=_x_,y=_y_,anchor=CENTER)

    def update_text(self,txt):
        self.label.config(text=txt)
        
class Entry_Box:
    def __init__(self, obj, _x_, _y_):
        validation = obj.window.register(self.only_numbers)
        self.entry_box = Entry(
            obj.window, background="white", width=20,validate="key",validatecommand=(validation,'%S'), font=('Helvetica 20 normal'))
        self.entry_box.place(x=_x_,y=_y_,anchor=CENTER)
        
        self.submit_button = Button(obj.window, text='Submit', command=lambda: self.submit(obj))
        self.submit_button.place(x=_x_-75,y=_y_+40,anchor=CENTER) 
        
        self.clear_button = Button(
            obj.window, text='Clear', command=lambda: self.clear(obj))
        self.clear_button.place(x=_x_+75, y=_y_+40, anchor=CENTER)
        

    def only_numbers(self,char):
        return char.isdigit()

    def submit(self,obj):
        value=self.entry_box.get()
        self.entry_box.delete(0,END)
        if len(value)<=0:
            return
            
        obj.previous_number.update_text(value)
        
        result, divisor = isPrime_fermats_method(int(value), int(value)//3)
        #result, divisor = isPrime_optimized_school_method(int(value))
        
        
        obj.result_box.update_result(result)
        obj.divisor_text.update_text("")
        if result==False:
            obj.divisor_text.update_text("Divisible by "+str(divisor))
        print(value)
        
    def clear(self,obj):
        self.entry_box.delete(0,END)
        obj.previous_number.update_text("")
        obj.divisor_text.update_text("")
        obj.result_box.update_result(-1)

def isPrime_optimized_school_method(number):
    # Corner case
    if (number <= 1):
        return False,number
  
    # Check from 2 to square root of n
    for i in range(2, int(math.sqrt(number)) + 1):
        if (number % i == 0):
            return False,i
    return True,-1

# If n is prime, then always returns true,
# If n is composite than returns false with
# high probability Higher value of k increases
# probability of correct result
def isPrime_fermats_method(number,k):
    # Corner cases
    if number == 1 or number == 4:
        return False, math.sqrt(number)
    elif number == 2 or number == 3:
        return True, -1

    else:  # Try k times
        for i in range(k):

            # Pick a random number in [2..number-2]
            rand = random.randint(2, number - 2)

            # Fermat's little theorem
            if power_fermat(rand, number - 1, number) != 1:
                return False , rand

    return True , -1


def power_fermat(rand, n, p):
    res = 1
    rand = rand % p  # Update 'a' if 'a' >= p

    while n > 0:
        if n % 2:  # If n is odd, multiply 'a' with result
            res = (res * rand) % p
            n = n - 1
        else:
            rand = (rand ** 2) % p
            n = n // 2 

    return res % p


if __name__ == "__main__":
    app=App()
    app.window.mainloop()
    