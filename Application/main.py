import math
from tkinter import *
import random
from threading import Thread
from time import sleep
isCarmichael = 0


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
        
        self.check_box = Check_Box(self,175,135)
        self.entry_box =Entry_Box(self,175,60)
class Check_Box:
    def __init__(self, obj, center_x, center_y):
        self.var = IntVar()
        # c0 = Checkbutton(obj.window, text="School Method", font=('Helvetica 14 normal'), variable=self.var,
        #                 onvalue=0, offvalue=0)
        #c0.place(x=center_x, y=center_y, anchor=CENTER)
        c1 = Checkbutton(obj.window, text="Fermat's Method", font=('Helvetica 14 normal'), variable=self.var,
                         onvalue=0, offvalue=0)
        c1.place(x=center_x, y=center_y, anchor=CENTER)
        c2 = Checkbutton(obj.window, text="Miller-Rabin Method", font=('Helvetica 14 normal'), variable=self.var,
                         onvalue=1, offvalue=1)
        c2.place(x=center_x, y=center_y+30, anchor=CENTER)

    def getSelection(self):
        return self.var.get()


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

    def update_text(self, txt):
        if len(txt) >= 15:
            txt = "~"+txt[0]+"."+txt[1:5]+" * 10^"+str(len(txt)-1)
        self.label.config(text=txt, font=('Helvetica 20 bold'))


class Entry_Box:
    def __init__(self, obj, _x_, _y_):
        validation = obj.window.register(self.only_numbers)
        self.entry_box = Entry(
            obj.window, background="white", width=20, validate="key", validatecommand=(validation, '%S'), font=('Helvetica 20 normal'))
        self.entry_box.place(x=_x_, y=_y_, anchor=CENTER)

        self.submit_button = Button(
            obj.window, text='Submit', command=lambda: self.submit(obj))
        self.submit_button.place(x=_x_-75, y=_y_+40, anchor=CENTER)

        self.clear_button = Button(
            obj.window, text='Clear', command=lambda: self.clear(obj))
        self.clear_button.place(x=_x_+75, y=_y_+40, anchor=CENTER)

    def only_numbers(self, char):
        return char.isdigit()

    def submit(self, obj):
        value = self.entry_box.get()
        self.entry_box.delete(0, END)
        if len(value) <= 0:
            return

        obj.previous_number.update_text(value)

        type = obj.check_box.getSelection()
        iteration = 5
        if type == -1:
            result = isPrime_optimized_basic_method(int(value))
        elif type == 0:
            result = isPrime_fermats_method(int(value), iteration)
        elif type == 1:
            result = isPrime_miller_rabin(int(value), iteration)
        else:
            result = -1

        obj.result_box.update_result(result)
        # if result==False:
        # str=self.getText(type,divisor,int(value))
        # obj.divisor_text.update_text(str)
        print(value)
        
    def getText(self,type,divisor,number=-1):
        if  type== 0:
            return "Divisible by "+str(divisor)
        elif type==1:
            return str(divisor)+"^"+str(number-1)+" %"+str(number)+ "!= 1"
        else:
            return ""
            
    def clear(self,obj):
        self.entry_box.delete(0,END)
        obj.previous_number.update_text("")
        # obj.divisor_text.update_text("")
        obj.result_box.update_result(-1)


def isPrime_optimized_basic_method(number):
    # Corner case
    if (number <= 1):
        return False

    # Check from 2 to square root of n
    for i in range(2, int(math.sqrt(number)) + 1):
        if (number % i == 0):
            return False
    return True

# If n is prime, then always returns true,
# If n is composite than returns false with
# high probability, Higher value of k increases
# probability of correct result
def isPrime_fermats_method(number, k):
    # Corner cases
    if number == 1 or number == 4:
        return False
    elif number == 2 or number == 3:
        return True
    else:  # Try k times
        for i in range(k):
            # Pick a random number in [2..number-2]
            rand = random.randint(2, number - 2)

            # Fermat's little theorem
            if power(rand, number - 1, number) != 1:
                return False
    
    if isCarmichaelNumber(number):
        return False
    
    return True

def isPrime_miller_rabin(number, k):

    # Corner cases
    if (number <= 1 or number == 4):
        return False, 0
    if (number <= 3):
        return True, -1

    # Find r such that n = 2^d * r + 1 for some r >= 1
    d = number - 1
    while (d % 2 == 0):
        d //= 2

    # Iterate given number of 'k' times
    for i in range(k):
        if (millerTest(d, number) == False):
            return False, d

    return True, -1


def millerTest(d, number):

    # Pick a random number in [2..n-2]
    # Corner cases make sure that n > 4
    a = 2 + random.randint(1, number - 4)

    # Compute a^d % n
    x = power(a, d, number)

    if (x == 1 or x == number - 1):
        return True

    # Keep squaring x while one of the following doesn't happen
    # (i) d does not reach n-1
    # (ii) (x^2) % n is not 1
    # (iii) (x^2) % n is not n-1
    while (d != number - 1):
        x = (x * x) % number
        d *= 2

        if (x == 1):
            return False
        if (x == number - 1):
            return True

    # Return composite
    return False

#Returns (Rand^n) % number
def power(rand, n, number):
    res = 1
    rand = rand % number  # Update 'a' if 'a' >= p

    while n > 0:
        if n % 2:  # If n is odd, multiply 'a' with result
            res = (res * rand) % number
            n = n - 1
        else:
            rand = (rand ** 2) % number
            n = n // 2

    return res % number


def isCarmichaelNumber(n):
    main_root = root_4 = root_8 = 1
    main_root = int(math.sqrt(n))+1         # 200-100-50
    root_4 = int(math.sqrt(main_root))+1    # 100-50-25
    root_8 = int(math.sqrt(root_4))+1       # 50-25-13  
    root_16 = int(math.sqrt(root_8))+1      # 25-13-7
    root_32 = int(math.sqrt(root_16))+1     # 13-7-4
    print("2nd: ", main_root, "D: ", int(math.log10(main_root))+1)  
    print("4th: ", root_4, "D: ", int(math.log10(root_4))+1)  
    print("8th: ", root_8, "D: ", int(math.log10(root_8))+1)  
    print("16th: ", root_16, "D: ", int(math.log10(root_16))+1)  
    print("32nd: ", root_32, "D: ", int(math.log10(root_32))+1)
    
    rand =1
    rand_start_4 = rand_start_8 = rand_start_16 = rand_start_32= 0
    
    if root_8 > 5:
        rand = random.randint(root_4, main_root)
        rand_start_4 = random.randint(root_8, root_4)
        rand_start_8 = random.randint(root_16, root_8)
        rand_start_16 = random.randint(root_32, root_16)
        rand_start_32 = random.randint(2, root_32)
        
        rand_end_4 = random.randint(rand_start_4//4, root_4//2)
        rand_end_8 = random.randint(rand_start_8//4, root_8//2)
        rand_end_16 = random.randint(rand_start_16//4, root_16//2)
        rand_end_32 = random.randint(rand_start_32, root_32)

    start = (main_root)
    start -= (rand_start_4*root_4)+(rand_start_8*root_8)+(rand_start_16*root_16)+(rand_start_32*root_32)
    end = start+(root_16)-(rand_end_32*root_32)#+(rand_end_4*root_4)+(rand_end_8*root_8)
    
    print("S: ", start, " E: ", end)
    if start%2 == 0:
        start -= 1
        
    if end % 2 == 0:
        end += 1

    interval=end-start
    if int(math.log10(interval))<5:
        thread_num=1
    else:
        thread_num = (int(math.log10(interval))+1)**3
    extras = interval%thread_num
    thread_interval=interval//thread_num
    print("Interval: ",interval,"T_number: ",thread_num,"T_interval: ",thread_interval)
    print(int(math.log10(start))+1," ", int(math.log10(interval))+1)
    thread_list=[]
    for i in range(thread_num):
        thread_list.append(Thread(target=partial_carmicheal_control, args=(n,start,start+thread_interval)))
        #thread oluştur
        
        start+=thread_interval
        if i== thread_num-2:
            thread_interval+=extras
    
    for i in range(thread_num):
        if getIsCarm():
            thread_num=i
            break
        thread_list[i].start()
        sleep(0.01)
        
    for i in range(thread_num):
        thread_list[i].join()
        #sleep(0.01)
        
    return getIsCarm()


def partial_carmicheal_control(number: int, start: int, end: int):
    print("I: ", number, " S: ", start, " E: ", end)
    if start % 2 == 0:
        start += 1

    if end % 2 == 0:
        end -= 1
        
    for k in range(start,end, 2):
        if math.gcd(6, k) != 1:
            continue
        if getIsCarm():
            return
        if math.gcd(number, k) != 1:
            setIsCarm(True)
            return
    
    return


def getIsCarm():
    global isCarmichael
    return isCarmichael

def setIsCarm(value:bool):
    global isCarmichael
    isCarmichael = value

    
if __name__ == "__main__":
    app = App()
    app.window.mainloop()
    # 1000000016531
    # 6231720984236661927862601680191594334327223260139907210971108379566305783259160955632448191195213287
    # 44531863691195734177338197455569767193298247502066806595979646595136492027235782814594845492097865682056265398300200700471798687479590613927231636475675017034786471249164892858870830712052808191802867