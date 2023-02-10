# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 17:52:30 2023

@author: jesus
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from stl import mesh  # Need to install library

nx=50
ny=50
sc=4
sr=4
s=sc*sr
stack=False
genSTL=False
genPhotos=True

if stack==True:
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
else:
    fig, ax = plt.subplots(nrows=sr,ncols=sc,subplot_kw={"projection": "3d"})

c_p=np.linspace(5,-5,nx)
y=np.linspace(0,2,ny)
u_0=np.linspace(-3,3,s)

[c_p_m,y_m]=np.meshgrid(c_p,y)
if genSTL==True:
    c_p_i=c_p_m.flatten()
    y_i=y_m.flatten()
    inputData=np.array([y_i,c_p_i]).T
    tri = Delaunay(inputData)
    tris=tri.simplices
    data = np.zeros(len(tris)*s, dtype=mesh.Mesh.dtype)
    mobius_mesh = mesh.Mesh(data, remove_empty_areas=False)
    c_p_arr=np.array([[],[],[]])
    y_i_arr=np.array([[],[],[]])
    u_n_arr=np.array([[],[],[]])

k=0
for u_0Var in u_0:
    u_n=u_0Var*y_m+c_p_m*(y_m**2/2-y_m)
    if stack==True:
        surf = ax.plot_surface(c_p_m, y_m, u_n, cmap="coolwarm",\
                                      linewidth=0, antialiased=False)
    else:
        j=k%sc
        i=int((k-j)/sc)
        print(str(k)+"->"+str(i)+";"+str(j))
        surf = ax[i][j].plot_surface(c_p_m, y_m, u_n, cmap="coolwarm",\
                                    linewidth=0, antialiased=False)
    if genSTL==True:
        u_n_i=u_n.flatten()
        c_p_arr=np.append(c_p_arr, c_p_i[tris].T,axis=1)
        y_i_arr=np.append(y_i_arr,5*y_i[tris].T,axis=1)
        u_n_arr=np.append(u_n_arr,u_n_i[tris].T,axis=1)
    k=k+1
    
if genSTL==True:
    mobius_mesh.x[:] = c_p_arr.T
    mobius_mesh.y[:] = y_i_arr.T
    mobius_mesh.z[:] = u_n_arr.T  
    mobius_mesh.save('CPSculpture.stl')   

if genPhotos==True:
    if stack==True:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.grid(False)
        az=[270,  0, 90,180]
        el=[  0,  0,  0,  0] 
        ax.set_xlabel("Pressure Gradient")
        ax.set_ylabel("Wall Distanceres")
        ax.set_zlabel("Velocity in X-Direction")
        for i in range(len(az)):
            ax.view_init(elev=el[i], azim=az[i])
            plt.savefig(f"CPSculpture_az{az[i]}_el{el[i]}.png",dpi=300)
    else:
        plt.savefig("CPSculptureSliced.png",dpi=300)
#%%
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.spatial import Delaunay
# from stl import mesh  # Need to install library

# c_p=np.linspace(5,-5,10)
# y=np.linspace(0,2,10)
# [c_p_m,y_m]=np.meshgrid(c_p,y)

# u_n=1*y_m+c_p_m*(y_m**2/2-y_m)
# u_n_i=u_n.flatten()
# ax = plt.axes(projection='3d')
# tris=tri.simplices
# ax.plot_trisurf(c_p_i, y_i, u_n_i, triangles=tri.simplices, cmap=plt.cm.Spectral)
# plt.show()
# #Create mesh




