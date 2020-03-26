"""Command line test program to send commands to the comm-module."""


# imports
import sys
import serial
import struct


# global configuration variables
BAUD_RFD = 9600
CMD_PKT_FMT = '>HHBBH'
START_SHORT = 0xface


def print_help():
	print('Syntax: > [function] [args]')
	print('Supported functions are:')
	print('set - set an actuator to a high state')
	print('\targ is the number of the actuator')
	print('reset - reset an actuator to a low state')
	print('\targ is the number of the actuator')


def set_actuator(ser, i, a):
	# TODO: use a CRC
	data = struct.pack(CMD_PKT_FMT, START_SHORT, i, 1, a, 0)
	ser.write(data)


def reset_actuator(ser, i, a):
	# TODO: use a CRC
	data = struct.pack(CMD_PKT_FMT, START_SHORT, i, 2, a, 0)
	ser.write(data)


def cli(port):
	i = 0
	with serial.Serial(port, BAUD_RFD, timeout=1) as ser:
		while True:
			f, a = input('> ').split(' ')
			if f == '-h' or f == '--help':
				print_help()
			elif f == 'set':
				set_actuator(ser, i, int(a))
			elif f == 'reset':
				reset_actuator(ser, i, int(a))
			else:
				print('Invalid command, type -h or --help for help')


if __name__ == '__main__':
	port = sys.argv[1]
	cli(port)

	sys.exit(0)
