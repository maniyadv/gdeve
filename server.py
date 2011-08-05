#############   gDEVE  ###############
############# server.py ###############
########Software Engineering Lab #######

# importing necessary packages
from twisted.internet import reactor, protocol
from twisted.protocols import basic

import time

# for timevalues
def timeStamp():
    return "["+ time.strftime("%H:%M:%S") +"] "

class EchoProtocol(basic.LineReceiver):
    name = "Unnamed"

    def connectionMade(self):
        self.sendLine("This is Test Message !!")
        self.sendLine("")
        self.count = 0
        self.factory.clients.append(self)
        print timeStamp() + "+ Connection from: "+ self.transport.getPeer().host

    def connectionLost(self, reason):
        self.sendMsg("- %s left." % self.name)
        print timeStamp() + "- Connection lost: "+ self.name
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        if line == 'quit':
            self.sendLine("Disconnecting")
            self.transport.loseConnection()
            return
        elif line == "userlist":
            self.chatters()
            return
        if not self.count:
            self.username(line)
        else:
	    self.sendMsg(line)


    def username(self, line):
        for x in self.factory.clients:
            if x.name == line:
                self.sendLine("This username is taken; please choose another")
                return

        self.name = line
        self.chatters()
        self.sendLine("Online")
        self.sendLine("")
        self.count += 1
        self.sendMsg("+ %s joined." % self.name)
        print '%s~ %s is now known as %s' % (timeStamp(), self.transport.getPeer().host, self.name)

    def chatters(self):
        x = len(self.factory.clients) - 1
        s = 'is' if x == 1 else 'are'
        p = 'person' if x == 1 else 'people'
        self.sendLine("There %s %i %s connected:" % (s, x, p) )

        for client in self.factory.clients:
            if client is not self:
                self.sendLine(client.name)
        self.sendLine("")

    def sendMsg(self, message):
        for client in self.factory.clients:
		 if client is not self:
			client.sendLine(message)


class EchoServerFactory(protocol.ServerFactory):
    protocol  = EchoProtocol
    clients = []

if __name__ == "__main__":
    reactor.listenTCP(5005, EchoServerFactory())
    reactor.run()
