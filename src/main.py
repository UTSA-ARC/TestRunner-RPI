#!/usr/bin/env python3
import pigpio
import serial # serial communication
# import select
import threading
import time
# import sys
import signal
import os
from config import COMMANDS

# get incoming data from arduino => main()
# get input from the user and send to arduino=> readCommand()

arduino_port = "/dev/ttyACM0"

def readCommand() -> None:
    while True:
        userInput = input()
        ser.write(userInput.encode("utf-8")) # convert to binary and send to arduino
        if userInput == "help":
            print("Help Menu (Command : Description)")
            for command in COMMANDS:
                print(f"{command[0]} : {command[1]}") # print out command descriptions
        if userInput == "quit":
            os.kill(os.getpid(), signal.SIGKILL) # terminates the main program
        

def main():
    # capture any incoming arduino data and output it
    while True:
        # check for data in serial buffer
        if ser.in_waiting > 0:
            # converts data to str and remove newline character
            line = ser.readline().decode('utf-8').rstrip()
            print(line)

if __name__ == "__main__":
    ser = serial.Serial(arduino_port, 115200, timeout=1) # port name, baud rate, and timeout
    
    t = threading.Thread(target=readCommand) # Pi waits for user input in the background
    t.daemon = True
    t.start()
    main()