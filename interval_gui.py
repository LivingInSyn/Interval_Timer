from tkinter import *
import sys
import time
import os

class Application(Frame):
	def __init__(self,master):
		#constructor, calls welcome screen, calls Frame constructor, sets grid layout		
		super(Application,self).__init__(master)
		self.grid()
		self.welcome_screen()
		

	def welcome_screen(self):
		#3 buttons and their settings
		self.new_button = Button(self, text = "New Intervals",width=50)
		self.new_button.grid(row = 0, column = 0,sticky=W)
		self.new_button["command"] = self.new_intervals
		self.load_button = Button(self, text = "Load Interval CSV",width=50)
		self.load_button.grid(row=1, column = 0, sticky=W)
		self.quit_button = Button(self, text = "Quit",width=50)
		self.quit_button.grid(row=2, column=0, sticky=W)
		self.quit_button["command"] = self.exit

	def new_intervals(self):
		#remove the old buttons		
		self.new_button.destroy()
		self.load_button.destroy()
		self.quit_button.destroy()
		#create the new labels
		self.int_label = Label(self,text="Interval Name")
		self.int_label.grid(row=0, column=0,sticky=W)
		self.int_time_label = Label(self,text="Time (in minutes)")
		self.int_time_label.grid(row=0, column=1,sticky=W)
		#create the text boxes
		self.boxes = []
		i=0
		for r in range(1,16):
			for c in range(2):
				self.boxes.append(Entry(self))			
				self.boxes[i].grid(row=r,column=c,sticky=W)
				i+=1
		#create back/start buttons
		self.back_button = Button(self,text="Back")
		self.back_button.grid(row=16,column=0,sticky=W)
		self.back_button["command"] = self.back_new
		self.start_button = Button(self,text = "Start")
		self.start_button.grid(row=16,column=1,sticky=E)
		self.start_button["command"] = self.start
		#manually update the window
		root.update()

	def back_new(self):
		#back function from the new setup, destroys all the current boxes and calls welcome screen
		for i in range(len(self.boxes)):
			self.boxes[i].destroy()
		self.back_button.destroy()
		self.start_button.destroy()
		self.welcome_screen()

	def start(self):
		#first get the entries from the boxes and put them into two lists, is_empty is used for error control		
		i=0
		self.is_empty = False
		self.names=[]		
		while i < len(self.boxes):
			#print(self.boxes[i].get())			
			if self.boxes[i].get() != '':		
				self.names.append(self.boxes[i].get())
			#if the first box is empty, call a popup with a dismiss button and set the error control/break the loop	
			elif self.boxes[0].get().strip() == '':
				self.is_empty = True
				popup = Toplevel(self)
				popup.title("Error")
				msg = Message(popup,text="You didn't enter in a time and/or an interval name in the first box")
				msg.pack()
				popup_button = Button(popup, text="Dismiss", command=lambda: popup.destroy())
				popup_button.pack()
				break
			i=i+2
		i=1
		self.times=[]
		while i < len(self.boxes):
			x = self.boxes[i].get()
			if x != '':	
				try:
					x = float(x)
				except ValueError:
					self.is_empty = True
					popup = Toplevel(self)
					popup.title("Error")
					msg = Message(popup,text="Something you entered in the time field isn't a number")
					msg.pack()
					popup_button = Button(popup, text="Dismiss", command=lambda: popup.destroy())
					popup_button.pack()
					break
				self.times.append(self.boxes[i].get())
			i = i+2

		#next clear and display the new display
		#clear, only if our error control allows it

		if self.is_empty == False:		
			for i in self.boxes:
				i.destroy()
			self.int_label.destroy()
			self.int_time_label.destroy()
			self.back_button.destroy()
			self.start_button.destroy()
		
		#new, if error control allows it
		if self.is_empty == False:
			#create a custom font for the label
			self.running_font = ('Times',24,'bold')
			self.running_label = Label(self,text="Your intervals are running",font=self.running_font)
			self.running_label.grid(row=0,column=0,columnspan=2)

			#add the pause, back and quit buttons
			self.back_button_run = Button(self,text="Back",width=7)
			self.back_button_run["command"]=self.back_run
			self.back_button_run.grid(row=2,column=0,sticky=W)
			self.pause_button = Button(self,text="Pause",width=7)
			self.pause_button["command"]=self.pause
			self.pause_button.grid(row=3,column=0,sticky=W)
			self.quit = Button(self,text="Quit",width=7)
			self.quit["command"]=self.exit
			self.quit.grid(row=4,column=0,sticky=W)
			#run the intervals
			self.run_ints()

	def run_ints(self):
		self.run_status = True
		self.exit_status = False	
		i=0
		for x in self.times:		
			x = float(x)			
			a=x*60
			#print("starting interval named ", self.names[i])
			#replace print with a label with the name, destroy the old label if it's there
			try:
				self.current_int_label.destroy()
			except AttributeError:
				pass
			self.int_label_font = ('Times',16,'bold')	
			self.time_label_font= ('Times',16,'bold')		
			self.current_int_label = Label(self,text=self.names[i],font=self.int_label_font)
			self.current_int_label.grid(row=1,column=0)
			root.update()
			os.system("espeak "+"'"+self.names[i]+"'"+" 2>/dev/null")			
			while a > 0:
				#runstatus is there to allow the pause button
				if self.run_status==True:				
					#time.sleep(1)				
					self.current_time_label = Label(self,text=str(a),font=self.time_label_font)
					self.current_time_label.grid(row=1,column=1)
					a = a-1
					time.sleep(1)
					root.update()
				else:
					time.sleep(.1)
					root.update()
				if self.exit_status == True:
					#exit status helps us quit
					break
				else:
					pass
			if self.exit_status == True:
				#print("we broke out of the for loop")				
				break
			else:
				pass
			i+=1
		if self.exit_status == False:		
			self.current_time_label["text"] = "      "
			self.current_int_label["text"] = "      "
			os.system("espeak 'Workout Done' 2>/dev/null")
			self.running_label["text"] = "Workout Done!"
			root.update()
		else:
			pass

	def exit(self):
		print("exit clicked")
		self.exit_status = True
		root.update()		
		sys.exit(0)

	def pause(self):
		print("pause clicked")		
		if self.run_status == True:
			self.run_status = False
		else:
			self.run_status = True

	def back_run(self):
		self.exit_status = True
		#self.new_intervals()		
		self.back_button_run.destroy()
		self.pause_button.destroy()
		self.quit.destroy()
		self.current_int_label.destroy()
		self.current_time_label.destroy()
		self.running_label.destroy()
		root.update()
		self.new_intervals()

		


root = Tk()
root.title("LivingInSyn's Interval Timer")
root.geometry("400x500")
app=Application(root)
root.mainloop()
		
		

