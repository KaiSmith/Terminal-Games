import Minesweeper
ms = Minesweeper.Minesweeper(10,10,10)
to_deal_with=[ms.board[j][k] for j in range(10) for k in range(10) ]
dealt_with=[]
def trivial():
    for t in to_deal_with:
        if t.status == 0:
            dealt_with.append(t)
            to_deal_with.remove(t)
        elif t.status < 9:
            if len(t.get_neighbors(t.row,t.col)) == t.status:
                for n in t.get_neighbors(t.row,t.col):
                    if n.flag==False:
                        n.toggle_flag()
            flagged=0
            for n in t.get_neighbors(t.row,t.col):
                if n.flag == True:
                    flagged+=1
            if flagged == t.status:
                ms.digall(t.row,t.col)
                dealt_with.append(t)
                to_deal_with.remove(t)
ms.dig(3,3)
for i in range(5):
    ms.print_board()
    trivial()
