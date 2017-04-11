import threading
import socket
import select
import sys
import queue
BUFF_SIZE=1024

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
