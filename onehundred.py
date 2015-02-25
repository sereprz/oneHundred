import pygame, sys, numpy, math
from pygame.locals import *

# board size
SQUARE_SIZE = 30
BOARD_SIZE = 10
GAP = 2
MARGINX = 50
TOP_MARGIN = 100
BOTTOM_MARGIN = 30
WINWIDTH = SQUARE_SIZE * BOARD_SIZE + MARGINX * 2  + GAP * (BOARD_SIZE + 2)
WINHEIGHT = SQUARE_SIZE * BOARD_SIZE + TOP_MARGIN + GAP * (BOARD_SIZE + 2) + BOTTOM_MARGIN

# colors
BACKGROUND = (255,165,0) # orange
GREEN = (0, 255, 0)
DGREEN = (50,205,50) # lime green
PURPLE = (153,50,204) # dark orchid
RED = (255, 0, 0)
FILLED = (64, 224, 208) # turquoise
EMPTY =  (192, 192, 192) # light grey
WHITE = (248, 248, 255)
TEXTCOLOR = (0, 0, 0)
BLACK = TEXTCOLOR

cols = [[BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK],\
[BLACK, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, BLACK], \
[BLACK, WHITE, DGREEN, BLACK, DGREEN, BLACK, DGREEN, BLACK, WHITE, BLACK], \
[BLACK, WHITE, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, WHITE, BLACK], \
[BLACK, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, BLACK], \
[BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK], \
[WHITE, WHITE, WHITE, BLACK, BLACK, BLACK, BLACK, WHITE, WHITE, WHITE], \
[WHITE, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, WHITE], \
[BLACK, WHITE, BLACK, WHITE, BLACK, WHITE, BLACK, WHITE, BLACK, BLACK], \
[BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK]]

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
			elif event.type == KEYDOWN and event.key == K_RETURN:
				if len(nextPossibleMoves(board)) == 0:
					score = 0
					board = initBoard(BOARD_SIZE)
					drawBoard(board)
					boxx, boxy = None, None

		boxx, boxy = getBoxAtPixel(board, mousex, mousey)

		if boxx != None and boxy != None:

			if score == 0:
				if mouseClicked:
					score+= 1
					board[boxx, boxy] = score
				
			if score != 0 and board[boxx, boxy] == 0:
				lastx, lasty = which(board, score)
				if (boxx, boxy) in nextPossibleMoves(board):
					drawHighlightedBox(boxx, boxy, GREEN) 
					if mouseClicked:
						score += 1
						board[boxx, boxy] = score
				else:
					drawHighlightedBox(boxx, boxy, RED)

		if len(nextPossibleMoves(board)) == 0:
			if score < 100:
				endOfGame = FONT.render('Game over, your score is ' + str(score), True, TEXTCOLOR)
			else:
				endOfGame = FONT.render('You won', True, TEXTCOLOR)

			WIN.blit(endOfGame, (MARGINX,30))
			WIN.blit(FONT.render('Press Enter to start again', True, TEXTCOLOR), (MARGINX, 60))
		
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
				col = cols[j][i]
			left, top = leftTopCoordsOfBox(i,j)
			pygame.draw.rect(WIN, col, (left, top, SQUARE_SIZE, SQUARE_SIZE))
			pygame.draw.rect(WIN, BLACK, (left, top, SQUARE_SIZE, SQUARE_SIZE), 1)
	if numpy.amax(board) > 0:
		boxx, boxy = which(board, numpy.amax(board))
		left, top = leftTopCoordsOfBox(boxx, boxy)
		pygame.draw.rect(WIN, GREEN, (left, top, SQUARE_SIZE, SQUARE_SIZE), 1)


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

def nextPossibleMoves(board):
	boxx, boxy = which(board, numpy.amax(board))
	next = [(boxx + 3, boxy),(boxx, boxy+3),(boxx-3, boxy),(boxx, boxy-3),\
	(boxx-2,boxy+2),(boxx+2,boxy+2),(boxx+2,boxy-2),(boxx-2, boxy -2)]
	invalid = []

	for i in next:
		if (i[0] not in xrange(BOARD_SIZE)) or (i[1] not in xrange(BOARD_SIZE)):
			invalid.append(i)
	next = list(set(next) - set(invalid))
	full = []
	for i in next:
		if board[i[0],i[1]] != 0:
			full.append(i)
	return(list(set(next) - set(full)))


if __name__ == '__main__':
	main()