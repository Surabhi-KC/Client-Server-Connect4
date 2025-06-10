class Game:
    def __init__(self,id):
        #board as a matrix. 1 if game piece is present at that position 0 otherwise
        self.board = [[0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0]]
        self.p1Went = 0         #player 1's column number of move made
        self.p2Went = 0         #player 2's column number of move made
        self.ready = False      #True is player is connected to server False otherwise
        self.id = id            #id of the current player
        self.turn = 0           #0 if player 1's turn, 1 if player 2's turn
        self.win = 2            #0 if player 1 wins, 1 if player 2 wins, default value 2 as both the players start without a win
        self.pos1 = 0           #position of player 1 above the board
        self.pos2 = 0           #position of player 2 above the board
        self.row1 = 0           #keeping track of only rows as column is decided by the position of the game piece above board when player clicks to drop game piece
        self.row2 = 0
        
    #getter and setter methods
    def update_win(self, p):
        self.win = p
    
    def get_winner(self):
        return self.win
    
    def pos_change(self,player,pos):
        if player==0:
            self.pos1=pos
        else:
            self.pos2=pos
            
    def get_player_pos(self,p):
        if p==0:
            return self.pos1
        else:
            return self.pos2
        
    def get_player_move(self, p):
        if p==0:
            return self.p1Went
        else:
            return self.p2Went
    
    def play(self, player, move, r):
        #move keeps track of current player's choice of column on board
        if player == 0:
            self.p1Went = move 
            self.row1=r
        else:
            self.p2Went = move
            self.row2=r
    
    def get_row(self,p):
        if p==0:
            return self.row1
        else:
            return self.row2
        
    def update_board(self, p):
        if p==0:
            self.board[self.row1][self.p1Went] = 1
        else:
            self.board[self.row2][self.p2Went] = 2
    
    def get_board(self):
        return self.board    
        
    def connected(self):
        return self.ready
    
    def change_turn(self):
        self.turn=(self.turn+1)%2
    
    def get_turn(self):
        return self.turn
    

    