from board import initial_board, move_piece, SIZE, count_pieces
from rules import (
    simple_move,
    capture_move,
    promote,
    player_has_capture,
    piece_can_capture,
    player_has_moves,
)


class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"

    def print_board(self):
        print("\n   " + " ".join(str(c) for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r}  " + " ".join(row))

    def game_over(self):
        opponent = "B" if self.player == "R" else "R"

        if count_pieces(self.board, opponent) == 0:
            print(f"\n{self.player} wins! Opponent has no pieces.")
            return True

        if not player_has_moves(self.board, opponent):
            print(f"\n{self.player} wins! Opponent has no legal moves.")
            return True

        return False

    def run(self):
        print("=" * 45)
        print("        CHECKERS GAME")
        print("SRN : PES2UG24CS581")
        print("Enter moves as: sr sc er ec")
        print("Example: 5 0 4 1")
        print("Type 'q' to quit.")
        print("=" * 45)

        while True:
            self.print_board()

            raw = input(f"{self.player}> ").strip().lower()

            if raw == "q":
                print("\nGame ended.")
                print("SRN: PES2UG24CS581")
                return

            raw = raw.split()

            if len(raw) != 4:
                print("Enter four coordinates.")
                continue

            try:
                sr, sc, er, ec = map(int, raw)
            except ValueError:
                print("Coordinates must be numbers.")
                continue

            if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
                print("Outside board.")
                continue

            piece = self.board[sr][sc]

            if piece not in (self.player, self.player + "K"):
                print("That is not your piece.")
                continue

            start = (sr, sc)
            end = (er, ec)

            must_capture = player_has_capture(self.board, self.player)

            if must_capture:

                if not capture_move(self.board, self.player, start, end):
                    print("Capture is mandatory.")
                    continue

                move_piece(self.board, start, end)
                print("Capture!")

                promote(self.board)

                while piece_can_capture(self.board, self.player, end):

                    self.print_board()
                    print("Multi-capture available.")

                    raw = input("Continue capture (sr sc er ec): ").split()

                    if len(raw) != 4:
                        print("Enter four coordinates.")
                        continue

                    try:
                        nsr, nsc, ner, nec = map(int, raw)
                    except ValueError:
                        print("Coordinates must be numbers.")
                        continue

                    if (nsr, nsc) != end:
                        print("Continue with the same piece.")
                        continue

                    if not capture_move(
                        self.board,
                        self.player,
                        (nsr, nsc),
                        (ner, nec),
                    ):
                        print("Invalid capture.")
                        continue

                    move_piece(
                        self.board,
                        (nsr, nsc),
                        (ner, nec),
                    )

                    end = (ner, nec)
                    promote(self.board)

            else:

                if not simple_move(self.board, self.player, start, end):
                    print("Invalid move.")
                    continue

                move_piece(self.board, start, end)
                print("Move completed.")

                promote(self.board)

            if self.game_over():
                self.print_board()
                print("\nSRN: PES2UG24CS581")
                return

            self.player = "B" if self.player == "R" else "R"
