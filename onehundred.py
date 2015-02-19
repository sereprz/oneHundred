import pygame, sys, numpy, math
from pygame.locals import *

# board size
SQUARE_SIZE = 30
BOARD_SIZE = 10
GAP = 4
MARGINX = 50
TOP_MARGIN = 100
BOTTOM_MARGIN = 30
WINWIDTH = SQUARE_SIZE * BOARD_SIZE + MARGINX * 2  + GAP * (BOARD_SIZE + 2)
WINHEIGHT = SQUARE_SIZE * BOARD_SIZE + TOP_MARGIN + GAP * (BOARD_SIZE + 2) + BOTTOM_MARGIN

# colors
BACKGROUND = (204, 229, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FILLED = (64, 224, 208) # turquoise
EMPTY = (248, 248, 255) # ghost white
TEXTCOLOR = (0, 0, 0)

FPS = 60 # 


def main():
	global WIN, FPSCLOCK

	pygame.init()

	FONT = pygame.font.Font('freesansbold.ttf', 20)

	WIN = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
	FPSCLOCK = pygame.time.Clock()

	pygame.display.set_caption('100')

	board = initBoard(BOARD_SIZE)
	
	mousex = None
	mousey = None

	score = 0

	while True:
		WIN.fill(BACKGROUND)
		drawBoard(board)

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
				if mouseClicked:
					score+= 1
					board[boxx, boxy] = score
				
			if score != 0 and board[boxx, boxy] == 0:
				if manhattanDist(which(board, score), (boxx, boxy)) == 3:
					drawHighlightedBox(boxx, boxy, GREEN)
					if mouseClicked:
						score += 1
						board[boxx, boxy] = score
				else:
					drawHighlightedBox(boxx, boxy, RED)

		if not moreMovesPossible(board):
			if score < 100:
				endOfGame = FONT.render('Game over, your score is ' + str(score), True, TEXTCOLOR)
			else:
				endOfGame = FONT.render('You won', True, TEXTCOLOR)

			WIN.blit(endOfGame, (MARGINX,40))
		
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
			left, top = leftTopCoordsOfBox(i,j)
			pygame.draw.rect(WIN, col, (left, top, SQUARE_SIZE, SQUARE_SIZE))

def leftTopCoordsOfBox(boxx, boxy):
	# convert board coordinates into pixel coordinates
	left = MARGINX + (boxx + 1) * GAP + boxx * SQUARE_SIZE # boxx * (SQUARE_SIZE + GAP) + MARGINX + GAP
	top = TOP_MARGIN + (boxy + 1) * GAP + boxy * SQUARE_SIZE #boxy * (SQUARE_SIZE + GAP) + TOP_MARGIN + GAP
	return(left, top)

def getBoxAtPixel(board, x, y):
	# get board coordinates given pixel coordinates
	BOARD_SIZE
	for boxx in xrange(BOARD_SIZE):
		for boxy in xrange(BOARD_SIZE):
			left, top = leftTopCoordsOfBox(boxx, boxy)
			boxRect = pygame.Rect(left, top, SQUARE_SIZE, SQUARE_SIZE)
			if boxRect.collidepoint(x,y):
				return(boxx, boxy)
	return(None, None)

def drawHighlightedBox(boxx, boxy, col):
	left, top = leftTopCoordsOfBox(boxx, boxy)
	pygame.draw.rect(WIN, col, (left, top, SQUARE_SIZE, SQUARE_SIZE), 5)


def manhattanDist(box1, box2):
	# calculates manhattan distance between two boxes on the board
	# box1, box2 tuples of (x,y) coordinates
	return math.fabs(box1[0]-box2[0]) + math.fabs(box1[1]-box2[1])

def moreMovesPossible(board):
	boxx, boxy = which(board, numpy.amax(board))
	possibleMoves =  0
	for i in xrange(BOARD_SIZE):
		for j in xrange(BOARD_SIZE):
			if manhattanDist((boxx,boxy), (i,j)) == 3:
				if board[i,j] == 0:
					possibleMoves += 1
	return possibleMoves > 0





if __name__ == '__main__':
	main()