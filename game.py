import sys, pygame, math
pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
LIMEGREEN = (124,252,0)

size = width, height = 600, 600
screen = pygame.display.set_mode(size)

class Dot:
	DOT_RADIUS = 10

	def __init__(self, pos = 0, clr = BLACK):
		self.radius = Dot.DOT_RADIUS
		self.position = pos
		self.color = dict({'r':clr[0], 'g':clr[1], 'b':clr[2]})

	def getClrTuple(self):
		return (self.color['r'], self.color['g'], self.color['b'])

	def setClrByTuple(self, clrTup):
		self.color['r'] = clrTup[0]
		self.color['g'] = clrTup[1]
		self.color['b'] = clrTup[2]


try:
	dotsWidth = int(sys.argv[1])
	dotsHeight = int(sys.argv[2])
except (IndexError, ValueError):
	print("No/Improper input so will default to 5 x 5 grid")
	dotsWidth = dotsHeight = 5

print ("dotColumns = " + str(dotsWidth) + ", dotRows = " + str(dotsHeight))

pygame.display.set_caption('DOTS')

myfont = pygame.font.SysFont("Droid Sans Regular", 25)
text = myfont.render("Welcome to the Game of Squares and Shit!", 1, BLACK)
textRect = text.get_rect()

print("screenWidth = " + str(width) + ", screenHeight = " + str(height))

deltaWidth = int((width - width/dotsWidth)/dotsWidth)
deltaHeight = int((height - height/dotsHeight)/dotsHeight)
x, y = 0, 0
dots = list()
for i in range(dotsWidth):
 	x += deltaWidth
 	y = 0
	for j in range(dotsHeight):
 		y += deltaHeight
 		dots.append( Dot( (x,y) ) )

dotclick = (False, (-1, -1))
clickedDot = None
connectedDotsSet = set()

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			dotclick = (True, pygame.mouse.get_pos())
		if event.type == pygame.MOUSEBUTTONUP:
			dotclick = (False, pygame.mouse.get_pos(), clickedDot)
			clickedDot = None

	screen.fill(WHITE)
	screen.blit(text, (width/2 - textRect.width/2, 10))

	for dot in dots:
		distance = math.sqrt((pygame.mouse.get_pos()[0] - dot.position[0])**2 + (pygame.mouse.get_pos()[1] - dot.position[1])**2)
		clickDist = math.sqrt((dotclick[1][0] - dot.position[0])**2 + (dotclick[1][1] - dot.position[1])**2)
		
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
				dot.setClrByTuple(BLUE)
			if dotclick[0] == False and clickDist <= dot.DOT_RADIUS and dotclick[2] != dot and ((dot, dotclick[2]) not in connectedDotsSet) and ((dotclick[2], dot) not in connectedDotsSet):
				dot.setClrByTuple(BLUE)
				connectedDotsSet.add( (dotclick[2], dot) )

		if clickDist <= dot.radius and dotclick[0] == True and pygame.mouse.get_pressed()[0] == 1:
			dot.setClrByTuple(RED)
			dot.radius = int(round(Dot.DOT_RADIUS*1.25))
			pygame.draw.line(screen, BLACK, dot.position, pygame.mouse.get_pos(), 10)
			clickedDot = dot

		pygame.draw.circle(screen, dot.getClrTuple(), dot.position, dot.radius)

	#Weird ass glitch, idk, just handle exception and remove the shitty element from set. YOLO
	toRemove = []
	for pts in connectedDotsSet:
		try:
			pygame.draw.line(screen, BLACK, pts[0].position, pts[1].position, 10)
			print(str(pts[0].position) + "<--->" + str(pts[1].position))
		except AttributeError:
			toRemove.append(pts)
	for item in toRemove:
		connectedDotsSet.remove(item)


	pygame.display.flip()