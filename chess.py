

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

    def is_valid_move(self, origin, target):
        # TODO
        # Write a method that returns True if there is one space between the origin and target 
        # AND the target space is not at risk of being taken by a piece of the opposing colour
        return True


class Queen(Piece):
    def __init__(self, color):
        piece_id = color + "Q"
        super().__init__(color, piece_id)

    def is_valid_move(self, origin, target):
        # TODO
        # Write a method that returns True if the path between origin and target is orthonogal or diagonal (straight lines only)
        # AND the spaces on the travelled path are clear
        return True

class Knight(Piece):
    def __init__(self, color):
        piece_id = color + "Kn"
        super().__init__(color, piece_id)

    
    def is_valid_move(self, origin, target):
        # Check if the move is valid for a knight

        # Convert coordinates to indices (0-based)
        origin_col, origin_row = ord(origin[0]) - ord('a'), 8 - int(origin[1])
        target_col, target_row = ord(target[0]) - ord('a'), 8 - int(target[1])

        # Check if the target position is within the bounds of the chessboard
        if target_row < 0 or target_row >= 8 or target_col < 0 or target_col >= 8:
            return False

        # Calculate the absolute differences between the rows and columns
        row_diff = abs(origin_row - target_row)
        col_diff = abs(origin_col - target_col)

        # Knights move in an L-shape pattern: two squares in one direction and one square in a perpendicular direction
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            return True

        return False


class Bishop(Piece):
    def __init__(self, color):
        piece_id = color + "B"
        super().__init__(color, piece_id)

    def is_valid_move(self, origin, target):
        # TODO Write a method that returns True if the move is diagonal AND all spaces on the diagonal path are clear
        return True

class Rook(Piece):
    def __init__(self, color):
        piece_id = color + "R"
        super().__init__(color, piece_id)
    
    def is_valid_move(self, origin, target):
        # Check if the move is valid for a rook

        # Convert coordinates to indices (0-based)
        origin_col, origin_row = ord(origin[0]) - ord('a'), 8 - int(origin[1])
        target_col, target_row = ord(target[0]) - ord('a'), 8 - int(target[1])

        # TODO adjust this code to check the spaces in between origin and target to ensure they are not occupied

        if origin_row == target_row or origin_col == target_col:
            return True

class Pawn(Piece):
    def __init__(self, color):
        piece_id = color + "P"
        super().__init__(color, piece_id)

    def is_valid_move(self, origin, target):
        # Check if the move is valid for a pawn

        # Convert coordinates to indices (0-based)
        origin_col, origin_row = ord(origin[0]) - ord('a'), 8 - int(origin[1])
        target_col, target_row = ord(target[0]) - ord('a'), 8 - int(target[1])

        if self.color == 'W':
            # White pawn moves forward one or two squares on its first move
            if (
                origin_col == target_col
                and origin_row - target_row in (1, 2 if origin_row == 6 else 0)
            ):
                return True
            # White pawn captures diagonally
            if (
                abs(origin_col - target_col) == 1
                and origin_row - target_row == 1
            ):
                return True
        else:
            # Black pawn moves forward one or two squares on its first move
            if (
                origin_col == target_col
                and target_row - origin_row in (1, 2 if origin_row == 1 else 0)
            ):
                return True
            # Black pawn captures diagonally
            if (
                abs(origin_col - target_col) == 1
                and target_row - origin_row == 1
            ):
                return True

        return False


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
        vert_label = "     a     b     c     d     e     f     g     h"
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


class Game:
    def __init__(self):
        self.game_board = Board()
        self.game_board.starting_position()
        self.game_board.print_board()

    def move_piece(self, move, turn):
        # Validate and parse the user's input move
        if not self.is_valid_move_syntax(move):
            print("Invalid move syntax. Please use the format YX to YX.")
            return turn

        origin, target = move.split(" to ")
        if not self.is_valid_coordinate(origin) or not self.is_valid_coordinate(target):
            print("Invalid coordinates. Use letters from a to h and numbers from 1 to 8.")
            return turn

        # Convert coordinates to indices (0-based)
        origin_col, origin_row = ord(origin[0]) - ord('a'), 8 - int(origin[1])
        target_col, target_row = ord(target[0]) - ord('a'), 8 - int(target[1])

        if turn:
            color = 'W'
        else:
            color = 'B'

        # Perform the move logic
        piece = self.game_board.board[origin_row][origin_col]
        if isinstance(piece, Piece) and piece.color == color and piece.is_valid_move(origin, target):
            # Check if the target position is occupied by opposing piece
            if isinstance(self.game_board.board[target_row][target_col], Piece) and piece.color != self.game_board.board[target_row][target_col].color:
                # target piece is taken, removed from board
                self.game_board.board[target_row][target_col] = piece
                self.game_board.board[origin_row][origin_col] = ' '
                self.game_board.print_board()
                return not turn
            elif not isinstance(self.game_board.board[target_row][target_col], Piece):
                # Move the piece to the target position
                self.game_board.board[target_row][target_col] = piece
                self.game_board.board[origin_row][origin_col] = ' '
                self.game_board.print_board()
                return not turn
            else:
                # players cannot remove their own pieces
                print("Invalid move. Target position is occupied.")
                return turn
        else:
            print("No", color, "piece at the specified origin.")
            return turn


    @staticmethod
    def is_valid_move_syntax(move):
        # Implement syntax validation logic here
        # For example, you can check if the move has the format "YX to YX"
        return True

    @staticmethod
    def is_valid_coordinate(coordinate):
        # Implement coordinate validation logic here
        # For example, you can check if the coordinate consists of a letter from 'a' to 'h'
        # followed by a digit from '1' to '8'
        return True
    
    def get_piece_at_origin():
        # TODO 
        # Write a method that accepts one coordinate (e.g., 'a1') and returns the Piece.piece_id on that coordinate on the board.
        # This is just for testing, and could potentially be used for check/checkmate checks
        pass
    
    def run(self):
        white_turn = True
        while True:
            if white_turn:
                user_input = input("White to move. \n>")
            else:
                user_input = input("Black to move. \n>")
            white_turn = game.move_piece(user_input, white_turn)

if __name__ == "__main__":
    game = Game()
    game.run()

