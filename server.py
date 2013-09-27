import socket
import thread
import xmpp

IP = '127.0.0.1'
PORT = 5222
BUFFER_SIZE = 1024 # use a power of 2 number
ID = 4235063100
onlineList = []
msgList = {}

def handler(client_conn, client_addr):
	global ID
	global msgList
	global onlineList

	print "Connected with ", client_addr # Debug print
	
	# Client request: create stream
	data = client_conn.recv(BUFFER_SIZE)
	print "Message from client: ", data  # Debug print
	
	# Server response: stream ID and available features
	resStream = "<?xml version=\'1.0\'?>" 
	resStream += "<stream:stream xmlns=\'jabber:client\' xmlns:stream=\'http://etherx.jabber.org/streams\'"
	resStream += " id=\'" + str(ID) + "\' from=\'" + str(IP) + "\' version=\'1.0\' xml:lang=\'en\'>"
	ID += 1
	resStream += "<stream:features>"
	resStream += "<compression xmlns=\"http://jabber.org/features/compress\">"
	resStream += "<method>zlib</method>"
	resStream += "</compression>"
	resStream += "<auth xmlns=\'http://jabber.org/features/iq-auth\'/>"
	resStream += "</stream:features>"	
	client_conn.send(resStream)
	
	# Client request: Authentication Fields
	data = client_conn.recv(BUFFER_SIZE)
	iq = xmpp.protocol.Iq(node=data)
	iqId = iq.getID()
	iqUser = iq.getCDATA()
	msgList[iqUser] = []
	
	# Server response: Authentication Fields
	resIq = "<iq id=\'" + str(iqId) + "\' type=\'result\'><query xmlns=\'jabber:iq:auth\'><username/><password/><digest/><resource/></query></iq>"
	client_conn.send(resIq)
	
	# Client response: Authentication information
	data = client_conn.recv(BUFFER_SIZE)
	iq = xmpp.protocol.Iq(node=data)
	iqId = iq.getID()
	userDigest = iq.getCDATA()
	userDigest = userDigest.replace(iqUser,"")
	userDigest = userDigest.replace("botty","")
	onlineList.append(iqUser)
	print "User:", iqUser		# Debug print
	print "Digest:", userDigest # Debug print
	
	# Server response: Authentication status
	authResponse = "<iq type=\'result\' id=\'" + str(iqId) + "'/>"
	client_conn.send(authResponse)
	
	# Client: Presence
	data = client_conn.recv(BUFFER_SIZE)	
	queryItens = ""
	for x in onlineList:
		queryItens += "<item name=\"" + x + "\"/>"
	onlineStatus = xmpp.protocol.Iq(node="<iq> <query xmlns=\"http://jabber.org/protocol/disco#items\" node=\"online users\" >" + queryItens + "</query> </iq>")
	client_conn.send(str(onlineStatus))
	
	# Message handler	
	while 1:		
		data = client_conn.recv(BUFFER_SIZE)
		
		# Disconnect
		if data == "</stream:stream>":
			onlineList.remove(iqUser)
			client_conn.send("</stream:stream>")
			break
		
		# Refresh online list
		queryItens = ""
		for x in onlineList:
			queryItens += "<item name=\"" + x + "\"/>"
		onlineStatus = xmpp.protocol.Iq(node="<iq> <query xmlns=\"http://jabber.org/protocol/disco#items\" node=\"online users\" >" + queryItens + "</query> </iq>")
		client_conn.send(str(onlineStatus))
		
		# Receive a message from the client
		if data.find("<message") >= 0 :
			msgP = xmpp.protocol.Message(node=data)			
			msgTo = msgP.getTo()
			if str(msgTo) in onlineList:
				if len(msgList[str(msgTo)]) > 0: 
					msgList[msgTo].insert(0,msgP)
				else:
					msgList[str(msgTo)].append(msgP)		
			
		# Send all message to the client
		while len(msgList[iqUser]) > 0:
			string1 = str(msgList[iqUser].pop())
			print string1
			client_conn.send(string1)
	
	print "Connetion with ", client_addr, " is closed"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(5)

while 1:
	print 'Waiting for connection'	
	conn, addr = s.accept()
	thread.start_new_thread(handler, (conn, addr))
	#handler(conn,addr)
	
