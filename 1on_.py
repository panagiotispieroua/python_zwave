#!/usr/bin/python2.7
import time
import serial
import string
from datetime import datetime,date
from array import *
def int2hex(n):
  return "%0.2X" % n
  
def hex2int(hex):
  return int(hex,16)

def sentcmd(data):
  ser = serial.Serial('/dev/ttyUSB0', 115200, 8, 'N', 1, timeout=5)
  ser.open()
  print "Connected to: " + ser.portstr
  ser.write( data )
  d1 = time.time()
  stage=0
  length=0
  while time.time()<d1+10:
    #print "stage -1"
    b = ser.read(1)
    if len(b)>0:
      if stage==0: #Wait for ACK
	print "stage 0"
	if b==chr(0x06):
	  stage=1
	elif b==chr(0x01):
	  stage=2
      elif stage==1:  #Wait for SOF
	print "stage 1"
	if b==chr(0x01):
	  stage=2
      elif stage==2:  #Wait for Length
	print "stage 2"
	length=ord(b)
	stage=3
	indata=int2hex(ord(b))
	cntr=length
	print length
      elif stage==3:
	print "stage 3"
	indata=indata+int2hex(ord(b))
	cntr=cntr-1
	if cntr==0:
	  #print indata
	  #print int2hex(hex2int(indata[0:2]) ^ hex2int(indata[2:4]))
	  #checksum= 255
	  #for i in range(0,length,2):
	  #checksum = checksum ^ hex2int(indata[i:i+2])
	  
	  ser.write("\x06")
	  stage=0
	  d1=0
  print "end of cmd"
  stage=0
  ser.close()
	  
      #elif stage==4:
      #print int2hex(ord(response))
  
sentcmd("\x01\x0A\x00\x13\x02\x03\x20\x01\xFF\x05\x03\x3F")