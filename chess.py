

class Piece:
    def __init__(self, color, id):
        self.color = color
        self.id = id  # Piece ID ('K', 'Q', 'R', 'Kn', 'B', 'P')

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
    def __init__(self, color):
        piece_id = color + "K"
        super().__init__(color, piece_id)


class Queen(Piece):
    def __init__(self, color):
        piece_id = color + "Q"
        super().__init__(color, piece_id)

class Knight(Piece):
    def __init__(self, color):
        piece_id = color + "Kn"
        super().__init__(color, piece_id)

class Bishop(Piece):
    def __init__(self, color):
        piece_id = color + "B"
        super().__init__(color, piece_id)

class Rook(Piece):
    def __init__(self, color):
        piece_id = color + "R"
        super().__init__(color, piece_id)

class Pawn(Piece):
    def __init__(self, color):
        piece_id = color + "P"
        super().__init__(color, piece_id)

class Board:
    def __init__(self):
        # Create an 8x8 chessboard as a list of lists
        self.board = [[' ' for _ in range(8)] for _ in range(8)]

    def starting_position(self):
        # Place white pieces in the first two rows
        self.board[0] = [
            Rook('B'), Knight('B'), Bishop('B'), Queen('B'), King('B'), Bishop('B'), Knight('B'), Rook('B')
        ]
        self.board[1] = [Pawn('B') for _ in range(8)]

        # Place black pieces in the last two rows
        self.board[6] = [Pawn('W') for _ in range(8)]
        self.board[7] = [
            Rook('W'), Knight('W'), Bishop('W'), Queen('W'), King('W'), Bishop('W'), Knight('W'), Rook('W')
        ]

    def print_board(self):
        # Print the chessboard with fixed-width squares, labels, and dividers
        print()
        vert_label = "    a     b     c     d     e     f     g     h"
        divider = "  +-----+-----+-----+-----+-----+-----+-----+-----+"
        print(vert_label)
        print(divider)
        for i, row in enumerate(self.board):
            if i > 0:
                print(divider)
            print(8 - i, end=' ')  # Print the row number
            for piece in row:
                if isinstance(piece, Piece):
                    # Use an f-string with a fixed width (5 characters) for each square
                    print(f"|{piece.id:^5}", end='')  # ^5 centers the text within a 5-character width
                else:
                    print("|     ", end='')  # Print an empty space with the same width
            print(f"| {8 - i}")  # Print the row number again
        print(divider)
        print(vert_label)


# Example usage:
if __name__ == "__main__":
    game_board = Board()
    game_board.starting_position()
    game_board.print_board()


