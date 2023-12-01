import random
import time
import pygame
import sys
import chess

board = chess.Board()

WIDTH = 650

#WIN = pygame.display.set_mode((WIDTH, WIDTH))
#bpygame.display.set_caption("Chess")
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)

class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(col * width)
        self.y = int(row * width)
        self.colour = WHITE

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / 8, WIDTH / 8))

    def setup(self, WIN,boardM):
        
        if boardM[self.row][self.col] != "None":
                WIN.blit(pygame.image.load(self.getImage(boardM[self.row][self.col])), (self.x, self.y))
    
    def getImage(self,letter):
        if letter == 'r':
            return "PiezasM/torre_N.png"
        if letter == 'n':
            return "PiezasM/Caballo_N.png"
        if letter == 'b':
            return "PiezasM/Alfil_N.png"
        if letter == 'q':
            return "PiezasM/Reyna_N.png"
        if letter == 'k':
            return "PiezasM/Rey_N.png"
        if letter == 'p':
            return "PiezasM/Peon_N.png"
        
        if letter == 'R':
            return "PiezasM/Torre.png"
        if letter == 'N':
            return "PiezasM/caballo.png"
        if letter == 'B':
            return "PiezasM/Alfil.png"
        if letter == 'Q':
            return "PiezasM/Reyna.png"
        if letter == 'K':
            return "PiezasM/Rey.png"
        if letter == 'P':
            return "PiezasM/peon.png"

        return ""

        """
        For now it is drawing a rectangle but eventually we are going to need it
        to use blit to draw the chess pieces instead
        """

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap)
            grid[i].append(node)
            if (i+j)%2 ==1:
                grid[i][j].colour = GREY
    return grid

def draw_grid(win, rows, width):
    gap = width // 8
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

def update_display(win, grid, rows, width):
    boardM = []
    for i in range(8):
        arr = [str(board.piece_at(chess.Square((i*8+j)))) for j in range(8)]
        boardM.insert(0,arr)

    for row in grid:
        for spot in row:
            spot.draw(win)
            spot.setup(win,boardM)
    draw_grid(win, rows, width)
    pygame.display.update()

def jugada(pos, WIDTH): #Regresa la posicion pero en jugadas g3, h5 etc
    interval = WIDTH / 8 #81.25
    x,y = pos
    rows = x // interval
    columns = y // interval
    x,y = int(rows), int(columns)
    pos = "" + ['a','b','c','d','e','f','g','h'][x] + f"{8-y}"
    return pos

def cuadros(pos, WIDTH):  #regresa la posicion de los cuadrados
    interval = WIDTH / 8 #81.25
    x,y = pos
    rows = x // interval
    columns = y // interval
    pos = int(rows), int(columns)
    return pos

def descomponer(movi):
    let = ['a','b','c','d','e','f','g','h']
    num = ['1','2','3','4','5','6','7','8']

    for i in range(8):
        if movi[0] == let[i]:
            x1=i
        if movi[1] == num[i]:
            y1=7-i
        if movi[2] == let[i]:
            x2=i
        if movi[3] == num[i]:
            y2=7-i

    return x1,y1,x2,y2

def TurMaqN(boardCopy):
    max_value = -99999
    movement = ""
    legal_moves = [str(mov) for mov in boardCopy.legal_moves]
    for move in legal_moves:
        result = pieces_heuristic(boardCopy.copy(), move)
        if result > max_value:
            movement = move
            max_value = result
    return movement

def TurMaqB(boardCopy):
    max_value = 99999
    movement = ""
    legal_moves = [str(mov) for mov in boardCopy.legal_moves]
    for move in legal_moves:
        result = pieces_heuristic(boardCopy.copy(), move)
        if result < max_value:
            movement = move
            max_value = result
    return movement

def pieces_heuristic(boardCopy, movement):
    value = 0
    boardCopy.push(chess.Move.from_uci(movement))
    for i in range(8):
        for j in range(8):
            piece = str(boardCopy.piece_at(chess.Square((i * 8 + j))))
            value += getValueOfPiece(piece)
    return value

def evaluateBoard(boardCopy,movement):
    value = 0
    boardCopy.push(chess.Move.from_uci(movement))
    for i in range(8):
        for j in range(8):
            piece = str(boardCopy.piece_at(chess.Square((i*8+j))))
            value += getValueOfPiece(piece)
    return value

def getValueOfPiece(letter):
        if letter == 'r':
            return 50
        if letter == 'n':
            return 30
        if letter == 'b':
            return 30
        if letter == 'q':
            return 90
        if letter == 'k':
            return 900
        if letter == 'p':
            return 10
        
        if letter == 'R':
            return -50
        if letter == 'N':
            return -30
        if letter == 'B':
            return -30
        if letter == 'Q':
            return -90
        if letter == 'K':
            return -900
        if letter == 'P':
            return -10

        return 0

def minMaxMax(boardCopy,movement,depth):
    if depth < 0:
        value = evaluateBoard(boardCopy,movement)
        return {"Value":value,"Movement":movement}
    
    boardCopy.push(chess.Move.from_uci(movement))
    max = -99999
    legal_moves = [str(mov) for mov in boardCopy.legal_moves]
    result = {}
    for move in legal_moves:
       evaluation = minMaxMin(boardCopy.copy(),move,depth-1)
       if  evaluation["Value"] > max:
            max = evaluation["Value"]
            result = evaluation
    return result

def minMaxMin(boardCopy,movement,depth):
    if depth < 0:
        value = evaluateBoard(boardCopy,movement)
        return {"Value":value,"Movement":movement}
    
    boardCopy.push(chess.Move.from_uci(movement))
    min = 99999
    legal_moves = [str(mov) for mov in boardCopy.legal_moves]
    result = {}
    for move in legal_moves:
       evaluation = minMaxMax(boardCopy.copy(),move,depth-1)
       if  evaluation["Value"] < min:
            min = evaluation["Value"]
            result = evaluation
    return result

def promotion_menu():
    font = pygame.font.Font(None, 36)
    text = font.render("Promote Pawn:", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, WIDTH // 2 - 50))

    queen_button = pygame.Rect(WIDTH // 2 - 50, WIDTH // 2, 100, 50)
    queen_text = font.render("Queen", True, BLACK)
    queen_text_rect = queen_text.get_rect(center=queen_button.center)

    knight_button = pygame.Rect(WIDTH // 2 - 50, WIDTH // 2 + 60, 100, 50)
    knight_text = font.render("Knight", True, BLACK)
    knight_text_rect = knight_text.get_rect(center=knight_button.center)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if queen_button.collidepoint(event.pos):
                    return 'q'
                elif knight_button.collidepoint(event.pos):
                    return 'n'

        WIN.fill(GREY)
        pygame.draw.rect(WIN, WHITE, queen_button)
        pygame.draw.rect(WIN, WHITE, knight_button)
        WIN.blit(text, text_rect)
        WIN.blit(queen_text, queen_text_rect)
        WIN.blit(knight_text, knight_text_rect)
        pygame.display.flip()

def PlayB(WIN, WIDTH):
    game = True
    movement = ""
    grid = make_grid(8, WIDTH)
    xa1 = xa2 = xm1 = xm2 = 0
    ya1 = ya2 = ym1 = ym2 = 7
    col1 = col2 = col3 = col4 =GREY
    i=0
    while game: #Que el juego siga hasta que alguien pierda
        pygame.time.delay(50) ##por precaucion
        for event in pygame.event.get(): #se termina el programa si cierran la ventana
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                node = jugada(pygame.mouse.get_pos(), WIDTH)
                if movement == "":
                    piece = board.piece_at(chess.Square(chess.parse_square(node)))
                    if piece != None and str(piece).isupper(): #Pregunta si la casilla que clicleo es una pieza valida
                        movement = node
                        grid[ya1][xa1].colour = col1
                        grid[ya2][xa2].colour = col2
                        grid[ym1][xm1].colour = col3
                        grid[ym2][xm2].colour = col4
                        xa1,ya1 = cuadros(pygame.mouse.get_pos(), WIDTH)
                        col1=grid[ya1][xa1].colour
                        grid[ya1][xa1].colour = BLUE
                    else:
                        print("Esta no es tu pieza")
                else:
                    movement += node
                    if not chess.Move.from_uci(movement) in board.legal_moves:
                        grid[ya1][xa1].colour = col1
                        print("Movieminto no valido")
                        movement = ""
                    else:
                        board.push(chess.Move.from_uci(movement))
                        xa2,ya2 = cuadros(pygame.mouse.get_pos(), WIDTH)
                        col2=grid[ya2][xa2].colour
                        grid[ya2][xa2].colour = BLUE
                        movement = ""

                        #Turno de la maquina
                        movement = TurMaqN(board.copy())
                        board.push(chess.Move.from_uci(movement))
                        xm1,ym1,xm2,ym2 = descomponer(movement)
                        col3=grid[ym1][xm1].colour
                        if (xa2 == xm2) and (ya2 == ym2):
                            col4 = col2
                        else:
                            col4 = grid[ym2][xm2].colour
                        grid[ym1][xm1].colour = YELLOW
                        grid[ym2][xm2].colour = YELLOW
                        movement = ""
                        print("Tu movimiento: ",board.move_stack[i])   #Muestra la lista de movimientos
                        print("Movimiento maquina: ",board.move_stack[i+1])
                        print("------------------------------") 
                        i += 2
                        
            update_display(WIN, grid, 8, WIDTH)
            if board.is_checkmate():
                if board.turn == chess.WHITE:
                    print("Ganaron las negras")
                elif board.turn == chess.BLACK:
                    print("Ganaron las Blancas")
                game = False
            elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves():
                print("Empate")
                game = False
        
def PlayN(WIN, WIDTH):
    movement = ""
    game = True
    grid = make_grid(8, WIDTH)
    xa1 = xa2 = xm1 = xm2 = 0
    ya1 = ya2 = ym1 = ym2 = 7
    col1 = col2 = col3 = col4 =GREY
    swich=0
    i = 0
    while game:
        pygame.time.delay(50) ##por precaucion
        for event in pygame.event.get(): #se termina el programa si cierran la ventana
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if swich == 0:
                grid[ya1][xa1].colour = col1
                grid[ya2][xa2].colour = col2
                grid[ym2][xm2].colour = col4
                grid[ym1][xm1].colour = col3
                #Turno de la maquina
                movement = TurMaqB(board.copy())
                board.push(chess.Move.from_uci(movement))
                xm1,ym1,xm2,ym2 = descomponer(movement)
                col3=grid[ym1][xm1].colour
                col4=grid[ym2][xm2].colour
                grid[ym2][xm2].colour = YELLOW
                grid[ym1][xm1].colour = YELLOW
                print("Movimiento maquina: ",board.move_stack[i])
                print("------------------------------") 
                i += 2
                movement = ""
                swich = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                node = jugada(pygame.mouse.get_pos(), WIDTH)
                if movement == "":
                    piece = board.piece_at(chess.Square(chess.parse_square(node)))
                    if piece != None and str(piece).islower(): #Pregunta si la casilla que clicleo es una pieza valida
                        movement = node
                        xa1,ya1 = cuadros(pygame.mouse.get_pos(), WIDTH)
                        col1=grid[ya1][xa1].colour
                        grid[ya1][xa1].colour = BLUE
                    else:
                        print("Esa no es una de tus piezas")
                else:
                    movement += node
                    if not chess.Move.from_uci(movement) in board.legal_moves:
                        grid[ya1][xa1].colour = col1
                        print("Movieminto no valido")
                        movement = ""
                    else:
                        board.push(chess.Move.from_uci(movement))
                        xa2,ya2 = cuadros(pygame.mouse.get_pos(), WIDTH)
                        if (xm2 == xa2) and (ym2 == ya2):
                            col2 = col4
                        else:
                            col2 = grid[ya2][xa2].colour
                        grid[ya2][xa2].colour = BLUE
                        movement = ""
                        swich = 0
            update_display(WIN, grid, 8, WIDTH)
            if board.is_checkmate():
                if board.turn == chess.BLACK:
                    print("Ganaron las Blancas")
                elif board.turn == chess.WHITE:
                    print("Ganaron las Negras")
                game = False
            elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves():
                print("Empate")
                game = False



#PlayN(WIN,WIDTH)
BaseException
Cpiezas = input("Escribe 'B' si quieres ser las Blancas o 'N' si quieres las negras: ")
Cpiezas = Cpiezas.lower()
if Cpiezas == "b":
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Chess")
    PlayB(WIN,WIDTH)
elif Cpiezas == "n":
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Chess")
    PlayN(WIN,WIDTH)