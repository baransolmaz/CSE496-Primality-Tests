import math
from tkinter import *
import random
from threading import Thread
from time import sleep

isCarmichael = False
finishedCounter = 0
finishedThreads=[]
thread_list = []
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
        clearGlobals()
        
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
    digit = int(math.log10(n))+1
    print(digit)
    if digit <=13:
        return not isPrime_optimized_basic_method(n)
    elif int(math.log10(n))+1<=25:
        return checkCarmichael_less25digit(n)
    elif int(math.log10(n))+1<=50:
        return checkCarmichael_less50digit(n)
    elif int(math.log10(n))+1 <= 100:
        return checkCarmichael_less100digit(n)
    else:
        return checkCarmichael_greater100digit(n)

def checkCarmichael_less25digit(n):
    main_root = int(math.sqrt(n))+1         # 13-6
    root_4 = int(math.sqrt(main_root))+1    # 7-3
    root_8 = int(math.sqrt(root_4))+1       # 4-2

    print("2nd: ", main_root, "D: ", int(math.log10(main_root))+1)
    print("4th: ", root_4, "D: ", int(math.log10(root_4))+1)
    print("8th: ", root_8, "D: ", int(math.log10(root_8))+1)

    rand_start = random.randint(10,root_8)
    rand_end_8 = random.randint(10,root_8*10)

    start = (main_root)-(root_4+root_8)*rand_start
    end = start+(root_8*root_4)-(root_8*rand_end_8)
    
    if start % 2 == 0:
        start -= 1

    if end % 2 == 0:
        end += 1

    interval = end-start
    thread_num =15
    print("S: ", start, " E: ", end)

    extras = interval % thread_num
    thread_interval = interval//(thread_num)
    print("Interval: ", interval, "T_number: ",thread_num, "T_interval: ", thread_interval)

    global thread_list
    for i in range(thread_num):
        thread_list.append(Thread(target=partial_carmicheal_control, args=(i, n, start, start+thread_interval)))
        start += thread_interval
        if i == thread_num-2:
            thread_interval += extras

    for i in range(thread_num):
        if getIsCarm():
            thread_num = i
            break
        thread_list[i].start()
        removeFinished()

    for i in range(thread_num):
        thread_list[i].join()
        print("Joined: ",i)

    return getIsCarm()
  
def checkCarmichael_less50digit(n):
    main_root = int(math.sqrt(n))+1         # 25-13
    root_4 = int(math.sqrt(main_root))+1    # 13-7
    root_8 = int(math.sqrt(root_4))+1       # 7-4
    root_16 = int(math.sqrt(root_8))+1      # 4-2

    print("2nd: ", main_root, "D: ", int(math.log10(main_root))+1)
    print("4th: ", root_4, "D: ", int(math.log10(root_4))+1)
    print("8th: ", root_8, "D: ", int(math.log10(root_8))+1)
    print("16th: ", root_16, "D: ", int(math.log10(root_16))+1)

    rand_start = random.randint(10, root_16)
    rand_end_16 = random.randint(10, root_16*10)

    start = main_root-(root_4+root_8+root_16)*rand_start
    end = start+(root_16*root_8)-(root_16*rand_end_16)

    if start % 2 == 0:
        start -= 1

    if end % 2 == 0:
        end += 1

    interval = end-start
    thread_num = 30
    print("S: ", start, " E: ", end)

    extras = interval % thread_num
    thread_interval = interval//(thread_num)
    print("Interval: ", interval, "T_number: ",thread_num, "T_interval: ", thread_interval)

    global thread_list
    for i in range(thread_num):
        thread_list.append(Thread(target=partial_carmicheal_control, args=(
            i, n, start, start+thread_interval)))
        start += thread_interval
        if i == thread_num-2:
            thread_interval += extras

    for i in range(thread_num):
        if getIsCarm():
            thread_num = i
            break
        thread_list[i].start()
        sleep(0.05)
        removeFinished()

    for i in range(thread_num):
        thread_list[i].join()
        print("Joined: ", i)

    return getIsCarm()
  
def checkCarmichael_less100digit(n):
    main_root = int(math.sqrt(n))+1         # 50-26
    root_4 = int(math.sqrt(main_root))+1    # 25-13
    root_8 = int(math.sqrt(root_4))+1       # 13-7
    root_16 = int(math.sqrt(root_8))+1      # 7-4
    root_32 = int(math.sqrt(root_16))+1     # 4-2

    print("2nd: ", main_root, "D: ", int(math.log10(main_root))+1)
    print("4th: ", root_4, "D: ", int(math.log10(root_4))+1)
    print("8th: ", root_8, "D: ", int(math.log10(root_8))+1)
    print("16th: ", root_16, "D: ", int(math.log10(root_16))+1)
    print("32th: ", root_32, "D: ", int(math.log10(root_32))+1)
    
    rand_start = random.randint(10, root_32)
    rand_end_32 = random.randint(10, root_32*10)

    start = main_root-((root_4+root_8+root_16+root_32)*rand_start)
    end = start+(root_32*root_16)-(rand_end_32*root_32)

    if start % 2 == 0:
        start -= 1

    if end % 2 == 0:
        end += 1

    interval = end-start
    thread_num = 50
    print("S: ", start, " E: ", end)

    extras = interval % thread_num
    thread_interval = interval//(thread_num)
    print("Interval: ", interval, "T_number: ",thread_num, "T_interval: ", thread_interval)

    global thread_list
    for i in range(thread_num):
        thread_list.append(Thread(target=partial_carmicheal_control, args=(
            i, n, start, start+thread_interval)))
        start += thread_interval
        if i == thread_num-2:
            thread_interval += extras

    for i in range(thread_num):
        if getIsCarm():
            thread_num = i
            break
        thread_list[i].start()
        sleep(0.05)
        removeFinished()

    for i in range(thread_num):
        thread_list[i].join()
        print("Joined: ", i)

    return getIsCarm()

def checkCarmichael_greater100digit(n):
    main_root = int(math.sqrt(n))+1         # 100-51
    root_4 = int(math.sqrt(main_root))+1    # 50-26
    root_8 = int(math.sqrt(root_4))+1       # 25-13
    root_16 = int(math.sqrt(root_8))+1      # 13-7
    root_32 = int(math.sqrt(root_16))+1     # 7-4
    root_64 = int(math.sqrt(root_32))+1     # 4-2
    
    print("2nd: ", main_root, "D: ", int(math.log10(main_root))+1)
    print("4th: ", root_4, "D: ", int(math.log10(root_4))+1)
    print("8th: ", root_8, "D: ", int(math.log10(root_8))+1)
    print("16th: ", root_16, "D: ", int(math.log10(root_16))+1)
    print("32th: ", root_32, "D: ", int(math.log10(root_32))+1)
    print("64th: ", root_64, "D: ", int(math.log10(root_64))+1)
    
    rand_start = random.randint(10, root_64)
    rand_end_64 = random.randint(10, root_64*10)

    start = main_root-(root_4+root_8+root_16+root_32+root_64)*rand_start
    end = start+(root_32*root_64)-(rand_end_64*root_64)

    if start % 2 == 0:
        start -= 1

    if end % 2 == 0:
        end += 1

    interval = end-start
    thread_num = 50
    print("S: ", start, " E: ", end)

    extras = interval % thread_num
    thread_interval = interval//(thread_num)
    print("Interval: ", interval, "T_number: ",
          thread_num, "T_interval: ", thread_interval)

    global thread_list
    for i in range(thread_num):
        thread_list.append(Thread(target=partial_carmicheal_control, args=(
            i, n, start, start+thread_interval)))
        start += thread_interval
        if i == thread_num-2:
            thread_interval += extras

    for i in range(thread_num):
        if getIsCarm():
            thread_num = i
            break
        thread_list[i].start()
        sleep(0.05)
        removeFinished()

    for i in range(thread_num):
        thread_list[i].join()
        print("Joined: ", i)

    return getIsCarm()

def partial_carmicheal_control(index:int,number: int, start: int, end: int):
    print("Basladi:",index,"Finished: ",getCounter())

    if start % 2 == 0:
        start -=1

    if end % 2 == 0:
        end -=1
        
    for k in range(start,end, 2):
        if getIsCarm():
            break
        if math.gcd(number, k) != 1:
            setIsCarm(True)
            break
    
    addFinished(index)
    print("Bitti: ",index)
    return


def getIsCarm():
    global isCarmichael
    return isCarmichael

def setIsCarm(value:bool):
    global isCarmichael
    isCarmichael = value
  
def getCounter():  
    global finishedCounter
    return finishedCounter

def addFinished(index):
    global finishedCounter
    global finishedThreads
    finishedCounter+=1
    finishedThreads.append(index)

def removeFinished():
    global finishedCounter
    global finishedThreads
    global thread_list
    if finishedCounter>0:
        finishedCounter -= 1
        index=finishedThreads[0]
        finishedThreads.remove(index)
        thread_list[index].join()
        print("Joined: ",index)
    
def clearGlobals():
    global finishedCounter
    global finishedThreads
    global thread_list
    
    setIsCarm(False)
    finishedCounter =0
    finishedThreads=[]
    thread_list=[]

if __name__ == "__main__":
    app = App()
    app.window.mainloop()
    # 1000000016531 -13
    # 1000000000000000035000061 -25
    # 9378381824836249332547441 -25
    # 33452526613163807108170062053440751665152000000001 -50
    # 6231720984236661927862601680191594334327223260139907210971108379566305783259160955632448191195213287 -100
    # 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999966671 -100
    # 44531863691195734177338197455569767193298247502066806595979646595136492027235782814594845492097865682056265398300200700471798687479590613927231636475675017034786471249164892858870830712052808191802867