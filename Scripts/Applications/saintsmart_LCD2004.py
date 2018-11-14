import csv, sys, time

#Include "Abstraction" path to be able to import abstraction scripts

LCD_Character_Dictionary = {}
"""
DDRAM LINE ADDRESSES
Line 1 is followed by line 3
Line 2 is followed by line 4
"""
LCD_LINE_1_ADDRESS = 0x00 | 0x80
LCD_LINE_2_ADDRESS = 0x40 | 0x80
LCD_LINE_3_ADDRESS = 0x14 | 0x80
LCD_LINE_4_ADDRESS = 0x54 | 0x80
LCD_LINE_ADDRESS_RW_RS = 0x00

"""
Wake up command
[RW/RS not needed]
"""
LCD_WAKEUP = 0x03
LCD_WAKEUP_RW_RS = 0x00

"""
Function set command
[RW/RS not needed]
current implementation will set the display to:
 - Work with 4 bits
 - Work in two lines
"""
LCD_FUNCTION_SET = 0x28
LCD_FUNCTION_SET_RW_RS = 0x00

"""
Display on/off
"""
LCD_DISPLAY_OFF = 0x08
LCD_DISPLAY_ON = 0x0C
LCD_DISPLAY_CURSOR_ON = 0x02
LCD_DISPLAY_CURSOR_BLINK = 0x01
LCD_DISPLAY_RW_RS = 0x00

"""
Clear display
"""
LCD_CLEAR_DISPLAY = 0x01
LCD_CLEAR_DISPLAY_RW_RS = 0x00

"""
Display entry mode
current implementation will set the display to:
 - Increase DDRAM by 1
 - Not perform display shifting
"""
LCD_SET_ENTRY_MODE = 0x06
LCD_SET_ENTRY_MODE_RW_RS = 0x00

"""
Write to LCD
"""
LCD_WRITE_RW_RS = 0x01

"""
LCD Enable Signal
"""
LCD_ENABLE_SIGNAL = 0x04

"""
LCD BACKLIGHT
"""
LCD_ENABLE_BACKLIGHT = 0x08


"""
Variables to keep track of rows when writing to CSV
"""
CSV_ROW_POSITION = 1

"""
I2C ADDRESS
"""
I2C_ADDRESS = 0x26


def Create_dictionary():
   csv_file = open('../../Input_data/Display/Characters_Table.csv',"r")
   characters_table = csv.reader(csv_file)
   for column in range(1,7):
      first_row = True
      csv_file.seek(0)
      for row in characters_table:
         if first_row:
            upper_value = row[column]
            first_row = False
            continue
#replace line 19 with dictionary
         #print(row[column], "0b"+upper_value+row[0])
         #adding byte indicator and 10 for writing operation
         LCD_Character_Dictionary[row[column]] = upper_value+row[0]
         #LCD_Character_Dictionary[row[column]].append(row[0])

def Initialize_LCD():
   write_to_LCD(LCD_WAKEUP_RW_RS| 0x08, LCD_WAKEUP)
   time.sleep(0.05)
   write_to_LCD(LCD_WAKEUP_RW_RS| 0x08, LCD_WAKEUP)
   time.sleep(0.05)
   write_to_LCD(LCD_WAKEUP_RW_RS| 0x08, LCD_WAKEUP)
   time.sleep(0.05)

   #FUNCTION SET
   write_to_LCD(LCD_FUNCTION_SET_RW_RS| 0x08, LCD_FUNCTION_SET)

   #FUNCTION SET
   write_to_LCD(LCD_FUNCTION_SET_RW_RS| 0x08, LCD_FUNCTION_SET)

   #DISPLAY OFF
   write_to_LCD(LCD_DISPLAY_RW_RS| 0x08, LCD_DISPLAY_OFF)

   #CLEAR DISPLAY HIGH NIBBLE
   write_to_LCD(LCD_CLEAR_DISPLAY_RW_RS| 0x08, LCD_CLEAR_DISPLAY)
   #CLEAR DISPLAY LOW NIBBLE

   #ENTRY MODE HIGH NIBBLE
   write_to_LCD(LCD_SET_ENTRY_MODE_RW_RS| 0x08, LCD_SET_ENTRY_MODE)
   #ENTRY MODE LOW NIBBLE

   #DISPLAY ON HIGH NIBBLE
   write_to_LCD(LCD_DISPLAY_RW_RS| 0x08, LCD_DISPLAY_ON | LCD_DISPLAY_CURSOR_ON | LCD_DISPLAY_CURSOR_BLINK)
   #DISPLAY ON LOW NIBBLE


def write_to_LCD(command, data):
   #write I2C address in column 0
   #write (data << 4 | command) in column 1
   #increase row
   global CSV_ROW_POSITION
   csv_file = open('../../Input_data/I2C/Test_10.csv', 'a', newline='',encoding='utf-8-sig')
   i2c_csv = csv.writer(csv_file)
   
   command |=  LCD_ENABLE_BACKLIGHT

   address_list = [format(I2C_ADDRESS,'x'),format(I2C_ADDRESS,'x'),format(I2C_ADDRESS,'x'),format(I2C_ADDRESS,'x'),format(I2C_ADDRESS,'x'),format(I2C_ADDRESS,'x')]

   data_list = [format((data & 0xF0 | command ),'x'),format((data & 0xF0 | command | LCD_ENABLE_SIGNAL),'x'), format((data & 0xF0 | command & (~LCD_ENABLE_SIGNAL & 0xFF)),'x'), format(((data & 0x0F)<<4|command),'x'),format(((data & 0x0F)<<4| command | LCD_ENABLE_SIGNAL),'x'), format(((data & 0x0F)<<4 | command & (~LCD_ENABLE_SIGNAL & 0xFF)),'x')]

   data_type = ["w","w","w","w","w","w"]

   register = ["AA","BB","CC","DD","EE","FF"]

   data_to_write = zip(address_list,data_list, data_type, register)


   for row in data_to_write:
      i2c_csv.writerow(row)

def import_data_to_write(file_name):
   safety_counter = 0
   csv_file = open(file_name,"r")
   data_to_write = csv.reader(csv_file)
   for row in data_to_write:  
      data_available = True 
      if row[0] == 'a':
        write_to_LCD(LCD_CLEAR_DISPLAY_RW_RS, LCD_CLEAR_DISPLAY)
        data_available = False
        safety_counter = 0;
        continue
      elif row[0] == '1':
         write_to_LCD(LCD_LINE_ADDRESS_RW_RS, LCD_LINE_1_ADDRESS)
      elif row[0] == '2':
         write_to_LCD(LCD_LINE_ADDRESS_RW_RS, LCD_LINE_2_ADDRESS)
      elif row[0] == '3':
         write_to_LCD(LCD_LINE_ADDRESS_RW_RS, LCD_LINE_3_ADDRESS)
      elif row[0] == '4':      
         write_to_LCD(LCD_LINE_ADDRESS_RW_RS, LCD_LINE_4_ADDRESS)
      elif row[0] == 'z':
         break
      else:
         data_available = False
         safety_counter+= 1
      
      if safety_counter > 3:
         break
      
      if data_available == True:
         safety_counter = 0
         for column in range(1,21):
            write_to_LCD(LCD_WRITE_RW_RS, int(LCD_Character_Dictionary[row[column]],2) )
  
   

"""
MAIN FUNCTION
"""

Create_dictionary()

Initialize_LCD()

import_data_to_write('../../Input_data/Display/Template.csv')

#Replace with reading from CSV
test_string = "hello world"

#for items in test_string:
   #Replace with convert to I2C list
   #print(LCD_Character_Dictionary[items][0], "" , LCD_Character_Dictionary[items][1])
   
exit




"""
CHANGE LOG
_______________________________________
USER_ID   DATE       CHANGE_DESCRIPTION
_______________________________________

aaflores  Jul-05-18  -Initial file

aaflores  Jul-05-18  -Added function to create dictionary based on a CSV table
                     -Added function to initialize the LCD
                     -Added function to import data to write to LCD from a CSV file
                     -Added function to write to LCD. Current implementation writes I2C data to a CSV file.

aaflores  Jul-09-18  -Added backlight and Enable signal bits.
 		     -When creating the messages, there will be 2 extra bytes that toggle the enable signal on and off.

"""
