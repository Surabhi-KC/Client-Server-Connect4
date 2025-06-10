import numpy as np
import pygame 
import sys
import math
from network import Network
from game import Game

#button class for Play and Quit buttons on menu page
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    #placing rect.png of the buttons on screen
	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

    #changing colour of button when cursor hovers over it
	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

ROW = 8
COL = 9
def create_board():
    """
    initializng board matrix

    Returns:
        list: game board matrix
    """
    board = np.zeros((ROW,COL))
    return board

def is_valid(board, selection):
    """validates game board position chosen by player

    Args:
        board (nested list): game board representation
        selection (int): board column chosen by player

    Returns:
        bool: True if position is valid, False otherwise
    """
    return board[ROW-2][selection] == 0

def get_next_open_row(board, selection):
    """finds the row number into which the game piece can be dropped

    Args:
        board (nested list): game board representation
        selection (int): board column chosen by player

    Returns:
        int: valid board row number
    """
    for r in range(ROW-2):
        if board[r+1][selection] == 0:
            return r+1
        
def drop_piece(board, row, col, piece):
    """updates player's game piece position in board matrix

    Args:
        board (nested list): game board representation
        row (int): player's move row number
        col (int): player's move column number
        piece (int): 1 if player 1's game piece, 2 if player 2's game piece
    """
    board[row][col] = piece

def draw_board(board):
    """converts board matrix to board drawing on screen

    Args:
        board (nested list): game board representation
    """
    #drawing only board on screen
    for c in range(1,COL-1):
        for r in range(ROW-2):
            pygame.draw.rect(screen, (0, 0, 255), (c* SquareSize, r*SquareSize+SquareSize, SquareSize, SquareSize))
            pygame.draw.circle(screen, (0, 0, 0), (int(c* SquareSize+SquareSize/2), int(r*SquareSize+SquareSize+SquareSize/2)), radius)
    #drawing players' game pieces on the board
    for c in range(1,COL-1):
        for r in range(ROW-1):
            if board[r][c] == 1:
                pygame.draw.circle(screen, (255, 255, 0), (int(c* SquareSize+SquareSize/2), height - int(r*SquareSize+SquareSize/2)), radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, (255, 0, 0), (int(c* SquareSize+SquareSize/2), height - int(r*SquareSize+SquareSize/2)), radius)
    pygame.display.update()
    
def print_board(board):
    """prints board matrix on client's cmd

    Args:
        board (nested list): game board representation
    """
    print(np.flip(board,0))

def get_font(size): 
    """renders font type of given size

    Args:
        size (int): font size

    Returns:
        pygame font object
    """
    return pygame.font.Font("font.ttf", size)

def check_no_zeros(board):
    """checks if board is full to declare a tie

    Args:
        board (nested list): game board representation

    Returns:
        bool: True if board is full, False otherwise 
    """
    for i in range(1,7):
        for j in range(1,8):
            if board[i][j]==0:
                return False
    return True

def winner(board, piece, row, col):
    """checks for a win i.e checks for four pieces along all the four directions

    Args:
        board (nested list): game board representation
        piece (int): player's game piece (1 or 2)
        row (int): row of latest game piece dropped
        col (int): column of latest game piece dropped

    Returns:
        bool: True if there are 4 pieces along any direction, False otherwise
    """
    #horizontal
    for c in range(COL-3):
        if board[row][c] == piece and board[row][c+1] == piece and board[row][c+2] == piece and board[row][c+3] == piece:
            return True
    #vertical
    for r in range(ROW-3):
        if board[r][col] == piece and board[r+1][col] == piece and board[r+2][col] == piece and board[r+3][col] == piece:
            return True
    #negative diagonal
    for c in range(COL-3):
        for r in range(3,ROW):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    #positive diagonal
    for c in range(COL-3):
        for r in range(ROW-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

#initializing and defining game screen
pygame.init()
SquareSize = 100
width = (COL) * SquareSize
height = (ROW) * SquareSize
size = (width, height)
radius = int(SquareSize/2 - 7)
screen = pygame.display.set_mode(size)
#setting game name on top-left corner of screen
pygame.display.set_caption("Connect4")
#setting game icon on top left corner of screen
icon = pygame.image.load('gameIcon.png').convert_alpha()
pygame.display.set_icon(icon)
text=""
pygame.display.update()

def play():
        n=Network()
        player=int(n.getP())
        print(player) 
        run_once =0     #flag to draw the black background only once
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, height)) 
        game_over = False
        turn = 0 #turn 0 - player 1, turn 1 - player 2
            
        while not game_over:
            try:
                game = n.sending("get")
            except:
                game_over = False
                print("Couldn't get game")
                break
            if not game.connected():
                pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, height))
                wait_font = get_font(30)
                wait_text = wait_font.render("Waiting for second player...", 1, (255, 255, 255))
                screen.blit(wait_text, (50, 400))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
            else:
                turn = game.get_turn()
                board = game.get_board()
                draw_board(board)
                if run_once == 0:
                    pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, height))
                    run_once = 1
                #Printing corresponding player's turn on screen
                if player == turn:
                    pygame.draw.rect(screen, (0, 0, 0), (0, 700, width,SquareSize))
                    turn_font = get_font(50)
                    if turn == 0:
                        colour =(255, 255, 0)
                    else:
                        colour = (255, 0, 0)
                    turn_text = turn_font.render("Your turn", 1, colour)
                else: 
                    pygame.draw.rect(screen, (0, 0, 0), (0, 700, width,SquareSize))
                    turn_font = get_font(50)
                    if turn == 0:
                        opp_colour =(255, 255, 0)
                    else:
                        opp_colour = (255, 0, 0)
                    turn_text = turn_font.render("Opponent's turn", 1, opp_colour)
                screen.blit(turn_text, (100,750))
                pygame.display.update()
                
                if player == turn:
                    for event in pygame.event.get():
                        #if close button on top right corner of window is clicked
                        if event.type == pygame.QUIT:
                            sys.exit()
                        #changing game piece position on top of board when the player moves it
                        if event.type == pygame.MOUSEMOTION:
                            if player == turn:
                                pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SquareSize))
                                posx = event.pos[0]
                                game = n.sending("pos "+str(posx))
                                #keeping the game piece within the window
                                if posx > 757:      #757 so that the edge of the circular game piece (and not its centre) touches the window edge
                                    posx= 757
                                if posx < 143:
                                    posx = 143
                                if turn == 0:
                                    pygame.draw.circle(screen, (255, 255, 0), (posx, int(SquareSize/2)), radius) #yellow game piece
                                if turn == 1:
                                    pygame.draw.circle(screen, (255, 0, 0), (posx, int(SquareSize/2)), radius)#red game piece
                        pygame.display.update()
                        #when player clicks to drop game piece
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            posx=event.pos[0]   #x coordinate of cursor when clicked
                            if posx>143 and posx<757:
                                #when it is player 1's turn
                                if turn == 0 and player == 0:
                                    board = game.get_board()
                                    posx = event.pos[0]
                                    selection = int(math.floor(posx / SquareSize))      #calculating board column number within which the cursor was clicked
                                    print(selection)
                                    if is_valid(board, selection):
                                        row = get_next_open_row(board, selection)
                                        game = n.sending("move "+str(selection)+" "+str(row))       #sending updated game info to server through Network instance
                                        drop_piece(board, row, selection, 1)
                                        pygame.draw.circle(screen, (255, 0, 0), (posx, int(SquareSize/2)), radius)
                                    else:
                                        continue
                                    if winner(board, 1, row, selection):
                                        font = get_font(80)
                                        text = font.render("You Win!!", 1, (255, 255, 255))
                                        game = n.sending("win")
                                        game_over = True
                                    if check_no_zeros(board):
                                        font = get_font(50)
                                        text = font.render("It's a Tie", 1, (255, 255, 255))
                                        game_over = True
                                    game = n.sending("change")  #info sent to server indicating to change players' turn
                                #when it is player 2's turn
                                elif turn == 1 and player == 1:
                                    board = game.get_board()
                                    posx = event.pos[0]
                                    selection = int(math.floor(posx / SquareSize))
                                    if is_valid(board, selection):
                                        row = get_next_open_row(board, selection)
                                        game = n.sending("move "+str(selection)+" "+str(row))
                                        drop_piece(board, row, selection, 2)
                                        pygame.draw.circle(screen, (255, 255, 0), (posx, int(SquareSize/2)), radius)
                                    else:
                                        continue
                                    game = n.sending("move "+str(selection)+" "+str(row))
                                    if winner(board, 2, row, selection):
                                        font = get_font(80)
                                        text = font.render("You Win!!", 1, (255, 255, 255))
                                        game = n.sending("win")
                                        game_over = True
                                    if check_no_zeros(board):
                                        font = get_font(50)
                                        text = font.render("It's a Tie", 1, (255, 255, 255))
                                        game_over = True 
                                    game = n.sending("change") 

                                print_board(board)
                                draw_board(board)

                                if game_over:
                                    pygame.time.wait(1000)
                                    screen.fill((0, 0, 0))
                                    screen.blit(text, (50,350))
                                    pygame.display.update()
                                    pygame.time.wait(2000)
                    #Text to display on looser's screen 
                    if game.get_winner() == 0 and player == 1 or game.get_winner() == 1 and player == 0:
                        font = get_font(60)
                        text = font.render("You Loose!!", 1, (255, 255, 255))
                        pygame.time.wait(1000)
                        screen.fill((0, 0, 0))
                        screen.blit(text, (50,350))
                        pygame.display.update()
                        pygame.time.wait(2000)
                        game_over = True
                
                #To not allow the non-turn player to make a move
                #Only dislaying the turn player's moves
                elif player != turn:
                    if player == 0:
                        posx1 = game.get_player_pos(1)
                        board = game.get_board()
                        pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SquareSize))
                        if posx1 > 757:
                            posx1 = 757
                        if posx1 < 143:
                            posx1 = 143
                        pygame.draw.circle(screen, (255, 0, 0), (posx1, int(SquareSize/2)), radius)
                    if player == 1:
                        posx0 = game.get_player_pos(0)
                        board = game.get_board()
                        pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SquareSize))
                        if posx0 > 757:
                            posx0 = 757
                        if posx0 < 143:
                            posx0 = 143
                        pygame.draw.circle(screen, (255, 255, 0), (posx0, int(SquareSize/2)), radius)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                            
def main_menu(): 
    while True:
        #Displaying background image
        bg = pygame.image.load('Background.jpg')
        screen.blit(bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        #Displaying the heading
        menu_text = get_font(100).render("CONNECT4", True, (182, 143, 64))
        menubox = menu_text.get_rect(center=(450, 130))
        #Displaying the play and quit buttons
        PLAY_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(450, 350), 
                            text_input="PLAY", font=get_font(60), base_color=(215, 252, 212), hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Quit Rect.png"), pos=(450, 550), 
                            text_input="QUIT", font=get_font(60), base_color=(215, 252, 212), hovering_color="White")

        screen.blit(menu_text, menubox)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(mouse_pos)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(mouse_pos):
                    play()
                if QUIT_BUTTON.checkForInput(mouse_pos):
                    pygame.quit()
                    exit()

        pygame.display.update()

main_menu()