import pygame as pg
import numpy as np
import random

pg.init()
def rast(start_0,start_1, finish):
    x=abs(start_0-finish[0])
    y=abs(start_1-finish[1])
    #p=((x**2+y**2)**0.5) #евклидово расстояние
    p=x+y #манхэтонское расстояние
    #p=max(x,y) #расстояние чебышёва
    return p
def rast1(start_0,start_1, finish):
    x=abs(start_0-finish//10000)
    y=abs(start_1-finish%10000)
    p=((x**2+y**2)**0.5)
    return p
text='test0.3.npy'# выбор карты с разной дискретизацией, доступны с шагом 0.1; 0.15; 0.2; 0.25; 0.3; 0.35; 0.5
A=np.load(text)
A=np.transpose(A)

#обработка матрицы
for i in range(len(A)):
    for j in range(len(A[i])):
        if A[i][j]>2:
            A[i][j]=255
        else:
            A[i][j]=0  
clock=pg.time.Clock()

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
PURPLE=(255,0,255)
TIGER=(253,106,2)
dis=float(text[4:-4])
scale=500/(dis*len(A))
st=int(dis*scale)
step=3*st #шаг для RRT
WIDTH=int(dis*len(A)*scale-(int(dis*len(A)*scale)%st))
HIGH=int(dis*len(A[0])*scale-(int(dis*len(A[0])*scale)%st))

#создание расширенной матрицы
A1=np.zeros((len(A)+2, len(A[0])+2))
for i in range(len(A1)):
    for j in range(len(A1[i])):
        if (i==0) | (i==len(A1)-1):
            A1[i][j]=-1
        if (j==0) | (j==len(A1[i])-1):
            A1[i][j]=-1
for i in range(1, len(A1)-1):
    for j in range(1, len(A1[i])-1):  
        A1[i][j]=A[i-1][j-1]
FPS=30
fl=True
wind=pg.display.set_mode((WIDTH,HIGH))
pg.display.set_caption('Поиск пути')
wind.fill(WHITE)

#отстройка местности
for i in range(len(A)):
    for j in range(len(A[i])):
        if A[i][j] == 255:
            pg.draw.rect(wind, BLACK, (i * st, j * st, st, st))

#отстройка сетки
for i in range(0,WIDTH+st, st):
    pg.draw.line(wind, RED, [i,0], [i,HIGH], 1)
for i in range(0,HIGH+st, st):
    pg.draw.line(wind, RED, [0,i], [WIDTH,i], 1)
    
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print('!! Выбран алгоритм поиска Дейкстры                              !!')
print('!! Для выбора другого алгоритма используйте клавиши "1","2","3" !!')
print('!! 1 - алгоритм поиска Дейкстры                                 !!')
print('!! 2 - алгоритм поиска A*                                       !!')
print('!! 3 - алгоритм поиска RRT                                      !!')
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
pg.display.update()
c=0
h=0
z=0
count=1
cloud=[]
path={}
start=[]
finish=[]
next=[]
#создание матрицы расстояний
B=np.zeros((len(A1), len(A1[0])))
for i in range(len(B)):
    for j in range(len(B[i])):
        B[i][j]=99999999

#обработка всех событий
while fl:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            fl=False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_1:#ДЕЙКСТРА
                count=1
                print('Алгоритм поиска Дейкстры')
                wind.fill(WHITE)
                for i in range(len(A)):
                    for j in range(len(A[i])):
                        if A[i][j] == 255:
                            pg.draw.rect(wind, BLACK, (i * st, j * st, st, st))
                for i in range(0,WIDTH+st, st):
                    pg.draw.line(wind, RED, [i,0], [i,HIGH], 1)
                for i in range(0,HIGH+st, st):
                    pg.draw.line(wind, RED, [0,i], [WIDTH,i], 1)
                c=0
                path={}
                next=[]
            elif event.key == pg.K_2:
                count=2
                print('Алгоритм поиска А*')
                wind.fill(WHITE)
                for i in range(len(A)):
                    for j in range(len(A[i])):
                        if A[i][j] == 255:
                            pg.draw.rect(wind, BLACK, (i * st, j * st, st, st))
                for i in range(0,WIDTH+st, st):
                    pg.draw.line(wind, RED, [i,0], [i,HIGH], 1)
                for i in range(0,HIGH+st, st):
                    pg.draw.line(wind, RED, [0,i], [WIDTH,i], 1)
                c=0
                path={}
                next=[]
            elif event.key == pg.K_3:
                count=3
                print('Алгоритм поиска RRT')
                wind.fill(WHITE)
                for i in range(len(A)):
                    for j in range(len(A[i])):
                        if A[i][j] == 255:
                            pg.draw.rect(wind, BLACK, (i * st, j * st, st, st))
                for i in range(0,WIDTH+st, st):
                    pg.draw.line(wind, RED, [i,0], [i,HIGH], 1)
                for i in range(0,HIGH+st, st):
                    pg.draw.line(wind, RED, [0,i], [WIDTH,i], 1)
                c=0
                path={}
                next=[]
                cloud=[]
        if event.type == pg.MOUSEBUTTONDOWN:
            #ДЕЙКСТРА
            if count==1:
                if(event.button == 1)&(c==0):
                    path={}
                    next=[]
                    for i in range(len(B)):
                        for j in range(len(B[i])):
                            B[i][j]=99999999
                    for i in range(1, len(A1)-1):
                        for j in range(1, len(A1[i])-1):  
                            A1[i][j]=A[i-1][j-1]
                    start=event.pos
                    start_number=[start[0]//st, start[1]//st]
                    B[start_number[0]+1][start_number[1]+1]=0
                    next.append([0, start_number[0], start_number[1]])
                    start_clone=start_number.copy()
                    if A[start_number[0]][start_number[1]]!=255:
                        pg.draw.circle(wind, RED, (start_number[0]*st+st/2,start_number[1]*st+st/2),3)
                        while len(next)>0:
                            start_clone[0], start_clone[1] = next[0][1], next[0][2]
                            if (A1[start_clone[0]+1+1][start_clone[1]+1]!=255) & (A1[start_clone[0]+1+1][start_clone[1]+1]!=-1):
                                if round(B[start_clone[0]+1][start_clone[1]+1]+1,3)<round(B[start_clone[0]+1+1][start_clone[1]+1],3):
                                    B[start_clone[0]+1+1][start_clone[1]+1]=round(B[start_clone[0]+1][start_clone[1]+1]+1,3)
                                    next.append([B[start_clone[0]+1+1][start_clone[1]+1],start_clone[0]+1, start_clone[1]])
                                    path[(start_clone[0]+1)*10000+start_clone[1]]=start_clone[0]*10000+start_clone[1]

                            if (A1[start_clone[0]+1+1][start_clone[1]+1+1]!=255) & (A1[start_clone[0]+1+1][start_clone[1]+1+1]!=-1):
                                if round(B[start_clone[0]+1][start_clone[1]+1]+1.4142,3)<round(B[start_clone[0]+1+1][start_clone[1]+1+1],3):
                                    B[start_clone[0]+1+1][start_clone[1]+1+1]=round(B[start_clone[0]+1][start_clone[1]+1]+1.4142, 3)
                                    next.append([B[start_clone[0]+1+1][start_clone[1]+1+1],start_clone[0]+1, start_clone[1]+1])
                                    path[(start_clone[0]+1)*10000+start_clone[1]+1]=start_clone[0]*10000+start_clone[1]

                            if (A1[start_clone[0]+1][start_clone[1]+1+1]!=255) & (A1[start_clone[0]+1][start_clone[1]+1+1]!=-1):
                                if round(B[start_clone[0]+1][start_clone[1]+1]+1,3)<round(B[start_clone[0]+1][start_clone[1]+1+1],3):
                                    B[start_clone[0]+1][start_clone[1]+1+1]=round(B[start_clone[0]+1][start_clone[1]+1]+1, 3)
                                    next.append([B[start_clone[0]+1][start_clone[1]+1+1],start_clone[0], start_clone[1]+1])
                                    path[(start_clone[0])*10000+start_clone[1]+1]=start_clone[0]*10000+start_clone[1]

                            if (A1[start_clone[0]-1+1][start_clone[1]+1+1]!=255) & (A1[start_clone[0]-1+1][start_clone[1]+1+1]!=-1):
                                if round(B[start_clone[0]+1][start_clone[1]+1]+1.4142,3)<round(B[start_clone[0]-1+1][start_clone[1]+1+1],3):
                                    B[start_clone[0]-1+1][start_clone[1]+1+1]=round(B[start_clone[0]+1][start_clone[1]+1]+1.4142,3)
                                    next.append([B[start_clone[0]+1-1][start_clone[1]+1+1],start_clone[0]-1, start_clone[1]+1])
                                    path[(start_clone[0]-1)*10000+start_clone[1]+1]=start_clone[0]*10000+start_clone[1]

                            if (A1[start_clone[0]-1+1][start_clone[1]+1]!=255) & (A1[start_clone[0]-1+1][start_clone[1]+1]!=-1):
                                if round(B[start_clone[0]+1][start_clone[1]+1]+1,3)<round(B[start_clone[0]-1+1][start_clone[1]+1],3):
                                    B[start_clone[0]-1+1][start_clone[1]+1]=round(B[start_clone[0]+1][start_clone[1]+1]+1,3)
                                    next.append([B[start_clone[0]-1+1][start_clone[1]+1],start_clone[0]-1, start_clone[1]])
                                    path[(start_clone[0]-1)*10000+start_clone[1]]=start_clone[0]*10000+start_clone[1]

                            if (A1[start_clone[0]-1+1][start_clone[1]-1+1]!=255) & (A1[start_clone[0]-1+1][start_clone[1]-1+1]!=-1):
                                if round(B[start_clone[0]+1][start_clone[1]+1]+1.4142,3)<round(B[start_clone[0]-1+1][start_clone[1]-1+1],3):
                                    B[start_clone[0]-1+1][start_clone[1]-1+1]=round(B[start_clone[0]+1][start_clone[1]+1]+1.4142,3)
                                    next.append([B[start_clone[0]-1+1][start_clone[1]-1+1],start_clone[0]-1, start_clone[1]-1])
                                    path[(start_clone[0]-1)*10000+start_clone[1]-1]=start_clone[0]*10000+start_clone[1]

                            if (A1[start_clone[0]+1][start_clone[1]-1+1]!=255) & (A1[start_clone[0]+1][start_clone[1]-1+1]!=-1):
                                if round(B[start_clone[0]+1][start_clone[1]+1]+1,3)<round(B[start_clone[0]+1][start_clone[1]-1+1],3):
                                    B[start_clone[0]+1][start_clone[1]+1-1]=round(B[start_clone[0]+1][start_clone[1]+1]+1,3)
                                    next.append([B[start_clone[0]+1][start_clone[1]-1+1],start_clone[0], start_clone[1]-1])
                                    path[(start_clone[0])*10000+start_clone[1]-1]=start_clone[0]*10000+start_clone[1]

                            if (A1[start_clone[0]+1+1][start_clone[1]-1+1]!=255) & (A1[start_clone[0]+1+1][start_clone[1]-1+1]!=-1):
                                if round(B[start_clone[0]+1][start_clone[1]+1]+1.4142,3)<round(B[start_clone[0]+1+1][start_clone[1]-1+1],3):
                                    B[start_clone[0]+1+1][start_clone[1]-1+1]=round(B[start_clone[0]+1][start_clone[1]+1]+1.4142,3)
                                    next.append([B[start_clone[0]+1+1][start_clone[1]-1+1],start_clone[0]+1, start_clone[1]-1])
                                    path[(start_clone[0]+1)*10000+start_clone[1]-1]=start_clone[0]*10000+start_clone[1]

                            A1[start_clone[0]+1][start_clone[1]+1]=255
                            del next[0]
                            next.sort()
                        c=1
                elif(event.button == 1)&(c == 1):
                    path[start_number[0]*10000+start_number[1]]=start_number[0]*10000+start_number[1]
                    finish=event.pos
                    finish_number=[finish[0]//st, finish[1]//st]
                    if A[finish_number[0]][finish_number[1]]!=255:
                        pg.draw.circle(wind, GREEN, (finish_number[0]*st+st/2,finish_number[1]*st+st/2),3)
                        fin=finish_number[0]*10000+finish_number[1]
                        while (fin in path.keys()):
                            if path[fin]!=fin:
                                pg.draw.line(wind,BLUE,[(fin//10000+0.5)*st,(fin%10000+0.5)*st],[(path[fin]//10000+0.5)*st, (path[fin]%10000+0.5)*st],3)
                                pg.display.update()
                                fin=path[fin]     
                            else:
                                break
                        else:
                            print('Проехать невозможно!')
                        c=2
                elif(event.button == 1)&(c==2):
                    wind.fill(WHITE)
                    for i in range(len(A)):
                        for j in range(len(A[i])):
                            if A[i][j] == 255:
                                pg.draw.rect(wind, BLACK, (i * st, j * st, st, st))
                    for i in range(0,WIDTH+st, st):
                        pg.draw.line(wind, RED, [i,0], [i,HIGH], 1)
                    for i in range(0,HIGH+st, st):
                        pg.draw.line(wind, RED, [0,i], [WIDTH,i], 1)
                    c=0
            #А*
            elif count==2:
                if(event.button == 1)&(c==0):
                    path={}
                    next=[]
                    for i in range(len(B)):
                        for j in range(len(B[i])):
                            B[i][j]=99999999
                    for i in range(1, len(A1)-1):
                        for j in range(1, len(A1[i])-1):  
                            A1[i][j]=A[i-1][j-1]
                    start=event.pos
                    start_number=[start[0]//st, start[1]//st]
                    B[start_number[0]+1][start_number[1]+1]=0
                    next.append([0, start_number[0], start_number[1],0,0])
                    start_clone=start_number.copy()
                    if A[start_number[0]][start_number[1]]!=255:
                        pg.draw.circle(wind, RED, (start_number[0]*st+st/2,start_number[1]*st+st/2),3)
                        c=1
                elif(event.button == 1)&(c == 1):
                    path[start_number[0]*10000+start_number[1]]=start_number[0]*10000+start_number[1]
                    finish=event.pos
                    finish_number=[finish[0]//st, finish[1]//st]
                    if A[finish_number[0]][finish_number[1]]!=255:
                        pg.draw.circle(wind, GREEN, (finish_number[0]*st+st/2,finish_number[1]*st+st/2),3)
                        while len(next)>0:
                            start_clone[0], start_clone[1] = next[0][1], next[0][2]
                            if (next[0][1]==finish_number[0]) & (next[0][2]==finish_number[1]):
                                break
                            if (A1[start_clone[0]+1+1][start_clone[1]+1]!=255) & (A1[start_clone[0]+1+1][start_clone[1]+1]!=-1):
                                if round(B[start_clone[0]+1][start_clone[1]+1]+1,3)<round(B[start_clone[0]+1+1][start_clone[1]+1],3):
                                    B[start_clone[0]+1+1][start_clone[1]+1]=round(B[start_clone[0]+1][start_clone[1]+1]+1,3)
                                    for i in range(len(next)):
                                        if (next[i][1]==start_clone[0]+1) & (next[i][2]==start_clone[1]):
                                            del next[i]
                                            break
                                    next.append([B[start_clone[0]+1+1][start_clone[1]+1]+rast(start_clone[0]+1,start_clone[1], finish_number),start_clone[0]+1, start_clone[1],
                                                 B[start_clone[0]+1+1][start_clone[1]+1],rast(start_clone[0]+1,start_clone[1], finish_number)])
                                    path[(start_clone[0]+1)*10000+start_clone[1]]=start_clone[0]*10000+start_clone[1]

                            if (A1[start_clone[0]+1+1][start_clone[1]+1+1]!=255) & (A1[start_clone[0]+1+1][start_clone[1]+1+1]!=-1):
                                if round(B[start_clone[0]+1][start_clone[1]+1]+1.4142,3)<round(B[start_clone[0]+1+1][start_clone[1]+1+1],3):
                                    B[start_clone[0]+1+1][start_clone[1]+1+1]=round(B[start_clone[0]+1][start_clone[1]+1]+1.4142, 3)
                                    for i in range(len(next)):
                                        if (next[i][1]==start_clone[0]+1) & (next[i][2]==start_clone[1]+1):
                                            del next[i]
                                            break
                                    next.append([B[start_clone[0]+1+1][start_clone[1]+1+1]+rast(start_clone[0]+1,start_clone[1]+1, finish_number),start_clone[0]+1, start_clone[1]+1,
                                                B[start_clone[0]+1+1][start_clone[1]+1+1],rast(start_clone[0]+1,start_clone[1]+1, finish_number)])
                                    path[(start_clone[0]+1)*10000+start_clone[1]+1]=start_clone[0]*10000+start_clone[1]

                            if (A1[start_clone[0]+1][start_clone[1]+1+1]!=255) & (A1[start_clone[0]+1][start_clone[1]+1+1]!=-1):
                                if round(B[start_clone[0]+1][start_clone[1]+1]+1,3)<round(B[start_clone[0]+1][start_clone[1]+1+1],3):
                                    B[start_clone[0]+1][start_clone[1]+1+1]=round(B[start_clone[0]+1][start_clone[1]+1]+1, 3)
                                    for i in range(len(next)):
                                        if (next[i][1]==start_clone[0]) & (next[i][2]==start_clone[1]+1):
                                            del next[i]
                                            break
                                    next.append([B[start_clone[0]+1][start_clone[1]+1+1]+rast(start_clone[0],start_clone[1]+1, finish_number),start_clone[0], start_clone[1]+1,
                                                B[start_clone[0]+1][start_clone[1]+1+1],rast(start_clone[0],start_clone[1]+1, finish_number)])
                                    path[(start_clone[0])*10000+start_clone[1]+1]=start_clone[0]*10000+start_clone[1]

                            if (A1[start_clone[0]-1+1][start_clone[1]+1+1]!=255) & (A1[start_clone[0]-1+1][start_clone[1]+1+1]!=-1):
                                if round(B[start_clone[0]+1][start_clone[1]+1]+1.4142,3)<round(B[start_clone[0]-1+1][start_clone[1]+1+1],3):
                                    B[start_clone[0]-1+1][start_clone[1]+1+1]=round(B[start_clone[0]+1][start_clone[1]+1]+1.4142,3)
                                    for i in range(len(next)):
                                        if (next[i][1]==start_clone[0]-1) & (next[i][2]==start_clone[1]+1):
                                            del next[i]
                                            break
                                    next.append([B[start_clone[0]+1-1][start_clone[1]+1+1]+rast(start_clone[0]-1,start_clone[1]+1, finish_number),start_clone[0]-1, start_clone[1]+1,
                                                B[start_clone[0]+1-1][start_clone[1]+1+1],rast(start_clone[0]-1,start_clone[1]+1, finish_number)])
                                    path[(start_clone[0]-1)*10000+start_clone[1]+1]=start_clone[0]*10000+start_clone[1]

                            if (A1[start_clone[0]-1+1][start_clone[1]+1]!=255) & (A1[start_clone[0]-1+1][start_clone[1]+1]!=-1):
                                if round(B[start_clone[0]+1][start_clone[1]+1]+1,3)<round(B[start_clone[0]-1+1][start_clone[1]+1],3):
                                    B[start_clone[0]-1+1][start_clone[1]+1]=round(B[start_clone[0]+1][start_clone[1]+1]+1,3)
                                    for i in range(len(next)):
                                        if (next[i][1]==start_clone[0]-1) & (next[i][2]==start_clone[1]):
                                            del next[i]
                                            break
                                    next.append([B[start_clone[0]-1+1][start_clone[1]+1]+rast(start_clone[0]-1,start_clone[1], finish_number),start_clone[0]-1, start_clone[1],
                                                 B[start_clone[0]-1+1][start_clone[1]+1],rast(start_clone[0]-1,start_clone[1], finish_number)])
                                    path[(start_clone[0]-1)*10000+start_clone[1]]=start_clone[0]*10000+start_clone[1]

                            if (A1[start_clone[0]-1+1][start_clone[1]-1+1]!=255) & (A1[start_clone[0]-1+1][start_clone[1]-1+1]!=-1):
                                if round(B[start_clone[0]+1][start_clone[1]+1]+1.4142,3)<round(B[start_clone[0]-1+1][start_clone[1]-1+1],3):
                                    B[start_clone[0]-1+1][start_clone[1]-1+1]=round(B[start_clone[0]+1][start_clone[1]+1]+1.4142,3)
                                    for i in range(len(next)):
                                        if (next[i][1]==start_clone[0]-1) & (next[i][2]==start_clone[1]-1):
                                            del next[i]
                                            break
                                    next.append([B[start_clone[0]-1+1][start_clone[1]-1+1]+rast(start_clone[0]-1,start_clone[1]-1, finish_number),start_clone[0]-1, start_clone[1]-1,
                                                 B[start_clone[0]-1+1][start_clone[1]-1+1],rast(start_clone[0]-1,start_clone[1]-1, finish_number)])
                                    path[(start_clone[0]-1)*10000+start_clone[1]-1]=start_clone[0]*10000+start_clone[1]

                            if (A1[start_clone[0]+1][start_clone[1]-1+1]!=255) & (A1[start_clone[0]+1][start_clone[1]-1+1]!=-1):
                                if round(B[start_clone[0]+1][start_clone[1]+1]+1,3)<round(B[start_clone[0]+1][start_clone[1]-1+1],3):
                                    B[start_clone[0]+1][start_clone[1]+1-1]=round(B[start_clone[0]+1][start_clone[1]+1]+1,3)
                                    for i in range(len(next)):
                                        if (next[i][1]==start_clone[0]) & (next[i][2]==start_clone[1]-1):
                                            del next[i]
                                            break
                                    next.append([B[start_clone[0]+1][start_clone[1]-1+1]+rast(start_clone[0],start_clone[1]-1, finish_number),start_clone[0], start_clone[1]-1,
                                                 B[start_clone[0]+1][start_clone[1]-1+1],rast(start_clone[0],start_clone[1]-1, finish_number)])
                                    path[(start_clone[0])*10000+start_clone[1]-1]=start_clone[0]*10000+start_clone[1]

                            if (A1[start_clone[0]+1+1][start_clone[1]-1+1]!=255) & (A1[start_clone[0]+1+1][start_clone[1]-1+1]!=-1):
                                if round(B[start_clone[0]+1][start_clone[1]+1]+1.4142,3)<round(B[start_clone[0]+1+1][start_clone[1]-1+1],3):
                                    B[start_clone[0]+1+1][start_clone[1]-1+1]=round(B[start_clone[0]+1][start_clone[1]+1]+1.4142,3)
                                    for i in range(len(next)):
                                        if (next[i][1]==start_clone[0]+1) & (next[i][2]==start_clone[1]-1):
                                            del next[i]
                                            break
                                    next.append([B[start_clone[0]+1+1][start_clone[1]-1+1]+rast(start_clone[0]+1,start_clone[1]-1, finish_number),start_clone[0]+1, start_clone[1]-1,
                                                 B[start_clone[0]+1+1][start_clone[1]-1+1],rast(start_clone[0]+1,start_clone[1]-1, finish_number)])
                                    path[(start_clone[0]+1)*10000+start_clone[1]-1]=start_clone[0]*10000+start_clone[1]

                            A1[start_clone[0]+1][start_clone[1]+1]=255
                            del next[0]
                            next.sort()
                        fin=finish_number[0]*10000+finish_number[1]
                        while (fin in path.keys()):
                            if path[fin]!=fin:
                                pg.draw.line(wind,BLUE,[(fin//10000+0.5)*st,(fin%10000+0.5)*st],[(path[fin]//10000+0.5)*st, (path[fin]%10000+0.5)*st],3)
                                pg.display.update()
                                fin=path[fin]     
                            else:
                                break
                        else:
                            print('Проехать невозможно!')
                        c=2
                elif(event.button == 1)&(c==2):
                    wind.fill(WHITE)
                    for i in range(len(A)):
                        for j in range(len(A[i])):
                            if A[i][j] == 255:
                                pg.draw.rect(wind, BLACK, (i * st, j * st, st, st))
                    for i in range(0,WIDTH+st, st):
                        pg.draw.line(wind, RED, [i,0], [i,HIGH], 1)
                    for i in range(0,HIGH+st, st):
                        pg.draw.line(wind, RED, [0,i], [WIDTH,i], 1)
                    c=0
            #RRT
            elif count==3:
                if(event.button == 1)&(c==0):
                    A1=np.zeros((len(A)+2, len(A[0])+2))
                    for i in range(len(A1)):
                        for j in range(len(A1[i])):
                            if (i==0) | (i==len(A1)-1):
                                A1[i][j]=-1
                            if (j==0) | (j==len(A1[i])-1):
                                A1[i][j]=-1
                    for i in range(1, len(A1)-1):
                        for j in range(1, len(A1[i])-1):  
                            A1[i][j]=A[i-1][j-1]
                    path={}
                    start=event.pos
                    start_number=[start[0]//st, start[1]//st]
                    if A[start_number[0]][start_number[1]]!=255:
                        pg.draw.circle(wind, RED, (start_number[0]*st+st/2,start_number[1]*st+st/2),3)
                        path[start_number[0]*10000+start_number[1]]=start_number[0]*10000+start_number[1]
                        cloud.append(start_number[0]*10000+start_number[1])
                        c=1
                elif(event.button == 1)&(c == 1):
                    finish=event.pos
                    finish_number=[finish[0]//st, finish[1]//st]
                    fin=[]
                    for i in range (-1, 2):
                        for j in range(-1, 2):
                            if A1[finish_number[0]+1+i][finish_number[1]+1+j]!=-1:
                                fin.append((finish_number[0]+i)*10000+finish_number[1]+j)
                    if A[finish_number[0]][finish_number[1]]!=255:
                        pg.draw.circle(wind, GREEN, (finish_number[0]*st+st/2,finish_number[1]*st+st/2),3)                    
                        pg.draw.rect(wind, GREEN,(finish_number[0]*st-st, finish_number[1]*st-st, 3*st+1, 3*st+1), 1)
                        if start_number[0]*10000+start_number[1] in fin:
                            print('Вы на финише')
                            c=4
                        else:
                            c=2
                elif(event.button == 1)&(c == 2):
                    go=True
                    #while go: 
                    while z!=2000: 
                        rand_x=random.randint(0,len(A)-1)
                        rand_y=random.randint(0,len(A[0])-1)
                        while (A[rand_x][rand_y]==255) | (rand_x*10000+rand_y in cloud):
                            rand_x=random.randint(0,len(A)-1)
                            rand_y=random.randint(0,len(A[0])-1)
                        if (A[rand_x][rand_y]!=255):
                            point=99999
                            for i in range(len(cloud)):
                                r=rast1(rand_x,rand_y,cloud[i])
                                if r<point:
                                    point=r
                                    naim=cloud[i]
                            rast_x=rand_x-naim//10000
                            rast_y=rand_y-naim%10000
                            for i in range(int(step)-1):
                                x_new=int(naim//10000*st+st/2+rast_x*i/point)
                                y_new=int(naim%10000*st+st/2+rast_y*i/point)
                                if (0<x_new<WIDTH)&(0<y_new<HIGH):
                                    if (A[x_new//st][y_new//st]==255):                                       
                                        x_new=int(naim//10000*st+st/2+rast_x*(i-1)/point)
                                        y_new=int(naim%10000*st+st/2+rast_y*(i-1)/point)
                                        break
                                else:
                                    x_new=int(naim//10000*st+st/2+rast_x*(i-1)/point)
                                    y_new=int(naim%10000*st+st/2+rast_y*(i-1)/point)
                                    break
                            if not (x_new//st*10000+y_new//st in cloud):
                                rast_x=x_new//st-naim//10000
                                rast_y=y_new//st-naim%10000
                                point=rast1(x_new//st, y_new//st, naim)
                                for i in range(int(step)-1):
                                    x_new=int(naim//10000*st+st/2+rast_x*i/point)
                                    y_new=int(naim%10000*st+st/2+rast_y*i/point)
                                    if (0<x_new<WIDTH)&(0<y_new<HIGH):
                                        if (A[x_new//st][y_new//st]==255):                                       
                                            x_new=int(naim//10000*st+st/2+rast_x*(i-1)/point)
                                            y_new=int(naim%10000*st+st/2+rast_y*(i-1)/point)
                                            break
                                    else:
                                        x_new=int(naim//10000*st+st/2+rast_x*(i-1)/point)
                                        y_new=int(naim%10000*st+st/2+rast_y*(i-1)/point)
                                        break
                                cloud.append(x_new//st*10000+y_new//st)
                                path[x_new//st*10000+y_new//st]=naim
                                pg.draw.circle(wind, BLUE, (x_new//st*st+st/2,y_new//st*st+st/2),3)
                        z+=1
                        if (x_new//st*10000+y_new//st) in fin:
                            final=x_new//st*10000+y_new//st
                            c=3
                            break
                        if z == 2000:
                            print('Путь не найден :(')
                            c=4
                elif(event.button == 1)&(c == 3):
                    while (final in path.keys()):
                        if path[final]!=final:
                            pg.draw.line(wind,BLUE,[(final//10000+0.5)*st,(final%10000+0.5)*st],[(path[final]//10000+0.5)*st, (path[final]%10000+0.5)*st],3)
                            pg.display.update()
                            final=path[final]     
                        else:
                            c=4
                            break
                    else:
                        print('Пути нет!')
                elif(event.button == 1)&(c == 4):
                    z=0
                    cloud=[]
                    wind.fill(WHITE)
                    for i in range(len(A)):
                        for j in range(len(A[i])):
                            if A[i][j] == 255:
                                pg.draw.rect(wind, BLACK, (i * st, j * st, st, st))
                    for i in range(0,WIDTH+st, st):
                        pg.draw.line(wind, RED, [i,0], [i,HIGH], 1)
                    for i in range(0,HIGH+st, st):
                        pg.draw.line(wind, RED, [0,i], [WIDTH,i], 1)
                    c=0
    pg.display.update()
    #pg.time.delay(30)      
    clock.tick(FPS)