import threading
import socket
import select
import sys
import queue
import chatserver
host='192.168.0.200'
#sys_arg_check
if len(sys.argv)!=2:
	print('usage: python my_server.py port_number')
	exit(1)
try:
	port=int(sys.argv[1])
except ValueError:
	print('invalid port_num:', sys.argv[1])
	exit(2)

if not (0< port <65536):
	print('port_num=1~65535, your input:', sys.argv[1])
	exit(3)
#
commandQueue=queue.Queue()

raspServer=chatserver.ChatServer(commandQueue, host, port)
raspServer.start()
print('='*50)
print('server init complete')
print('waiting for connect')
print('='*50)
try:
	while True:
	#	try:
		command=commandQueue.get()
		print('[srv]:', command)
		raspServer.send(command)
	#	except:
	#		pass
except KeyboardInterrupt:
	raspServer.serverSocket.close()
	sys.exit()
