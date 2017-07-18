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

class Residency(Frame):
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

	def createProb(self):
		
		self.probability = LabelFrame(self.parent, text="Probability", bg=self.color)
		self.probability.grid(row=1, padx=10, sticky=E+W)
		self.probEntry = Entry(self.probability, highlightbackground=self.color, width=5)
		self.probEntry.grid(row=0, column=1, padx=5)
		self.probEntry.insert(0, 0) # initialize to 0



	def saveEdgeAttributes(self):

		titles = ["Probability"]
		values = [self.probEntry.get()]
		# for each field, check if coord is updated in NetworkX; if not, save and add to 'updated'
		for i in range(0, len(titles)):
			if (titles[i] not in self.G.edge[self.nodes[0]][self.nodes[1]]) or (self.G.edge[self.nodes[0]][self.nodes[1]][titles[i]] != values[i]):
				self.G.edge[self.nodes[0]][self.nodes[1]][titles[i]] = values[i]


	def repopulateEdgeData(self):
		# repopulate demand values
		if 'Probability' in self.G.edge[self.nodes[0]][self.nodes[1]]:
			self.probEntry.delete(0, END)
			self.probEntry.insert(0, self.G.edge[self.nodes[0]][self.nodes[1]]['Probability'])


	def initUI(self):
		self.createProb()

		self.repopulateEdgeData()
