# test.py
import serial
ser = serial.Serial('COM3', 9600)
num = 0
while num < 1000:
	s = ser.readline()
	s = str(s)[2:-5]
	num += 1
	print(s, num)
