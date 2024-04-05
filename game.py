class Game:
    def __init__(self,id):
        self.board = [[0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0]]
        self.p1Went = 0
        self.p2Went = 0
        self.ready = False
        self.id = id 
        self.turn = 0
        self.win = 2
        self.pos1 = 0
        self.pos2 = 0
        self.row1 = 0 
        self.row2 = 0
        
    
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
    

    