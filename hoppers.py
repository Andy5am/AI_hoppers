#Andy Castillo 18040
#IA Hoppers


victory = 0
coords=['0','1','2','3','4','5','6','7','8','9']
board=[
    ['X','X','X','X','X','-','-','-','-','-'],
    ['X','X','X','X','-','-','-','-','-','-'],
    ['X','X','X','-','-','-','-','-','-','-'],
    ['X','X','-','-','-','-','-','-','-','-'],
    ['X','-','-','-','-','-','-','-','-','-'],
    ['-','-','-','-','-','-','-','-','-','O'],
    ['-','-','-','-','-','-','-','-','O','O'],
    ['-','-','-','-','-','-','-','O','O','O'],
    ['-','-','-','-','-','-','O','O','O','O'],
    ['-','-','-','-','-','O','O','O','O','O'],
]

def print_board(board):
    string='  '
    for coord in coords:
        string+=coord+' '
    print(string+'\n')
    counter = 0
    for line in board:
        string=''
        for cell in line:
            string+=cell+' '
        print(str(counter)+' '+string)
        counter+=1

def turn(board, turn):
    if(turn):
        player_char="X"
    else:
        player_char="O"
    empty_char="-"
    if(not turn):
        initial_board = board
        temp_board = board
    # Jugadas se ingresa Y-X,Y-X,...
        play = input("Ingrese su jugada: ")
        #separar los saltos
        play = play.replace(" ","")
        jump_list = play.split(',')
        print(jump_list)

        #Quitar la posicion inicial de la lista
        start_pos=jump_list.pop(0)
        start_X = int(start_pos.split("-")[0])
        start_Y = int(start_pos.split("-")[1])

        #separar coordenadas de cada salto
        for jump in  jump_list:
            jump_coordY = int(jump.split("-")[1])
            jump_coordX = int(jump.split("-")[0])

            valid = validate_jump(start_X,start_Y,jump_coordX,jump_coordY,board)
            if (valid):
                temp_board[start_X][start_Y] = empty_char
                temp_board[jump_coordX][jump_coordY] = player_char

                start_X = jump_coordX
                start_Y = jump_coordY
            else:
                print("Jugada invalida")
                board=initial_board
                return(False)
        
        board=temp_board
    else:
        move = minimax(board, 1, turn)[1]
        start_pos = move[0]
        final_pos = move[1]
        board[int(start_pos.split("-")[0])][int(start_pos.split("-")[1])] = empty_char
        board[int(final_pos.split("-")[0])][int(final_pos.split("-")[1])] = player_char
        print(move)
        return(True)

    return(True)


def validate_jump(initX, initY, finalX, finalY, board):
    valid = False

    if(player_turn):
        player_char="X"
    else:
        player_char="O"
    empty_char="-"

    #Verificar que haya pieza ahi
    init_cell = board[initX][initY]
    final_cell = board[finalX][finalY]

    if(init_cell==player_char and final_cell==empty_char):
        #validar el salto
        difX = initX-finalX
        difY = initY-finalY
        
        #Cuando es mover al lado
        if((difX==0 and difY==1) or (difX==-1 and difY==1) or (difX==1 and difY==1) or (difX==1 and difY==0) or (difX==-1 and difY==0) or (difX==0 and difY==-1) or (difX==1 and difY==-1) or (difX==-1 and difY==-1)):
            valid=True
            return(valid)
        elif((difX==0 and difY==2) or (difX==-2 and difY==2) or (difX==2 and difY==2) or (difX==2 and difY==0) or (difX==-2 and difY==0) or (difX==0 and difY==-2) or (difX==2 and difY==-2) or (difX==-2 and difY==-2)):
            #cuando salta una ficha
            if(difX==2):
                difX = 1
            elif(difX==-2):
                difX = -1
            if(difY==2):
                difY = 1
            elif(difY==-2):
                difY = -1
            
            #Verificar que la de en medio este ocupada
            middleX = finalX+difX
            middleY = finalY+difY
            middle_Cell = board[middleX][middleY]
            if(middle_Cell!=empty_char):
                valid = True
                return(valid)
            else:
                return(valid)
        else:
            return(valid)
    else:
        #no es valida la jugada
        return(valid)

def validate_win(board):
    x_counter_top = 0
    o_counter_top = 0
    x_counter_bottom = 0
    o_counter_bottom = 0
    for i in range(10):
        if (i<5):
            for j in range(5-i):
                if(board[i][j]=="X"):
                    x_counter_top+=1
                elif(board[i][j]=="O"):
                    o_counter_top+=1
        if (i>4):
            for k in range(14-i,10):
                if(board[i][k]=="X"):
                    x_counter_bottom+=1
                elif(board[i][k]=="O"):
                    o_counter_bottom+=1
    if(x_counter_top+o_counter_top==15 and x_counter_top<15):
        return(1)
    elif(x_counter_bottom+o_counter_bottom==15 and o_counter_bottom<15):
        return(-1)
    else:
        return(0)

def get_possible_moves(board, turn):
    if(turn):
        player_char="X"
    else:
        player_char="O"
    moves=[]
    for i in range(len(board)):
        for j in range(len(board)):
            if (board[i][j]==player_char):
                coords = get_around_coords(i, j)
                for coord in coords:
                    if(validate_jump(i,j,int(coord.split("-")[0]),int(coord.split("-")[1]),board)):
                        move=[]
                        move.append(str(i)+'-'+str(j))
                        move.append(coord)
                        moves.append(move)
    return moves


def get_around_coords(x, y):
    if(x==0):
        if(y==0):
            return([str(x+1)+'-'+str(y), str(x)+'-'+str(y+1), str(x+1)+'-'+str(y+1), str(x+2)+'-'+str(y), str(x)+'-'+str(y+2), str(x+2)+'-'+str(y+2)])
        elif(y==9):
            return([str(x+1)+'-'+str(y), str(x)+'-'+str(y-1), str(x+1)+'-'+str(y-1), str(x+2)+'-'+str(y), str(x)+'-'+str(y-2), str(x+2)+'-'+str(y-2)])
        elif(y==1):
            return([str(x+1)+'-'+str(y), str(x)+'-'+str(y-1), str(x+1)+'-'+str(y-1), str(x)+'-'+str(y+1), str(x+1)+'-'+str(y+1), str(x+2)+'-'+str(y), str(x)+'-'+str(y+2), str(x+2)+'-'+str(y+2)])
        elif(y==8):
            return([str(x+1)+'-'+str(y), str(x)+'-'+str(y-1), str(x+1)+'-'+str(y-1), str(x)+'-'+str(y+1), str(x+1)+'-'+str(y+1), str(x+2)+'-'+str(y), str(x)+'-'+str(y-2), str(x+2)+'-'+str(y-2)])
        else:
            return([str(x+1)+'-'+str(y), str(x)+'-'+str(y-1), str(x+1)+'-'+str(y-1), str(x)+'-'+str(y+1), str(x+1)+'-'+str(y+1), str(x+2)+'-'+str(y), str(x)+'-'+str(y-2), str(x+2)+'-'+str(y-2), str(x)+'-'+str(y+2), str(x+2)+'-'+str(y+2)])
    elif(x==9):
        if(y==0):
            return([str(x-1)+'-'+str(y), str(x)+'-'+str(y+1), str(x-1)+'-'+str(y+1), str(x-2)+'-'+str(y), str(x)+'-'+str(y+2), str(x-2)+'-'+str(y+2)])
        elif(y==9):
            return([str(x-1)+'-'+str(y), str(x)+'-'+str(y-1), str(x-1)+'-'+str(y-1), str(x-2)+'-'+str(y), str(x)+'-'+str(y-2), str(x-2)+'-'+str(y-2)])
        elif(y==8):
            return([str(x-1)+'-'+str(y), str(x)+'-'+str(y-1), str(x-1)+'-'+str(y-1), str(x)+'-'+str(y+1), str(x-1)+'-'+str(y+1), str(x-2)+'-'+str(y), str(x)+'-'+str(y-2), str(x-2)+'-'+str(y-2)])
        elif(y==1):
            return([str(x-1)+'-'+str(y), str(x)+'-'+str(y-1), str(x-1)+'-'+str(y-1), str(x)+'-'+str(y+1), str(x-1)+'-'+str(y+1), str(x-2)+'-'+str(y), str(x)+'-'+str(y+2), str(x-2)+'-'+str(y+2)])
        else:
            return([str(x-1)+'-'+str(y), str(x)+'-'+str(y-1), str(x-1)+'-'+str(y-1), str(x)+'-'+str(y+1), str(x-1)+'-'+str(y+1), str(x-2)+'-'+str(y), str(x)+'-'+str(y-2), str(x-2)+'-'+str(y-2), str(x)+'-'+str(y+2), str(x-2)+'-'+str(y+2)])
    elif(x==1):
        if(y==1):
            return([str(x+1)+'-'+str(y), str(x+1)+'-'+str(y+1), str(x+1)+'-'+str(y-1), str(x)+'-'+str(y-1), str(x)+'-'+str(y+1), str(x-1)+'-'+str(y), str(x-1)+'-'+str(y+1), str(x-1)+'-'+str(y-1), str(x+2)+'-'+str(y), str(x+2)+'-'+str(y+2), str(x)+'-'+str(y+2)])
        elif(y==8):
            return([str(x+1)+'-'+str(y), str(x+1)+'-'+str(y+1), str(x+1)+'-'+str(y-1), str(x)+'-'+str(y-1), str(x)+'-'+str(y+1), str(x-1)+'-'+str(y), str(x-1)+'-'+str(y+1), str(x-1)+'-'+str(y-1), str(x+2)+'-'+str(y), str(x+2)+'-'+str(y-2), str(x)+'-'+str(y-2)])
        elif(y==0):
            return([str(x+1)+'-'+str(y), str(x)+'-'+str(y+1), str(x+1)+'-'+str(y+1), str(x+2)+'-'+str(y), str(x)+'-'+str(y+2), str(x+2)+'-'+str(y+2)])
        elif(y==9):
            return([str(x+1)+'-'+str(y), str(x)+'-'+str(y-1), str(x+1)+'-'+str(y-1), str(x+2)+'-'+str(y), str(x)+'-'+str(y-2), str(x+2)+'-'+str(y-2)])
        else:
            return([str(x+1)+'-'+str(y), str(x+1)+'-'+str(y+1), str(x+1)+'-'+str(y-1), str(x)+'-'+str(y-1), str(x)+'-'+str(y+1), str(x-1)+'-'+str(y), str(x-1)+'-'+str(y+1), str(x-1)+'-'+str(y-1), str(x+2)+'-'+str(y), str(x+2)+'-'+str(y+2), str(x+2)+'-'+str(y-2), str(x)+'-'+str(y-2), str(x)+'-'+str(y+2)])
    elif(x==8):
        if(y==1):
            return([str(x+1)+'-'+str(y), str(x+1)+'-'+str(y+1), str(x+1)+'-'+str(y-1), str(x)+'-'+str(y-1), str(x)+'-'+str(y+1), str(x-1)+'-'+str(y), str(x-1)+'-'+str(y+1), str(x-1)+'-'+str(y-1), str(x)+'-'+str(y+2), str(x-2)+'-'+str(y), str(x-2)+'-'+str(y+2)])
        elif(y==8):
            return([str(x+1)+'-'+str(y), str(x+1)+'-'+str(y+1), str(x+1)+'-'+str(y-1), str(x)+'-'+str(y-1), str(x)+'-'+str(y+1), str(x-1)+'-'+str(y), str(x-1)+'-'+str(y+1), str(x-1)+'-'+str(y-1), str(x)+'-'+str(y-2), str(x-2)+'-'+str(y), str(x-2)+'-'+str(y-2)])
        elif(y==0):
            return([str(x-1)+'-'+str(y), str(x)+'-'+str(y+1), str(x-1)+'-'+str(y+1), str(x-2)+'-'+str(y), str(x)+'-'+str(y+2), str(x-2)+'-'+str(y+2)])
        elif(y==9):
            return([str(x-1)+'-'+str(y), str(x)+'-'+str(y-1), str(x-1)+'-'+str(y-1), str(x-2)+'-'+str(y), str(x)+'-'+str(y-2), str(x-2)+'-'+str(y-2)])
        else:
            return([str(x+1)+'-'+str(y), str(x+1)+'-'+str(y+1), str(x+1)+'-'+str(y-1), str(x)+'-'+str(y-1), str(x)+'-'+str(y+1), str(x-1)+'-'+str(y), str(x-1)+'-'+str(y+1), str(x-1)+'-'+str(y-1), str(x)+'-'+str(y-2), str(x)+'-'+str(y+2), str(x-2)+'-'+str(y), str(x-2)+'-'+str(y+2), str(x-2)+'-'+str(y-2)])
    else:
        if(y==0):
            return([str(x-1)+'-'+str(y), str(x)+'-'+str(y+1), str(x-1)+'-'+str(y+1), str(x+1)+'-'+str(y), str(x+1)+'-'+str(y+1), str(x-2)+'-'+str(y), str(x)+'-'+str(y+2), str(x-2)+'-'+str(y+2), str(x+2)+'-'+str(y), str(x+2)+'-'+str(y+2)])
        elif(y==9):
            return([str(x-1)+'-'+str(y), str(x)+'-'+str(y-1), str(x-1)+'-'+str(y-1), str(x+1)+'-'+str(y), str(x+1)+'-'+str(y-1), str(x-2)+'-'+str(y), str(x)+'-'+str(y-2), str(x-2)+'-'+str(y-2), str(x+2)+'-'+str(y), str(x+2)+'-'+str(y-2)])
        elif(y==1):
            return([str(x+1)+'-'+str(y), str(x+1)+'-'+str(y+1), str(x+1)+'-'+str(y-1), str(x)+'-'+str(y-1), str(x)+'-'+str(y+1), str(x-1)+'-'+str(y), str(x-1)+'-'+str(y+1), str(x-1)+'-'+str(y-1), str(x+2)+'-'+str(y), str(x+2)+'-'+str(y+2), str(x)+'-'+str(y+2), str(x-2)+'-'+str(y), str(x-2)+'-'+str(y+2)])
        elif(y==8):
            return([str(x+1)+'-'+str(y), str(x+1)+'-'+str(y+1), str(x+1)+'-'+str(y-1), str(x)+'-'+str(y-1), str(x)+'-'+str(y+1), str(x-1)+'-'+str(y), str(x-1)+'-'+str(y+1), str(x-1)+'-'+str(y-1), str(x+2)+'-'+str(y), str(x+2)+'-'+str(y-2), str(x)+'-'+str(y-2), str(x-2)+'-'+str(y), str(x-2)+'-'+str(y-2)])
        else:
            return([str(x+1)+'-'+str(y), str(x+1)+'-'+str(y+1), str(x+1)+'-'+str(y-1), str(x)+'-'+str(y-1), str(x)+'-'+str(y+1), str(x-1)+'-'+str(y), str(x-1)+'-'+str(y+1), str(x-1)+'-'+str(y-1), str(x+2)+'-'+str(y), str(x+2)+'-'+str(y+2), str(x+2)+'-'+str(y-2), str(x)+'-'+str(y-2), str(x)+'-'+str(y+2), str(x-2)+'-'+str(y), str(x-2)+'-'+str(y+2), str(x-2)+'-'+str(y-2)])

def utility(board, turn):
    x_counter_top = 0
    o_counter_top = 0
    x_counter_bottom = 0
    o_counter_bottom = 0
    up_left_counter = 0
    down_rigth_counter = 0
    for i in range(10):
        if (i<5):
            for j in range(5-i):
                if(board[i][j]=="X"):
                    x_counter_top+=1
                elif(board[i][j]=="O"):
                    o_counter_top+=1
        if (i>4):
            for k in range(14-i,10):
                if(board[i][k]=="X"):
                    x_counter_bottom+=1
                elif(board[i][k]=="O"):
                    o_counter_bottom+=1
    for i in range(10):
        if (i<5):
            for j in range(5-i,10):
                if(board[i][j]=="X"):
                    down_rigth_counter+= (9-i+9-j)
                if(board[i][j]=="O"):
                    up_left_counter+= (i+j)
        if (i>4):
            for k in range(0,14-i):
                if(board[i][k]=="X"):
                    down_rigth_counter+= (9-i+9-k)
                if(board[i][k]=="O"):
                    up_left_counter+= (i+k)
                    
    return(x_counter_bottom**2 + o_counter_bottom**2 - x_counter_top**2 - o_counter_top**2 + up_left_counter - down_rigth_counter)

    
def minimax(board, depth, turn, alpha=float('-inf'), beta=float('inf')):
    best_move = None

    if (validate_win(board) or depth == 0):
        return [utility(board, turn), None]

    if (turn):
        best_value = float('-inf')
        other_player = not turn
    else:
        best_value = float('inf')
        other_player = turn

    if (turn):
        player = turn
    else:
        player = other_player

    moves = get_possible_moves(board, player)


    for move in moves :
        
        start_pos = move[0]
        final_pos = move[1]

        player_char = board[int(start_pos.split("-")[0])][int(start_pos.split("-")[1])]

        board[int(start_pos.split("-")[0])][int(start_pos.split("-")[1])] = "-"
        board[int(final_pos.split("-")[0])][int(final_pos.split("-")[1])] = player_char

        value, movement = minimax(board, depth -1, other_player, alpha, beta)

        board[int(start_pos.split("-")[0])][int(start_pos.split("-")[1])] = player_char
        board[int(final_pos.split("-")[0])][int(final_pos.split("-")[1])] = "-"

        if (turn):
            if value > best_value:
                best_move = move
                best_value = value
                alpha = max(alpha, best_value)
        else:
            if value < best_value:
                best_move = move
                best_value = value
                beta = min(beta, best_value)

        if (turn and alpha > beta) or (not turn and alpha < beta):
            return [best_value, best_move]

    return [best_value, best_move]


player_turn = True
print_board(board)
while(victory==0):
    if player_turn:
        print("Turno IA: ")
    else:
        print("Turno jugador 2: ")
    played = turn(board,player_turn)
    if (played):
        player_turn = not player_turn
        print_board(board)
        victory = validate_win(board)

print(victory)