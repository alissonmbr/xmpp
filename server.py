import socket
import thread
import xmpp

IP = '127.0.0.1'
PORT = 5222
BUFFER_SIZE = 1024 # use a power of 2 number
ID = 4235063100

def handler(client_conn, client_addr):
	global ID

	print "Connected with ", client_addr # Debug print
	
	# Client request: create stream
	data = client_conn.recv(BUFFER_SIZE) # Debug print
	print "Message from client: ", data
	
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
	print "User:", iqUser		# Debug print
	print "Digest:", userDigest # Debug print
	
	# Server response: Authentication status
	if 1:
		authResponse = "<iq type=\'result\' id=\'" + str(iqId) + "'/>"
		client_conn.send(authResponse)
	else:
		authResponse = "<iq type=\'result\' id=\'" + str(iqId) + "'><error code=\'401\' type=\'auth\'> <not-authorized xmlns=\'urn:ietf:params:xml:ns:xmpp-stanzas\'/> </error></iq>"
		client_conn.send(authResponse)
	
	# Message handler	
	while 1:
		data = client_conn.recv(BUFFER_SIZE)
		print "Message from client: ", data
		
		if data == "close\n":
			client_conn.send("Bye..")
			client_conn.close()
			break
	print "Connetion with ", client_addr, " is closed"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(5)

while 1:
	print 'Waiting for connection'	
	conn, addr = s.accept()
	thread.start_new_thread(handler, (conn, addr))
	#handler(conn,addr)
	
