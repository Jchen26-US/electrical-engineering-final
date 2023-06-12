import tkinter as tk
from tkinter import *
import pyautogui
import time 
import serial


class RITO_ALARM:
    def __init__(self):
        #Window checker 
        self.RunP = False
        self.Windows = []
        self.count = 0 
        self.target_list = []
        self.cycle_count = 0 

        self.Setup_appdisplay()
        
    def start_serial(self,Port, Baudrate, Timeout): #starts serial connection
        self.ard = serial.Serial(port = Port, baudrate = Baudrate, timeout = Timeout)
    
    def Comm(self, time_threshold): #time_threshold should be in seconds
        if (self.count > time_threshold):
            self.ard.write("s".encode())
        elif (self.count < time_threshold):
            self.ard.write("c".encode())
#app start up, runs once
    
    def Setup_appdisplay(self):
        self.root = tk.Tk()
        self.root.title("Number Updater")  # Set the window title
        self.root.geometry(str(self.root.winfo_screenwidth())+ "x" + str(int(self.root.winfo_screenheight())-100))  # Set the window size
        self.label = tk.Label(self.root, text = "enter target window", font = ("Arial",20))
        self.label.grid(row= 0 ,column=0)
        self.root.configure(bg = "beige")
        
        self.target_window = tk.StringVar()
        self.timethreshold = tk.IntVar()

        self.target_input = tk.Entry(self.root, textvariable = self.target_window)
        self.btn_add_to_list = Button(self.root, text = "add to list",fg = "green",
            command = self.add_to_list, font = ("Arial", 20))
        self.btn_start = Button(self.root, text = "press to start" ,
             fg = "red", command=self.clicked, font = ("Arial", 20))
        self.list_display = tk.Label(self.root, text = self.target_list, font = ("Arial", 20))

        self.timerequest = tk.Entry(self.root, textvariable = self.timethreshold)
        self.timerequest_label = tk.Label(self.root, text = "Enter time limit here(seconds): ")
        self.target_input.grid(row = 0, column = 1)
        self.btn_add_to_list.grid(row = 0, column = 2)
        self.btn_start.grid(row=1, column=2)
        self.list_display.grid(row = 0, column = 4)
        self.timerequest.grid(row = 3, column = 2)
        self.timerequest_label.grid(row = 3, column = 1)
        
        
    def Window_check(self):     #gets list of all open windows and returns a counter for number of times window appears in list
        self.cycle_count += 1
        for x in pyautogui.getAllWindows():  #pyautogui command that gets list of all current windows
            self.Windows.append(x.title) #adds every list to a windows list in order to check if target window is in list
        for x in range(len(self.target_list)): # repeats for each target window
            if self.count == self.cycle_count:  #allows only one detection per cycle
                    continue
            if self.target_list[x-1] in self.Windows: # if target window is in gotten list
                self.count += 1
                #print(count) #^
                #self.target_list.append(self.target_window) #adds 1 character to target list  used for testing
                #print(target_list) #prints to show amount of terms in target_list
            else: 
                self.count = 0 #sets count to zero if target not in list
        self.Windows.clear()

    #print(Windows) #testing
    #print(RunP)    #testing


    ##BUTTONS 
    def clicked(self): #runs once
        self.btn_start.destroy()
        self.btn_add_to_list.destroy()
        self.target_input.destroy()
        self.timerequest.destroy()
        self.timerequest_label.destroy()



        self.plain_text = Label(self.root, text = "TARGET WINDOWS", bg = "red", font = ("Arial",20), fg = "purple")
        self.plain_text.grid(row = 1, column = 0)
        self.list_display.grid(row=2, column = 0)
        self.list_display.configure(bg = "red", text = self.target_list, font = ("Arial",20), fg = "purple")
        self.label.configure(text = "PROGRAM IS RUNNING", fg = "yellow", font = ("Arial", 20), bg = "red")
        self.root.configure(bg = "red")
        
        self.count_L  = Label(self.root , text = "Counter #", fg = "green", bg = "red", font  = ("Arial",20))
        self.cycle_L = Label(self.root, text= 'Cycle #', fg = "blue", bg = "red", font = ("Arial", 20))
        self.count_disp = Label(self.root, text = self.count, bg = "red", font = ("Arial", 20), fg = "green")
        self.cycle_disp = Label(self.root, text = self.cycle_count, bg = "red", font = ("Arial", 20), fg = "blue")
        


        self.count_L.grid(row = 0, column = 2)
        self.cycle_L.grid(row = 0, column = 3)
        self.count_disp.grid(row = 1, column = 2)
        self.cycle_disp.grid(row = 1, column = 3)

        self.update()

    def add_to_list(self):
        self.target_list.append(self.target_window.get())
        self.target_window.set("")
        self.list_display.config(text = self.target_list)
    
    def update(self):  #repeat
        self.Window_check()
        self.count_disp.configure(text = "Windows have been detected " + str(self.count) + " times")
        self.cycle_disp.configure(text = "Program has been running for " + str(self.cycle_count) + " seconds")
        self.Comm(self.timethreshold.get())
        self.root.after(self.update)  # Schedule the next update after 1 second
    
    #start command
    def start(self):
        self.start_serial("COM5", 9600, .1)

        self.root.mainloop()


Alarm = RITO_ALARM()
Alarm.start()   
