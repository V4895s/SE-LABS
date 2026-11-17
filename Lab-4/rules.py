SIZE = 8


def inside(r, c):
    return 0 <= r < SIZE and 0 <= c < SIZE


def is_king(piece):
    return piece.endswith("K")


def opponent(player):
    return "B" if player == "R" else "R"


def piece_directions(piece):
    if piece == "R":
        return [(-1, -1), (-1, 1)]
    if piece == "B":
        return [(1, -1), (1, 1)]

    # Kings
    return [
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1),
    ]


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end

    if not inside(er, ec):
        return False

    piece = board[sr][sc]

    if piece not in (player, player + "K"):
        return False

    if board[er][ec] != ".":
        return False

    dr = er - sr
    dc = ec - sc

    for rdir, cdir in piece_directions(piece):
        if (dr, dc) == (rdir, cdir):
            return True

    return False


def capture_move(board, player, start, end):
    sr, sc = start
    er, ec = end

    if not inside(er, ec):
        return False

    piece = board[sr][sc]

    if piece not in (player, player + "K"):
        return False

    if board[er][ec] != ".":
        return False

    dr = er - sr
    dc = ec - sc

    for rdir, cdir in piece_directions(piece):

        if (dr, dc) == (2 * rdir, 2 * cdir):

            mr = sr + rdir
            mc = sc + cdir

            if board[mr][mc] in (
                opponent(player),
                opponent(player) + "K",
            ):
                return True

    return False


def player_has_capture(board, player):

    for r in range(SIZE):
        for c in range(SIZE):

            if board[r][c] not in (player, player + "K"):
                continue

            piece = board[r][c]

            for dr, dc in piece_directions(piece):

                er = r + 2 * dr
                ec = c + 2 * dc

                if inside(er, ec):

                    if capture_move(board, player, (r, c), (er, ec)):
                        return True

    return False


def piece_can_capture(board, player, pos):

    r, c = pos

    piece = board[r][c]

    for dr, dc in piece_directions(piece):

        er = r + 2 * dr
        ec = c + 2 * dc

        if inside(er, ec):

            if capture_move(board, player, pos, (er, ec)):
                return True

    return False


def player_has_moves(board, player):

    for r in range(SIZE):
        for c in range(SIZE):

            if board[r][c] not in (player, player + "K"):
                continue

            piece = board[r][c]

            for dr, dc in piece_directions(piece):

                er = r + dr
                ec = c + dc

                if inside(er, ec):

                    if simple_move(board, player, (r, c), (er, ec)):
                        return True

                er = r + 2 * dr
                ec = c + 2 * dc

                if inside(er, ec):

                    if capture_move(board, player, (r, c), (er, ec)):
                        return True

    return False


def promote(board):

    for c in range(SIZE):

        if board[0][c] == "R":
            board[0][c] = "RK"

        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"