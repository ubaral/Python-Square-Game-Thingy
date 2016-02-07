import operator


class Player:

	def __init__(self, pName, clr, isComputer=False):
		self.capturedSet = set()
		self.playerName = pName
		self.isAI = isComputer
		self.color = clr
		self.numSquares = 0

	# move should return which two dots the computer wants
	# to connect based on the current board layout. The value of a square for
	# the opponent is -1 and the value of a square for the computer is +1 so
	# the comp will try to maximize its minimized score. This creates a search
	# tree of solutions and we will brute force this search tree to the max
	# depth. Again, probably a shitty thing to do but gotta make it actually
	# work beforeadding optimizations..... wow this is gonna be hella
	# exponential. Will look up how to optimize the search tree later.

	def moveLogic(self, connectedDotsSet, possConnections, squares, currentRects):
		solution = self.recursiveBruteForce(connectedDotsSet, possConnections, squares,currentRects,True, 0, float("-inf"), float("inf"))
		if solution is not None:
			return solution[0]

	# for arbitrary players, we can use a tuple of utlity values and index based on player
	def recursiveBruteForce(self, connectedDotsSet, possConnections, squares, rectsToDraw,MaxTurnLoc, currentMaxxerUtility, alpha, beta):
		if len(possConnections) == 1:
			for connection in possConnections:
				MaxTurn = MaxTurnLoc
				utility_cpy = currentMaxxerUtility
				cpy_connectedDotsSet = set(connectedDotsSet)
				cpy_connectedDotsSet.add(connection)
				#check if we make a square with this hypothetical move, if so increase utility of this path
				for square in squares:
					c1, c2, c3, c4 = square[0]
					if (c1 in cpy_connectedDotsSet) and (c2 in cpy_connectedDotsSet) and (c3 in cpy_connectedDotsSet) and (c4 in cpy_connectedDotsSet):
						if tuple(square[1]) not in rectsToDraw:
							if MaxTurn:
								utility_cpy += 1
							else:
								utility_cpy -= 1
							
				return (connection, utility_cpy)

		elif len(possConnections) > 1:
			connDict = dict()
			for connection in possConnections:
				repeatTurn = False
				MaxTurn = MaxTurnLoc
				utility_cpy = currentMaxxerUtility
				cpy_connectedDotsSet = set(connectedDotsSet)
				cpy_connectedDotsSet.add(connection)

				cpy_possConnections = set(possConnections)
				cpy_possConnections.remove(connection)

				rectsToDraw_cpy = set(rectsToDraw)

				for square in squares:
					c1, c2, c3, c4 = square[0]
					if (c1 in cpy_connectedDotsSet) and (c2 in cpy_connectedDotsSet) and (
							c3 in cpy_connectedDotsSet) and (c4 in cpy_connectedDotsSet):
						if tuple(square[1]) not in rectsToDraw_cpy:
							if MaxTurn:
								utility_cpy += 1
							else:
								utility_cpy -= 1
							if not repeatTurn:
								repeatTurn = True
							rectsToDraw_cpy.add(tuple(square[1]))
				
				if repeatTurn:
					MaxTurn = not MaxTurn

				recurTup = self.recursiveBruteForce(cpy_connectedDotsSet, cpy_possConnections, squares, rectsToDraw_cpy, utility_cpy, not MaxTurn, alpha, beta)
				connDict[connection] = recurTup[1]				
				# if MaxTurn:
				# 	if recurTup[1] > alpha:
				# 		alpha = recurTup[1]
				# 	if beta <= alpha:
				# 		break
				# else:
				# 	if recurTup[1] < beta:
				# 		beta = recurTup[1]
				# 		connToReturn = connection
				# 	if beta <= alpha:
				# 		break

			if MaxTurn:
				return max(connDict.iteritems(), key=operator.itemgetter(1))
			else:
				return min(connDict.iteritems(), key=operator.itemgetter(1))

		else:
			return None

	def minner(self, possConnections):
		if len(possConnections == 1):
			return (possConnections.pop(), -1)
