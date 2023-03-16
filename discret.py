import matplotlib.pyplot as plt
import numpy as np
with open ('examp2.txt','r') as f :
    Data = [i.rstrip() for i in f]
    
odometria=[]
lidar=[]
lidar_coord=np.ndarray(shape=(0,2),dtype=float)
lidar_cloud=np.ndarray(shape=(0,2),dtype=float)
x_cloud=[]
y_cloud=[]
vrem=0

for i in range(len(Data)-1):
    Data[i]=Data[i].split(';')
    odometria.append(Data[i][0].split(','))
    lidar.append(Data[i][1].split(','))
for i in range (len(odometria)):
    for j in range(len(odometria[0])):
        odometria[i][j]=float(odometria[i][j])
for i in range (len(lidar)):
    for j in range(len(lidar[0])):
        lidar[i][j]=float(lidar[i][j])
odometria=np.array(odometria)
lidar=np.array(lidar)

vid=[]
vrem=2.0944 #120grad v rad :)
for i in range (len(lidar[0])):
    vid.append(vrem-i*0.0061)
vid=np.array(vid)

for i in range(len(odometria)):
    lidar_coord=np.append(lidar_coord,
                          [[odometria[i][0]+0.3*np.cos(odometria[i][2]),
                            odometria[i][1]+0.3*np.sin(odometria[i][2])]],
                            axis=0)
    
maxx=-99
maxy=-99
a=[0,0]
b=[0,0]
c=0
for i in range(len(lidar)):
    for j in range(70, len(lidar[0])-70):
        if lidar[i][j]<=4.35:
            lidar_cloud=np.append(lidar_cloud,
                                  [[lidar_coord[i][0] + lidar[i][j]*np.cos(odometria[i][2] + vid[j]),
                                    lidar_coord[i][1] + lidar[i][j]*np.sin(odometria[i][2] + vid[j])]],
                                    axis=0)
            if lidar_cloud[c][0]>maxx:
                maxx=lidar_cloud[c][0]
                a[0]=round(maxx, 1)
                a[1]=round(lidar_cloud[c][1], 1)
            if lidar_cloud[c][1]>maxy:
                maxy=lidar_cloud[c][1]
                b[0]=round(lidar_cloud[c][0], 1)
                b[1]=round(maxy, 1)
            c+=1
c=0
alp=0.0017 #0.1 grad
o=0
while True:
    if abs(a[0]-b[0])>0.01:
        a[0]=a[0]*np.cos(alp)+a[1]*np.sin(alp)
        a[1]=a[1]*np.cos(alp)-a[0]*np.sin(alp)
        
        b[0]=b[0]*np.cos(alp)+b[1]*np.sin(alp)
        b[1]=b[1]*np.cos(alp)-b[0]*np.sin(alp)
        o+=1
    else:
        break
for i in range(len(odometria)):
    odometria[i][0]=odometria[i][0]*np.cos(o/10*np.pi/180) + odometria[i][1]*np.sin(o/10*np.pi/180)
    odometria[i][1]=odometria[i][1]*np.cos(o/10*np.pi/180) - odometria[i][0]*np.sin(o/10*np.pi/180)   
    lidar_coord[i][0]=lidar_coord[i][0]*np.cos(o/10*np.pi/180) + lidar_coord[i][1]*np.sin(o/10*np.pi/180)
    lidar_coord[i][1]=lidar_coord[i][1]*np.cos(o/10*np.pi/180) - lidar_coord[i][0]*np.sin(o/10*np.pi/180)
for i in range(len(lidar_cloud)):
    x_cloud.append(lidar_cloud[i][0]*np.cos(o/10*np.pi/180) + lidar_cloud[i][1]*np.sin(o/10*np.pi/180))
    y_cloud.append(lidar_cloud[i][1]*np.cos(o/10*np.pi/180) - lidar_cloud[i][0]*np.sin(o/10*np.pi/180))
# отстройка местности
x_new=[]
y_new=[]
for i in range(len(lidar_cloud)):
    x_new.append(x_cloud[i])
    y_new.append(y_cloud[i])
minx=min(x_new)
miny=min(y_new)
for i in range(len(lidar_cloud)):
    x_new[i]=(x_cloud[i]-minx)
    y_new[i]=(y_cloud[i]-miny)
plt.plot(x_new, y_new,'.g', markersize=6)
plt.title('Я карта')
plt.show
#дискретизация
dx=max(x_new)-min(x_new)
dy=max(y_new)-min(y_new)
dis=float(input('введите шаг дискретизации в диапазоне 0.1<=шаг<=1:'))
flag=True
while flag:
    if(0.1<=dis<=1):
        dop=dis*0.25
        flag=False
    else:
        dis=float(input('введите шаг дискретизации в диапазоне 0.1<=шаг<=1:'))
height=int(dx//dis)
width=int(dy//dis)
A=np.zeros((width, height))
for i in range(len(A)):
    for j in range(len(A[i])):
        for k in range(len(x_new)):
            x_r=j*dis
            x_l=x_r-dis
            y_down=i*dis
            y_up=y_down-dis
            if (x_l+x_r)/2-dop<=x_new[k]<=(x_l+x_r)/2+dop and (y_up+y_down)/2-dop<=y_new[k]<=(y_up+y_down)/2+dop:
                A[i][j]+=1
np.save(f'test{dis}', A)
A=np.load(f'test{dis}.npy')
for i in range(len(A)):
    for j in range(len(A[i])):
        if A[i][j]>2:
            A[i][j]=255
        else:
            A[i][j]=0
plt.matshow(A)
plt.show()