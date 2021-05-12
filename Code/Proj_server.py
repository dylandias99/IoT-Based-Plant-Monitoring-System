import serial
import time
import socket



# @brief: Send a read/write command to the Arduino
# @par ser: The serial port instance
# @par command: The name of the read/write command
# @ret None
def send_command(ser, command):
	ser.write(command.encode())


# @brief: Read the Serial port for a newline and return the output (data / string/ newline)
# @par ser: The serial port instance
# @ret value: Received serial transmission (newline)	
def read_uart(ser):	
	value = ser.readline().decode('utf-8')	# Read and print the received serial transmission
	print(value)
	return value

# @brief: Configure the Serial port of the Omega board
# @par None
# @ret ser: Instantiation of Serial Port
def serial_port():
	ser = serial.Serial(
	    port='/dev/ttyS1',\
	    baudrate=9600,\
	    parity=serial.PARITY_NONE,\
	    stopbits=serial.STOPBITS_ONE,\
	    bytesize=serial.EIGHTBITS,\
	    timeout=None)
	print("Connected to: " + ser.portstr)
	return ser
	
s = socket.socket()
print ("Socket successfully created")

port = 9090

s.bind(('', port))
print ("socket binded to %s" %(port))

s.listen(5)
print ("socket is listening")

c,addr = s.accept()
print ('Got connection from', addr )

def check_ack(ser, ack_string):
    while (1):
        recd_ack = ser.readline().decode('utf-8')
        if (recd_ack == ack_string + "\r\n"):
            break

def main():
	# Configure the Serial port of the Omega board
	ser = serial_port()
	while(1): 
		output = c.recv(1024).decode('utf-8')
		if output == "CONNECT":
			send_command(ser, "CONNECT")
			#define light A1
			light = float(read_uart(ser))
			print("Light: " + str(light))
			c.sendall(str(light).encode('utf-8'))
			time.sleep(3)
			check_ack(ser, "ACKNOWLEDGE")
			# temperture
			temp = float(read_uart(ser))
			print("Temperature: " + str(temp) +"°F")
			c.sendall(str(temp).encode('utf-8'))
			time.sleep(3)
			check_ack(ser, "ACKNOWLEDGE")
			# Humidity
			hum = float(read_uart(ser))
			print("Humidity: " + str(hum) + "%")
			c.sendall(str(hum).encode('utf-8'))
			time.sleep(3)
			check_ack(ser, "ACKNOWLEDGE")
			moist = float(read_uart(ser))
			print("Moisture: " + str(moist) + "%")
			c.sendall(str(moist).encode('utf-8'))
			time.sleep(3)
			check_ack(ser, "ACKNOWLEDGE")
		elif output == "PUMP":
			print("Pump Sucessful")
			send_command(ser, "PUMP")
			time.sleep(3)
			check_ack(ser, "ACKNOWLEDGE")
		elif output == "EXIT":	
			print("Exiting")
			break
	s.close()

if __name__ == "__main__":
    main()