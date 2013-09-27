import socket
import sys
import xmpp
import getpass
import thread
import select

IP = '127.0.0.1'
PORT = 5222
BUFFER_SIZE = 1024

onlineList = []

def messageCB(sess,mess):
	message = xmpp.protocol.Message(node=mess)
	msgFrom = message.getFrom()
	msgTo = message.getTo()
	msgText = message.getBody()
	#print msgFrom, msgTo, msgText # Debug print
	#if len(msgText) > 0:
	print msgFrom, ">>", msgText

def iqCB(sess,mess):
	iq = xmpp.protocol.Iq(node=mess)
	query = iq.getTag("query")
	itens = query.getTags("item")
	global onlineList
	onlineList = []
	for item in itens:
		onlineList.append(str(item).replace("<item name=\"","").replace("\" />",""))
	print "Online:"
	for item in onlineList:
		print "\t" + item

# User name and password
sys.stdout.write("User: ")
userName = sys.stdin.readline()
userName = userName.replace("\n","")
pwd = getpass.getpass()

# Connect with the server
#jid = xmpp.JID(userName)
connection = xmpp.Client(IP)
print "Connecting..."
connection.connect((IP, PORT))
connection.RegisterHandler("message", messageCB)
connection.RegisterHandler("iq", iqCB)
result = connection.auth(userName, pwd, 'botty')
connection.sendInitPresence()
print "Connected!"

while 1:
	connection.Process(1)
	sys.stdout.write("To: ")
	userTo = sys.stdin.readline().strip()
	if userTo == ":close":
		break
	message = ""
	if len(userTo) > 0:
		sys.stdout.write("Message: ")
		message = sys.stdin.readline().strip()	
	msg = xmpp.Message(userTo, message)
	connection.send(msg)

connection.disconnect()
