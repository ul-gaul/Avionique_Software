"""Command line test program to send commands to the comm-module."""


# imports
import sys
import serial
import struct
import pycrc.algorithms as crcalgo


# global configuration variables
BAUD_RFD = 115200
CMD_PKT_FMT = '>HHBB'
CRC_FMT = '>H'
START_SHORT = 0xface
CRC = crcalgo.Crc(width=16, poly=0x1021,
				reflect_in=False, reflect_out=False,
				xor_in=0xffff, xor_out=0x0000)


def print_help():
	print('Syntax: > [function] [args]')
	print('Supported functions are:')
	print('set - set an actuator to a high state')
	print('\targ is the number of the actuator')
	print('reset - reset an actuator to a low state')
	print('\targ is the number of the actuator')
	print('exit - quit the command line tool')


def compute_crc(data):
	return CRC.bit_by_bit(data)


def get_ack(ser):
	return ser.read(7)


def set_actuator(ser, i, a):
	data = struct.pack(CMD_PKT_FMT, START_SHORT, i, 1, a)
	data += struct.pack(CRC_FMT, compute_crc(data))
	size = ser.write(data)
	print('wrote:', [hex(x) for x in list(data)], size)
	print('CRC on data sent =', hex(compute_crc(data)))

	print('waiting for response')
	ack = get_ack(ser)
	print([hex(i) for i in list(ack)])
	print('CRC on ACK:', hex(compute_crc(ack)))


def test_comm_error(ser, i, a):
	data = struct.pack(CMD_PKT_FMT, START_SHORT, i, 1, a)
	# flip a bit in the start short
	err_data = struct.pack(CMD_PKT_FMT, (START_SHORT ^ 0b00001000), i, 1, a)
	err_data += struct.pack(CRC_FMT, compute_crc(data)) # crc on original data
	size = ser.write(err_data)
	print('wrote:', [hex(x) for x in list(err_data)], size)
	print('CRC on data sent =', hex(compute_crc(err_data)))

	print('waiting for response')
	ack = get_ack(ser)
	print([hex(i) for i in list(ack)])
	print('CRC on ACK:', hex(compute_crc(ack)))


def reset_actuator(ser, i, a):
	data = struct.pack(CMD_PKT_FMT, START_SHORT, i, 2, a)
	data += struct.pack(CRC_FMT, compute_crc(data))
	size = ser.write(data)
	print('wrote:', [hex(x) for x in list(data)], size)
	print('CRC on data sent =', hex(compute_crc(data)))

	print('waiting for response')
	ack = get_ack(ser)
	print([hex(i) for i in list(ack)])
	print('CRC on ACK:', hex(compute_crc(ack)))


def cli(port):
	i = 0
	with serial.Serial(port, BAUD_RFD, timeout=None) as ser:
		while True:
			# get input
			s = input('> ')
			# treat simple functions first
			if s == '-h' or s == '--help':
				print_help()
			elif s == 'exit':
				break
			# get function and arguments
			try:
				f, a = s.split(' ')
				a = int(a) 
			except ValueError as e:
				print('Invalid command, error occured:', e)
				continue
			# treat function calls
			if f == 'set':
				set_actuator(ser, i, a)
			elif f == 'reset':
				reset_actuator(ser, i, a)
			elif f == 'error':
				test_comm_error(ser, i, a)
			else:
				print('Invalid command, type -h or --help for help')
			i += 1


if __name__ == '__main__':
	port = sys.argv[1]

	if len(sys.argv) == 2:
		cli(port)

	else:
		with serial.Serial(port, BAUD_RFD, timeout=None) as ser:
			f = sys.argv[2]
			a = int(sys.argv[3])
			if f == 'set':
				set_actuator(ser, 0, a)
			elif f == 'reset':
				reset_actuator(ser, 0, a)
			elif f == 'error':
				test_comm_error(ser, 0, a)
			else:
				print('Invalid command')
				print_help()

	sys.exit(0)
