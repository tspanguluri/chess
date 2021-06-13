class King:
	def __init__(self, row, col, color):
		self.row = row
		self.col = col
		self.color = color
		self.type = "K"

	# creates a new object to avoid changes due to pass-by-reference
	def copy(self) -> "King":
		return King(self.row, self.col, self.color)

	def isInCheck(self, board, colors) -> bool:
		opposite = {"W":"B", "B":"W"}

		for row in board:
			for piece in row:
				if piece != "-" and piece.color == opposite[self.color]:
					if piece.type == "P":
						if piece.color == "W":
							if self.row == piece.row-1 and (self.col == piece.col-1 or self.col == piece.col+1):
								return False
						elif piece.color == "B":
							if self.row == piece.row+1 and (self.col == piece.col-1 or self.col == piece.col+1):
								return False
					elif piece.canMoveTo(self.row, self.col, colors, board):
						return True
		return False

	def canMoveTo(self, targetRow, targetCol, colors, board) -> bool:
		def findKing(board, color) -> "List[int]":
			lst = [-1, -1]
			for i in range(0, 8):
				for j in range(0, 8):
					if board[i][j] != "-":
						if board[i][j].type == "K" and board[i][j].color == color:
							lst = [i, j]
							return lst
			return lst
		if colors[targetRow][targetCol] == self.color:
				return False

		output = False

		opposite = {"W":"B", "B":"W"}
		otherKing = findKing(board, opposite[self.color])

		# Kings cannot move into check, nor can they be within one square of another King is any direction
		if abs(targetRow-self.row) <= 1 and abs(targetCol-self.col) <= 1 and (abs(targetRow-otherKing[0])>1 or abs(targetCol-otherKing[1])>1):

			piece = board[self.row][self.col]
			oldRow = self.row
			oldCol = self.col
			displaced = board[targetRow][targetCol]

			board[targetRow][targetCol] = piece
			piece.row = targetRow
			piece.col = targetCol
			board[oldRow][oldCol] = "-"

			if not self.isInCheck(board, colors):
				output = True

			board[targetRow][targetCol] = displaced
			board[oldRow][oldCol] = piece
			piece.row = oldRow
			piece.col = oldCol

		return output
	
	
	def __str__(self) -> str:
		return "K"

class Knight:
	def __init__(self, row, col, color):
		self.row = row
		self.col = col
		self.color = color
		self.type = "N"
	
	# creates a new object to avoid changes due to pass-by-reference
	def copy(self) -> "Knight":
		return Knight(self.row, self.col, self.color)

		# a Knight can move 2 squares in one direction and one square perpendicular, as long as the target square is not taken by the same color
	def canMoveTo(self, targetRow, targetCol, colors, board) -> bool:
		if colors[targetRow][targetCol] != self.color:
			if targetRow==self.row+1:
				if targetCol==self.col+2:
					return True
				elif targetCol==self.col-2:
					return True
			elif targetRow==self.row-1:
				if targetCol==self.col+2:
					return True
				elif targetCol==self.col-2:
					return True
			elif targetRow==self.row+2:
				if targetCol==self.col+1:
					return True
				elif targetCol==self.col-1:
					return True
			elif targetRow==self.row-2:
				if targetCol==self.col+1:
					return True
				elif targetCol==self.col-1:
					return True
		return False

	def __str__(self) -> str:
		return "N"

class Pawn:
	def __init__(self, row, col, color):
		self.row = row
		self.col = col
		self.color = color
		self.type = "P"

	# creates a new object to avoid changes due to pass-by-reference
	def copy(self) -> "Pawn":
		return Pawn(self.row, self.col, self.color)

	# a Pawn can only move forward except for the first move (double move) and can only capture diagonally (one square)
	def canMoveTo(self, targetRow, targetCol, colors, board) -> bool:
		if self.color=="B":
			if (targetCol==self.col and targetRow==self.row+1) or (targetCol==self.col and self.row==1 and targetRow==self.row+2):
				if colors[targetRow][targetCol]=="-":
					return True
				else:
					return False
			elif targetCol==self.col+1 or targetCol==self.col-1:
				if targetRow!=self.row+1:
					return False
				if colors[targetRow][targetCol]=="W":
					return True
				else:
					return False
		else:
			if (targetCol==self.col and targetRow==self.row-1) or (targetCol==self.col and self.row==6 and targetRow==self.row-2):
				if colors[targetRow][targetCol]=="-":
					return True
				else:
					return False
			elif targetCol==self.col+1 or targetCol==self.col-1:
				if targetRow!=self.row-1:
					return False
				if colors[targetRow][targetCol]=="B":
					return True
				else:
					return False
		return False

	def __str__(self) -> str:
		return ""

class Rook:
	def __init__(self, row, col, color):
		self.row = row
		self.col = col
		self.color = color
		self.type = "R"

	# creates a new object to avoid changes due to pass-by-reference
	def copy(self) -> "Rook":
		return Rook(self.row, self.col, self.color)

	# Rooks can move any number of spaces in a straight line
	def canMoveTo(self, targetRow, targetCol, colors, board) -> bool:
		if colors[targetRow][targetCol]==self.color:
			return False
		if (targetRow==self.row or targetCol==self.col):
			if (targetRow==self.row):
				placeNow = self.col
				toMove = targetCol

				if toMove < placeNow:
					toMove, placeNow = placeNow, toMove

				for i in range(placeNow+1, toMove):
					if colors[self.row][i] != "-":
						return False
			elif targetCol==self.col:
				placeNow=self.row
				toMove=targetRow

				if toMove < placeNow:
					toMove, placeNow = placeNow, toMove
				for i in range(placeNow+1, toMove):
					if colors[i][self.col]!="-":
						return False

			return True
		return False

	def __str__(self) -> str:
		return "R"

class Bishop:
	def __init__(self, row, col, color):
		self.row = row
		self.col = col
		self.color = color
		self.type = "B"

	# creates a new object to avoid changes due to pass-by-reference
	def copy(self) -> "Bishop":
		return Bishop(self.row, self.col, self.color)

	# Bishops can move any number of spaces in a diagonal
	def canMoveTo(self, targetRow, targetCol, colors, board) -> bool:
		if colors[targetRow][targetCol]!=self.color:
			# if target row, col are on the same diagnonal as the bishop
			if abs(self.row-targetRow) != abs(self.col-targetCol):
				return False
			i = self.row
			j = self.col

			if self.row > targetRow:
				# up-left of the bishop
				if self.col > targetCol:
					i-=1
					j-=1
					while(i!=targetRow):
						if colors[i][j]!="-":
							return False
						i-=1
						j-=1
				# up-right of the bishop
				elif self.col < targetCol:
					i-=1
					j+=1
					while(i!=targetRow):
						if colors[i][j]!="-":
							return False
						i-=1
						j+=1
			else:
				# down-left of the bishop
				if self.col > targetCol:
					i+=1
					j-=1
					while(i!=targetRow):
						if colors[i][j]!="-":
							return False
						i+=1
						j-=1
				# down-right of the bishop
				elif self.col < targetCol:
					i+=1
					j+=1
					while(i!=targetRow):
						if colors[i][j]!="-":
							return False
						i+=1
						j+=1
			return True

		return False

	def __str__(self) -> str:
		return "B"

class Queen:
	def __init__(self, row, col, color):
		self.row = row
		self.col = col
		self.color = color
		self.type = "Q"

	# creates a new object to avoid changes due to pass-by-reference
	def copy(self) -> "Queen":
		return Queen(self.row, self.col, self.color)

	# Queens can move any number of spaces in stright lines or in diagonals
	def canMoveTo(self, targetRow, targetCol, colors, board) -> bool:
		if colors[targetRow][targetCol]==self.color:
			return False
		if (targetRow==self.row or targetCol==self.col):
			if (targetRow==self.row):
				placeNow = self.col
				toMove = targetCol

				if toMove < placeNow:
					toMove, placeNow = placeNow, toMove

				for i in range(placeNow+1, toMove):
					if colors[self.row][i] != "-":
						return False
			elif targetCol==self.col:

				placeNow=self.row
				toMove=targetRow

				if toMove < placeNow:
					toMove, placeNow = placeNow, toMove
				for i in range(placeNow+1, toMove):
					if colors[i][self.col]!="-":
						return False

			return True
		elif abs(self.row-targetRow) == abs(self.col-targetCol):
			i = self.row
			j = self.col

			if self.row > targetRow:
				# up-left of the queen
				if self.col > targetCol:
					i-=1
					j-=1
					while(i!=targetRow):
						if colors[i][j]!="-":
							return False
						i-=1
						j-=1
				# up-right of the queen
				elif self.col < targetCol:
					i-=1
					j+=1
					while(i!=targetRow):
						if colors[i][j]!="-":
							return False
						i-=1
						j+=1
			else:
				# down-left of the queen
				if self.col > targetCol:
					i+=1
					j-=1
					while(i!=targetRow):
						if colors[i][j]!="-":
							return False
						i+=1
						j-=1
				# down-right of the queen
				elif self.col < targetCol:
					i+=1
					j+=1
					while(i!=targetRow):
						if colors[i][j]!="-":
							return False
						i+=1
						j+=1
			return True
		return False

	def __str__(self) -> str:
		return "Q"