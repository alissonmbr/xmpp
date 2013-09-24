import socket
import thread
import xmpp

IP = '127.0.0.1'
PORT = 5222
BUFFER_SIZE = 1024 # use a power of 2 number
ID = 4235063100

def handler(client_conn, client_addr):
	print "Connected with ", client_addr
	data = client_conn.recv(BUFFER_SIZE)
	print "Message from client: ", data
	
	res = "<?xml version=\'1.0\'?>" 
	#change id
	res += "<stream:stream xmlns=\'jabber:client\' xmlns:stream=\'http://etherx.jabber.org/streams\'"
	res += " id=\'" + str(ID) + "\' from=\'127.0.0.1\' version=\'1.0\' xml:lang=\'en\'>"
	res += "<stream:features>"
	res += "<compression xmlns=\"http://jabber.org/features/compress\">"
	res += "<method>zlib</method>"
	res += "</compression>"
	res += "<auth xmlns=\'http://jabber.org/features/iq-auth\'/>"
	res += "</stream:features>"
	
	client_conn.send(res)
	
	while 1:
		data = client_conn.recv(BUFFER_SIZE)
		print "Message from client: ", data
				
		#con  = "<?xml version=\'1.0\'?><stream:stream xmlns=\"jabber:client\" to=\"127.0.0.1\" version=\"1.0\" xmlns:stream=\"http://etherx.jabber.org/streams\" >"
		
		#if data == con:
		#	client_conn.send(res)
		#	print "Con"
		if data == "<iq type=\"get\" id=\"1\"><query xmlns=\"jabber:iq:auth\"><username>user1</username></query></iq>":
			client_conn.send("<iq id=\'1\' type=\'result\'><query xmlns=\'jabber:iq:auth\'><username>username</username><password/><digest/><sequence>499</sequence><token>3D5A392D</token><resource/></query></iq>")
		else: #data == "<iq type=\"set\" id=\"2\"><query xmlns=\"jabber:iq:auth\"><username /><digest>00f2dd21edafe827d8369a7e7b9c52aa2b09cc31</digest><sequence>499</sequence><token>3D5A392D</token><resource>xmpppy</resource></query></iq>"
			client_conn.send("<iq id=\'2\' type=\'result\'/>")
		#elif data == "<starttls xmlns=\"urn:ietf:params:xml:ns:xmpp-tls\"/>":
		#	client_conn.send("<proceed xmlns=\"urn:ietf:params:xml:ns:xmpp-tls\"/>")
		#	print "Data"
		#else :
		#	client_conn.send("<success xmlns=\'urn:ietf:params:xml:ns:xmpp-sasl\'/>")
		#	print "Else"
		#client_conn.send("res")
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
	
