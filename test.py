import serial
import re
ser = serial.Serial(port='COM13', baudrate=9600)
while True:
    data = re.split("[,']", str(ser.readline()).rstrip('\n'))
    print(data)
