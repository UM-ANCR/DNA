from Tkinter import *
from frontendRight import *

class FrontendLeft(Frame):
	def __init__(self, parent, rightFrame):
		Frame.__init__(self, parent)

		self.parent = parent
		self.rightFrame = rightFrame
		self.color = "light blue"
		self.initUI()

	#toolbar button click events
	def nodeButtonClick(self):
		self.systemsCanvas.bind('<Button-1>', self.createNode)
		self.systemsCanvas.unbind('<ButtonRelease-1>')
	
	def edgeButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.bind('<ButtonPress-1>', self.edgeStart)
		self.systemsCanvas.bind('<ButtonRelease-1>', self.createEdge)
	
	def selectButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.selectNode)

	#creates nodes, edges and selction events
	def createNode(self, event):
		r = 8
		self.systemsCanvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill='red') 
	
	def deleteNode(self):
		pass

	def edgeStart(self, event):
		self.edgeStartX=event.x
		self.edgeStartY=event.y
	
	def createEdge(self, event):
		self.systemsCanvas.create_line(self.edgeStartX, self.edgeStartY, event.x, event.y, tag='edge')

	def deleteEdge(self):
		pass

	def selectNode(self, event):
		r = 24
		selected = self.systemsCanvas.find_enclosed(event.x-r, event.y-r, event.x+r, event.y+r)

		systemInfo = FrontendRight(self.rightFrame, selected[0])
		pass

	def undo(self):
		itemList=self.systemsCanvas.find_all()
		lastItemIndex=len(itemList)-1
		self.systemsCanvas.delete(itemList[lastItemIndex])

	def newOptionMenu(self, event):
		if self.v.get()=="Create New":
			self.createNewPopUpMenu=Toplevel(self.parent)
			self.createNewPopUpMenu.title('Create New')
			self.createNewEntry=Entry(self.createNewPopUpMenu)
			self.createNewEntry.pack()
			self.createNewPopUpMenu.bind('<Return>', self.createNew)
		else:
			self.systemsCanvas.delete('edge')
	
	def createNew(self, event):
		entry=self.createNewEntry.get()
		self.optionList.insert(len(self.optionList)-1, entry)
		self.dropdown.destroy()
		self.dropdown = OptionMenu(self.toolbar, self.v, *self.optionList, command=self.newOptionMenu)
		self.dropdown.configure(bg="light blue")
		self.dropdown.pack(side='left')
		self.createNewPopUpMenu.destroy()


	def initUI(self):
		# TODO: create toolbar
		#       create canvas
		#       implement functionality to draw on canvas

		# toolbar: implemented using a frame with dropdown/buttons placed on it
		#          referenced from http://zetcode.com/gui/tkinter/menustoolbars/
		self.toolbar = Frame(self.parent, bg=self.color)
		self.toolbar.pack()

		self.optionList = ['Geometry', 'Electric', 'Egress', 'Information', 'Chill Water', 'All', 'Create New']
		self.v = StringVar()
		self.v.set(self.optionList[0])

		self.dropdown = OptionMenu(self.toolbar, self.v, *self.optionList, command=self.newOptionMenu)
		self.dropdown.configure(bg=self.color)
		self.dropdown.pack(side='left')

		#creates toolbar buttons, with functionality 
		nodeButton = Button(self.toolbar, text="node", command=self.nodeButtonClick,
                        highlightbackground=self.color)
		edgeButton = Button(self.toolbar, text="edge", command=self.edgeButtonClick,
                        highlightbackground=self.color)
		selectButton = Button(self.toolbar, text="select", command=self.selectButtonClick,
                          highlightbackground=self.color)
		selectButton.pack(side='right')
		edgeButton.pack(side='right')
		nodeButton.pack(side='right')

		#creates canvas 
		self.systemsCanvas = Canvas(self.parent, height=570, width=600, bg='white')
		self.systemsCanvas.pack(fill="both", expand=1)
