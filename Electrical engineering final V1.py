import pyautogui
import time 
import keyboard
import serial 
#import threading          (later stuff if I get to it)
#import multiprocessing
#Control C stops script

#This version only works within the terminal

#what it does
#
#
# this program will check for a term that is listed as active in the windows section
# once this term surpasses 15 it will activate and send the message "on"  in the terminal
# there is a lot of extraneous code that will be marked with #*

RunP = False
Windows = []
count = 0 # can be replaced by using the length of the target_list
pyautogui.FAILSAFE = True #*
target_list = []

def start():
    global RunP #necessary as python does not recognize RunP as a global before this 
    while RunP == False:
     print("press s to start detecting and c to end")
     if keyboard.read_key() == "s": #waits for the key "s" to be pressed which will determine bool RunP as True
            RunP = True
            print(RunP)

def Window_check():     #gets list of all open windows and returns a counter for number of times window appears in list
    global count #global def
    for x in pyautogui.getAllWindows():  #pyautogui command that gets list of all current windows
        Windows.append(x.title) #adds every list to a windows list in order to check if target window is in list
    time.sleep(5) #checks every five seconds 
    if target_window in Windows: # if target window is in gotten list
        count += 1 #can be removed
        Windows.clear()# clears windows list to prevent piling up behind the scenes
        target_list.append(target_window) #adds 1 character to target list  used for testing
        #print(target_list) #prints to show amount of terms in target_list
    else: 
        count = 0 #sets count to zero if target not in list
        Windows.clear()
    print(count) #can be removed and replaced with a function that counts the number of terms in target_list
    #print(RunP)    # un# to test if process is running despite RunP = False
    #print(target_list) #testing un# to test if target_list is being added to despite not being in list. 

def start_serial(Port, Baudrate, Timeout): #starts serial connection
    global ard 
    ard = serial.Serial(port = Port, baudrate = Baudrate, timeout = Timeout) #must be done manually 
    print(ard.name) 


def Comm(time_threshold): #time_threshold should be in seconds
        if (count > time_threshold):
            ard.write("s".encode())
        elif (count < time_threshold):
            ard.write("c".encode())

def main():
    test_list = []
    time_limit = int(input("enter the maximum amount of seconds for the window to be open: "))
    for x in pyautogui.getAllWindows():
        test_list.append(x.title)
    print(test_list)#testing
    global target_window
    target_window = input("target window: ")
    start_serial("COM5", 9600, .1) #starts connection with arduino
    start() #waits for user input if they want to start the program
    while RunP == True: #loop after start() goes true
        Window_check() 
        Comm(time_limit) #if tab open for more than x seconds than yolo



main()
