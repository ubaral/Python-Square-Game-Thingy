class Player:
	def __init__(self, pName, clr, isComputer=False):
		self.capturedSet = set()
		self.playerName = pName
		self.isAI = isComputer
		self.color = clr
		self.numSquares = 0

	#move should return which two dots the player wants
	#to connect based on the current board layout.
	def moveLogic(self, currBoardLayout):
		#should return null if real player and use the mouse to determine move
		return None