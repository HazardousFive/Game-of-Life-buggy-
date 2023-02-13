import sys, pygame, numpy as np, sqlite3 as sql


pygame.init()
screen_info = pygame.display.Info()
w = screen_info.current_w
h = screen_info.current_h
size = w,h
screen = pygame.display.set_mode(size)
black = (0, 0, 0)
white=(255,255,255)
lince= [(np.linspace(0,w,50)),(np.linspace(0,h,50))]
grid=[i.astype(int) for i in lince]
midX,midY=grid[0][:-1]+grid[0][1]//2,grid[1][:-1]+grid[1][1]//2
clock = pygame.time.Clock()
clock.tick(5)
def reset():
    screen.fill(black)
    for a in grid[0]:
        for b in grid[1]:
            pygame.draw.rect(screen, white,(int(a), int(b),grid[0][1],grid[1][1]), 1)
    print("Board reseted")
    pygame.display.update()

class DB:
    name=""
    #db acces
    con=""
    cur=""
    def __init__(self,dBname) -> None:
        self.name=f"{dBname}.db"

    def p(self)->None:
        print(self.name)
    def connect(self)->None:
        self.con=sql.connect(self.name)
        self.cur= self.con.cursor()
    def createTable(self, nameTable)->None:
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {nameTable} (x, y, sur)""")
        print(f'Table "{nameTable}" was created')
    def dropTable(self, name):
        self.cur.execute(f"""DROP TABLE IF EXISTS {name}""")
        print(f'Table "{name}" was dropped')
    def showTables(self):
        self.cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
        print(self.cur.fetchall())
    def insertValues(self, name, values, col=["x","y","sur"]):
        tmp1,tmp2="(","("
        
        for each in col:
            tmp1+=f"{each},"
            tmp2+="?,"
        tmp1=tmp1[:-1]+")"
        tmp2=tmp2[:-1]+")"
        self.cur.execute(f"""INSERT INTO {name} {tmp1} VALUES {tmp2}""", values)
        self.con.commit()
    def printValues(self, name, search="*"):
        try:
            self.cur.execute(f"SELECT {search} FROM {name}")
            rows = self.cur.fetchall()
            for row in rows:
                print(*row)
        except:
            print("No tables with that name")
    def returnValues(self, name, search="*"):
        lista=[]
        try:
            self.cur.execute(f"SELECT {search} FROM {name}")
            rows = self.cur.fetchall()
            for row in rows:
                lista.append(row)
        except:
            print("ERROR in returnValues()")
        return lista
    def findXY(self,name, x, y):
        self.cur.execute(f"SELECT * FROM {name} WHERE x = ? AND y = ?", (x,y))
        return self.cur.fetchone()
    def updateXY(self, name, col, value, x, y):
        sql = f''' UPDATE {name}
                SET {col} = ? 
                WHERE x = ? AND y = ?'''
        self.cur.execute(sql, [value, x, y])
        self.con.commit()


db=DB("LOL")
db.connect()
#print(db.name)
#db.createTable("life")
#db.dropTable("life")
#db.showTables()
#db.insertValues("life", [1,1,1])
#db.printValues("life")
#print(type(db.findXY("life", 1,1)))
#db.updateXY("life", "sur", 3, 1,1)






def around(x,y,lx,ly):
    tmp = [[x+a*lx,y+b*ly] for a in range(-1,2) for b in range(-1,2)]
    return tmp[:4]+tmp[5:]
def findCorner(x,y):
    print(x,y)
    return grid[0][np.argmin(np.abs(midX-x))], grid[1][np.argmin(np.abs(midY-y))]
    ##IM AM HERE
def makeRec(x,y,color=""):
    #Add dict with colors to chose
    pygame.draw.rect(screen, (0,255,0),(x, y,grid[0][1],grid[1][1]))
    pygame.display.update()
def logic():
    
def start():
    times=1
    db.createTable("life")
    while True:
        for a in midX:
            for b in midY:
                for each in around(a,b,grid[0][1],grid[1][1]):
                    if each[0] > 0 and each[1] > 0 and each[0] < grid[0][-1] and each[1] < grid[1][-1]:
                        check=screen.get_at(each)
                        if check !=black:
                            check = db.findXY("life", int(a), int(b))
                            if check == None:
                                db.insertValues("life", [int(a),int(b),1])
                            else:
                                db.updateXY("life", "sur", check[2]+1, int(a),int(b))
        #db.printValues("life")
        for each in db.returnValues("life", search="x,y"):
            cordx,cordy= findCorner(each[0], each[1])
            makeRec(cordx, cordy)
        db.dropTable("life")
        break
        



reset()
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.unicode == 's':
                print("s")
                start()
            if event.unicode == "r":
                reset()



        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            # get the mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            print("Mouse clicked at", mouse_x, mouse_y)
            diffx,diffy = np.abs(midX- mouse_x),np.abs( midY- mouse_y)

            ix = np.argmin(diffx)
            iy=np.argmin(diffy)
            nearest_values = grid[0][ix],grid[1][iy]
            pygame.draw.rect(screen, (255,0,0),(nearest_values[0], nearest_values[1],grid[0][1],grid[1][1]))
            pygame.display.update()
        


