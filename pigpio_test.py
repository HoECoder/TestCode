#!/usr/bin/python
import pigpio
import time

# A sample program driving the OpenSprinkler Pi HW using pigpio.
# This way, the only thing that has to run as root is the tested pigpio daemon
# My program can live in a non-root user.
# My testbed uses low current, low-volt AC lamps.
# OSPI can drive all 8 channels, but I'm betting I can't drive 8 valves at once.
# In the future, I should have a clear shutoff before turning the next on...

# I'm assuming a RPi A+/B+ or RPi 2
# Swiped the definition from OpenSprinkler Unified Firmware
# OpenSprinkler-Firmware/defines.h
# https://github.com/OpenSprinkler/OpenSprinkler-Firmware/blob/a62856969722f8185b1168737b67d8497ffb95b2/defines.h#L307
pin_sr_dat = 27 # Shift Register Data Pin
pin_sr_clk = 4  # Shift Register Clock Pin
pin_sr_oe = 17  # Shift Register Output Enable Pin
pin_sr_lat = 22 # Shift Register Latch Pin

# print pin_sr_dat
# print pin_sr_clk
# print pin_sr_noe
# print pin_sr_lat

def enable_sr(pi):
	pi.write(pin_sr_oe,0)
	
def disable_sr(pi):
	pi.write(pin_sr_oe,1)
	
def setup_pins(pi):
	pi.set_mode(pin_sr_oe,pigpio.OUTPUT)
	pi.set_mode(pin_sr_clk, pigpio.OUTPUT)
	pi.set_mode(pin_sr_dat, pigpio.OUTPUT)
	pi.set_mode(pin_sr_lat, pigpio.OUTPUT)
	pi.write(pin_sr_noe, 1)
	pi.write(pin_sr_clk, 0)
	pi.write(pin_sr_dat, 0)
	pi.write(pin_sr_lat, 0)
	
def write_register(pi,bit_pattern):
	print "Bit Pattern %s" % (str(bit_pattern))
	pi.write(pin_sr_clk,0)
	pi.write(pin_sr_lat,0)
	# Near as I can tell, we actually put the top-bit in first...
	# I'm sure my brother (and/or Ray) would be peeved that I can't remember why this is so...
	bits = list(bit_pattern)
	bits.reverse()
	for bit in bits:
		pi.write(pin_sr_clk,0)
		pi.write(pin_sr_dat,bit)
		pi.write(pin_sr_clk,1)
	pi.write(pin_sr_lat,1)

if __name__ == "__main__":
	pi = pigpio.pi()
	#Toy pattern holder
	bit_pattern = [0,0,0,0,0,0,0,0]
	#Turn everything off at the end
	stop_mask = [0,0,0,0,0,0,0,0]
	i = 0
	#Setup the pins for work
	setup_pins(pi)
	try:
		while True: # Go forever
			idx = i % 8
			bit_pattern[idx]=1 #Flip a station on.
			print "Station %d fire" % (idx+1)
			disable_sr(pi) # Pause the Shift Register
			write_register(pi,bit_pattern) # Push in my bit pattern
			enable_sr(pi) # Release the shift register
			bit_pattern[idx]=0 #Reset the bit buffer
			#print bit_pattern
			i = i + 1
			time.sleep(2) # Take a nap
	except KeyboardInterrupt: #This gives us a break point
		print ""
		print "KeyboardInterrupt!"
		# print stop_mask
		disable_sr(pi)
		write_register(pi,stop_mask) # Turn everything off
		enable_sr(pi)
	pi.stop()
	print "Done"