#############   gDEVE  ###############
############# client.py ###############
######## Software Engineering Lab#######

# Importing required packages 
import re                               
import wx
import wx.aui
import wx.html
from twisted.internet import wxreactor
wxreactor.install()

# import twisted reactor *only after* installing wxreactor
from twisted.internet import reactor, protocol
from twisted.protocols import basic
#----------------------------------------------------------------------


#Panel class for drawing tab windows for client   
class TestPanel(wx.Panel):
    def __init__(self, parent, log,data):
        self.protocol =ChatFactory
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        self.nb = wx.aui.AuiNotebook(self)
        self.WelcomePage =wx.html.HtmlWindow(parent, -1, wx.DefaultPosition)
        self.WelcomePage.SetPage(GetWelcomeText())
        self.nb.AddPage(self.WelcomePage, "WelcomePage")
        
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        
        MessageText='Type Your Name in UserPage First and Hit ENTER. Your First Line Will Corrospond to Your UserName  '
        self.MessagePage = wx.TextCtrl(self.nb, -1, MessageText,
                           style=wx.TE_MULTILINE| wx.TE_READONLY)
        self.MessagePage.SetFont(wx.Font(11, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL))
        self.nb.AddPage(self.MessagePage, 'Messages')
        
    
    
        self.UserPage = wx.TextCtrl(self.nb, -1, style=wx.TE_MULTILINE| wx.TE_PROCESS_ENTER)
        self.UserPage.SetFont(wx.Font(10, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL))
        self.nb.AddPage(self.UserPage, "User's Page")
        self.UserPage.Bind(wx.EVT_TEXT_ENTER, self.SendText)
        
    
# For sending text from User's Page window to other clients
    def SendText(self, evt):
        val = self.UserPage.GetValue()
        self.UserPage.SetValue(val+'\n')
        self.UserPage.SetInsertionPointEnd()
        self.protocol.sendLine(str(val))
        
# For adding tab windows         
    def AddPages(self,data,pageName):
        if pageName=='Messages':
            self.MessagePage = wx.TextCtrl(self.nb, -1, data,
                           style=wx.TE_MULTILINE)
            self.nb.AddPage(self.MessagePage, pageName)
        else:
            self.page = wx.TextCtrl(self.nb, -1, data,
                           style=wx.TE_MULTILINE| wx.TE_READONLY)
            self.page.SetFont(wx.Font(10, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL))
            self.nb.AddPage(self.page, pageName)
            
# For addind data to Receive Page        
    def AddPageData(self,data):
        self.page.SetValue(data)
        
  

# Main frame window class
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,parent= None, title="gDEVE for Google Summer of Code 2010", size = ( 700,400))
        self.protocol = None 
    

#data forwarding        
class DataForwardingProtocol(basic.LineReceiver,TestPanel):   
    def __init__(self):
        self.output = None
        self.flag=0
        self.a=[]
       
    def dataReceived(self, data):
        gui = self.factory.gui
        data1=data
        gui.protocol = self
        if self.flag==0:
            gui.AddPages('',"ReceivePage")
        else:
            gui.AddPageData(data)
            
        self.flag=self.flag+1
        
    def connectionMade(self):
        self.output = self.factory.gui # redirect Twisted's output

class ChatFactory(protocol.ClientFactory):
    def __init__(self, gui):
        self.gui = gui
        self.protocol = DataForwardingProtocol

    def clientConnectionLost(self, transport, reason):
        reactor.stop()

    def clientConnectionFailed(self, transport, reason):
        reactor.stop()
        

#Welcome page text
def GetWelcomeText():

    text = \
    "<html><body>" \
    "<h3>Welcome To Gnome Developer's Editor gDEVe</h3>" \
    "<br/><b>About</b><br/>" \
    "<p><b>gDEVe</b> is a lightweight Developer's Text Editor with User Interface written completely in wxPython " \
    "that allows developers to work with each other and with new users in a collaborative manner.</p>" \
    "</body></html>"

    return text


if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame()
    panel  = TestPanel(frame,'','')

    frame.Show()
    reactor.registerWxApp(app)
    reactor.connectTCP("localhost", 5005, ChatFactory(panel))
    reactor.run()
