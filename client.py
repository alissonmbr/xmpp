import socket
import sys
import xmpp

IP = '127.0.0.1'
PORT = 5222
BUFFER_SIZE = 1024

username = 'user1'
pwd = '1'
to = 'usr2'
msg = 'Hail'

jid = xmpp.JID(username)
connection = xmpp.Client('127.0.0.1')
print "Connecting..."
connection.connect((IP, PORT))
print "Connected!"
#result = connection.auth(jid.getNode(), pwd)
result = connection.auth(username, pwd, 'botty')
print "Result: ", result
connection.send(xmpp.Message(to,msg))
#print "Result: ", result 
#connection.sendInitPresence()
#connection.disconnect()

#message = xmpp.Message('me', 'Surprise motherfucker')
#connection.send(message)


while connection.Process(1):
	pass

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((IP, PORT))
#print "Type a message:"
#line = sys.stdin.readline()
#s.send(line)
#data = s.recv(BUFFER_SIZE)

#s.close()

#print "Message from server: ", data
