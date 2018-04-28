# test.py
import serial
ser = serial.Serial('COM4', 9600)
num = 0
while num < 1000:
	s = ser.readline()
	num += 1
	print(s, num)
