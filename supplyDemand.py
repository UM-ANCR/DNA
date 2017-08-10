'''
 * Component.py
 * 
 * Assumes the selected node is of type component;
 * adds a box where demands of this component can be
 * specified
 * 
 * Major functionalities include:
 *     demand box / create new demand
 *     update sizes of nodes if current system is not 'All'
 *     save/repopulate
 *
'''
from Tkinter import *
import tkSimpleDialog
import networkx as nx

class supplyDemand(Frame):
	def __init__(self, parent, leftFrame, index, G, manager, nodes):
		Frame.__init__(self, parent)

		self.parent = parent
		self.leftFrame = leftFrame
		self.index = index
		self.G = G
		self.manager = manager
		self.nodes = nodes

		self.systemDict = {}
 		self.color = "dark gray" 
		self.initUI()

	def createNewDemand(self, label=None):

		# Create new Label and corresponding check box
		self.newDemandLabel = Label(self.demandGroup, text=label, bg=self.color)
		self.newDemandLabel.grid(row=0+self.numDemands, column=0, sticky=E+W)
		incVar = IntVar()
		newInc = Checkbutton(self.demandGroup, variable = incVar)
		newInc.grid(row=0+self.numDemands, column=1, padx=5, sticky=E+W)
		self.systemDict[label] = incVar # save the check box widget in the dictionary systemDict


		# add the new demand/system to the main toolbar dropdown
		if label not in self.leftFrame.optionList:
			self.leftFrame.optionList.insert(len(self.leftFrame.optionList)-2, label)
			self.leftFrame.dropdown.destroy()
			self.leftFrame.dropdown = OptionMenu(self.leftFrame.toolbar, self.leftFrame.v, 
				*self.leftFrame.optionList, command=self.leftFrame.newOptionMenu)
			self.leftFrame.dropdown.configure(highlightbackground="light blue", bg='light blue')
			self.leftFrame.dropdown.pack(side='left')

	def createDemandLabel(self):
		self.demandGroup.columnconfigure(0, weight=1)
		self.demandGroup.columnconfigure(1, weight=1)
		
		self.numDemands = 0

		# create a new demand entry for every system in our manager list (in Manager.py)
		for systemLabel in self.manager.systems:
			self.createNewDemand(systemLabel)


	def updateNodeSizes(self):
		if self.leftFrame.v.get() != 'All' and self.leftFrame.v.get() != 'Create New':
			self.leftFrame.minDemand = 1000000000
			self.leftFrame.maxDemand = -1
			visibleNodes = []

			# for each node on the canvas
			for nodeitem in self.leftFrame.systemsCanvas.find_withtag('node'):
				# if it has a demand value for current system we're in
				if self.leftFrame.v.get() in self.G.node[nodeitem]:
					visibleNodes.append(nodeitem) # add to a list of visible nodes

					# find minimum and maximum values for this demand
					thisDemand = self.G.node[nodeitem][self.leftFrame.v.get()]
					if abs(thisDemand) < self.leftFrame.minDemand:
						self.leftFrame.minDemand = abs(thisDemand)
					if abs(thisDemand) > self.leftFrame.maxDemand:
						self.leftFrame.maxDemand = abs(thisDemand)

			# delete old '+' or '-' labels
			self.leftFrame.systemsCanvas.delete('label')

			# update node sizes
			for nodeitem in visibleNodes:
				self.leftFrame.normalNodeSize(nodeitem)
				self.leftFrame.scaleNodeSize(nodeitem)

	def saveEdgeAttributes(self):
		# save demands values of this node
		for x in self.manager.systems: 
			# if there is a value for this node
			if self.systemDict[x].get() != None and self.systemDict[x].get() != '':
				# if system doesn't exist in NetworkX already OR if the curr value in NetworkX isn't updated, save the curr value
				if (x not in self.G.edge[self.nodes[0]][self.nodes[1]]) or (self.G.edge[self.nodes[0]][self.nodes[1]][x] != int(self.systemDict[x].get())):
					self.G.edge[self.nodes[0]][self.nodes[1]][x] = int(self.systemDict[x].get())

			# else if a previous value was cleared
			elif x in self.G.edge[self.nodes[0]][self.nodes[1]] and self.systemDict[x].get() == '':
				# if we're not in 'All', hide this node and the edges connected to it bc there isn't a demand value anymore
				if self.leftFrame.v.get() != 'All':
					nodeCoords = self.leftFrame.systemsCanvas.coords(self.index)
					overlapped = self.leftFrame.systemsCanvas.find_overlapping(nodeCoords[0], nodeCoords[1], nodeCoords[2], nodeCoords[3])
					for edge in overlapped:
						if self.leftFrame.checkTag(edge) == 'edge':
							self.leftFrame.systemsCanvas.itemconfig(edge, state='hidden')
					self.leftFrame.systemsCanvas.itemconfig(self.index, state='hidden')
				del self.G.edge[self.nodes[0]][self.nodes[1]][x]


	def repopulateEdgeData(self):
		# repopulate demand values
		for x in self.manager.systems:
			if x in self.G.edge[self.nodes[0]][self.nodes[1]]:
				#self.systemDict[x].delete(0, END)
				self.systemDict[x].set(self.G.edge[self.nodes[0]][self.nodes[1]][x])

		
	def initUI(self):
		self.demandGroup = LabelFrame(self.parent, text="Demands", bg=self.color)
		self.demandGroup.grid(row=1, padx=10, sticky=E+W)
		self.createDemandLabel()

		self.repopulateEdgeData()
