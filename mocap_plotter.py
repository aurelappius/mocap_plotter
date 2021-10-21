import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import os
import csv
import statistics

#fig_proj = plt.title("3D Projection")
fig_proj = plt.figure() #projected plot

#fig_xyz = plt.title("XYZ Projection")
fig_xyz = plt.figure() #xyz plot

#fig_rpy = plt.title("Roll,Pitch,Yaw Projection")
fig_rpy = plt.figure() #roll,pitch,yaw plot


proj_plt = fig_proj.add_subplot(111, projection='3d')
x_plt = fig_xyz.add_subplot(311)
y_plt = fig_xyz.add_subplot(312)
z_plt = fig_xyz.add_subplot(313)
rol_plt = fig_rpy.add_subplot(311)
pit_plt = fig_rpy.add_subplot(312)
yaw_plt = fig_rpy.add_subplot(313)
header_list = ["Frame", "Framerate", "Latency", "x", "y", "z", "roll", "pitch", "yaw","err"]
pathToData = "data.csv"
################################################# Command line arguments
if len(sys.argv)==2:
	pathToData = sys.argv[1]
print("Loading " + pathToData + " ...")
################################################# Parameters
Start = 11300 #start frame
N = 750 #how many frames
Framerate = 100
POSMAX = [2000,2000,2000] #maximal allowed xyz values>

################################################# Read Data
FRA = pd.read_csv(pathToData, usecols=["Frame"],skiprows=Start,nrows=N, names=header_list).to_numpy()
ZeroFrame = FRA[0,0]
Time = (FRA - FRA[0,0])/Framerate
RPY = pd.read_csv(pathToData, usecols=["roll", "pitch", "yaw"],skiprows=Start,nrows=N, names=header_list).to_numpy()
POS = pd.read_csv(pathToData, usecols=["x", "y", "z"],skiprows=Start,nrows=N, names=header_list).to_numpy()

################################################# Prepare Data
#delete outlier
d=[0]
for i in range(0,len(POS[:,0])):
	if abs(POS[i,0]) > POSMAX[0] or abs(POS[i,1]) > POSMAX[1] or abs(POS[i,2]) > POSMAX[2]:
		d = np.append(i,d)
POS=np.delete(POS, d ,0)
RPY=np.delete(RPY, d ,0)
Time=np.delete(Time, d ,0)
#calculate mean 
MEAN = [statistics.mean(POS[:,0]), statistics.mean(POS[:,1]), statistics.mean(POS[:,2])]

################################################# Plot X,Y,Z
x_plt.scatter(Time,POS[:,0]-MEAN[0],marker='o',s=1)
x_plt.set_xlabel('time [s]')
x_plt.set_ylabel('X [m]')
y_plt.scatter(Time,POS[:,1]-MEAN[1],marker='o',s=1)
y_plt.set_xlabel('time [s]')
y_plt.set_ylabel('Y [m]')
z_plt.scatter(Time,POS[:,2]-MEAN[2],marker='o',s=1)
z_plt.set_xlabel('time [s]')
z_plt.set_ylabel('Z [m]')

plt.savefig(pathToData.split(".")[0] + "_xyz.png")
print("Saving " + pathToData.split(".")[0] + "_xyz.png ...")



################################################# Plot Roll,Pitch, Yaw
rol_plt.scatter(Time,RPY[:,0],marker='o',s=1)
rol_plt.set_xlabel('time [s]')
rol_plt.set_ylabel('roll [deg]')
pit_plt.scatter(Time,RPY[:,1],marker='o',s=1)
pit_plt.set_xlabel('time [s]')
pit_plt.set_ylabel('pitch [deg]')
yaw_plt.scatter(Time,RPY[:,2],marker='o',s=1)
yaw_plt.set_xlabel('time [s]')
yaw_plt.set_ylabel('yaw [deg]')

################################################# Plot Projection
proj_plt.scatter(POS[:,0]-MEAN[0],POS[:,1]-MEAN[1],POS[:,2]-MEAN[2],marker='o',s=1)
proj_plt.set_xlabel("X [m]")
proj_plt.set_ylabel("Y [m]")
proj_plt.set_zlabel("Z [m]")

################################################# Display Plots and Save them

plt.savefig(pathToData.split(".")[0] + ".png")
print("Saving " + pathToData.split(".")[0] + ".png ...")

plt.show()