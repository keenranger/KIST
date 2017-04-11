import sys
import tcpServer
import executer
import Queue
import time


def isNumber(s):
	try:
		int(s)
		return True
	except ValueError:
		return False	


if len(sys.argv) == 1:
	print 'usage: python server_v_1.py port_number'
	exit(1)
elif not isNumber(sys.argv[1]):
	print 'Invalid port_number, ', sys.argv[1]
	exit(2)

port = int(sys.argv[1])

commandQueue = Queue.Queue()

print 'Server open with port of ', port

andRaspTCP = tcpServer.TCPServer(commandQueue, "", port)
andRaspTCP.start()

commandExecuter = executer.Executer(andRaspTCP)

while True:
	try:
		command = commandQueue.get()
		commandExecuter.startCommand(command)
	except:
		pass
