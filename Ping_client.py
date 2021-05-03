'''
Author: William Cobb
Title: COMP430 HW2
Description:
'''

import socket as skt
from time import asctime, sleep, perf_counter
from sys import argv, exit

# prints script parameters and examples
if len(argv) == 2 and argv[1] == 'help':
	print('Ping_client.py server_name[ex: 127.0.0.1] server_port[ex: 12000]')
	exit(0)

if len(argv) < 3:
	print('ERROR: This script takes a server_address and server_port as parameters | Ping_client.py server_name[ex: 127.0.0.1] server_port[ex: 12000]')  # check to ensure an argument is present
	exit(-1)
if len(argv) > 3:
	print('ERROR: This script only takes a server_address and server_port as parameters | Ping_client.py server_name[ex: 127.0.0.1] server_port[ex: 12000]')  # check to ensure an argument is present
	exit(-1)

if argv[1] == 'localhost':
	server_name = '127.0.0.1'
else:
	server_name = argv[1]

try:
	int(argv[2])  # ensures server_port parameter entered is an integer value
except ValueError as e:
	print('ERROR: server_port must be an integer value | Ping_client.py server_name[ex: 127.0.0.1] server_port[ex: 12000]')
	exit(-1)

server_port = int(argv[2])
client_port = 12002

client_socket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
client_socket.bind(('', client_port))
client_socket.settimeout(0.5)  # causes client_socket to throw a socket.timeout error after 0.5 sec

# used for diagnostic print at program close
successful_resp = 0
rtt_sum = 0

for _ in range(1, 11):

	message = f'ping {_} | {asctime()}'

	try:
		client_socket.sendto(message.encode(), (server_name, server_port))
		rtt1 = perf_counter()
	except skt.gaierror as e:
		print('ERROR: Invalid server_address')
		exit(-1)

	try:
		modified_message, server_address = client_socket.recvfrom(1024)
	except skt.timeout as e:
		print(message)
		print('Time out.\n')
		sleep(1)
		continue

	rtt2 = perf_counter()
	rtt = rtt2 - rtt1
	modified_message = modified_message.decode()
	print(modified_message[2:].replace("'", ""))
	print(f'Reply from {server_name} | RTT: {rtt} sec\n')
	successful_resp += 1
	rtt_sum += rtt
	sleep(1)

print(f'Successful responses from {server_name}: {successful_resp} | Average RTT: {rtt_sum / successful_resp}')
client_socket.close()