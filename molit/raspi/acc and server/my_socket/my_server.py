import threading
import socket
import select
import sys
import queue
host='192.168.0.200'
BUFF_SIZE=1024
class ChatServer(threading.Thread):
	def __init__(self, commandQueue, host, port):
		threading.Thread.__init__(self)
		self.commandQueue=commandQueue
		self.host=host
		self.port=port

		self.serverSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serverSocket.bind((self.host,self.port))
		self.serverSocket.listen(10)
		self.serverSockets=[self.serverSocket]
		self.clientSockets=[]
		self.chatThreads=[]
	def run(self):
		try:
			while self.serverSockets:
				rlist,wlist,xlist=select.select(self.serverSockets,[],[],10)
				for sock in rlist:
					if sock == self.serverSocket:
						clientSocket,clientAddress=self.serverSocket.accept()
						self.clientSockets.append(clientSocket)
						chatThread=ChatThread(self.commandQueue, self.chatThreads, self.clientSockets, clientSocket, clientAddress)
						chatThread.start()
						self.chatThreads.append(chatThread)
		except:
			self.serverSocket.close()
			sys.exit()
	def send(self, data):
		try:
			print('[srv->cli]:', data.encode())
			for i in range(len(self.clientSockets)):
				self.clientSockets[i].sendall(data.encode())
		except:
			pass
class ChatThread(threading.Thread):
	socket=False
	def __init__(self,commandQueue,chatThreads, clientSockets, clientSocket, clientAddress):
		threading.Thread.__init__(self)
		self.commandQueue=commandQueue
		self.chatThreads=chatThreads
		self.clientSockets=clientSockets
		self.clientSocket=clientSocket
		self.clientAddress=clientAddress


	def run(self):
		try:
			while self.clientSocket:
				rlist,wlist,xlist=select.select([self.clientSocket],[],[],10)
				for sock in rlist:
					if sock==self.clientSocket:
						data=sock.recv(BUFF_SIZE).decode()
					if not data:
						exit()
					print('[cli->srv]:',data)
					self.commandQueue.put(data)
		except:
			print('[srv]: exit2 :',self.clientSocket)
			self.clientSocket.close()
			self.clientSockets.remove(self.clientSocket)
			self.chatThreads.remove(self)
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

raspServer=ChatServer(commandQueue, host, port)
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
