class Minesweeper: 
    def __init__(this,w,h,m):
        this.width=w
        this.height=h
        this.num_mines=m
        this.board=[]
        this.mines=[]
        this.flags=[]
        for r in range(this.height):
            row=[]
            for c in range(this.width):
                row.append(this.Tile(this,r,c))
            this.board.append(row)
        this.first=True
        this.done=False
        this.header=this.create_header(this.height,this.width)
        this.initialize_mines(this.width,this.height,this.num_mines)
    def initialize_mines(this,w,h,m):
        import random
        while m > 0:
            randw=random.randint(0,w-1)
            randh=random.randint(0,h-1)
            if this.board[randh][randw].mine==False:
                this.board[randh][randw].mine=True
                this.mines.append(this.board[randh][randw])
                m-=1
    def dig(this,r,c):
        if this.board[r][c].mine==True:
            if this.first==True:
                while this.board[r][c] in this.mines:
                    this.mines.remove(this.board[r][c])
                    this.board[r][c].mine=False
                    this.initialize_mines(this.width,this.height,1)
                this.board[r][c].dig()
            else:
                this.die()
        else:
            this.board[r][c].dig()
        this.first=False
    def digall(this,r,c):
        for n in this.board[r][c].get_neighbors(r,c):
            if n.flag == False:
                this.dig(n.row,n.col)
    def die(this):
        this.done=True
        for m in this.mines:
            if m in this.flags:
                m.display='\033[91mX\033[0m'
            else:
                m.display='\033[91m*\033[0m'
        this.print_board()
    def flag(this,r,c):
        this.board[r][c].toggle_flag()
    def colkey(this,n):
        if n < 26:
            return chr(n+97)
        if n >=26:
            return chr(n+22)
    def create_header(this,h,w):
        if h <= 10:
            hdr='  '
            hdr2='  '
        else:
            hdr='   '
            hdr2='   '
        for c in range(w):
            hdr+=this.colkey(c)+' '
        hdr2+='_'*2*(w-1)+'_'
        return (hdr,hdr2)
    def print_board(this):
        print(this.header[0])
        #print(this.header[1])
        for row in range(this.height):
            r=str(row)
            if len(r)==1 and this.height > 10:
                r+=' '
            r+='\033[97m|\033[0m'
            for col in range(this.width):
                r+=this.board[row][col].display+'\033[97m|\033[0m'
            print(r)
        #print(this.header[1])
    def check_win(this):
        win=True
        for t in this.mines:
            if t not in this.flags:
                win=False
        if win==True and len(this.mines) == len(this.flags):
            this.win()
    def win(this):
        this.done=True
        print('YOU WIN!!!')
    class Tile:
        def __init__(this,board,r,c):
            this.pboard=board
            this.row=r
            this.col=c
            this.mine=False
            this.flag=False
            this.display='#'
            this.status=9
        def dig(this):
            this.status=this.count_mines()
            if this.status > 0:
                this.display=str(this.status)
            else:
                this.display='_'
                for t in this.get_neighbors(this.row,this.col):
                    t.dig()
        def count_mines(this):
            count=0
            for m in this.get_neighbors(this.row,this.col):
                if m.mine == True:
                    count+=1
            return count
        def get_neighbors(this,r,c):
            neighbors=[]
            for t in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
                try:
                    if r+t[0] < 0 or c+t[1] < 0:
                        1/0 #go to except
                    if this.pboard.board[r+t[0]][c+t[1]].status==9:
                        neighbors.append(this.pboard.board[r+t[0]][c+t[1]])
                except:
                    pass
            return neighbors
        def toggle_flag(this):
            if this.status == 9 and this.flag == False:
                this.flag = True
                this.display='\033[91m>\033[0m'
                this.pboard.flags.append(this)
            elif this.flag == True:
                this.flag=False
                this.display='\033[97m#\033[0m'
                this.pboard.flags.remove(this)
            this.pboard.check_win()
def play(w,h,m):
    import subprocess
    def clear():
        cl=subprocess.Popen('clear')
        subprocess.Popen.wait(cl)
    def colkey(l):
        n=ord(l)
        if n>=97:
            n-=97
        else:
            n-=22
        return n
    ms = Minesweeper(w,h,m)
    r=int(h/2)
    c=int(w/2)
    while ms.done==False:
        clear()
        ms.print_board()
        action = input('Action: ')
        try:
            loc=action.split('(')[1]
        except:
            print('invalid format')
            continue
        if loc[-1] == ')':
            loc=loc[:-1]
        if ',' in loc:
            try:
                int(loc.split(',')[0])
                r=int(loc.split(',')[0])
                c=colkey(loc.split(',')[1])
            except:
                r=int(loc.split(',')[1])
                c=colkey(loc.split(',')[0])
        else:
            if loc.lower() == 'q':
                r-=1
                c-=1
            elif loc.lower() == 'w':
                r-=1
            elif loc.lower() == 'e':
                r-=1
                c+=1
            elif loc.lower() == 'a':
                c-=1
            elif loc.lower() == 'd':
                c+=1
            elif loc.lower() == 'z':
                r+=1
                c-=1
            elif loc.lower() == 'x':
                r+=1
            elif loc.lower() == 'c':
                r+=1
                c+=1
        if r < 0 or c < 0 or r >= ms.height or c >= ms.width:
            print('invalid coordinates')
            continue
        action=action.split('(')[0]
        if action.lower() == 'd':
            ms.dig(r,c)
        elif action.lower() == 'da':
            ms.digall(r,c)
        elif action.lower() == 'f':
            ms.flag(r,c)
        else:
            print('Invalid action')
if __name__ == '__main__':
    play(10,10,10)
