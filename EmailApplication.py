#!/usr/bin/python3

# Development platform: Windows
# Python version: 3.8.10

from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from tkinter import filedialog
import re
import os
import pathlib
import sys
import base64
import socket
#import ssl

#
# Global variables
#

# Replace this variable with your CS email address
YOUREMAIL = "tylo2@cs.hku.hk"
# Replace this variable with your student number
MARKER = '3035782188'

# The Email SMTP Server
SERVER = "testmail.cs.hku.hk"   #SMTP Email Server
TESTSERVER = 'smtp.gmail.com' 
SPORT = 25                    #SMTP listening port

# For storing the attachment file information
fileobj = None                  #For pointing to the opened file
filename = ''                   #For keeping the filename


#
# For the SMTP communication
#
  
def do_Send():
  
  # Initialization 
  sendingCheck = 3    #Become to 0 when all checking done
  formatCheck = 0      #Become 0 when all checking done
  ToFieldPresent = True
      
  # Input Field checking
  
  if get_TO() == "":
    alertbox("Must enter the recipient's email")
    ToFieldPresent = False
    sendingCheck -= 1
  if get_Subject() == "":
    alertbox("Must enter the subject")
    sendingCheck -= 1
  if len(get_Msg()) == 1:
    alertbox("Must enter the message")
    sendingCheck -= 1
  
  # Email format checking
  # Checking TO:
  
  if ToFieldPresent:
    TO_List = [x.strip() for x in get_TO().split(',')]
    TO_notok = []
    for x in TO_List:
      if not echeck(x):
        TO_notok.append(x)
    if TO_notok != []:
      formatCheck -= 1
      alertbox("Invalid TO: Email - " + ', '.join(map(str, TO_notok)))
  
  # Checking CC:
  CC_List = [x.strip() for x in get_CC().split(',')]
  if CC_List != ['']:
    CC_notok = []
    for x in CC_List:
      if not echeck(x):
        CC_notok.append(x)
    if CC_notok != []:
      formatCheck -= 1
      alertbox("Invalid CC: Email - " + ', '.join(map(str, CC_notok)))
  
  # Checking BCC:
  BCC_List = [x.strip() for x in get_BCC().split(',')]
  if BCC_List != ['']:
    BCC_notok = []
    for x in BCC_List:
      if not echeck(x):
        BCC_notok.append(x)
    if BCC_notok != []:
      formatCheck -= 1
      alertbox("Invalid BCC: Email - " + ', '.join(map(str, BCC_notok)))
      
      
  # If passed all check then proceed to send
  if sendingCheck == 3 and formatCheck == 0:         
    
    # initialize message and socket 
    endmsg = "\r\n"
    message = get_Msg()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # client socket connect to mail server
    client_socket.connect((SERVER, SPORT))
    # set timeout to 10s
    client_socket.settimeout(10)
    
    try:
      recv = client_socket.recv(1024).decode()
    except socket.timeout:
      alertbox("SMTP server is not available")
      client_socket.close()
      print("Connection Terminated")
      return
    
    print(recv)
    if recv[:3] != '220':
        print("220 reply not received from server.")
        alertbox("Fail to connect to server\n" + recv)
        client_socket.close()
        print("Connection Terminated")
        return
      
    # Hi server    
    ehloCommand = ("EHLO me" + endmsg).encode()
    print("EHLO " + socket.gethostbyname(socket.gethostname()) + "\n")
    client_socket.send(ehloCommand)
    
    try:
      recv1 = client_socket.recv(1024).decode()
    except socket.timeout:
      alertbox("SMTP server is not available")
      client_socket.close()
      print("Connection Terminated")
      return
    
    print(recv1)

    if recv1[:3] != '250':
      print('250 reply not received from server.')
      alertbox("Fail in EHLO TEST TO\n" + recv1)
      client_socket.close()
      print("Connection Terminated")
      return
      

    #Print Command
    # MAIL FROM
    mailCommand = ("MAIL FROM: <" + YOUREMAIL + ">" + endmsg).encode()
    print(mailCommand.decode())
    client_socket.send(mailCommand)
    
    try:
      recv2 = client_socket.recv(1024).decode()
    except socket.timeout:
      alertbox("SMTP server is not available")
      client_socket.close()
      print("Connection Terminated")
      return
    
    print(recv2)
    if recv2[:3] != '250':
      print('250 reply not received from server.')
      alertbox("Fail in sending RCPT TO\n" + recv2)
      client_socket.close()
      print("Connection Terminated")
      return
    
    # RCPT TO (TO,CC,BCC)
    if TO_List != ['']:
      for i in range(len(TO_List)):
        mailCommand = ("RCPT TO: <" + TO_List[i] + ">" + endmsg).encode()
        print(mailCommand.decode())
        client_socket.send(mailCommand)
        
        try:
          recv3 = client_socket.recv(1024).decode()
        except socket.timeout:
          alertbox("SMTP server is not available")
          client_socket.close()
          print("Connection Terminated")
          return
        
        print(recv3)
        if recv3[:3] != '250':
          print('250 reply not received from server.')
          alertbox("Fail in sending RCPT TO\n" + recv3)
          client_socket.close()
          print("Connection Terminated")
          return
        
    if CC_List != ['']:      
      for i in range(len(CC_List)):
        mailCommand = ("RCPT TO: <" + CC_List[i] + ">" + endmsg).encode()
        print(mailCommand.decode())
        client_socket.send(mailCommand)
        
        try:
          recv3 = client_socket.recv(1024).decode()
        except socket.timeout:
          alertbox("SMTP server is not available")
          client_socket.close()
          print("Connection Terminated")
          return
        
        print(recv3)
        if recv3[:3] != '250':
          print('250 reply not received from server.')
          alertbox("Fail in sending RCPT TO\n" + recv3)
          client_socket.close()
          print("Connection Terminated")
          return
        
    if BCC_List != ['']:      
      for i in range(len(CC_List)):
        mailCommand = ("RCPT TO: <" + BCC_List[i] + ">" + endmsg).encode()
        print(mailCommand.decode())
        client_socket.send(mailCommand)
        
        try:
          recv3 = client_socket.recv(1024).decode()
        except socket.timeout:
          alertbox("SMTP server is not available")
          client_socket.close()
          print("Connection Terminated")
          return
        
        print(recv3)
        if recv3[:3] != '250':
          print('250 reply not received from server.')
          alertbox("Fail in sending RCPT TO\n" + recv3)
          client_socket.close()
          print("Connection Terminated")
          return
          
    # DATA  
    dataCommand = ("DATA" + endmsg).encode()
    print(dataCommand.decode())
    client_socket.send(dataCommand)
    
    try:
      recv4 = client_socket.recv(1024).decode()
    except socket.timeout:
      alertbox("SMTP server is not available")
      client_socket.close()
      print("Connection Terminated")
      return
    
    print(recv4)
    if recv4[:3] != '354':
        print('354 reply not received from server.')
        alertbox("Fail in sending DATA TO\n" + recv4)
        client_socket.close()
        print("Connection Terminated")
        return
        
    """
    MIME Formatting 
    """    
    # From
    client_socket.send(("From: " + YOUREMAIL + endmsg).encode())
    # Subject
    subject = "Subject: " + get_Subject()  + endmsg 
    client_socket.send(subject.encode())
    # TO:
    if TO_List != ['']:
      client_socket.send("To: ".encode())
      for i in range(len(TO_List)):
        client_socket.send((TO_List[i]).encode())
        if i != len(TO_List):
          client_socket.send((",").encode())
      client_socket.send(endmsg.encode())
    # CC:
    if CC_List != ['']:
      client_socket.send("Cc: ".encode())
      for i in range(len(CC_List)):
        client_socket.send((CC_List[i]).encode())
        if i != len(CC_List):
          client_socket.send((",").encode())
      client_socket.send((endmsg).encode())    
           
    dataCommand = ("MIME-Version: 1.0" + endmsg).encode()
    #print(dataCommand.decode())
    client_socket.send(dataCommand)
    
    dataCommand = ("Content-Type: multipart/mixed; boundary=" + MARKER + endmsg).encode()
    #print(dataCommand.decode())
    client_socket.send(dataCommand)
    client_socket.send(endmsg.encode())   
                 
    dataCommand = ("--" + MARKER + endmsg).encode()
    #print(dataCommand.decode())
    client_socket.send(dataCommand) 
       
    dataCommand = ("Content-Type: text/plain" + endmsg).encode()
    #print(dataCommand.decode())
    client_socket.send(dataCommand)
        
    dataCommand = ("Content-Transfer-Encoding: 7bit" + endmsg).encode()
    #print(dataCommand.decode())
    client_socket.send(dataCommand)    
    client_socket.send(endmsg.encode())  
                  
    # Send main message
    client_socket.send((message + endmsg).encode())
    #client_socket.send(endmsg.encode())
  

    #Send file if exists
    if fileobj != None:
      
      dataCommand = ("--" + MARKER + endmsg).encode()
      #print(dataCommand.decode())
      client_socket.send(dataCommand)
      
      dataCommand = ("Content-Type: application/octet-stream" +  endmsg).encode()
      #print(dataCommand.decode())
      client_socket.send(dataCommand)
      
      dataCommand = ("Content-Transfer-Encoding: base64" + endmsg ).encode()
      #print(dataCommand.decode())
      client_socket.send(dataCommand)    
      
      dataCommand = ("Content-Disposition: attachment; filename=" + filename + endmsg).encode()
      #print(dataCommand.decode())
      client_socket.send(dataCommand)   
      client_socket.send(endmsg.encode())  
      
      while True:
        filedata = fileobj.read(-1)
        #print(filedata)
        if not filedata:
          break
        client_socket.send(base64.encodebytes(filedata))
      
    dataCommand = ("--" + MARKER + "--" + endmsg).encode()
    #print(dataCommand.decode())
    client_socket.send(dataCommand)  
    
    # End DATA
    client_socket.send(".\r\n".encode())
    
    try:
      recv5 = client_socket.recv(1024).decode()
    except socket.timeout:
      alertbox("SMTP server is not available")
      client_socket.close()
      print("Connection Terminated")
      return
    
    print(recv5)
    if recv5[:3] != '250':
        print('250 reply not received from server.')
        alertbox("Fail in sending end message TO\n" + recv5)
        client_socket.close()
        print("Connection Terminated")
        return
                
              
    # Quit 
    quitCommand = 'QUIT\r\n'.encode()
    print(quitCommand.decode())
    client_socket.send(quitCommand)
    
    try:
      recv6 = client_socket.recv(1024).decode()
    except:
      alertbox("SMTP server is not available")
      client_socket.close()
      print("Connection Terminated")
      return
    
    print(recv6)
    if recv6[:3] != '221':
        print('quit 221 reply not received from server.')
        alertbox("Fail in sending QUIT TO\n" + recv6)
        client_socket.close()
        print("Connection Terminated")
        return
    
    alertbox("Successful")
    quit()
      
  
#
# Utility functions
#

#This set of functions is for getting the user's inputs
def get_TO():
  return tofield.get()

def get_CC():
  return ccfield.get()

def get_BCC():
  return bccfield.get()

def get_Subject():
  return subjfield.get()

def get_Msg():
  return SendMsg.get(1.0, END)

#This function checks whether the input is a valid email
def echeck(email):   
  regex = '^([A-Za-z0-9]+[.\-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'  
  if(re.fullmatch(regex,email)):   
    return True  
  else:   
    return False

#This function displays an alert box with the provided message
def alertbox(msg):
  messagebox.showwarning(message=msg, icon='warning', title='Alert', parent=win)

#This function calls the file dialog for selecting the attachment file.
#If successful, it stores the opened file object to the global
#variable fileobj and the filename (without the path) to the global
#variable filename. It displays the filename below the Attach button.
def do_Select():
  global fileobj, filename
  if fileobj:
    fileobj.close()
  fileobj = None
  filename = ''
  filepath = filedialog.askopenfilename(parent=win)
  if (not filepath):
    return
  print(filepath)
  if sys.platform.startswith('win32'):
    filename = pathlib.PureWindowsPath(filepath).name
  else:
    filename = pathlib.PurePosixPath(filepath).name
  try:
    fileobj = open(filepath,'rb')
  except OSError as emsg:
    print('Error in open the file: %s' % str(emsg))
    fileobj = None
    filename = ''
  if (filename):
    showfile.set(filename)
  else:
    alertbox('Cannot open the selected file')

#################################################################################
#Do not make changes to the following code. They are for the UI                 #
#################################################################################

#
# Set up of Basic UI
#
win = Tk()
win.title("EmailApp")

#Special font settings
boldfont = font.Font(weight="bold")

#Frame for displaying connection parameters
frame1 = ttk.Frame(win, borderwidth=1)
frame1.grid(column=0,row=0,sticky="w")
ttk.Label(frame1, text="SERVER", padding="5" ).grid(column=0, row=0)
ttk.Label(frame1, text=SERVER, foreground="green", padding="5", font=boldfont).grid(column=1,row=0)
ttk.Label(frame1, text="PORT", padding="5" ).grid(column=2, row=0)
ttk.Label(frame1, text=str(SPORT), foreground="green", padding="5", font=boldfont).grid(column=3,row=0)

#Frame for From:, To:, CC:, Bcc:, Subject: fields
frame2 = ttk.Frame(win, borderwidth=0)
frame2.grid(column=0,row=2,padx=8,sticky="ew")
frame2.grid_columnconfigure(1,weight=1)
#From 
ttk.Label(frame2, text="From: ", padding='1', font=boldfont).grid(column=0,row=0,padx=5,pady=3,sticky="w")
fromfield = StringVar(value=YOUREMAIL)
ttk.Entry(frame2, textvariable=fromfield, state=DISABLED).grid(column=1,row=0,sticky="ew")
#To
ttk.Label(frame2, text="To: ", padding='1', font=boldfont).grid(column=0,row=1,padx=5,pady=3,sticky="w")
tofield = StringVar()
ttk.Entry(frame2, textvariable=tofield).grid(column=1,row=1,sticky="ew")
#Cc
ttk.Label(frame2, text="Cc: ", padding='1', font=boldfont).grid(column=0,row=2,padx=5,pady=3,sticky="w")
ccfield = StringVar()
ttk.Entry(frame2, textvariable=ccfield).grid(column=1,row=2,sticky="ew")
#Bcc
ttk.Label(frame2, text="Bcc: ", padding='1', font=boldfont).grid(column=0,row=3,padx=5,pady=3,sticky="w")
bccfield = StringVar()
ttk.Entry(frame2, textvariable=bccfield).grid(column=1,row=3,sticky="ew")
#Subject
ttk.Label(frame2, text="Subject: ", padding='1', font=boldfont).grid(column=0,row=4,padx=5,pady=3,sticky="w")
subjfield = StringVar()
ttk.Entry(frame2, textvariable=subjfield).grid(column=1,row=4,sticky="ew")

#frame for user to enter the outgoing message
frame3 = ttk.Frame(win, borderwidth=0)
frame3.grid(column=0,row=4,sticky="ew")
frame3.grid_columnconfigure(0,weight=1)
scrollbar = ttk.Scrollbar(frame3)
scrollbar.grid(column=1,row=1,sticky="ns")
ttk.Label(frame3, text="Message:", padding='1', font=boldfont).grid(column=0, row=0,padx=5,pady=3,sticky="w")
SendMsg = Text(frame3, height='10', padx=5, pady=5)
SendMsg.grid(column=0,row=1,padx=5,sticky="ew")
SendMsg.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=SendMsg.yview)

#frame for the button
frame4 = ttk.Frame(win,borderwidth=0)
frame4.grid(column=0,row=6,sticky="ew")
frame4.grid_columnconfigure(1,weight=1)
Sbutt = Button(frame4, width=5,relief=RAISED,text="SEND",command=do_Send).grid(column=0,row=0,pady=8,padx=5,sticky="w")
Atbutt = Button(frame4, width=5,relief=RAISED,text="Attach",command=do_Select).grid(column=1,row=0,pady=8,padx=10,sticky="e")
showfile = StringVar()
ttk.Label(frame4, textvariable=showfile).grid(column=1, row=1,padx=10,pady=3,sticky="e")

win.mainloop()

