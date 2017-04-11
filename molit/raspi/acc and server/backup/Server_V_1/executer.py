class Executer:
	def __init__(self, tcpServer):
		self.andRaspTCP = tcpServer
	
	def startCommand(self, command):
		if command == "123\n":
			self.andRaspTCP.sendAll("123\n")
		elif command == "456\n":
			self.andRaspTCP.sendAll("456\n")
		elif command == "789\n":
			self.andRaspTCP.sendAll("789\n")
		else:
			pass
