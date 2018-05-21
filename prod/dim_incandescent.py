import sys
import serial

# # value from bash command
dim = str(sys.argv[1])

ser = serial.Serial(
    
    port='/dev/ttyACM0',
    baudrate = 57600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
ser.write(dim)