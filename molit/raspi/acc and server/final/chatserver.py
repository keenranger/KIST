import threading
import socket
import select
import sys
import queue
import chatthread
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
						chatThread=chatthread.ChatThread(self.commandQueue, self.chatThreads, self.clientSockets, clientSocket, clientAddress)
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
