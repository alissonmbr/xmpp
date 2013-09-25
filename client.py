import socket
import sys
import xmpp
import getpass

IP = '127.0.0.1'
PORT = 5222
BUFFER_SIZE = 1024

to = 'usr2'
msg = 'Hail'

def messageCB(sess,mess):
    nick=mess.getFrom().getResource()
    text=mess.getBody()
    print nick,text
    print mess

# User name and password
print "User:"
userName = sys.stdin.readline()
userName = userName.replace("\n","")
pwd = getpass.getpass()

# Connect with the server
#jid = xmpp.JID(userName)
connection = xmpp.Client(IP)
print "Connecting..."
connection.connect((IP, PORT))
connection.RegisterHandler("message", messageCB)
result = connection.auth(userName, pwd, 'botty')
connection.sendInitPresence()

print "Connected!"

connection.send(xmpp.Message(to,msg))

while True:	
	connection.Process(1)
	

connection.disconnect()
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((IP, PORT))
#print "Type a message:"
#line = sys.stdin.readline()
#s.send(line)
#data = s.recv(BUFFER_SIZE)

#s.close()

#print "Message from server: ", data
