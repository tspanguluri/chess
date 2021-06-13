from graphics import *
from Pieces import *

# draws the chessboard using a Graphics object
def drawBoard(panel, master, images) -> None:
	for row in range(0, 8):
		for col in range(0, 8):
			if row%2!=col%2:
				master[row][col].setFill(color_rgb(160, 82, 45))
			master[row][col].draw(panel)

	# uses list comprehension to get the locations and text for the rank and file numbers/letters
	fileNames = [Text(Point(master[7][i].getP2().getX()-40, master[7][i].getP2().getY()+20), str(chr(97+i))) for i in range(0, 8)]
	rankNums = [Text(Point(master[i][0].getP1().getX()-20, master[i][0].getP1().getY()+40), str(8-i)) for i in range(0, 8)]	

	# sets the design for the rank/file markings and draws them
	for j in range(0, 8):

		format(rankNums[j], "helvetica", "bold", 15)
		format(fileNames[j], "helvetica", "bold", 15)
		rankNums[j].draw(panel)
		fileNames[j].draw(panel)

	# draws the images into the board
	for row in images:
		for image in row:
			if image is not None:
				image.draw(panel)

# format a text object to specifications
def format(text, face, style, size) -> None:
	text.setFace(face)
	text.setStyle(style)
	text.setSize(size)


# makes a copy of the list so that I can avoid the list being changed in functions because of pass-by-reference
def copyOf(arr) -> "List[List[]]":
	lst = [[None for i in range(0, 8)] for j in range(0, 8)]
	
	for i in range(0, 8):
		for j in range(0, 8):
			if type(arr[i][j])==type("-"):
				lst[i][j] = ""+arr[i][j]
			else:
				lst[i][j] = arr[i][j].copy()
	return lst


# returns whether or not the specified color's king is in check
def kingInCheck(board, color, colors) -> bool:
	opposite = {"W":"B", "B":"W"}

	for i in range(0, 8):
		for j in range(0, 8):
			if board[i][j] != "-":
				if board[i][j].type == "K" and board[i][j].color == color:
					lst = [i, j]
	for row in range(0, 8):
		for col in range(0, 8):
			if board[row][col] != "-":
				if board[row][col].color == opposite[color]:
					if board[row][col].canMoveTo(lst[0], lst[1], colors, board):
						return True
	return False


# returns whether or not the piece in question is pinned
def pieceIsPinned(board, row, col, colors) -> bool:

	if kingInCheck(board, board[row][col].color, colors):
		return False
	elif board[row][col] == "-":
		return False

	# it is physically impossible for the King to be pinned
	elif board[row][col].type == "K":

		return False
	else:

		piece = board[row][col]
		color = colors[row][col]

		board[row][col], colors[row][col] = "-", "-"
		output = kingInCheck(board, color, colors)

		board[row][col] = piece
		colors[row][col] = color

		return output

# returns whether or not the King is moving into check
def intoCheck(board, rowInit, colInit, rowFinal, colFinal, colors) -> bool:
	if board[rowInit][colInit] != "-":
		if board[rowInit][colInit].type == "K":
			piece = board[rowInit][colInit]
			color = colors[rowInit][colInit]
			displacedPiece = board[rowFinal][colFinal]
			displacedColor = colors[rowFinal][colFinal]

			board[rowFinal][colFinal] = board[rowInit][colInit]
			colors[rowFinal][colFinal] = colors[rowInit][colInit]
			board[rowInit][colInit] = "-"
			colors[rowInit][colInit] = "-"

			output = (kingInCheck(board, colors[rowFinal][colFinal], colors))

			board[rowInit][colInit] = piece
			colors[rowInit][colInit] = color
			board[rowFinal][colFinal] = displacedPiece
			colors[rowFinal][colFinal] = displacedColor

			return output
	return False

# whether or not the move block a possible check
def relieveCheck(board, rowInit, colInit, rowFinal, colFinal, colors) -> bool:

	if kingInCheck(board, colors[rowInit][colInit], colors):

		board[rowFinal][colFinal] = board[rowInit][colInit]
		colors[rowFinal][colFinal] = colors[rowInit][colInit]

		board[rowInit][colInit] = "-"
		colors[rowInit][colInit] = "-"

		return (not kingInCheck(board, colors[rowFinal][colFinal], colors))
			
	return True

# takes a valid input from the user (e.g., will reject "e2 e 4" and will accept "e2 e4")
def takeValidInput(message = "") -> "List[int]":
	while True:
		try:
			moveFrom, moveTo = input(message + "Enter move: ").split()

			rankFrom = 8-(int(moveFrom[1]))
			fileFrom = files[moveFrom[0]]

			rankTo = 8-(int(moveTo[1]))
			fileTo = files[moveTo[0]]

			lst = [rankFrom, fileFrom, rankTo, fileTo]
			return lst
		except ValueError:
			print("invalid input")


# determines the legality of the move and, if it is legal, makes the move and changes the appropriate boards (board, colors, images)
def move(board, colors, turn, whoseTurn, moveRecord, opposite, files, fullName, panel) -> None:
	validInput = takeValidInput()
	rankFrom = validInput[0]
	fileFrom = validInput[1]
	rankTo = validInput[2]
	fileTo = validInput[3]
	
	while ( colors[rankFrom][fileFrom] != whoseTurn[turn%2] or 										# moving a piece that isn't mine
			not board[rankFrom][fileFrom].canMoveTo(rankTo, fileTo, colors, board) or 				# making a physically illegal move
			colors[rankTo][fileTo] == colors[rankFrom][fileFrom] or 								# moving onto my own piece
			pieceIsPinned(copyOf(board), rankFrom, fileFrom, copyOf(colors)) or 					# moving a pinned piece
			intoCheck(copyOf(board), rankFrom, fileFrom, rankTo, fileTo, copyOf(colors)) or 		# King is moving into check
			not relieveCheck(copyOf(board), rankFrom, fileFrom, rankTo, fileTo, copyOf(colors)) ): 	# move does not block a check

		if colors[rankFrom][fileFrom] != whoseTurn[turn%2]:
			errorMessage = "Cannot move a piece that is not your own. "
		elif not board[rankFrom][fileFrom].canMoveTo(rankTo, fileTo, colors, board):
			errorMessage = "Illegal move. "
		elif colors[rankTo][fileTo] == colors[rankFrom][fileFrom]:
			errorMessage = "Cannot move onto your own piece. "
		elif pieceIsPinned(copyOf(board), rankFrom, fileFrom, copyOf(colors)):
			errorMessage = "Piece is pinned. "
		elif intoCheck(copyOf(board), rankFrom, fileFrom, rankTo, fileTo, copyOf(colors)):
			errorMessage = "King cannot move into check. "
		elif not relieveCheck(copyOf(board), rankFrom, fileFrom, rankTo, fileTo, copyOf(colors)):
			errorMessage = "Move does not block the check. "
		
		errorText = Text(Point(955, 200), errorMessage)
		format(errorText, "helvetica", "bold", 20)
		errorText.draw(panel)

		validInput = takeValidInput(errorMessage)
		rankFrom = validInput[0]
		fileFrom = validInput[1]
		rankTo = validInput[2]
		fileTo = validInput[3]

		errorText.undraw()

	board[rankTo][fileTo] = board[rankFrom][fileFrom];
	board[rankFrom][fileFrom] = "-";
	board[rankTo][fileTo].row = rankTo
	board[rankTo][fileTo].col = fileTo

	colors[rankTo][fileTo] = colors[rankFrom][fileFrom];
	colors[rankFrom][fileFrom] = "-";

	updateMoveRecord(moveRecord, board, turn, rankFrom, fileFrom, rankTo, fileTo, files, fullName, opposite)

	# if the move captures, removes the image previously in the new tile
	if images[rankTo][fileTo] is not None:
		images[rankTo][fileTo].undraw()

	# shift the image to its new location
	images[rankFrom][fileFrom].anchor = master[rankTo][fileTo].getCenter()
	images[rankFrom][fileFrom], images[rankTo][fileTo] = images[rankTo][fileTo], images[rankFrom][fileFrom]
	images[rankTo][fileTo].undraw()
	images[rankTo][fileTo].draw(panel)

# updates the record of moves, in convention with chess algebraic notation (mostly)
def updateMoveRecord(moveRecord, board, turn, rankFrom, fileFrom, rankTo, fileTo, files, fullName, opposite) -> None:
	addative = ""
	if gameOver(board, colors, opposite[whoseTurn[turn%2]], turn+1, whoseTurn, panel, fullName, opposite):
		addative = "#"
	elif kingInCheck(board, opposite[whoseTurn[turn%2]], colors):
		addative = "+"


	if turn%2==0:
		moveRecord[0] += str(int(turn/2)+1) + ". " + str(board[rankTo][fileTo]) + list(files.keys())[list(files.values()).index(fileTo)] + "" + str(8-rankTo) + addative + "\t\t"
	else:
		moveRecord[0] += str(board[rankTo][fileTo]) + list(files.keys())[list(files.values()).index(fileTo)] + "" + str(8-rankTo) + addative + "\n"


# determines whether or not a given move is legal
def moveForEndgames(board, colors, turn, whoseTurn, rankFrom, fileFrom, rankTo, fileTo) -> bool:
	
	return ( colors[rankFrom][fileFrom] == whoseTurn[turn%2] and 									# moving a piece that isn't mine
			board[rankFrom][fileFrom].canMoveTo(rankTo, fileTo, colors, board) and 					# making a physically illegal move
			colors[rankTo][fileTo] != colors[rankFrom][fileFrom] and 								# moving onto my own piece
			not pieceIsPinned(copyOf(board), rankFrom, fileFrom, copyOf(colors)) and 				# moving a pinned piece
			not intoCheck(copyOf(board), rankFrom, fileFrom, rankTo, fileTo, copyOf(colors)) and 	# King is moving into check
			relieveCheck(copyOf(board), rankFrom, fileFrom, rankTo, fileTo, copyOf(colors)) ) 		# move does not block a check


# determines whether or not the game is over
def gameOver(board, colors, color, turn, whoseTurn, panel, fullName, opposite, checking=True) -> bool:

	# returns a list of pieces which are all a specified color
	def getColorPieces(board, color) -> "List[Piece]":
		lst = []
		for row in board:
			for piece in row:
				if piece != "-":
					if piece.color == color:
						lst.append(piece)
		return lst

	# checks every square for any possible legal move for a given color
	def noLegalMoves(board, colors, color, turn, whoseTurn) -> bool:
		listOfPieces = getColorPieces(board, color)
		for i in range(0, 8):
			for j in range(0, 8):
				for piece in listOfPieces:
					if moveForEndgames(board, colors, turn, whoseTurn, piece.row, piece.col, i, j):
						return False
		return True
	
	# determines checkmate or stalemate
	if noLegalMoves(board, colors, color, turn, whoseTurn):
		if kingInCheck(board, color, colors):
			if not checking:
				text = Text(Point(955, 350), "Checkmate. " + fullName[opposite[color]] + " wins.")
				format(text, "helvetica", "bold", 30)
				text.draw(panel)
				print("Checkmate. " + fullName[opposite[color]] + " wins.")
		else:
			if not checking:
				text = Text(Point(955, 450), "Stalemate. Game drawn.")
				format(text, "helvetica", "bold", 30)
				text.draw(panel)
				print("Stalemate. Game drawn.")
		return True
	return False


panel = GraphWin("Chess", 1200, 800)

files = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}

board = [
	[Rook(0, 0, "B"), Knight(0, 1, "B"), Bishop(0, 2, "B"), Queen(0, 3, "B"), King(0, 4, "B"), Bishop(0, 5, "B"), Knight(0, 6, "B"), Rook(0, 7, "B")],
	[Pawn(1, 0, "B"), Pawn(1, 1, "B"), Pawn(1, 2, "B"), Pawn(1, 3, "B"), Pawn(1, 4, "B"), Pawn(1, 5, "B"), Pawn(1, 6, "B"), Pawn(1, 7, "B")],
	["-", "-", "-", "-", "-", "-", "-", "-"],
	["-", "-", "-", "-", "-", "-", "-", "-"],
	["-", "-", "-", "-", "-", "-", "-", "-"],
	["-", "-", "-", "-", "-", "-", "-", "-"],
	[Pawn(6, 0, "W"), Pawn(6, 1, "W"), Pawn(6, 2, "W"), Pawn(6, 3, "W"), Pawn(6, 4, "W"), Pawn(6, 5, "W"), Pawn(6, 6, "W"), Pawn(6, 7, "W")],
	[Rook(7, 0, "W"), Knight(7, 1, "W"), Bishop(7, 2, "W"), Queen(7, 3, "W"), King(7, 4, "W"), Bishop(7, 5, "W"), Knight(7, 6, "W"), Rook(7, 7, "W")]
]

colors = [
	["B", "B", "B", "B", "B", "B", "B", "B"],
	["B", "B", "B", "B", "B", "B", "B", "B"],
	["-", "-", "-", "-", "-", "-", "-", "-"],
	["-", "-", "-", "-", "-", "-", "-", "-"],
	["-", "-", "-", "-", "-", "-", "-", "-"],
	["-", "-", "-", "-", "-", "-", "-", "-"],
	["W", "W", "W", "W", "W", "W", "W", "W"],
	["W", "W", "W", "W", "W", "W", "W", "W"]
]


# list with all of the Rectangle objects
master = [[Rectangle(Point(i, j), Point(i+80, j+80)) for i in range(70,631, 80)] for j in range(70, 631, 80)]

images = [
	[Image(master[0][0].getCenter(), "BlackRook.png"), Image(master[0][1].getCenter(), "BlackKnight.png"), Image(master[0][2].getCenter(), "BlackBishop.png"), Image(master[0][3].getCenter(), "BlackQueen.png"), Image(master[0][4].getCenter(), "BlackKing.png"), Image(master[0][5].getCenter(), "BlackBishop.png"), Image(master[0][6].getCenter(), "BlackKnight.png"), Image(master[0][7].getCenter(), "BlackRook.png")],
	[Image(master[1][0].getCenter(), "BlackPawn.png"), Image(master[1][1].getCenter(), "BlackPawn.png"), Image(master[1][2].getCenter(), "BlackPawn.png"), Image(master[1][3].getCenter(), "BlackPawn.png"), Image(master[1][4].getCenter(), "BlackPawn.png"), Image(master[1][5].getCenter(), "BlackPawn.png"), Image(master[1][6].getCenter(), "BlackPawn.png"), Image(master[1][7].getCenter(), "BlackPawn.png")],
	[None, None, None, None, None, None, None, None],
	[None, None, None, None, None, None, None, None],
	[None, None, None, None, None, None, None, None],
	[None, None, None, None, None, None, None, None],
	[Image(master[6][0].getCenter(), "WhitePawn.png"), Image(master[6][1].getCenter(), "WhitePawn.png"), Image(master[6][2].getCenter(), "WhitePawn.png"), Image(master[6][3].getCenter(), "WhitePawn.png"), Image(master[6][4].getCenter(), "WhitePawn.png"), Image(master[6][5].getCenter(), "WhitePawn.png"), Image(master[6][6].getCenter(), "WhitePawn.png"), Image(master[6][7].getCenter(), "WhitePawn.png")],
	[Image(master[7][0].getCenter(), "WhiteRook.png"), Image(master[7][1].getCenter(), "WhiteKnight.png"), Image(master[7][2].getCenter(), "WhiteBishop.png"), Image(master[7][3].getCenter(), "WhiteQueen.png"), Image(master[7][4].getCenter(), "WhiteKing.png"), Image(master[7][5].getCenter(), "WhiteBishop.png"), Image(master[7][6].getCenter(), "WhiteKnight.png"), Image(master[7][7].getCenter(), "WhiteRook.png")]

]

drawBoard(panel, master, images)

# the move record is a list so that I don't have to return anything when I update it in a function
moveRecord = [""]
turn = 0
opposite = {"W":"B", "B":"W"}
whoseTurn = {0:"W", 1:"B"}
fullName = {"W":"White", "B":"Black"}
print()

toMove = Text(Point(955, 100), "Game Begins")
format(toMove, "helvetica", "bold", 30)
toMove.draw(panel)

while (True):
	toMove.undraw()
	toMove.setText(fullName[whoseTurn[turn%2]] + " to move.")
	toMove.draw(panel)

	print(fullName[whoseTurn[turn%2]] + " to move. ")
	move(board, colors, turn, whoseTurn, moveRecord, opposite, files, fullName, panel)
	print()

	if gameOver(board, colors, opposite[whoseTurn[turn%2]], turn+1, whoseTurn, panel, fullName, opposite, False):
		print("\n" + moveRecord[0] + "\n")
		str(input("Press enter to exit. "))
		print()
		break

	else:
		turn+=1