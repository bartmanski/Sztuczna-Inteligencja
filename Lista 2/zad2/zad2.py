from copy import*

from random import randint
class State:
    def __init__(self):
        self.possiblepos = set()
        self.mvtostate = ""

endpos = set()
used = set()

n,m=0,0
def possible(x,y):
    return (x>=0 and x<n and y>=0 and y<m and plansza[x][y] != "#")

def prep(plansza):
    CurrentS=State()
    for i in range(n):
        for j in range(m):
            if plansza[i][j] == "S": 
                CurrentS.possiblepos.add((i,j))
            elif plansza[i][j] == "B": 
                CurrentS.possiblepos.add((i,j))
                endpos.add((i,j))
            elif plansza[i][j] == "G":
                endpos.add((i,j))
    return CurrentS

def moveall(ItStateS,howmuch,xoff,yoff,letter):
    pom = ItStateS.possiblepos
    NextS=State()
    for _ in range(howmuch):
        tmp=set()
        for pos in  pom:
            if possible(pos[0]+xoff,pos[1]+yoff): tmp.add((pos[0]+xoff,pos[1]+yoff))
            else:  tmp.add(pos)
        pom=copy(tmp)
        # print(tmp)
    NextS.mvtostate=ItStateS.mvtostate+letter*howmuch
    NextS.possiblepos=pom
    # print(ItStateS.possiblepos)
    return NextS
    
def allgood(positions):
    for pos in positions:
        if pos not in endpos: return False
    return True
def hash(positions):
    a,b=0,0
    mno=1
    for pos in positions:
        a+=pos[0]*mno
        b+=pos[1]*mno
        mno*=m
    return (a,b)

def proc(plansza):
    rethor=-1
    for i in range(n):
        tmp=0
        for j in range(m):
            if plansza[i][j]=='#' or plansza[i][j]==" ": tmp=0
            else:
                tmp+=1
                rethor=max(rethor,tmp)
    retver=-1
    for j in range(m):
        tmp=0
        for i in range(n):
            if plansza[i][j]=='#' or plansza[i][j]==" ": tmp=0
            else:
                tmp+=1
                retver=max(retver,tmp)         
    return rethor,retver   


juzdobrze=1000
queue=[]

def ifs(NextS):
    global juzdobrze
    global queue
    global used
    
    if len(NextS.possiblepos) < juzdobrze: 
        queue = []
        juzdobrze = len(NextS.possiblepos)
        # print("pwaw")
    hashed = hash(NextS.possiblepos)
    # print("hasz stanu ",NextS.possiblepos, " : ",hashed)
    if len(NextS.possiblepos) <= juzdobrze and hashed not in used:
        used.add(hashed)
        queue.append(NextS)
 

def solve(plansza):

    global juzdobrze
    global queue

    CurrentS = prep(plansza)
    maxhor,maxver = proc(plansza)
    # print(maxhor,' ', maxver)

    # maxver,maxhor = proc2(CurrentS)
    flip = randint(0,1)
    for _ in range(4):
        which = randint(0,1)
        if flip == 0:
            if which == 0:  CurrentS = moveall(CurrentS,maxhor-1,0,-1,"L")
            else :  CurrentS = moveall(CurrentS,maxhor-1,0,1,"R")
        else:
            if which == 0: CurrentS = moveall(CurrentS,maxver-1,-1,0,"U")
            else: CurrentS = moveall(CurrentS,maxver-1,1,0,"D")
        flip = (flip + 1) % 2
   
    queue=[CurrentS]
    used.add(hash(CurrentS.possiblepos))
    juzdobrze=len(CurrentS.possiblepos)
    while True:
        
        # for q in queue:
        #     print(q.possiblepos)
        # print()

        CurrentS = queue[0]
        # print(CurrentS.possiblepos,"\n")
        queue.pop(0)


        NextS=moveall(CurrentS,1,-1,0,"U")
        # print(NextS.possiblepos)
        ifs(NextS)
        if allgood(NextS.possiblepos): break
        NextS=moveall(CurrentS,1,1,0,"D")
        if allgood(NextS.possiblepos): break
        # print(NextS.possiblepos)
        ifs(NextS)
        NextS=moveall(CurrentS,1,0,-1,"L")
        if allgood(NextS.possiblepos): break
        # print(NextS.possiblepos)
        ifs(NextS)
        NextS=moveall(CurrentS,1,0,1,"R")
        if allgood(NextS.possiblepos): break

        # print(NextS.possiblepos)
        ifs(NextS)

    # if(pos>=len(queue)): return queue[pos-1].mvtostate
    return NextS.mvtostate
    # return CurrentS.mvtostate

read = open("zad_input.txt")
write = open("zad_output.txt",'w')
plansza = []

while True:
    line = read.readline()
    if not line: break 
    plansza.append(line.rstrip())
n=len(plansza)
m=len(plansza[0])
write.write(solve(plansza))