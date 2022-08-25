from copy import deepcopy
import numpy as np
import random
import time
import pygame
import math
import sys

class connect4Player(object):
	def __init__(self, position, seed=0):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)

	def play(self, env, move):
		move = [-1]

class human(connect4Player):

	def play(self, env, move):
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env, move):
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

class minimaxAI(connect4Player):

	def simulateMove(self, env, move, player):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)
		return env

	def play(self, env, move):
		self.Minimax(deepcopy(env), move, 3)

	def eval(self, board):   #this function is our evaluation function that we call in MIN and MAX 

		our_count = 0
		our_spaces = 0
		our_seq = [0,0,0,0]
		our_weight1 = 20
		our_weight2 = 50
		our_weight3 = 100
		our_weight_space = 5

		opp_count = 0
		opp_spaces = 0
		opp_seq = [0,0,0,0]
		opp_weight1 = 20
		opp_weight2 = 50
		opp_weight3 = 100
		opp_weight_space = 5

		score = 0

		for i in range(len(board)):
			if np.all((board[-i-1] == 0)):
				break
			for j in range(len(board[i])):
				if board[-i-1][j] == self.position:
					our_count += 1
					if our_count > 3:
						return 100000000
					opp_seq[opp_count] += 1
					if opp_seq[1] * 1 + opp_seq[2] * 2 + opp_seq[3] * 3 + opp_spaces >= 4:
						score -= opp_seq[1] * opp_weight1 + opp_seq[2] * opp_weight2 + opp_seq[3] * opp_weight3 + opp_spaces * opp_weight_space
					opp_seq = [0,0,0,0]
					opp_count = 0
					opp_spaces = 0
				elif board[-i-1][j] == self.opponent.position:
					opp_count += 1
					if opp_count > 3:
						return -100000000
					our_seq[our_count] += 1
					if our_seq[1] * 1 + our_seq[2] * 2 + our_seq[3] * 3 + our_spaces >= 4:
						score += our_seq[1] * our_weight1 + our_seq[2] * our_weight2 + our_seq[3] * our_weight3 + our_spaces * our_weight_space
					our_seq = [0,0,0,0]
					our_count = 0
					our_spaces = 0
				else:
					our_seq[our_count] += 1
					opp_seq[opp_count] += 1
					our_count = 0
					opp_count = 0
					our_spaces += 1
					opp_spaces += 1
					
			if opp_count != 0:
				opp_seq[opp_count] += 1
				if opp_seq[1] * 1 + opp_seq[2] * 2 + opp_seq[3] * 3 + opp_spaces >= 4:
					score -= opp_seq[1] * opp_weight1 + opp_seq[2] * opp_weight2 + opp_seq[3] * opp_weight3 + opp_spaces * opp_weight_space
					opp_count = 0
					opp_spaces = 0
			elif our_count != 0:
				our_seq[our_count] += 1
				if our_seq[1] * 1 + our_seq[2] * 2 + our_seq[3] * 3 + our_spaces >= 4:
					score += our_seq[1] * our_weight1 + our_seq[2] * our_weight2 + our_seq[3] * our_weight3 + our_spaces * our_weight_space
					our_count = 0
					our_spaces = 0
			our_count = 0
			our_spaces = 0
			our_seq = [0,0,0,0]
			opp_count = 0
			opp_spaces = 0
			opp_seq = [0,0,0,0]
		
		# columns
		last_player = 0
		for i in range(len(board[i])):
			for j in range(len(board)):
				if board[-j-1][i] == self.position:
					our_count += 1
					if our_count > 3:
						return 100000000
					opp_count = 0 # if other player is on the top, theres no advantages
					last_player = self.position
				elif board[-j-1][i] == self.opponent.position:
					opp_count += 1
					if opp_count > 3:
						return -100000000
					our_count = 0
					last_player = self.opponent.position
				else: # count for spaces left on the top, depending on the last player # if spaces + piece >= 4, then returns value(more piece is better)
					if last_player == self.position:
						our_spaces = len(board) - j
						if our_count == 1:
							if our_spaces >= 3:
								score += 20
						if our_count == 2:
							if our_spaces >= 2:
								score += 50
						if our_count == 3:
							if our_spaces >= 1:
								score += 100
						break
					if last_player == self.opponent.position:
						opp_spaces = len(board) - j
						if opp_count == 1:
							if opp_spaces >= 3:
								score -= 20
						if opp_count == 2:
							if opp_spaces >= 2:
								score -= 50
						if opp_count == 3:
							if opp_spaces >= 1:
								score -= 100
						break
						
			our_count = 0
			our_spaces = 0
			opp_count = 0
			opp_spaces = 0
		
		# diagonals
		diag_board = board

		for k in range(2):
			for i in range(-2, 4):
				for j in range(len(np.diag(diag_board, k=i))):
					if np.diag(diag_board, k=i)[j] == self.position:
						our_count += 1
						opp_seq[opp_count] += 1
						if opp_seq[1] * 1 + opp_seq[2] * 2 + opp_seq[3] * 3 + opp_spaces >= 4: # if you can make sequence of 4 including spaces
							score -= opp_seq[1] * opp_weight1 + opp_seq[2] * opp_weight2 + opp_seq[3] * opp_weight3 + opp_spaces * opp_weight_space
						opp_seq = [0,0,0,0] # reset the list because if you see 1 1 1 2 1 0 1, then 1 cannot make a sequence of 4. these 1's are useless.
						opp_count = 0
						opp_spaces = 0
						if our_count > 3:
							return 100000000
					elif np.diag(diag_board, k=i)[j] == self.opponent.position:
						our_seq[our_count] += 1
						opp_count += 1
						if opp_count > 3:
							return -100000000
						if our_seq[1] * 1 + our_seq[2] * 2 + our_seq[3] * 3 + our_spaces >= 4:
							score += our_seq[1] * our_weight1 + our_seq[2] * our_weight2 + our_seq[3] * our_weight3 + our_spaces * our_weight_space
						our_seq = [0,0,0,0]
						our_count = 0
						our_spaces = 0
					else:
						our_seq[our_count] += 1
						opp_seq[opp_count] += 1
						our_spaces += 1
						opp_spaces += 1
						our_count = 0
						opp_count = 0

				if opp_count != 0:
					opp_seq[opp_count] += 1
					if opp_seq[1] * 1 + opp_seq[2] * 2 + opp_seq[3] * 3 + opp_spaces >= 4:
						score -= opp_seq[1] * opp_weight1 + opp_seq[2] * opp_weight2 + opp_seq[3] * opp_weight3 + opp_spaces * opp_weight_space
						opp_count = 0
						opp_spaces = 0
				elif our_count != 0:
					our_seq[our_count] += 1
					if our_seq[1] * 1 + our_seq[2] * 2 + our_seq[3] * 3 + our_spaces >= 4:
						score += our_seq[1] * our_weight1 + our_seq[2] * our_weight2 + our_seq[3] * our_weight3 + our_spaces * our_weight_space
						our_count = 0
						our_spaces = 0
				our_count = 0
				our_spaces = 0
				our_seq = [0,0,0,0]
				opp_count = 0
				opp_spaces = 0
				opp_seq = [0,0,0,0]

			diag_board = np.flip(diag_board,1)
		return score
		

	def Minimax(self, env, move, max_depth):
		possible = env.topPosition >= 0 # possible is an array of seven True
		max_v = -math.inf

		for move_index, p in enumerate(possible):
			if not p:
				continue
			child = self.simulateMove(deepcopy(env), move_index, self.position)
			v = self.MIN(child, max_depth - 1)
			if v > max_v:
				max_v = v 
				move[:] = [move_index]
		print('done')
		return move

		
	def MAX(self, env, depth): #env is the board 

		if len(env.history[0]) + len(env.history[1]) == env.board.shape[0] * env.board.shape:
			return 0

		if env.gameOver(env.history[0][-1], self.opponent.position):
			return -10000000

		if depth == 0:
			return self.eval(env.board)

		possible = env.topPosition >= 0
		max_v = -math.inf

		for move_index, p in enumerate(possible):
			if not p:
				continue
			child = self.simulateMove(deepcopy(env), move_index, self.position) #simulatemove adding whoever turn it is to environment 
			max_v = max(max_v, self.MIN(child, depth - 1))
		return max_v

	
	def MIN(self, env, depth):

		if len(env.history[0]) + len(env.history[1]) == env.board.shape[0] * env.board.shape:
			return 0

		if env.gameOver(env.history[0][-1], self.position):
			return 10000000
		
		if depth == 0:
			return self.eval(env.board)

		possible = env.topPosition >= 0
		min_v = math.inf

		for move_index, p in enumerate(possible):
			if not p:
				continue
			child = self.simulateMove(deepcopy(env), move_index, self.opponent.position)
			min_v = min(min_v, self.MAX(child, depth - 1))
		return min_v 

	


class alphaBetaAI(connect4Player):

	def simulateMove(self, env, move, player):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)
		return env

	def play(self, env, move):
		self.Minimax(deepcopy(env), move, 3)

	def eval(self, board):   #this function is our evaluation function that we call in MIN and MAX 

		our_count = 0
		our_spaces = 0
		our_seq = [0,0,0,0]
		our_weight1 = 20
		our_weight2 = 50
		our_weight3 = 100
		our_weight_space = 5

		opp_count = 0
		opp_spaces = 0
		opp_seq = [0,0,0,0]
		opp_weight1 = 20
		opp_weight2 = 50
		opp_weight3 = 100
		opp_weight_space = 5

		score = 0

		for i in range(len(board)):
			if np.all((board[-i-1] == 0)):
				break
			for j in range(len(board[i])):
				if board[-i-1][j] == self.position:
					our_count += 1
					if our_count > 3:
						return 100000000
					opp_seq[opp_count] += 1
					if opp_seq[1] * 1 + opp_seq[2] * 2 + opp_seq[3] * 3 + opp_spaces >= 4:
						score -= opp_seq[1] * opp_weight1 + opp_seq[2] * opp_weight2 + opp_seq[3] * opp_weight3 + opp_spaces * opp_weight_space
					opp_seq = [0,0,0,0]
					opp_count = 0
					opp_spaces = 0
				elif board[-i-1][j] == self.opponent.position:
					opp_count += 1
					if opp_count > 3:
						return -100000000
					our_seq[our_count] += 1
					if our_seq[1] * 1 + our_seq[2] * 2 + our_seq[3] * 3 + our_spaces >= 4:
						score += our_seq[1] * our_weight1 + our_seq[2] * our_weight2 + our_seq[3] * our_weight3 + our_spaces * our_weight_space
					our_seq = [0,0,0,0]
					our_count = 0
					our_spaces = 0
				else:
					our_seq[our_count] += 1
					opp_seq[opp_count] += 1
					our_count = 0
					opp_count = 0
					our_spaces += 1
					opp_spaces += 1
					
			if opp_count != 0:
				opp_seq[opp_count] += 1
				if opp_seq[1] * 1 + opp_seq[2] * 2 + opp_seq[3] * 3 + opp_spaces >= 4:
					score -= opp_seq[1] * opp_weight1 + opp_seq[2] * opp_weight2 + opp_seq[3] * opp_weight3 + opp_spaces * opp_weight_space
					opp_count = 0
					opp_spaces = 0
			elif our_count != 0:
				our_seq[our_count] += 1
				if our_seq[1] * 1 + our_seq[2] * 2 + our_seq[3] * 3 + our_spaces >= 4:
					score += our_seq[1] * our_weight1 + our_seq[2] * our_weight2 + our_seq[3] * our_weight3 + our_spaces * our_weight_space
					our_count = 0
					our_spaces = 0
			our_count = 0
			our_spaces = 0
			our_seq = [0,0,0,0]
			opp_count = 0
			opp_spaces = 0
			opp_seq = [0,0,0,0]
		
		# columns
		last_player = 0
		for i in range(len(board[i])):
			for j in range(len(board)):
				if board[-j-1][i] == self.position:
					our_count += 1
					if our_count > 3:
						return 100000000
					opp_count = 0 # if other player is on the top, theres no advantages
					last_player = self.position
				elif board[-j-1][i] == self.opponent.position:
					opp_count += 1
					if opp_count > 3:
						return -100000000
					our_count = 0
					last_player = self.opponent.position
				else: # count for spaces left on the top, depending on the last player # if spaces + piece >= 4, then returns value(more piece is better)
					if last_player == self.position:
						our_spaces = len(board) - j
						if our_count == 1:
							if our_spaces >= 3:
								score += 20
						if our_count == 2:
							if our_spaces >= 2:
								score += 50
						if our_count == 3:
							if our_spaces >= 1:
								score += 100
						break
					if last_player == self.opponent.position:
						opp_spaces = len(board) - j
						if opp_count == 1:
							if opp_spaces >= 3:
								score -= 20
						if opp_count == 2:
							if opp_spaces >= 2:
								score -= 50
						if opp_count == 3:
							if opp_spaces >= 1:
								score -= 100
						break
						
			our_count = 0
			our_spaces = 0
			opp_count = 0
			opp_spaces = 0
		
		# diagonals
		diag_board = board

		for k in range(2):
			for i in range(-2, 4):
				for j in range(len(np.diag(diag_board, k=i))):
					if np.diag(diag_board, k=i)[j] == self.position:
						our_count += 1
						opp_seq[opp_count] += 1
						if opp_seq[1] * 1 + opp_seq[2] * 2 + opp_seq[3] * 3 + opp_spaces >= 4: # if you can make sequence of 4 including spaces
							score -= opp_seq[1] * opp_weight1 + opp_seq[2] * opp_weight2 + opp_seq[3] * opp_weight3 + opp_spaces * opp_weight_space
						opp_seq = [0,0,0,0] # reset the list because if you see 1 1 1 2 1 0 1, then 1 cannot make a sequence of 4. these 1's are useless.
						opp_count = 0
						opp_spaces = 0
						if our_count > 3:
							return 100000000
					elif np.diag(diag_board, k=i)[j] == self.opponent.position:
						our_seq[our_count] += 1
						opp_count += 1
						if opp_count > 3:
							return -100000000
						if our_seq[1] * 1 + our_seq[2] * 2 + our_seq[3] * 3 + our_spaces >= 4:
							score += our_seq[1] * our_weight1 + our_seq[2] * our_weight2 + our_seq[3] * our_weight3 + our_spaces * our_weight_space
						our_seq = [0,0,0,0]
						our_count = 0
						our_spaces = 0
					else:
						our_seq[our_count] += 1
						opp_seq[opp_count] += 1
						our_spaces += 1
						opp_spaces += 1
						our_count = 0
						opp_count = 0

				if opp_count != 0:
					opp_seq[opp_count] += 1
					if opp_seq[1] * 1 + opp_seq[2] * 2 + opp_seq[3] * 3 + opp_spaces >= 4:
						score -= opp_seq[1] * opp_weight1 + opp_seq[2] * opp_weight2 + opp_seq[3] * opp_weight3 + opp_spaces * opp_weight_space
						opp_count = 0
						opp_spaces = 0
				elif our_count != 0:
					our_seq[our_count] += 1
					if our_seq[1] * 1 + our_seq[2] * 2 + our_seq[3] * 3 + our_spaces >= 4:
						score += our_seq[1] * our_weight1 + our_seq[2] * our_weight2 + our_seq[3] * our_weight3 + our_spaces * our_weight_space
						our_count = 0
						our_spaces = 0
				our_count = 0
				our_spaces = 0
				our_seq = [0,0,0,0]
				opp_count = 0
				opp_spaces = 0
				opp_seq = [0,0,0,0]

			diag_board = np.flip(diag_board,1)
		return score
		

	def Minimax(self, env, move, max_depth):
		possible = env.topPosition >= 0 # possible is an array of seven True
		max_v = -math.inf

		for move_index, p in enumerate(possible):
			if not p:
				continue
			child = self.simulateMove(deepcopy(env), move_index, self.position)
			v = self.MIN(child, max_depth - 1, -math.inf, math.inf)
			if v > max_v:
				max_v = v 
				move[:] = [move_index]
		print('done')
		return move

		
	def MAX(self, env, depth, alpha, beta): #env is the board 

		if len(env.history[0]) + len(env.history[1]) == env.board.shape[0] * env.board.shape:
			return 0

		if env.gameOver(env.history[0][-1], self.opponent.position):
			return -10000000

		if depth == 0:
			return self.eval(env.board)

		possible = env.topPosition >= 0
		max_v = -math.inf

		for move_index, p in enumerate(possible):
			if not p:
				continue
			child = self.simulateMove(deepcopy(env), move_index, self.position) #simulatemove adding whoever turn it is to environment 
			max_v = max(max_v, self.MIN(child, depth - 1, alpha, beta))
			alpha = max(alpha, max_v)
			if max_v >= beta:
				break
		return max_v

	
	def MIN(self, env, depth, alpha, beta):

		if len(env.history[0]) + len(env.history[1]) == env.board.shape[0] * env.board.shape:
			return 0

		if env.gameOver(env.history[0][-1], self.position):
			return 10000000
		
		if depth == 0:
			return self.eval(env.board)

		possible = env.topPosition >= 0
		min_v = math.inf

		for move_index, p in enumerate(possible):
			if not p:
				continue
			child = self.simulateMove(deepcopy(env), move_index, self.opponent.position)
			min_v = min(min_v, self.MAX(child, depth - 1, alpha, beta))
			beta = max(beta, min_v)
			if min_v <= alpha:
				break
		return min_v 


SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)




