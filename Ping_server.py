'''
Author: William Cobb
Title: COMP430 HW2
Description:
'''

import socket as skt
from random import randint

server_port = 12000
server_socket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
server_socket.bind(('', server_port))
 
while True:
	
	print('The server is ready to receive!')

	rand = randint(0, 10)
	print(f'Random Number: {rand}')

	message, address = server_socket.recvfrom(1024)
	if rand < 4:
		continue 
	message = f'{message.upper()} | Random Number: {rand}'
	server_socket.sendto(message.encode(), address)