import sys, pygame
pygame.init()

size = width, height = 600, 900
screen = pygame.display.set_mode(size)

white = 255,255,255
black = 0,0,0

pygame.display.set_caption('DOTS')

myfont = pygame.font.SysFont("Droid Sans Regular", 25)
text = myfont.render("Welcome to the Game of Squares and Shit!", 1, black)
textRect = text.get_rect()

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	screen.fill(white)

	
	screen.blit(text, (width/2 - textRect.width/2, 10))

	pygame.draw.circle(screen, black,(width/2, height/2),15,0)

	pygame.display.flip()