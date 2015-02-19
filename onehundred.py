import pygame, sys, numpy, math
from pygame.locals import *

# board size
SQUARE_SIZE = 30
BOARD_SIZE = 10
GAP = 4
MARGINX = 50
TOP_MARGIN = 100
BOTTOM_MARGIN = 30

# colors
BACKGROUND = (204, 229, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FILLED = (64, 224, 208) # turquoise
EMPTY = (248, 248, 255) # ghost white

FPS = 60 # 

def main():
	global WIN, FPSCLOCK

	pygame.init()

	WIN = pygame.display.set_mode((SQUARE_SIZE * BOARD_SIZE + MARGINX * 2  + GAP * (BOARD_SIZE + 2), SQUARE_SIZE * BOARD_SIZE + TOP_MARGIN + GAP * (BOARD_SIZE + 2) + BOTTOM_MARGIN))
	FPSCLOCK = pygame.time.Clock()

	pygame.display.set_caption('100')

	WIN.fill(BACKGROUND)

	board = initBoard(BOARD_SIZE)
	drawBoard(board)

	mousex = None
	mousey = None

	score = 0

	while True:
		mouseClicked = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				mouseClicked = True

		boxx, boxy = getBoxAtPixel(board, mousex, mousey)

		if boxx != None and boxy != None:

			if score == 0:
				
			if score != 0 and board[boxx, boxy] == 0:
				if manhattanDist(which(board, score), (boxx, boxy)) == 3:
					drawhighlightedBox(boxx, boxy, GREEN)
					if mouseClicked:
						score += 1
						board[boxx, boxy] = score
				else:
					drawhighlightedBox(boxx, boxy, RED)

			drawBoard(board)
		
		# draws boarder of box when mouse over
		

		pygame.display.update()
		FPSCLOCK.tick(FPS)




# functions

def which(m, val):
	# m is a matrix
	# val is a value
	# find indeces of val in a matrix m
	for i in xrange(m.shape[0]):
		for j in xrange(m.shape[1]):
			if m[i,j] == val:
				return (i,j)
	return (None, None)

def initBoard(dim):
	# initialize board
	return numpy.zeros(shape = (dim, dim), dtype = numpy.int)

def drawBoard(board):
	# draw board
	for i in xrange(board.shape[0]):
		for j in xrange(board.shape[1]):
			if board[i,j] == 0 :
				col = EMPTY
			else:
				col = FILLED
			pygame.draw.rect(WIN, col, (MARGINX + (i + 1) * GAP + i * SQUARE_SIZE, TOP_MARGIN + (j + 1) * GAP + j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def leftTopCoordsOfBox(boxx, boxy):
	# convert board coordinates into pixel coordinates
	left = boxx * (SQUARE_SIZE + GAP) + MARGINX + GAP
	top = boxy * (SQUARE_SIZE + GAP) + TOP_MARGIN + GAP
	return(left, top)

def getBoxAtPixel(board, x, y):
	# get board coordinates given pixel coordinates
	dim = len(board)
	for boxx in range(dim):
		for boxy in range(dim):
			left, top = leftTopCoordsOfBox(boxx, boxy)
			boxRect = pygame.Rect(left, top, SQUARE_SIZE, SQUARE_SIZE)
			if boxRect.collidepoint(x,y):
				return(boxx, boxy)
	return(None, None)

def drawhighlightedBox(boxx, boxy, col):
	left, top = leftTopCoordsOfBox(boxx, boxy)
	pygame.draw.rect(WIN, col, (left, top, SQUARE_SIZE, SQUARE_SIZE), 3)


def manhattanDist(box1, box2):
	# calculates manhattan distance between two boxes on the board
	# box1, box2 tuples of (x,y) coordinates
	return math.fabs(box1[0]-box2[0]) + math.fabs(box1[1]-box2[1])



if __name__ == '__main__':
	main()