'''
 * main.py
 * 
 * Sets up the main layout of the GUI
 * 
 * Major functionalities include:
 *     file/edit/view/analysis toolbar
 *         > open, save, quit
 *     specifies size of left frame and right frame
 *     sets up scrollbar of right frame
'''
try:
	from Tkinter import *
	root = Tk()
	import tkMessageBox
	from dnagui.GUI.CanvasFrame import CanvasFrame
	from dnagui.GUI.DockedWindows import DockedWindows
	from dnagui.GUI.Geometry import *
	import networkx as nx
	import tkFileDialog
	import pickle
	from sys import platform as _platform
	import sys
	import matplotlib.pyplot as plt

	# make sure modules used in other files are imported
	import tkSimpleDialog
	from datetime import datetime
	import matplotlib
	from mpl_toolkits.mplot3d import Axes3D
	import numpy as np
	from itertools import product, combinations
	from PIL import Image, ImageTk
	from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
	from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
	from matplotlib.figure import Figure

except ImportError, e:
	root.wm_withdraw()
	tkMessageBox.showerror('Import Error', 'Error: ' + str(e))
	quit()

class Window(Frame):
  
	def __init__(self, parent):
		Frame.__init__(self, parent)
		 
		self.parent = parent
		self.G = nx.DiGraph()
		self.D = nx.DiGraph()
		self.initUI()
			

	# exits out of gui when clicked on 
	def exit(self, event=None):
		self.quit()

	# will update saved file if filename already exists or open up save as function 
	def save(self, event=None):
		if hasattr(self, 'filename'):
			pickle.dump(self.G, open(str(self.filename), 'w'))
			# add to log file
			s = str(self.filename)
			filename = s.split('/')
			log = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Saved file: " + filename[len(filename)-1]
			self.geoCanvas.appendLog(log)
		else:
			self.save_as()

	# can save network x graph (node/edges and attributes) as any type of text file
	def save_as(self, event=None):
		for node in self.G.nodes():
			self.G.node[node]['systems'] = self.geoCanvas.manager.systems
		fileExt = tkFileDialog.asksaveasfilename(defaultextension=".txt")
		if fileExt != '': # asksaveasfile returns '' if dialog closed with "cancel".
			self.filename = fileExt
			s = str(self.filename)
			filename = s.split('/')
			self.parent.title("ANCR-GUI - " + filename[len(filename)-1])
			pickle.dump(self.G, open(str(self.filename), 'w'))

		# add to log file
		log = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Saved file as: " + str(self.filename)
		self.geoCanvas.appendLog(log)

	# can open any previously saved network x graph and plot nodes and edges onto the canvas, and resume all gui functionality 
	def open(self, event=None):
		fileExt = tkFileDialog.askopenfilename()
		if fileExt != '':
			self.filename = fileExt
			s = str(self.filename)
			filename = s.split('/')
			self.parent.title("ANCR-GUI - " + filename[len(filename)-1])

			self.G = pickle.load(open(str(self.filename)))
			self.G = nx.convert_node_labels_to_integers(self.G, first_label=1)
			for widget in self.leftFrame.winfo_children():
				widget.destroy()
			self.geoCanvas = CanvasFrame(self.leftFrame, self.rightCanvasFrame, self.G, self.D)
			self.createTabs()

			# redraw nodes
			for nodeNum in self.G.nodes():
				r = 8
				if 'Type' in self.G.node[nodeNum] and self.G.node[nodeNum]['Type'] == 'Compartment':
					self.geoCanvas.systemsCanvas.create_oval(self.G.node[nodeNum]['x_coord']-r, self.G.node[nodeNum]['y_coord']-r, self.G.node[nodeNum]['x_coord']+r, self.G.node[nodeNum]['y_coord']+r, fill='blue', tag='node') 
				else:
					self.geoCanvas.systemsCanvas.create_oval(self.G.node[nodeNum]['x_coord']-r, self.G.node[nodeNum]['y_coord']-r, self.G.node[nodeNum]['x_coord']+r, self.G.node[nodeNum]['y_coord']+r, fill='red', tag='node') 
			# redraw edges
			for startNode, endNode in self.G.edges():
				edgeItem=self.geoCanvas.systemsCanvas.create_line(self.G.edge[startNode][endNode]['x1_coord'], self.G.edge[startNode][endNode]['y1_coord'], self.G.edge[startNode][endNode]['x2_coord'], self.G.edge[startNode][endNode]['y2_coord'], tag='edge')
				self.geoCanvas.systemsCanvas.addtag_withtag(str(startNode), edgeItem)
				self.geoCanvas.systemsCanvas.addtag_withtag(str(endNode), edgeItem)
				self.G.edge[startNode][endNode]['edgeID'] = edgeItem
			
			# reload demands
			self.geoCanvas.manager.systems = self.G.node[1]['systems']
			for key in self.geoCanvas.manager.systems:
				self.geoCanvas.optionList.insert(len(self.geoCanvas.optionList)-2, key)
				self.geoCanvas.dropdown.destroy()
				self.geoCanvas.dropdown = OptionMenu(self.geoCanvas.toolbar, self.geoCanvas.v, *self.geoCanvas.optionList, command=self.geoCanvas.newOptionMenu)
				self.geoCanvas.dropdown.configure(bg="light blue")
				self.geoCanvas.dropdown.pack(side='left')

			# add to log file
			log = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Opened file: " + str(self.filename)
			self.geoCanvas.appendLog(log)	
	# creates the gui menubar
	def createTabs(self):
		# Binds submenus to their shortcut key; use ctrl for windows and cmd for OS X
		if _platform == "win32":
			self.parent.bind('<Control-z>', self.geoCanvas.undo)
			self.parent.bind('<Control-Z>', self.geoCanvas.redo)
			self.parent.bind('<Control-s>', self.save)
			self.parent.bind('<Control-S>', self.save_as)
			self.parent.bind('<Control-o>', self.open)
			self.parent.bind('<Control-q>', self.exit)
			accelPrefix = "Ctrl-"
		else:
			self.parent.bind('<Command-z>', self.geoCanvas.undo)
			self.parent.bind('<Command-Z>', self.geoCanvas.redo)
			self.parent.bind('<Command-s>', self.save)
			self.parent.bind('<Command-S>', self.save_as)
			self.parent.bind('<Command-o>', self.open)
			self.parent.bind('<Command-q>', self.exit)
			accelPrefix = "Cmd-"

		# MAIN MENUBAR
		menubar = Menu(self.parent)
		self.parent.config(menu=menubar)

		# File Tab
		fileTab = Menu(menubar, tearoff=0)
		fileTab.add_command(label="Open...", command=self.open, accelerator=accelPrefix+"O")
		fileTab.add_command(label="Save", command=self.save, accelerator=accelPrefix+"S")
		fileTab.add_command(label="Save As...", command=self.save_as, accelerator=accelPrefix+"Shift-S")
		fileTab.add_command(label="Exit", command=self.exit, accelerator=accelPrefix+"Q")
		menubar.add_cascade(label="File", menu=fileTab)

		# Edit Tab
		editTab = Menu(menubar, tearoff=0)
		editTab.add_command(label="Undo", command=self.geoCanvas.undo, accelerator=accelPrefix+"Z")
		editTab.add_command(label="Redo", command=self.geoCanvas.redo, accelerator=accelPrefix+"Shift-Z")
		menubar.add_cascade(label="Edit", menu=editTab)

		#View Tab
		viewTab = Menu(menubar, tearoff=0)
		viewTab.add_command(label="Show Labels", command=self.geoCanvas.showLabels)
		viewTab.add_command(label="Hide Labels", command=self.geoCanvas.hideLabels)
		menubar.add_cascade(label="View", menu=viewTab)

		#Window Tab
		windowTab = Menu(menubar, tearoff=0)
		windowTab.add_command(label='Log Window', command=self.geoCanvas.dockedWindows.logWindow)
		windowTab.add_command(label='Component Geometry', command=lambda:viewComponentGeo(self.G)) 
		windowTab.add_command(label='Compartment Geometry', command=lambda:viewCompartmentGeo(self.G))
		menubar.add_cascade(label="Windows", menu=windowTab)

		#Analysis Tab
		analysisTab = Menu(menubar, tearoff=0)
		analysisTab.add_command(label="Node Degrees", command=self.geoCanvas.dockedWindows.nodeDegreesAnalysis)
		analysisTab.add_command(label='Centrality', command=self.geoCanvas.dockedWindows.centralityAnalysis)
		analysisTab.add_command(label='Test', command=self.geoCanvas.dockedWindows.testAnalysis)
		menubar.add_cascade(label="Analysis", menu=analysisTab)

	def initUI(self):
		self.parent.title("ANCR-GUI")

		# Create left and right frames and packs them within the parent frame
		self.leftFrame = Frame(self.parent, bg='light blue', height=700, width=700) #light colored bg to see panel
		self.rightFrame = Frame(self.parent, bg="dark gray", height=700, width=400) #dark colored bg to see panel

		self.leftFrame.pack(side="left", fill="both", expand=1)
		#self.leftFrame.pack_propagate(0)
		self.rightFrame.pack(side="right", fill="y", expand=0)
		#self.rightFrame.pack_propagate(0)
		
		# Creates a scrollbar on the right frame and corresponding window which it controls
		self.rightSideCanvas = Canvas(self.rightFrame, height=700, width=400, bg='dark gray', highlightbackground='dark gray', highlightthickness=0)
		self.rightCanvasFrame = Frame(self.rightSideCanvas, bg='dark gray')
		self.vsb = Scrollbar(self.rightFrame, orient="vertical", command=self.rightSideCanvas.yview)
		self.rightSideCanvas.configure(yscrollcommand=self.vsb.set)

		self.vsb.pack(side="right", fill="y")
		self.rightSideCanvas.pack(side="left", expand=True)
		self.rightSideCanvas.create_window((0,0), window=self.rightCanvasFrame, anchor="nw")
		
		self.geoCanvas = CanvasFrame(self.leftFrame, self.rightCanvasFrame, self.G, self.D) # handles creation of canvas and miniframes
		self.rightCanvasFrame.bind("<Configure>", self.onFrameConfigure) # enables scrollbar functionality

		self.createTabs()

	# set the right frame window to match the scroll bar configure
	def onFrameConfigure(self, event):
		self.rightSideCanvas.configure(scrollregion=self.rightSideCanvas.bbox("all"), width=400, height=700)


#__init.py:
#	from dna.gui import Window


#from . import Window
#put all stuff in class window into its own file
#have __init__ have import lines


def main():
	if sys.version_info[0] != 2 or sys.version_info[1] != 7:
			root.wm_withdraw()
			tkMessageBox.showerror('Version Error', 'Please run the program with Python 2.7')		
	else:
		app = Window(root)
		root.mainloop()
	#to see the networkx representation of the graph after exiting the gui:
	#nx.draw(app.G)
	#plt.show()

if __name__ == '__main__':
	main()
	


