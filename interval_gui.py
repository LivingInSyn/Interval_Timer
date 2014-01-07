from tkinter import *
import sys
import time
import os

class Application(Frame):
	def __init__(self,master):
		super(Application,self).__init__(master)
		self.grid()
		self.welcome_screen()
		#self.new_intervals()

	def welcome_screen(self):
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

	def back_new(self):
		for i in range(len(self.boxes)):
			self.boxes[i].destroy()
		self.back_button.destroy()
		self.start_button.destroy()
		self.welcome_screen()

	def start(self):
		#first get the entries from the boxes and put them into two lists		
		i=0
		self.names=[]		
		while i < len(self.boxes):
			if self.boxes[i].get() != '':		
				self.names.append(self.boxes[i].get())
			i=i+2
		i=1
		self.times=[]
		while i < len(self.boxes):
			if self.boxes[i].get() != '':
				self.times.append(self.boxes[i].get())
			i = i+2

		#next clear and display the new display
		#clear		
		for i in self.boxes:
			i.destroy()
		self.int_label.destroy()
		self.int_time_label.destroy()
		self.back_button.destroy()
		self.start_button.destroy()
		#new

		#create a custom font for the label
		self.running_font = ('Times',24,'bold')
		self.running_label = Label(self,text="Your intervals are running",font=self.running_font)
		self.running_label.grid(row=0,column=0,columnspan=2)
		#run the intervals
		self.run_ints()

	def run_ints(self):
		i=0
		for x in self.times:
			x = float(x)			
			a=x*60
			#print("starting interval named ", self.names[i])
			#replace print with a label with the name
			#self.current_int_label.destroy()
			self.int_label_font = ('Times',16,'bold')	
			self.time_label_font= ('Times',16,'bold')		
			self.current_int_label = Label(self,text=self.names[i],font=self.int_label_font)
			self.current_int_label.grid(row=1,column=0)
			root.update()
			os.system("say "+"'"+self.names[i]+"'"+" 2>/dev/null")
			while a > 0:
				time.sleep(1)
				#print(a)
				self.current_time_label = Label(self,text=str(a),font=self.time_label_font)
				self.current_time_label.grid(row=1,column=1)
				a = a-1
				root.update()
			i+=1
		os.system("say 'Workout Done' 2>/dev/null")
		self.running_label["text"] = "Workout Done!"
		root.update()

	def exit(self):
		sys.exit(0)

		


root = Tk()
root.title("LivingInSyn's Interval Timer")
root.geometry("400x500")
app=Application(root)
root.mainloop()
		
		

