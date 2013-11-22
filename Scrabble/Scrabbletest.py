import random, subprocess
#Creating tiles and board
Amounts = {'A':9,'B':2,'C':2,'D':4,'E':12,'F':2,'G':3,'H':2,'I':9,'J':1,'K':1,'L':4,'M':2,'N':6,'O':8,'P':2,'Q':1,'R':6,'S':4,'T':6,'U':4,'V':2,'W':2,'X':1,'Y':2,'Z':1,'?':2}
Points = {'A':1,'B':3,'C':3,'D':2,'E':1,'F':4,'G':2,'H':4,'I':1,'J':8,'K':5,'L':1,'M':3,'N':1,'O':1,'P':3,'Q':10,'R':1,'S':1,'T':1,'U':1,'V':4,'W':4,'X':8,'Y':4,'Z':10,'?':0}
Letters = []
for letter in Amounts.keys():
    Letters.append(letter)
Bag = []
for letter in Amounts.keys():
    for n in range(Amounts[letter]):
        Bag.append(letter)
Row = ['   ','1  ','2  ','3  ','4  ','5  ','6  ','7  ','8  ','9  ','10 ','11 ','12 ','13 ','14 ','15 ']
Columns = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
ColKey={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,'i':8,'j':9,'k':10,'l':11,'m':12,'n':13,'o':14}
r1 = ['#',' ',' ','2',' ',' ',' ','#',' ',' ',' ','2',' ',' ','#']
r2 = [' ','@',' ',' ',' ','3',' ',' ',' ','3',' ',' ',' ','@',' ']
r3 = [' ',' ','@',' ',' ',' ','2',' ','2',' ',' ',' ','@',' ',' ']
r4 = ['2',' ',' ','@',' ',' ',' ','2',' ',' ',' ','@',' ',' ','2']
r5 = [' ',' ',' ',' ','@',' ',' ',' ',' ',' ','@',' ',' ',' ',' ']
r6 = [' ','3',' ',' ',' ','3',' ',' ',' ','3',' ',' ',' ','3',' ']
r7 = [' ',' ','2',' ',' ',' ','2',' ','2',' ',' ',' ','2',' ',' ']
r8 = ['#',' ',' ','2',' ',' ',' ','@',' ',' ',' ','2',' ',' ','#']
r9 = [' ',' ','2',' ',' ',' ','2',' ','2',' ',' ',' ','2',' ',' ']
r10 = [' ','3',' ',' ',' ','3',' ',' ',' ','3',' ',' ',' ','3',' ']
r11 = [' ',' ',' ',' ','@',' ',' ',' ',' ',' ','@',' ',' ',' ',' ']
r12 = ['2',' ',' ','@',' ',' ',' ','2',' ',' ',' ','@',' ',' ','2']
r13 = [' ',' ','@',' ',' ',' ','2',' ','2',' ',' ',' ','@',' ',' ']
r14 = [' ','@',' ',' ',' ','3',' ',' ',' ','3',' ',' ',' ','@',' ']
r15 = ['#',' ',' ','2',' ',' ',' ','#',' ',' ',' ','2',' ',' ','#']
Board=[Columns,r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15]
grid=False
score=True
done=False
#Clear screen
def clear():
    cl=subprocess.Popen('clear')
    subprocess.Popen.wait(cl)
#Switch to next player
def NextTurn(curr):
    global Players
    n=Players.index(curr)
    n+=1
    return Players[n%len(Players)]
#Adds the players information from their last turn
def AddInfo(player,word,points):
    player.words.append(word)
    player.scores.append(points)
    player.score+=points
#Adds grid for viewing pleasure
def toggrid(grid):
    global Board
    if grid==True:
        for r,row in enumerate(Board):
            for c,space in enumerate(row):
                if space=='_':
                    Board[r][c]=' '
        return False
    else:
        for r,row in enumerate(Board):
            for c,space in enumerate(row):
                if space==' ':
                    Board[r][c]='_'
        return True
#Prints the board in wonderful authentic colors
def PrintBoard(board,rows,grid):
    print('Board:')
    for n,row in enumerate(board):
        out=rows[n]
        if grid==True:
            out+='|'
        for tile in row:
            if tile=='#' or tile=='@':
                out+='\033[91m'+tile+'\033[0m'
            elif tile=='3' or tile=='2':
                out+='\033[94m'+tile+'\033[0m'
            elif tile in ColKey.keys():
                out+=tile
            else:
                out+='\033[93m'+tile+'\033[0m'
            if grid==True:
                out+='\033[93m|\033[0m'
            else:
                out+=' '
        print(out)

#Shows tiles on the player's rack
def PrintTiles(player,score):
    rack='Your Rack: ['
    for letter in player.tiles:
        rack+=letter
        if score == True:
            rack+='('+str(Points[letter])+')'
        rack+=','
    rack=rack[:-1]+']'
    print(rack)
#Shows the words and corresponding scores of the other players since your last play
def Recap(player):
    global Players
    info=""
    info=NextTurn(player)
    while info != player:
        if len(info.words)>0:
            print(info.name+' played '+info.words[-1]+' for '+str(info.scores[-1])+' points, giving them a total of '+str(info.score)+' points.')
        info=NextTurn(info)
    print('You currently have a score of '+str(player.score)+' points.')
#Draw back to 7 tiles
def DrawTiles(rack):
    global Bag
    tneeded=7-len(rack)
    for t in range(tneeded):
        if len(Bag) != 0:
            index=random.randint(0,len(Bag)-1)
            rack.append(Bag[index])
            Bag.remove(Bag[index])
    return rack
#Checks validity of word
def Check(rack,word,r,c,o):
    global Board, Letters, Players
    blanks=rack.count('?')
    for l in range(len(word)):
        if o == 'v':
            r+=1
        else:
            c+=1
        if Board[r][c] in Letters:
            if Board[r][c] != word[l]:
                return False
        elif word[l] not in rack:
            if blanks > 0:
                blanks-=1
            else:
                return False
    return True
#Puts tiles on board
def LayTiles(rack,word,r,c,o,player):
    global Board, Letters, done
    wscore=0
    cscore=0
    multiplier=1
    if len(rack) == 7:
        full=True
    else:
        full=False
    for l in range(len(word)):
        sc=False
        if o == 'v':
            r+=1
        else:
            c+=1
        cmult=1
        if Board[r][c] == '@':
            multiplier*=2
            cmult=2
        if Board[r][c] == '#':
            multiplier*=3
            cmult=3
        if Board[r][c] == '2':
            wscore+=Points[word[l]]*2
        elif Board[r][c] == '3':
            wscore+=Points[word[l]]*3
        else:
            wscore+=Points[word[l]]
        if Board[r][c] not in Letters:
            Board[r][c]=word[l]
            if word[l] in rack:
                rack.remove(word[l])
            else:
                rack.remove('?')
            sc=True
        if l == len(word)-1:
            wscore*=multiplier
        #Check for side chains
        if sc == True:
            if orientation == 'v':
                if l == 0:
                    if r > 1:
                        if Board[r-1][c] in Letters:
                            cscore+=CountChain(r,c,'u',False)*cmult
                if l == len(word)-1:
                    if r < 15:
                        if Board[r+1][c] in Letters:
                            cscore+=CountChain(r,c,'d',False)*cmult
                if c > 0:
                    if Board[r][c-1] in Letters:
                        cscore+=CountChain(r,c,'l',True)*cmult
                if c < 14:
                    if Board[r][c+1] in Letters:
                        cscore+=CountChain(r,c,'r',True)*cmult
            else:
                if l == 0:
                    if c > 0:
                        if Board[r][c-1] in Letters:
                            cscore+=CountChain(r,c,'l',False)*cmult
                if l == len(word)-1:
                    if c < 14:
                        if Board[r][c+1] in Letters:
                            cscore+=CountChain(r,c,'r',False)*cmult
                if r > 1:
                    if Board[r-1][c] in Letters:
                        cscore+=CountChain(r,c,'u',True)*cmult
                if r < 15:
                    if Board[r+1][c] in Letters:
                        cscore+=CountChain(r,c,'d',True)*cmult
    score = wscore+cscore
    if len(rack)==0 and full == True:
        score+=50
    #Game finished TODO: Instead  of check full, check that bag is empty
    if len(rack)==0 and full == False:
        sub=NextTurn(player)
        while sub != player:
            for t in sub.tiles:
                sub.score-=Points[t]
                player.score+=Points[t]
            sub=NextTurn(sub)
        done = True
    return score
#Awards the player points for adding to other words
#TODO: make orientation as opposed to direction
def CountChain(r,c,direction,include):
    global Letters, Board
    score=0
    if include == True:
        score+=Points[Board[r][c]]
    word=[]
    if direction == 'u':
        while r > 1:
            if Board[r-1][c] in Letters:
                r-=1
                score+=Points[Board[r][c]]
                word.append(Board[r][c])
            else:
                break
    if direction == 'l':
        while c > 0:
            if Board[r][c-1] in Letters:
                c-=1
                score+=Points[Board[r][c]]
                word.append(Board[r][c])
            else:
                break
    if direction == 'd':
        while r < 15:
            if Board[r+1][c] in Letters:
                r+=1
                score+=Points[Board[r][c]]
                word.append(Board[r][c])
            else:
                break
    if direction == 'r':
        while c < 14:
            if Board[r][c+1] in Letters:
                c+=1
                score+=Points[Board[r][c]]
                word.append(Board[r][c])
            else:
                break
    print(r,c,direction)
    print('You scored '+str(score)+' points for the word '+str(word))
    return score
#Creating player class
class Player:
    def __init__(self,number):
        self.num=number
        self.name=''
        self.password=''
        self.tiles=[]
        self.score=0
        self.turn=True
        self.words=[]
        self.scores=[]
clear()
#Set player data
p=int(input('Number of players: '))
p1=Player(1)
p2=Player(2)
p3=Player(3)
p4=Player(4)
possibilities=[p1,p2,p3,p4]
Players=[]
for n in range(p):
    Players.append(possibilities[n])
    possibilities[n].name=raw_input("Enter Player "+str(possibilities[n].num)+"'s name: ")
    possibilities[n].password=raw_input("Enter Player "+str(possibilities[n].num)+"'s password: ")
    clear()
#Set up game
grid = toggrid(grid)
turn=Players[random.randint(0,p-1)]
for pl in Players:
    pl.tiles=DrawTiles(pl.tiles)
print(turn.name+' has been selected to go first')
while True:
    word='nothing'
    points=0
    if turn.turn == False:
        AddInfo(word,points)
        turn.turn = True
    print("It is "+turn.name+"'s turn.")
    while True:
        pw = raw_input("Insert "+turn.name+"'s password: ")
        if pw == turn.password or pw == 'oVeRiDe': 
            break
    clear()
    print('Welcome '+turn.name+'!')
    Recap(turn)
    PrintBoard(Board,Row,grid)
    PrintTiles(turn,score)
    while True:
        complete=False
        action = raw_input('Action: ')
        if 'place' in action.lower():
            #Gather information
            toplace=raw_input('Input the word would you like to place: ').upper()
            word=[]
            for n in range(len(toplace)):
                word.append(toplace[n])
            rack=[]
            for n in turn.tiles:
                rack.append(n)
            orientation=raw_input('Would you like to place the word vertically or horizontally (v/h)? ')
            if 'v' in orientation.lower():
                orientation='v'
            if 'h' in orientation.lower():
                orientation='h'
            placement=raw_input('What are the coordinates of the first letter (letter,number)? ')
            try:
                row=int(placement[1:])
                col=ColKey[placement[0].lower()]
            except:
                print('Invalid coordinates. Try again.')
            if row > 15 or col > 15:
                print('Invalid coordinates. Try again.')
                continue
            if orientation == 'h':
                col-=1
            else:
                row-=1
            #Test validity of word
            if Check(turn.tiles,word,row,col,orientation)==True:
                s=LayTiles(turn.tiles,word,row,col,orientation,turn)
                turn.words.append(toplace.lower())
                turn.scores.append(s)
                turn.score+=s
                complete=True
                PrintBoard(Board,Row,grid)
                print('You scored '+str(s)+' points with the word '+toplace.lower())
            else:
                print('This word cannot be placed there. You either have insufficient tiles or the word will not fit here.')
        elif 'trade' in action.lower():
            totrade=raw_input('Input all of the letters you want to trade in seperated by commas: ').upper()
            totrade=totrade.split(',')
            rack=[]
            for tile in turn.tiles:
                rack.append(tile)
            problems=[]
            addback=[]
            for letter in totrade:
                try:
                    rack.remove(letter)
                    addback.append(letter)
                except:
                   problems.append(letter)
            if len(problems) == 0:
                for l in addback:
                    Bag.append(l)
                rackcopy=[]
                for tile in rack:
                    rackcopy.append(tile)
                rack=DrawTiles(rack)
                for n,tile in enumerate(rack):
                    turn.tiles[n]=tile
                for t in rackcopy:
                    rack.remove(t)
                print(str(totrade)+' was successfully traded for '+str(rack))
                print(turn.tiles)
                complete=True
            else:
                print('Invalid trade. Try again.')
        elif 'grid' in action.lower():
            grid=toggrid(grid)
            PrintBoard(Board,Row,grid)
        elif 'score' in action.lower():
            if score == True:
                score = False
            else:
                score =True
            PrintTiles(turn,score)
        elif 'count' in action.lower():
            print(len(Bag))
        elif 'shake' in action.lower():
            print('Shake. Shake. Shake.')
            #Randomize the bag just for the hell of it.
        if complete == True:
            break
    turn.tiles=DrawTiles(turn.tiles)
    PrintTiles(turn,score)
    if done==True:
        raw_input('The game has ended.\nPress ENTER for final results.')
        break
    else:
        raw_input('Press ENTER to complete turn.')
        turn = NextTurn(turn)
        clear()
clear()
print('FINAL RESULTS:')
e=['1st','2nd','3rd','4th']
playernames=[]
playerscores=[]
for pl in Players:
    playernames.append(pl.name)
    playerscores.append(pl.score)
for n in range(p):
    m=max(playerscores)
    i=playerscores.index(m)
    print(playernames[i]+' came in '+e[n]+' place with a score of '+str(m)+'!')
    playerscores.remove(m)
    playernames.remove(playernames[i])
print('GAME HIGHLIGHTS:')
for pl in Players:
    print(pl.name+"'s best word was"+pl.words[pl.scores.index(max(pl.scores))]+' which scored '+str(max(pl.scores))+' points.')
