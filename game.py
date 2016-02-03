import sys, pygame, math
from playerLogic import Player

pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0, 0, 255)
LIMEGREEN = (124,252,0)
BGCOLOR = (255,228,225)

class Dot(object):
	DOT_RADIUS = 10

	def __init__(self, pos, grdPos, clr=BLACK):
		self.radius = Dot.DOT_RADIUS
		self.position = pos
		self.color = dict({'r':clr[0], 'g':clr[1], 'b':clr[2]})
		self.gridPosition = grdPos

	def getClrTuple(self):
		return (self.color['r'], self.color['g'], self.color['b'])

	def setClrByTuple(self, clrTup):
		self.color['r'] = clrTup[0]
		self.color['g'] = clrTup[1]
		self.color['b'] = clrTup[2]

	def __str__(self):
		return "Dot(" + str(self.gridPosition) + ")"

	def __repr__(self):
		return "Dot(" + str(self.gridPosition) + ")"

	def __eq__(self, other):
		return ((self.position[0]==other.position[0]) and (self.position[1]==other.position[1]))

size = width, height = 600, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('DOTS')

try:
	dotsWidth = int(sys.argv[1])
	dotsHeight = int(sys.argv[2])
except (IndexError, ValueError):
	print("No/Improper input so will default to 5 x 5 grid")
	dotsWidth = dotsHeight = 5

myfont = pygame.font.Font(None, 25)
text = myfont.render("Welcome to the Game of Squares and Shit!", 1, BLACK)
textRect = text.get_rect()

myfont = pygame.font.Font(None, 35)
turn = myfont.render("Player Turn: P1", 1, BLACK)
turnRect = turn.get_rect()

#Stupid way to do this buut fuck it...
dots = []
dots2 = []

deltaWidth = int((width - width/dotsWidth)/dotsWidth)
deltaHeight = int(((height) - (height)/dotsHeight)/dotsHeight)
xKnot = 0
#create the set of dots
for i in range(dotsWidth):
 	xKnot += deltaWidth
 	yKnot = 15
 	sublist = []
	for j in range(dotsHeight):
 		yKnot += deltaHeight
 		sublist.append( Dot((xKnot,yKnot), (i,j)) )
 	dots2.append(sublist)
 	dots = dots + sublist

squares = []
for i in range(dotsWidth - 1):
	for j in range(dotsHeight - 1):
		squares.append (([frozenset([dots2[i][j], dots2[i+1][j]]),frozenset([dots2[i][j], dots2[i][j+1]]),frozenset([dots2[i+1][j+1], dots2[i][j+1]]),frozenset([dots2[i+1][j+1], dots2[i+1][j]])], [dots2[i][j].position, dots2[i+1][j].position, dots2[i+1][j+1].position, dots2[i][j+1].position,dots2[i][j].position]))

dotclick = (False, (-1, -1))
clickedDot = None
connectedDotsSet = set()
rectsToDraw = set()

P_1 = Player("P1", (127, 0, 255), False)
P_2 = Player("P2", BLUE, False)
PList = [P_1, P_2]
turnNum, numPlayers = 0, len(PList)
currPlayerTurn = PList[turnNum%numPlayers]
recColorDict = dict()
totalSquares = dotsHeight*dotsWidth - dotsHeight - dotsWidth + 1
re = False

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			dotclick = (True, pygame.mouse.get_pos())
		if event.type == pygame.MOUSEBUTTONUP:
			dotclick = (False, pygame.mouse.get_pos(), clickedDot)
			clickedDot = None

	screen.fill(BGCOLOR)
	screen.blit(text, (width/2 - textRect.width/2, 10))
	turn = myfont.render("Player Turn: "+str(currPlayerTurn.playerName), 1, currPlayerTurn.color)
	screen.blit(turn, (width/2 - turnRect.width/2, 40))

	for rect in rectsToDraw:
		pygame.draw.polygon(screen, recColorDict[rect], list(rect), 0)

	for frozenDotSet in connectedDotsSet:
		dot1, dot2 = frozenDotSet
		pygame.draw.line(screen, BLACK, dot1.position, dot2.position, 10)

	for dot in dots:
		if currPlayerTurn.isAI == False:
			distance = math.sqrt((pygame.mouse.get_pos()[0] - dot.position[0])**2 + (pygame.mouse.get_pos()[1] - dot.position[1])**2)
			if dotclick[1][0] > 0:
				clickDist = math.sqrt((dotclick[1][0] - dot.position[0])**2 + (dotclick[1][1]-dot.position[1])**2)
			else:
				clickDist = float("inf")
			
			if distance > Dot.DOT_RADIUS:
				for key in dot.color:
					if dot.color['r'] > 0:
						dot.color['r'] *= .9992	
					if dot.color['g'] > 0:
						dot.color['g'] *= .9992
					if dot.color['b'] > 0:
						dot.color['b'] *= .9992
					dot.radius =  int(round(dot.radius + (Dot.DOT_RADIUS - dot.radius)/(2)))

			if distance <= dot.radius:
				dot.setClrByTuple(LIMEGREEN)
				dot.radius = int(round(Dot.DOT_RADIUS*1.25))
				if clickedDot != None and clickedDot != dot:
					dot.setClrByTuple(RED)
				if dotclick[0] == False and clickDist <= dot.DOT_RADIUS and dotclick[2] != None and dotclick[2] != dot and ({dot, dotclick[2]} not in connectedDotsSet):
					dot.setClrByTuple(RED)
					x1, y1 = dotclick[2].gridPosition[0], dotclick[2].gridPosition[1]
					x2, y2 = dot.gridPosition[0], dot.gridPosition[1]
					# print("dot gridPosition is :" + str(dot.gridPosition))
					# print("clickedDot gridPosition is :" + str(dotclick[2].gridPosition))
					# someone connected a line!
					if ((x1==x2+1 or x1==x2-1) and y1==y2) or ((y1==y2+1 or y1==y2-1) and x1==x2):
						connectedDotsSet.add( frozenset([dotclick[2], dot]) )
						currPlayerTurn.capturedSet.add(frozenset([dotclick[2], dot]))
						turnNum += 1

						for square in squares:
							c1, c2, c3, c4 = square[0]
							if (c1 in connectedDotsSet) and (c2 in connectedDotsSet) and (c3 in connectedDotsSet) and (c4 in connectedDotsSet):
								if tuple(square[1]) not in rectsToDraw:
									rectsToDraw.add( tuple(square[1]) )
									recColorDict[tuple(square[1])] = currPlayerTurn.color
									if re == False:
										re = True
									currPlayerTurn.numSquares += 1

						if re == True:
							turnNum -= 1
							re = False
						if sum([plr.numSquares for plr in PList]) >= totalSquares:
							print("GAME OVER. Here's the SCOREs : " + str([plr.playerName + ": " + str(plr.numSquares) + " square(s) captured" for plr in PList]))

						currPlayerTurn = PList[turnNum%numPlayers]

			if clickDist <= dot.radius and dotclick[0] == True and pygame.mouse.get_pressed()[0] == 1:
				dot.setClrByTuple(RED)
				dot.radius = int(round(Dot.DOT_RADIUS*1.25))
				pygame.draw.line(screen, BLACK, dot.position, pygame.mouse.get_pos(), 10)
				clickedDot = dot
		else:
			pass #the player is an ai, call the players move funtion or whatever

		pygame.draw.circle(screen, dot.getClrTuple(), dot.position, dot.radius)

	#Weird ass glitch, idk, just handle exception and remove the shitty element from set. YOLO
	# toRemove = []
	# print connectedDotsSet
	
	# 	except AttributeError:re
	# 		toRemove.append(dotSet)
	# for item in toRemove:
	# 	connectedDotsSet.remove(item)

	pygame.display.flip()