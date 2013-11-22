import random, subprocess

class Hearts:

    def __init__(self, player1, player2, player3, player4):
        self.pd = {0:player1, 1:player2, 2:player3, 3:player4}
        self.players = [player1, player2, player3, player4]
        for i, p in enumerate(self.players):
            p.pid = i
            p.game = self
            p.score = 0
            p.total = 0
            p.hand = []
        values = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
        suits = ['H','C','D','S']
        self.heirarchy = {'2':0,'3':1,'4':2,'5':3,'6':4,'7':5,'8':6,'9':7,'T':8,'J':9,'Q':10,'K':11,'A':12}
        self.deck = []
        for v in values:
            for s in suits:
                self.deck.append(v+s)

    def play(self, play_to = 100, QS_breaks_hearts = True):
        self.direction = 0
        while max([p.total for p in self.players]) < play_to:
            #Start round
            deck = self.deck[:]
            for r in range(51,-1,-1):
                random_card = random.randint(0,r)
                self.pd[r%4].hand.append(deck.pop(random_card))

            #Passing
            passes = [p.pass_cards(self.direction) for p in self.players]
            shift = {0:-1, 1:1, 2:2, 3:0}[self.direction]
            for n,p in enumerate(passes):
                for c in p:
                    self.pd[(n+shift)%4].hand.append(self.pd[n].hand.pop(self.pd[n].hand.index(c)))

            #Playing
            for p in self.players:
                if '2C' in p.hand:
                    self.start = p.pid
                    break
            self.broken = False
            self.played_cards = []
            self.round_num = 1
            while self.round_num < 14:
                self.leading = '?'
                self.board = []
                for t in range(4):
                    self.turn = self.pd[(self.start + t)%4]
                    c = self.turn.play(self.board)
                    print(c)
                    print(str(self.turn.hand.index(c)))
                    if t == 0:
                        self.leading = c[1]
                    self.board.append(self.turn.hand.pop(self.turn.hand.index(c)))
                self.played_cards.extend(self.board)
                r = [self.heirarchy[c[0]] if c[1] == self.leading else -1 for c in self.board]
                s = (r.index(max(r))+self.start)%4
                winner = self.pd[s]
                hearts = sum([1 if c[1] == 'H' else 0 for c in self.board])
                winner.score += hearts
                winner.total += hearts
                if hearts > 0:
                    self.broken = True
                if 'QS' in self.board:
                    winner.score += 13
                    winner.total += 13
                    if QS_breaks_hearts == True:
                        self.broken = True
                self.start = winner.pid
                self.round_num += 1
            self.direction = (self.direction+1)%4
        #Present Scores
        print('Final Standings')
        for p in self.players:
            print(p.name+' - '+str(p.total))

    def get_score(self, pid):
        scores=[]
        for p in range(4):
            scores.append(self.pd[(pid+p)%4])
        return scores
    
    
class Player:
    def playable(self, board):
        if '2C' in self.hand:
            #You are starting
            return ['2C']
        s = self.game.leading
        if s == '?':
            #You are leading
            if self.game.broken == True:
                return self.hand
            else:
                return filter(lambda x: x != 0, [c if c[1] != 'H' else 0 for c in self.hand])
        else:
            matching = filter(lambda x: x != 0, [c if c[1] == s else 0 for c in self.hand])
            if len(matching) > 0:
                return matching
            else:
                return self.hand
    
class BasicPlayer(Player):
    def __init__(self, name):
        self.name = name
    
    def pass_cards(self, direction):
        if direction != 3:
            passing = []
            if 'QS' in self.hand and sum([1 if c[1] == 'S' else 0 for c in self.hand]) < 5:
                passing.append('QS')
            for c in ['AS', 'KS']:
                if c in self.hand and 'QS' not in passing:
                    passing.append(c)
            for c in ['AH', 'KH', 'QH', 'JH', 'TH', 'AD', 'KD', 'QD', 'JD', 'TD', 'AC', 'KC', 'QC', 'JC', 'TC']:
                if c in self.hand and len(passing) < 3:
                    passing.append(c)
                elif len(passing) >= 3:
                    break
            for c in self.hand:
                if len(passing) >= 3:
                    break
                elif c not in passing:
                    passing.append(c)
            print(passing)
            return passing
        return self.hand[:3]

    def play(self, board):
        p = self.playable(board)
        return p[0]
        '''if self.game.round_num == 1:
            return p.sort(key = lambda x: self.game.heirarchy[x[0]])[-1]
        elif p[0][1] == self.game.leading:
            return p.sort(key = lambda x: self.game.heirarchy[x[0]])[0]
        else:
            if 'QS' in self.hand:
                return 'QS'
            return p.sort(key = lambda x: self.game.heirarchy[x[0]])[-1]
            #if len([1 if c[1] == 'H' for c in p])>0'''


class HumanPlayer(Player):
#Allows humans to play through the terminal. Not user friendly, but, as far as I know, usable.
    def __init__(self, name):
        self.name = name
        self.dc = {0:'Left', 1:'Right', 2:'Across', 3:'Hold'}

    def clear(self):
        cl=subprocess.Popen('clear')
        subprocess.Popen.wait(cl)

    def show_board(self):
        print('            '+self.game.players[0].name+': '+str(self.game.players[0].total)+'('+str(self.game.players[0].score)+')')
        print(self.game.players[3].name+': '+str(self.game.players[3].total)+'('+str(self.game.players[3].score)+')'+'               '+self.game.players[1].name+': '+str(self.game.players[1].total)+'('+str(self.game.players[1].score)+')')
        print('            '+self.game.players[2].name+': '+str(self.game.players[2].total)+'('+str(self.game.players[2].score)+')')
        print(self.game.board)
        print(self.game.start)


    def pass_cards(self, direction):
        self.clear()
        print(self.name+"'s turn to pass.")
        print('Pass status: '+self.dc[direction])
        raw_input()
        if direction != 3:
            passing=[]
            while len(passing) < 3:
                print('Your cards are '+str(self.hand))
                passing.extend(raw_input('Which cards do you want to pass? ').strip().upper().split(','))
                #TODO: Check validity
            return passing[:3]
        return self.hand[:3]

    def play(self, board):
        self.clear()
        print(self.name+"'s turn to play.")
        raw_input()
        self.show_board()
        print(str(self.hand))
        while True:
            c = raw_input('Which card do you want to play? ')[:2].upper()
            if c in self.playable(self.game.board):
                return c
            print('Invalid selection. Choose another.')
    
if __name__ == '__main__':
    h = Hearts(HumanPlayer('Kai'), BasicPlayer('Comp1'), HumanPlayer('Ari'), BasicPlayer('Comp2'))
    h.play()
