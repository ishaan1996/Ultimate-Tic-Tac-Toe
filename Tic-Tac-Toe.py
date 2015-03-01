import sys
import random
import signal

#Timer handler, helper function
class TimedOutExc(Exception):
        pass
		
def handler(signum, frame):
    #print 'Signal handler called with signal', signum
    raise TimedOutExc()


class Manual_player:
	def __init__(self):
		pass
	def move(self, temp_board, temp_block, old_move, flag):
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"	
		mvp = raw_input()
		mvp = mvp.split()
		return (int(mvp[0]), int(mvp[1]))
		
def  getpos(block, pos, cells): 
	num1 = (1, 2)
	num2 = 1


	if type(pos) == type(num1):
		return int(block/3) * 27 + (block % 3) * 3 + (pos[0] * 9) + pos[1]
	elif type(pos) == type(num2) : 
		return int(block/3) * 27 + (block % 3) * 3 + (pos/3) * 9 + pos%3
class Player73:
	
	def __init__(self):
		self.FLAG = ['o', 'x']
		pass
	def move_copy(self, temp_board, temp_block, node, flag):
		for_corner = [0, 2, 3, 5, 6, 8]
		blocks_allowed_copy = []
		if node[0] in for_corner and node[1] in for_corner:
		## we will have 3 representative blocks, to choose from
			if node[0] % 3 == 0 and node[1] % 3 == 0:
			## top left 3 blocks are allowed
				blocks_allowed_copy = [0, 1, 3]
			elif node[0] % 3 == 0 and node[1] in [2, 5, 8]:
			## top right 3 blocks are allowed
				blocks_allowed_copy = [1,2,5]
			elif node[0] in [2,5, 8] and node[1] % 3 == 0:
			## bottom left 3 blocks are allowed
				blocks_allowed_copy  = [3,6,7]
			elif node[0] in [2,5,8] and node[1] in [2,5,8]:
			### bottom right 3 blocks are allowed
				blocks_allowed_copy = [5,7,8]
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
				sys.exit(1)
		else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
			if node[0] % 3 == 0 and node[1] in [1,4,7]:
			## upper-center block
				blocks_allowed_copy = [1]
			elif node[0] in [1,4,7] and node[1] % 3 == 0:
			## middle-left block
				blocks_allowed_copy = [3]
			elif node[0] in [2,5,8] and node[1] in [1,4,7]:
			## lower-center block
				blocks_allowed_copy = [7]
			elif node[0] in [1,4,7] and node[1] in [2,5,8]:
			## middle-right block
				blocks_allowed_copy = [5]
			elif node[0] in [1,4,7] and node[1] in [1,4,7]:
				blocks_allowed_copy = [4]
			# remove the already won blocks
		for i in reversed(blocks_allowed_copy):
			if temp_block[i] != '-':
				blocks_allowed_copy.remove(i)
		# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
		cells_copy = get_empty_out_of(temp_board, blocks_allowed_copy,temp_block)
		return cells_copy

	def heuristic(self, game_board, game_block, my_move):
		if my_move == 'o':
			not_my_move = 'x'
		elif my_move == 'x':
			not_my_move = 'o'
		total_val = []
		count_my_move = 0
		count_not_my_move = 0
		for i in range(len(game_block)):
			if game_block[i] == '-':
				id1 = i/3
				id2 = i%3
				add = 0
				count_my_move = 0
				count_not_my_move = 0
				for j in range(id1*3, id1*3 + 3):
					count_my_move = 0
					count_not_my_move = 0
					for k in range(id2*3, id2*3 + 3):
						if game_board[j][k] == my_move:
							count_my_move += 1
						elif game_board[j][k] == not_my_move:
							count_not_my_move += 1
					if count_not_my_move == 0 and count_my_move != 0:
						add = add + pow(10, count_my_move)
					elif count_my_move == 0 and count_not_my_move != 0:
						add = add + pow(10, count_not_my_move)
					else:
						add = add + pow(10, count_my_move) - pow(10, count_not_my_move)
				for j in range(id2*3, id2*3 + 3):
					count_my_move = 0
					count_not_my_move = 0
					for k in range(id1*3, id1*3 + 3):
						if game_board[k][j] == my_move:
							count_my_move += 1
						elif game_board[k][j] == not_my_move:
							count_not_my_move += 1
					if count_not_my_move == 0 and count_my_move != 0:
						add = add + pow(10, count_my_move)
					elif count_my_move == 0 and count_not_my_move != 0:
						add = add + pow(10, count_not_my_move)
					else:
						add = add + pow(10, count_my_move) - pow(10, count_not_my_move)
				count_my_move = 0
				count_not_my_move = 0
				for j in range(0, 3):
					if game_board[id1*3 + j][id2*3 + j] == my_move:
						count_my_move += 1
					elif game_board[id1*3 + j][id2*3 + j] == not_my_move:
						count_not_my_move += 1
				if count_not_my_move == 0 and count_my_move != 0:
					add = add + pow(10, count_my_move)
				elif count_my_move == 0 and count_not_my_move != 0:
					add = add + pow(10, count_not_my_move)
				else:
					add = add + pow(10, count_my_move) - pow(10, count_not_my_move)
				count_my_move = 0
				count_not_my_move = 0
				for j in range(0, 3):
					if game_board[id1*3 + j][id2*3 + (2 - j)] == my_move:
						count_my_move += 1
					elif game_board[id2*3 + j][id2*3 + (2 - j)] == not_my_move:
						count_not_my_move += 1
				if count_not_my_move == 0 and count_my_move != 0:
					add = add + pow(10, count_my_move)
				elif count_my_move == 0 and count_not_my_move != 0:
					add = add + pow(10, count_not_my_move)
				else:
					add = add + pow(10, count_my_move) - pow(10, count_not_my_move)
				total_val.append(add)	
			elif game_block[i] == my_move:
				total_val.append(1000)
			elif game_block[i] == not_my_move:
				total_val.append(-1000)
			else:
				total_val.append(0)
		total = 0
		count_my_move = 0
		count_not_my_move = 0
		temp_sum = 0
		for i in range(0, 3):
			for j in range(0, 3):
				if total_val[(i*3) + j] == 1000:
					count_my_move += 1
				elif total_val[(i*3) + j] == -1000:
					count_not_my_move += 1
				else:
					temp_sum += total_val[(i*3) + j]
			if count_not_my_move == 0 and count_my_move != 0:
				total = total + pow(1000, count_my_move) + temp_sum
			elif count_not_my_move != 0 and count_my_move == 0:
				total = total - pow(1000, count_not_my_move) + temp_sum
			else:
				total = total + pow(1000, count_my_move) - pow(1000, count_not_my_move) + temp_sum
		count_my_move = 0
		count_not_my_move = 0
		temp_sum = 0
		for i in range(0, 3):
			for j in range(0, 3):
				if total_val[(j*3) + i] == 1000:
					count_my_move += 1
				elif total_val[(j*3) + i] == -1000:
					count_not_my_move += 1
				else:
					temp_sum += total_val[(j*3) + i]
			if count_not_my_move == 0 and count_my_move != 0:
				total = total + pow(1000, count_my_move) + temp_sum
			elif count_not_my_move != 0 and count_my_move == 0:
				total = total - pow(1000, count_not_my_move) + temp_sum
			else:
				total = total + pow(1000, count_my_move) - pow(1000, count_not_my_move) + temp_sum
		count_my_move = 0
		count_not_my_move = 0
		temp_sum = 0			
		for i in range(0, 3):
			if total_val[(i*3) + i] == 1000:
				count_my_move += 1
			elif total_val[(i*3) + i] == -1000:
				count_not_my_move += 1
			else:
				temp_sum += total_val[(i*3) + i]
		if count_not_my_move == 0 and count_my_move != 0:
			total = total + pow(1000, count_my_move) + temp_sum
		elif count_not_my_move != 0 and count_my_move == 0:
			total = total - pow(1000, count_not_my_move) + temp_sum
		else:
			total = total + pow(1000, count_my_move) - pow(1000, count_not_my_move) + temp_sum
		count_my_move = 0
		count_not_my_move = 0
		temp_sum = 0
		for i in range(0, 3):
			if total_val[(i*3) + (2 - i)] == 1000:
				count_my_move += 1
			elif total_val[(i*3) + (2 - i)] == -1000:
				count_not_my_move += 1
			else:
				temp_sum += total_val[(i*3) + (2 - i)]
		if count_not_my_move == 0 and count_my_move != 0:
			total = total + pow(1000, count_my_move) + temp_sum
		elif count_not_my_move != 0 and count_my_move == 0:
			total = total - pow(1000, count_not_my_move) + temp_sum
		else:
			total = total + pow(1000, count_my_move) - pow(1000, count_not_my_move) + temp_sum

		return total	

	def alphabeta(self, node, depth, alpha, beta, board, block, flag):
		if depth == 0 :
			return self.heuristic(board, block, self.myflag)
		if flag == self.myflag :
			value = -100
			cells_copy = self.move_copy(board, block, node, flag)
			for i in cells_copy :
				value = max(value, self.alphabeta(i, depth -1, alpha, beta, board, block, self.FLAG[(self.FLAG.index(self.myflag) + 1) % 2]))
				alpha = max(alpha, value)
				if beta <= alpha :
					break
			return value
		else :
			value = 100
			cells_copy = self.move_copy(board, block, node, flag)
			for i in cells_copy :
				value = min(value, self.alphabeta(i, depth-1, alpha, beta, board, block, self.FLAG[self.FLAG.index(self.myflag)]))
				beta = min(beta, value)
				if beta <= alpha :
					break
			return value


	def move(self,temp_board,temp_block,old_move,flag):
#		while(1):
#			pass
		self.myflag = flag
		for_corner = [0,2,3,5,6,8]

		#List of permitted blocks, based on old move.
		print 'temp_board = '
		print temp_board
		print 'temp_block = '
		print temp_block
		print 'old_move = ' + str(old_move)
		blocks_allowed  = []

		if old_move[0] in for_corner and old_move[1] in for_corner:
			## we will have 3 representative blocks, to choose from

			if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
				## top left 3 blocks are allowed
				blocks_allowed = [0, 1, 3]
			elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
				## top right 3 blocks are allowed
				blocks_allowed = [1,2,5]
			elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
				## bottom left 3 blocks are allowed
				blocks_allowed  = [3,6,7]
			elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
				### bottom right 3 blocks are allowed
				blocks_allowed = [5,7,8]
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
				sys.exit(1)
		else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
			if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
				## upper-center block
				blocks_allowed = [1]
	
			elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
				## middle-left block
				blocks_allowed = [3]
		
			elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
				## lower-center block
				blocks_allowed = [7]

			elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
				## middle-right block
				blocks_allowed = [5]
			elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
				blocks_allowed = [4]

		# remove the already won blocks
                for i in reversed(blocks_allowed):
                    if temp_block[i] != '-':
                        blocks_allowed.remove(i)
	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
		cells = get_empty_out_of(temp_board, blocks_allowed,temp_block)
		if(len(cells) == 81):
			return cells[3 * 9 + 4]
		prune_value = []
		for i in cells :
			temp_board_copy = [row[:] for row in temp_board]
			temp_block_copy = temp_block[:]
		   	prune_value.append(self.alphabeta(i, 2, -100, 100, temp_board_copy, temp_block_copy, flag))
		return cells[prune_value.index(max(prune_value))]




class Player2:
	
	def __init__(self):
		pass
	def move(self,temp_board,temp_block,old_move,flag):
		for_corner = [0,2,3,5,6,8]

		#List of permitted blocks, based on old move.
		blocks_allowed  = []

		if old_move[0] in for_corner and old_move[1] in for_corner:
			## we will have 3 representative blocks, to choose from

			if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
				## top left 3 blocks are allowed
				blocks_allowed = [0, 1, 3]
			elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
				## top right 3 blocks are allowed
				blocks_allowed = [1,2,5]
			elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
				## bottom left 3 blocks are allowed
				blocks_allowed  = [3,6,7]
			elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
				### bottom right 3 blocks are allowed
				blocks_allowed = [5,7,8]
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
				sys.exit(1)
		else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
			if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
				## upper-center block
				blocks_allowed = [1]
	
			elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
				## middle-left block
				blocks_allowed = [3]
		
			elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
				## lower-center block
				blocks_allowed = [7]

			elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
				## middle-right block
				blocks_allowed = [5]
			elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
				blocks_allowed = [4]
                
                for i in reversed(blocks_allowed):
                    if temp_block[i] != '-':
                        blocks_allowed.remove(i)

	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
		cells = get_empty_out_of(temp_board,blocks_allowed,temp_block)
		return cells[random.randrange(len(cells))]

#Initializes the game
def get_init_board_and_blockstatus():
	board = []
	for i in range(9):
		row = ['-']*9
		board.append(row)
	
	block_stat = ['-']*9
	return board, block_stat

# Checks if player has messed with the board. Don't mess with the board that is passed to your move function. 
def verification_fails_board(board_game, temp_board_state):
	return board_game == temp_board_state	

# Checks if player has messed with the block. Don't mess with the block array that is passed to your move function. 
def verification_fails_block(block_stat, temp_block_stat):
	return block_stat == temp_block_stat	

#Gets empty cells from the list of possible blocks. Hence gets valid moves. 
def get_empty_out_of(gameb, blal,block_stat):
	cells = []  # it will be list of tuples
	#Iterate over possible blocks and get empty cells
	for idb in blal:
		id1 = idb/3
		id2 = idb%3
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if gameb[i][j] == '-':
					cells.append((i,j))

	# If all the possible blocks are full, you can move anywhere
	if cells == []:
		for i in range(9):
			for j in range(9):
                                no = (i/3)*3
                                no += (j/3)
				if gameb[i][j] == '-' and block_stat[no] == '-':
					cells.append((i,j))	
	return cells
		
# Note that even if someone has won a block, it is not abandoned. But then, there's no point winning it again!
# Returns True if move is valid
def check_valid_move(game_board,block_stat, current_move, old_move):

	# first we need to check whether current_move is tuple of not
	# old_move is guaranteed to be correct
	if type(current_move) is not tuple:
		return False
	
	if len(current_move) != 2:
		return False

	a = current_move[0]
	b = current_move[1]	

	if type(a) is not int or type(b) is not int:
		return False
	if a < 0 or a > 8 or b < 0 or b > 8:
		return False

	#Special case at start of game, any move is okay!
	if old_move[0] == -1 and old_move[1] == -1:
		return True


	for_corner = [0,2,3,5,6,8]

	#List of permitted blocks, based on old move.
	blocks_allowed  = []

	if old_move[0] in for_corner and old_move[1] in for_corner:
		## we will have 3 representative blocks, to choose from

		if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
			## top left 3 blocks are allowed
			blocks_allowed = [0,1,3]
		elif old_move[0] % 3 == 0 and old_move[1] in [2,5,8]:
			## top right 3 blocks are allowed
			blocks_allowed = [1,2,5]
		elif old_move[0] in [2,5,8] and old_move[1] % 3 == 0:
			## bottom left 3 blocks are allowed
			blocks_allowed  = [3,6,7]
		elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
			### bottom right 3 blocks are allowed
			blocks_allowed = [5,7,8]

		else:
			print "SOMETHING REALLY WEIRD HAPPENED!"
			sys.exit(1)

	else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
		if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
			## upper-center block
			blocks_allowed = [1]
	
		elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
			## middle-left block
			blocks_allowed = [3]
		
		elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
			## lower-center block
			blocks_allowed = [7]

		elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
			## middle-right block
			blocks_allowed = [5]

		elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
			blocks_allowed = [4]

        #Check if the block is won, or completed. If so you cannot move there. 

        for i in reversed(blocks_allowed):
            if block_stat[i] != '-':
                blocks_allowed.remove(i)
        
        # We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
        cells = get_empty_out_of(game_board, blocks_allowed,block_stat)

	#Checks if you made a valid move. 
        if current_move in cells:
     	    return True
        else:
    	    return False

def update_lists(game_board, block_stat, move_ret, fl):
	#move_ret has the move to be made, so we modify the game_board, and then check if we need to modify block_stat
	game_board[move_ret[0]][move_ret[1]] = fl

	block_no = (move_ret[0]/3)*3 + move_ret[1]/3
	id1 = block_no/3
	id2 = block_no%3
	mg = 0
	mflg = 0
	if block_stat[block_no] == '-':
		if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-':
			mflg=1
		if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-':
			mflg=1
		
                if mflg != 1:
                    for i in range(id2*3,id2*3+3):
                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-':
                                mflg = 1
                                break

                ### row-wise
		if mflg != 1:
                    for i in range(id1*3,id1*3+3):
                        if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-':
                                mflg = 1
                                break

	
	if mflg == 1:
		block_stat[block_no] = fl
	
        #check for draw on the block.

        id1 = block_no/3
	id2 = block_no%3
        cells = []
	for i in range(id1*3,id1*3+3):
	    for j in range(id2*3,id2*3+3):
		if game_board[i][j] == '-':
		    cells.append((i,j))

        if cells == [] and mflg!=1:
            block_stat[block_no] = 'd' #Draw
        
        return

def terminal_state_reached(game_board, block_stat):
	
        #Check if game is won!
        bs = block_stat
	## Row win
	if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='d') or (bs[3]!='d' and bs[3]!='-' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='d' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
		print block_stat
		return True, 'W'
	## Col win
	elif (bs[0]!='d' and bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1]!='d'and bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2]!='d' and bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
		print block_stat
		return True, 'W'
	## Diag win
	elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='d') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='d'):
		print block_stat
		return True, 'W'
	else:
		smfl = 0
		for i in range(9):
			for j in range(9):
				if game_board[i][j] == '-' and block_stat[(i/3)*3+(j/3)] == '-':
					smfl = 1
					break
		if smfl == 1:
                        #Game is still on!
			return False, 'Continue'
		
		else:
                        #Changed scoring mechanism
                        # 1. If there is a tie, player with more boxes won, wins.
                        # 2. If no of boxes won is the same, player with more corner move, wins. 
                        point1 = 0
                        point2 = 0
                        for i in block_stat:
                            if i == 'x':
                                point1+=1
                            elif i=='o':
                                point2+=1
			if point1>point2:
				return True, 'P1'
			elif point2>point1:
				return True, 'P2'
			else:
                                point1 = 0
                                point2 = 0
                                for i in range(len(game_board)):
                                    for j in range(len(game_board[i])):
                                        if i%3!=1 and j%3!=1:
                                            if game_board[i][j] == 'x':
                                                point1+=1
                                            elif game_board[i][j]=='o':
                                                point2+=1
			        if point1>point2:
				    return True, 'P1'
			        elif point2>point1:
				    return True, 'P2'
                                else:
				    return True, 'D'	

def decide_winner_and_get_message(player,status, message):
	if player == 'P1' and status == 'L':
		return ('P2',message)
	elif player == 'P1' and status == 'W':
		return ('P1',message)
	elif player == 'P2' and status == 'L':
		return ('P1',message)
	elif player == 'P2' and status == 'W':
		return ('P2',message)
	else:
		return ('NONE','DRAW')
	return

def print_lists(gb, bs):
	print '=========== Game Board ==========='
	for i in range(9):
		if i > 0 and i % 3 == 0:
			print
		for j in range(9):
			if j > 0 and j % 3 == 0:
				print " " + gb[i][j],
			else:
				print gb[i][j],

		print
	print "=================================="

	print "=========== Block Status ========="
	for i in range(0, 9, 3):
		print bs[i] + " " + bs[i+1] + " " + bs[i+2] 
	print "=================================="
	print

def simulate(obj1,obj2):
	
	# Game board is a 9x9 list, block_stat is a 1D list of 9 elements
	game_board, block_stat = get_init_board_and_blockstatus()

	pl1 = obj1 
	pl2 = obj2
	

	### basically, player with flag 'x' will start the game
	pl1_fl = 'x'
	pl2_fl = 'o'

	old_move = (-1, -1) # For the first move

	WINNER = ''
	MESSAGE = ''

        #Make your move in 6 seconds!
	TIMEALLOWED = 60

	print_lists(game_board, block_stat)

	while(1):

		# Player73 will move
		
		temp_board_state = game_board[:]
		temp_block_stat = block_stat[:]
	
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		# Player73 to complete in TIMEALLOWED secs. 
		try:
			ret_move_pl1 = pl1.move(temp_board_state, temp_block_stat, old_move, pl1_fl)
		except TimedOutExc as e:
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'TIMED OUT')
			break
		signal.alarm(0)
	
                #Checking if list hasn't been modified! Note: Do not make changes in the lists passed in move function!
		if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			#Player73 loses - he modified something
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
		
		# Check if the move made is valid
		if not check_valid_move(game_board, block_stat,ret_move_pl1, old_move):
			## Player73 loses - he made the wrong move.
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MADE AN INVALID MOVE')
			break


		print "Player 1 made the move:", ret_move_pl1, 'with', pl1_fl

                #So if the move is valid, we update the 'game_board' and 'block_stat' lists with move of pl1
                update_lists(game_board, block_stat, ret_move_pl1, pl1_fl)

		# Checking if the last move resulted in a terminal state
		gamestatus, mesg =  terminal_state_reached(game_board, block_stat)
		if gamestatus == True:
			print_lists(game_board, block_stat)
			WINNER, MESSAGE = decide_winner_and_get_message('P1', mesg,  'COMPLETE')	
			break

		
		old_move = ret_move_pl1
		print_lists(game_board, block_stat)

                # Now player2 plays

                temp_board_state = game_board[:]
                temp_block_stat = block_stat[:]


		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		try:
                	ret_move_pl2 = pl2.move(temp_board_state, temp_block_stat, old_move, pl2_fl)
		except TimedOutExc as e:
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'TIMED OUT')
			break
		signal.alarm(0)

                if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
			
                if not check_valid_move(game_board, block_stat,ret_move_pl2, old_move):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MADE AN INVALID MOVE')
			break


		print "Player 2 made the move:", ret_move_pl2, 'with', pl2_fl
                
                update_lists(game_board, block_stat, ret_move_pl2, pl2_fl)

		gamestatus, mesg =  terminal_state_reached(game_board, block_stat)
                if gamestatus == True:
			print_lists(game_board, block_stat)
                        WINNER, MESSAGE = decide_winner_and_get_message('P2', mesg,  'COMPLETE' )
                        break
		old_move = ret_move_pl2
		print_lists(game_board, block_stat)
	
	print WINNER
	print MESSAGE
	#print myflag

if __name__ == '__main__':
	## get game playing objects
	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Random player vs. AI bot'
		print '                2 => Human vs. AI bot'
		print '                3 => Human vs. Human'
		sys.exit(1)

	obj1 = ''
	obj2 = ''
	option = sys.argv[1]	
	if option == '1':
		obj1 = Player73()
		obj2 = Player2()
	elif option == '2':
		obj1 = Player73()
		obj2 = Manual_player()
	elif option == '3':
		obj1 = Manual_player()
		obj2 = Manual_player()

	num = random.uniform(0,1)
	if num > 0.5:
		myflag = 'o'
		simulate(obj2, obj1)
	else:
		myflag = 'x'
		simulate(obj1, obj2)
	simulate(obj1, obj2)
