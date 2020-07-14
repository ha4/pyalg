#import tkinter
from tkinter import *
import serial
import struct

# for python:
# if old pip: python -m pip install --upgrade pip
# python -m pip install pyserial
# betaflight: Enter and send command "serialpassthrough 2 57600"
# ('2' is the UART ID; UART3 ID 2, UART2 ID 1, UART1 ID = 0), then press ENTER.
# If all went well, you should see: "Port 2 opened, baud = 57600" "Forwarding, power cycle to exit"
# python -m serial.tools.miniterm -h  # python -m serial.tools.miniterm COM19
# python -m serial.tools.list_ports  # 


def runcam_req():
    pass

def runcam_decode(req,resp):
    pass


def runcam_getinfo(): # 0x00 => {proto-vers,feature}
    """
1. Read camera information  RCDEVICE_PROTOCOL_COMMAND_GET_DEVICE_INFO = 0x00
Request packet structure, the length is 3 bytes:
    0xCC 	0x00 	CRC8
Response packet structure:
    Header 	     | 0xCC 	| uint8_t
    Protocol Version |	Protocol version | 	uint8_t
    Feature          |	Device feature | uint16_t
    crc8 	     | | 	uint8_t
Feature
Features 	Value 	Description
RCDEVICE_PROTOCOL_FEATURE_SIMULATE_POWER_BUTTON 	1 << 0 	Simulation Click the power button
RCDEVICE_PROTOCOL_FEATURE_SIMULATE_WIFI_BUTTON 	1 << 1 	Simulation Click the Wi-Fi button
RCDEVICE_PROTOCOL_FEATURE_CHANGE_MODE 	1 << 2 	Switch the device operating mode
RCDEVICE_PROTOCOL_FEATURE_SIMULATE_5_KEY_OSD_CABLE 	1 << 3 	Simulation 5-key OSD remote control
RCDEVICE_PROTOCOL_FEATURE_DEVICE_SETTINGS_ACCESS 	1 << 4 	Support access to device settings
RCDEVICE_PROTOCOL_FEATURE_DISPLAYP_PORT 	1 << 5 	The device is identified as a DisplayPort device by flying controller and receives the OSD data display from the flight controller
RCDEVICE_PROTOCOL_FEATURE_START_RECORDING 	1 << 6 	Control the camera to start recording video
RCDEVICE_PROTOCOL_FEATURE_STOP_RECORDING 	1 << 7 	Control the camera to stop recording video

    """
    pass

def runcam_control(action):  # 0x01, action(0,1,2,3,4,5) => ?
    """
2. Camera control   RCDEVICE_PROTOCOL_COMMAND_CAMERA_CONTROL = 0x01
Request packet structure, the length is fixed to 4 bytes：
    0xCC 	0x01 	Action   CRC8
Action 	Value 	Description
RCDEVICE_PROTOCOL_SIMULATE_WIFI_BTN 	0x00 	Simulation Click the Wi-Fi button
RCDEVICE_PROTOCOL_SIMULATE_POWER_BTN 	0x01 	Simulation Click the Power button
RCDEVICE_PROTOCOL_CHANGE_MODE 	0x02 	Switch the camera mode
RCDEVICE_PROTOCOL_CHANGE_START_RECORDING 	0x03 	Control the camera to start recording
RCDEVICE_PROTOCOL_CHANGE_STOP_RECORDING 	0x04 	Control the camera to stop recording    
    """
    pass

def runcam_5key_press(action):  # 0x02, action(1-set,2<,3>,4^,5v) => {}
    """
3.Simulate Press command of the 5 key remote control RCDEVICE_PROTOCOL_COMMAND_5KEY_SIMULATION_PRESS = 0x02
Request packet structure, the length is fixed to 4 bytes：
    0xCC 	0x02 	Action   CRC8
Action 	Value 	Description
RCDEVICE_PROTOCOL_5KEY_SIMULATION_SET 	0x01 	Simulate the confirmation key of the 5 key remote control
RCDEVICE_PROTOCOL_5KEY_SIMULATION_LEFT 	0x02 	Simulate the left key of the 5 key remote control
RCDEVICE_PROTOCOL_5KEY_SIMULATION_RIGHT 	0x03 	Simulate the right key of the 5 key remote control
RCDEVICE_PROTOCOL_5KEY_SIMULATION_UP 	0x04 	Simulate the up key of the 5 key remote control
RCDEVICE_PROTOCOL_5KEY_SIMULATION_DOWN 	0x05 	Simulate the down key of the 5 key remote control
Response packet structure, the length is fixed to 2 bytes：
    0xCC 	CRC8
    """
    pass

def runcam_5key_release(): # 0x03 => {}
    """
4.Simulate Release command of the 5 key remote control RCDEVICE_PROTOCOL_COMMAND_5KEY_SIMULATION_RELEASE = 0x03
Request packet structure, the length is fixed to 3 bytes：
    0xCC 	0x03 	CRC8
Response packet structure, the length is fixed to 2 bytes：
    0xCC 	CRC8

    """
    pass

def runcam_5key_conn(state): # 0x04, action(1-open,2-close) => {acton<<4+status}
    """
5.Simulate handshake/disconnection command RCDEVICE_PROTOCOL_COMMAND_5KEY_CONNECTION = 0x04
Request packet structure, the length is fixed to 4 bytes：
    0xCC 	0x04 	Action 	CRC8
Action 	Value 	Description
RCDEVICE_PROTOCOL_5KEY_FUNCTION_OPEN 	0x01 	Initiate a handshake action to the camera
RCDEVICE_PROTOCOL_5KEY_FUNCTION_CLOSE 	0x02 	Initiate a disconnection action to the camera
Response packet structure, the length is fixed to 3 bytes：
    0xCC 	[(Action ID << 4) + result(1：Succes 0：Failure) ] 	CRC8
    """
    pass

#settings
# Reserved Setting IDs
# Setting 	ID 	Type 	Description 	Access Mode
# SETTINGID_DISP_CHARSET 	0 	TEXT_SELECTION 	This setting is store current charset of the device 	Read & Write
# SETTINGID_DISP_COLUMNS 	1 	UINT8 	Read the number of columns displayed on the screen line 	Read only
# SETTINGID_DISP_TV_MODE 	2 	TEXT_SELECTION 	Read and set the camera's TV mode(NTSC,PAL) 	Read & Write
# SETTINGID_DISP_SDCARD_CAPACIT 	3 	STRING 	Read the camera's memory card capacity 	Read only
# SETTINGID_DISP_REMAIN_RECORDING_TIME 	4 	STRING 	Read the remaining recording time of the camera 	Read only
# SETTINGID_DISP_RESOLUTION 	5 	TEXT_SELECTION 	Read and set the camera's resolution 	Read & Write
# SETTINGID_DISP_CAMERA_TIME 	6 	STRING 	Read and set the camera's time 	Read & Write
# RESERVED 	7 - 19 	- 	these setting are reserved 	-
def runcam_setting_getsub():
    """
6. Get sub settings with special setting ID RCDEVICE_PROTOCOL_COMMAND_GET_SETTINGS=0x10
Camera feature requirements: RCDEVICE_PROTOCOL_FEATURE_DEVICE_SETTINGS_ACCESS
Request packet structure, the length is fixed to 5 bytes：
    Header 	Comman ID 	setting ID 	Chunk Index 	crc8
    0xCC 	0x10 	Retrieve the sub settings through the parent setting ID 	chunk index 	Check code

Response packet structure，the length is not fixed:
Field 	Value 	Size
Remaining Chunk 	remaining chunk count 	uint8_t
Data Length 	The length of data from current field to the CRC field. This length does not include the current field and the CRC field 	 
Setting ID 	unique id (Relative to the entire setting tree) 	uint8_t
Setting name 	setting name 	char[], a null-terminated string
Setting value 	value of setting 	char[], a null-terminated string
Setting ID 	unique id (Relative to the entire setting tree) 	uint8_t
Setting name 	setting name 	char[], a null-terminated string
Setting value 	value of setting 	char[], a null-terminated string
... 	... 	...
... 	... 	...
crc 	crc8 code 	uint8_t
    """
    pass

def runcam_setting_detail():
    """
7. Read a setting detail RCDEVICE_PROTOCOL_COMMAND_READ_SETTING_DETAIL = 0x11
Request packet structure, the length is fixed to 5 bytes：
    0xCC 	0x11 	setting ID 	Chunk Index 	CRC8
Response packet structure，the length is not fixed:
Field 	Size 	Description
Remaining Chunk 	remaining chunk count 	uint8_t
Data length 	uint8_t 	The length of data from current field to the CRC field. This length does not include the current field and the CRC field
setting type 	uint8_t 	the type of setting，refer to 'setting type' section to know more
value 	current value, the size is depending on setting 	the current value of setting
min value 	the size is depending on setting 	max value
max value 	the size is depending on setting 	min value
decimal point 	uint16_t 	the digtal count after decimal point
step size 	the size is depending on setting 	the increment/decrement value when modifying the setting
max string size 	uint8_t 	max size of string
text_selections 	char[] 	a null-terminated string，the content is all available string in the setting, they are separated by a semicolon(;)
crc 	uint8_t 	crc8 code

setting type
available setting type 	setting id
UINT8 	0
INT8 	1
UINT16 	2
INT16 	3
FLOAT 	8
TEXT_SELECTION 	9
STRING 	10
FOLDER 	11
INFO 	12

INTEGER
when setting type is UINT8, INT8, UINT16 or INT16，the min value, max value, step size will be returned from Device，and the size of min value, max value and step size are depending on their setting type, e.g if the setting type is UINT8, then min value and max value are uint8_t.

FLOAT
min value, max value, decimal point, step size will be returned, the type of step size is int32_t

TEXT_SELECTION
text_selections will be returned as a null-terminated string, the content is all available string in the setting, they are separated by a semicolon(;)

STRING
max string size will be returned, it's used to limit the max size of the string when user editing it.

FOLDER
If the setting type is FOLDER, means it contains a set of settings. This setting can't be modified, when you call Get Detail Command(0x7) with it, it will return a empty response and the error code won't be zero.

INFO
if the settings type is INFO，this field is same with FOLDER, can't be modified.

COMMAND
not design yet
    
    """
    pass

def runcam_setting_wr():
    """
8. Write a setting RCDEVICE_PROTOCOL_COMMAND_WRITE_SETTING = 0x13
Request packet structure, the length is not fixed：
    Header 	Command ID 	Setting ID 	value 	crc8
    0xCC 	0x13 	setting ID 	value of the setting, size is depending on setting type 	Check code

INTEGER
when setting type is UINT8, INT8, UINT16 or INT16，the value type is integer, the difference is the size, e.g if the setting type is UINT8, the vlaue field size is uint8_t, same with others.

FLOAT
a null-terminated string, it describing a float value

TEXT_SELECTION
the index in text_selections that point to new value.

STRING
a null-terminated string

COMMAND
not design yet

Response packet structure，the length is fixed to 4 bytes:
Field 	Size 	Description
result code 	  	uint8_t
update menu items 	uint8_t 	if the value of this field is not zero, the FC size should resend the RCDEVICE_PROTOCOL_COMMAND_GET_SETTINGS(0x10) to retrieve the settings of current page.
crc 	uint8_t 	crc code
    """
    pass

def runcam_fillscreen():
    """
9. Fill screen area RCDEVICE_PROTOCOL_COMMAND_DISP_FILL_REGION = 0x20
Request packet structure, the length is not fixed：
    Header 	Comman ID 	x 	y 	width 	height 	character 	crc8
    0xCC 	0x20 	x 	y 	width 	height 	the character that going to fill the area 	Check code
    """
    pass

def runcam_writechar():
    """
10. write a single character RCDEVICE_PROTOCOL_COMMAND_DISP_WRITE_CHAR=0x21
Request packet structure, the length is not fixed：
    Header 	Comman ID 	x 	y 	character 	crc8
    0xCC 	0x21 	x 	y 	the character that going to draw 	Check code
    """
    pass

def runcam_writestrhoriz():
    """
11. Write a string horizontally RCDEVICE_PROTOCOL_COMMAND_DISP_WRITE_HORT_STRING = 0x22
Request packet structure, the length is not fixed：
    Header 	Comman ID 	string length 	x 	y 	string 	crc8
    0xCC 	0x22 	the length of string(60 is max length) 	x 	y 	the string that going to draw 	Check code
    """
    pass

def runcam_writestrvert():
    """
12. Write a string vertical RCDEVICE_PROTOCOL_COMMAND_DISP_WRITE_VERT_STRING=0x23
Request packet structure, the length is not fixed：
    Header 	Comman ID 	string length 	x 	y 	string 	crc8
    0xCC 	0x23 	the length of string(60 is max length) 	x 	y 	the string that going to draw 	Check code

    """
    pass

def runcam_writechars():
    """
13. Write a chars  RCDEVICE_PROTOCOL_COMMAND_DISP_WRITE_CHARS=0x24
Request packet structure, the length is not fixed：
    Header 	Comman ID 	data length 	data 	crc8
    0xCC 	0x24 	the length of data(60 is max length) 	The data is used to draw different characters at one or more locations, each of which needs to occupy 3 bytes, which is x, y, char. Allows up to 20 sets of data, that means the maximum length can not exceed 60 bytes. 	Check code
    """
    pass

def runcam_crc8(crc, a):
    """
    crc init = 0
    """
    crc ^= a
    for i in range(8):
        crc = (crc << 1)^(0xD5 if crc&0x80 else 0)
    return crc&0xFF

def connect():
    """
https://github.com/cleanflight/cleanflight/blob/master/src/main/io/rcdevice.c

speed 115200

https://github.com/iNavFlight/inav/issues/4172
after sent "cc 00 60" to RunCam Split, and read from split(serialRead or rxCallback in openSerialPort), it should get 5 bytes response, and the content is "CC 01 57 00 B7"

python -m serial.tools.miniterm -e --encoding hexlify com8 115200
    """
    global conf_port
    global conf_baud
    global conf_fd
    print(conf_port.get())
    pass

def frames():
    global conf_port
    global conf_baud
    root = Tk()
    Label(root,text="Serial port").grid(row=0,column=0)
    conf_port=Entry(root,width=10)
    conf_port.grid(row=0,column=1)
    Label(root,text="Baud").grid(row=0,column=2)
    conf_baud=Entry(root,width=5,text="115200")
    conf_baud.grid(row=0,column=3)
    Button(root,text="Connect",command=connect).grid(row=0,column=5)

frames()
