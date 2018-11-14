#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:05:44 2018

@author: aaflores
"""
import time, csv, sys
import Adafruit_BBIO.GPIO as GPIO

#Include "Abstraction" path to be able to import abstraction scripts
sys.path.append('../Abstraction/')


from I2C import I2C_Bus

#import hmc5883l_magnetometer

print("\n")
Com_Bus = I2C_Bus(sys.argv[2])

csv_file = open(sys.argv[1],"r")

current_day = time.strftime("%a-%d-%b-%H:%M:%S", time.localtime())

out_file = open("../../Logs/Test-started-" + current_day + ".csv", "w")
out_file_GPIO = open("../../Logs/Test-started-" + current_day + "GPIO.csv", "w")

testing_sequence = csv.reader(csv_file)
output_sequence = csv.writer(out_file, delimiter=',')
output_GPIO = csv.writer(out_file_GPIO, delimiter=',')

 	
GPIO.setup("P8_7", GPIO.OUT)

def get_vals(row):
    offset = 0
    if(str(row[2]) == 'w'):
        write = True

        if len(row) > 3:
            offset = str(row[3])

    else:
        write = False

    return write, str(row[0]), str(row[1]), offset

print("running test '%s' at %s ms" % (sys.argv[1],sys.argv[3]))

first_row = True

for row in testing_sequence:
    if first_row:
        first_row = False
        continue
    write, address, value, offset = get_vals(row)
    if write:
        #Generate starting reference pulse
        GPIO.output("P8_7", GPIO.HIGH)
        time.sleep(0.002)
        GPIO.output("P8_7", GPIO.LOW)

        Com_Bus.Send_Message(address,value,offset)

        #Generate ending reference pulse
        GPIO.output("P8_7", GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output("P8_7", GPIO.LOW)
        time.sleep(0.001)
        GPIO.output("P8_7", GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output("P8_7", GPIO.LOW)
    else:
        #Generate starting reference pulse
        GPIO.output("P8_7", GPIO.HIGH)
        time.sleep(0.002)
        GPIO.output("P8_7", GPIO.LOW)
        current_time = time.strftime("%a-%d-%b-%H:%M:%S", time.localtime())
#        output_GPIO.writerow([current_time, row[(len(row)*2)-1], "MESSAGE SENT"])
        
        data = Com_Bus.Recieve_Message(address, offset)
        
        #Generate ending reference pulse
        GPIO.output("P8_7", GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output("P8_7", GPIO.LOW)
        time.sleep(0.001)
        GPIO.output("P8_7", GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output("P8_7", GPIO.LOW)
        current_time = time.strftime("%a-%d-%b-%H:%M:%S", time.localtime())
#        output_GPIO.writerow([current_time, row[len(row)*2], "MESSAGE RECEIVED"])
        #min, deg = hmc5883l_magnetometer.print_readings(data)
    current_time = time.strftime("%a-%d-%b-%H:%M:%S", time.localtime())
#    output_sequence.writerow([current_time, row[len(row)-1], address, value, offset])

    time.sleep(float(sys.argv[3])/1000)

Com_Bus.close()
csv_file.close()
out_file.close()

#Allow port to close
time.sleep(0.2)

print("Exiting")


exit




"""
CHANGE LOG
_______________________________________
USER_ID   DATE      CHANGE_DESCRIPTION
_______________________________________

aaflores  05-16-18  -Initial file

aaflores  05-17-18  -Moved CAN code to CAN module
                    -Added file reading using CSV to load a test sequence

aaflores  05-22-18  -Changed CAN module for J1939 module

jdimatte  07-11-18  -Implementated read operation with if statement
                    -Imported magnetometer interface file

"""

