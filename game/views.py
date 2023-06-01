from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    if "board" not in request.session:
        request.session["board"] = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]
        request.session["turn"] = ["X"]
        request.session["moves"] = []

    board = request.session["board"]
    turn = request.session["turn"]
    moves = request.session["moves"]

    winnerRows = [
        # Rows
        [(0,0), (0,1), (0,2)],
        [(1,0), (1,1), (1,2)],
        [(2,0), (2,1), (2,2)],
        # Cols
        [(0,0), (1,0), (2,0)],
        [(0,1), (1,1), (2,1)],
        [(0,2), (1,2), (2,2)],
        # Cross
        [(0,0), (1,1), (2,2)],
        [(0,2), (1,1), (2,0)],
    ]
    
    for row in moves:
        board[row[0][0]][row[0][1]] = row[1]

    moves_made = 0
    playerX = []
    playerO = []
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col == "X":
                playerX.append((i,j))
                moves_made += 1
            if col == "O":
                playerO.append((i,j))
                moves_made += 1
    
    for row in winnerRows:
        countX = 0
        countO = 0
        for col in row:
            if col in playerX:
                countX += 1

            if col in playerO:
                countO += 1

        if countX == 3:
            return render(request, 'game/index.html',{
                'message': 'X wins!',
                'board': board,
            })
        
        if countO == 3:
            return render(request, 'game/index.html',{
                'message': 'O wins!',
                'board': board,
            })
        
    if moves_made == 9:
        return render(request, 'game/index.html',{
                'message': 'Tie!',
                'board': board,
            })
        

    return render(request, 'game/index.html', {
        'board': board,
        'turn': turn[-1],
    })


def play(request, row, col):
    turn = request.session["turn"]
    moves = request.session["moves"]

    if turn[-1] == "X":
        moves.append([(row, col), "X"])
        turn.append("O")
    else:
        moves.append([(row, col), "O"])
        turn.append("X")

    request.session.save()

    return redirect('/')


def reset(request):
    request.session.flush()
    return redirect('/')


def undo(request):
    turn = request.session["turn"]
    moves = request.session["moves"]

    if moves:
        turn.pop()
        moves.pop()

    request.session.save()
    return redirect('/')