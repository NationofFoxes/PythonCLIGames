

class Piece:
    def __init__(self, color):
        self.color = color

    def move(self, origin, target):
        # Check if the move is valid according to the rules of the specific piece
        if self.is_valid_move(origin, target):
            # Implement the actual move logic here
            pass
        else:
            print("Invalid move!")

    def is_valid_move(self, origin, target):
        # Implement the rules for valid moves for each piece
        pass

    
class King(Piece):
    pass

class Queen(Piece):
    pass

class Knight(Piece):
    pass

class Bishop(Piece):
    pass

class Rook(Piece):
    pass

class Pawn(Piece):
    pass

class Board:
    def __init__(self):
        # Create an 8x8 chessboard as a list of lists
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        

    def print_board(self):
        # Print the chessboard with increased spacing and dividers
        print()
        print("    a   b   c   d   e   f   g   h")
        divider = "  +---+---+---+---+---+---+---+---+"
        print(divider)
        for i, row in enumerate(self.board):
            if i > 0:
                print(divider)
            print(8 - i, end=' ')  # Print the row number
            for piece in row:
                print(f"| {piece} ", end='')
            print(f"| {8 - i}")  # Print the row number again
        print(divider)
        print("    a   b   c   d   e   f   g   h")

    def get_piece():
        pass

class Game:
    def play():
        chessboard = Board()
        chessboard.print_board()


if __name__ == "__main__":
    Game.play()

