import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import math
import os
import csv
import statistics

################################################# Parameters
Start = 1600  # start frame
N = 2000 # how many frames
label1 = "delay 1ms"

#two data set stettings
two_data_sets = 0  # set 0 to hide, 1 to show
Start2 = 750  # start frame second dataset
N2 = 1000  # how many frames second dataset
label2 = "delay 5ms"


Framerate = 100
show_square_ref = 0  # set 0 to hide, 1 to show
show_circle_ref = 0  # set 0 to hide, 1 to show
show_lemni_ref = 0  # set 0 to hide, 1 to show
a_lemni = 1500
lemni_origin = [500, -500, 1500]  # xyz
circle_radius = 1500
circle_origin = [500, -500, 1500]  # xyz
delete_start_land = 0  # set 0 to keep, 1 to delete
height = 1450 #height to cut start land
ref_color = "black"  # reference color
curve_color = "red"  # measurement color
curve_color2 = "green"  # measurement color
################################################# Plot initialization
plt.figure(figsize=(12, 6))
proj_plt = plt.subplot(2, 2, 1,projection="3d")
xy_plt = plt.subplot(2, 2, 3)
x_plt = plt.subplot(6, 2, 2)
y_plt = plt.subplot(6, 2, 4)
z_plt = plt.subplot(6, 2, 6)
ro_plt = plt.subplot(6, 2, 8)
pi_plt = plt.subplot(6, 2, 10)
ya_plt = plt.subplot(6, 2, 12)
################################################# Data initialization / Read Data
pathToData = "Flight_Data/10_21_square_good.csv"  # standard data Path if there is no argument given
pathToData2 = "Flight_Data/10_21_square_good.csv"  # standard data Path if there is no argument given
if len(sys.argv) == 2:
	pathToData = sys.argv[1]
if len(sys.argv) == 3:
	pathToData = sys.argv[1]
	pathToData2 = sys.argv[2]

header_list = ["Frame", "x", "y", "z", "roll", "pitch", "yaw"]  # new format
#header_list = ["Frame","Framerate","Latency","x","y","z","roll","pitch","yaw","err",]  # old format

#read first data set
FRA = pd.read_csv(pathToData, usecols=["Frame"], skiprows=Start, nrows=N, names=header_list).to_numpy()
ZeroFrame = FRA[0, 0]
Time = (FRA - ZeroFrame) / Framerate
RPY = pd.read_csv(pathToData,usecols=["roll", "pitch", "yaw"],skiprows=Start,nrows=N,names=header_list,).to_numpy()
POS = (pd.read_csv(pathToData, usecols=["x", "y", "z"], skiprows=Start, nrows=N, names=header_list).to_numpy()* 1000)

#read second data set
FRA2=0
Time2=0
POS2=0
if two_data_sets:
	FRA2 = pd.read_csv(pathToData2, usecols=["Frame"], skiprows=Start2, nrows=N2, names=header_list).to_numpy()
	Time2 = (FRA2 - FRA2[0, 0]) / Framerate
	POS2 = (pd.read_csv(pathToData2, usecols=["x", "y", "z"], skiprows=Start2, nrows=N2, names=header_list).to_numpy()* 1000)

################################################# Prepare / Manipulate Data
# delete outlier #abs(POS[i,0]) > POSMAX[0] or abs(POS[i,1]) > POSMAX[1] or abs(POS[i,2]) > POSMAX[2]:
# delete start/land part
if delete_start_land:
    d = [0]
    for i in range(0, len(POS[:, 0])):
        if abs(POS[i, 2]) < height:
            d = np.append(i, d)
    POS = np.delete(POS, d, 0)
    RPY = np.delete(RPY, d, 0)
    Time = np.delete(Time, d, 0)
# set offset for position data [x,y,z]
Offset = [0,0,0,]  # [statistics.mean(POS[:,0]), statistics.mean(POS[:,1]), statistics.mean(POS[:,2])]

################################################# Data for trajectory
if show_square_ref:
    # square
    lin_0_1000 = np.linspace(0, 1000, num=1000)
    con_0 = np.full(1000, 0)
    con_1000 = np.full(1000, 1000)
    # proj data
    X_t = np.concatenate((lin_0_1000, con_1000, lin_0_1000, con_0))
    Y_t = np.concatenate((con_0, -lin_0_1000, -con_1000, -lin_0_1000))
    Z_t = np.full(4000, 2000)
    # xyz data
    tx_P = np.concatenate(
        (
            np.full(500, 0),
            np.linspace(0, 1000, num=500),
            np.full(1000, 1000),
            np.linspace(0, 1000, num=500),
            np.full(1000, 0),
        )
    )
    tx_t = np.concatenate(
        (
            np.linspace(10, 15, num=500),
            np.full(500, 15),
            np.linspace(15, 25, num=1000),
            np.full(500, 25),
            np.linspace(25, 35, num=1000),
        )
    )
    ty_P = np.concatenate(
        (
            np.full(1000, 0),
            np.linspace(0, -1000, num=500),
            np.full(1000, -1000),
            np.linspace(0, -1000, num=500),
            np.full(500, 0),
        )
    )
    ty_t = np.concatenate(
        (
            np.linspace(10, 20, num=1000),
            np.full(500, 20),
            np.linspace(20, 30, num=1000),
            np.full(500, 30),
            np.linspace(30, 35, num=500),
        )
    )
    tz_P = np.full(1000, 2000)
    tz_t = np.linspace(10, 35, num=1000)
    # plot
    proj_plt.scatter(X_t, Y_t, Z_t, marker="o", s=1, c=ref_color)
    x_plt.scatter(tx_t, tx_P, marker="o", s=1, c=ref_color)
    y_plt.scatter(ty_t, ty_P, marker="o", s=1, c=ref_color)
    z_plt.scatter(tz_t, tz_P, marker="o", s=1, c=ref_color)

if show_circle_ref:
    # circle ref
    phi = np.linspace(0, 2 * math.pi, num=circle_radius)
    X_c = np.cos(phi) * circle_radius
    Y_c = np.sin(phi) * circle_radius
    Z_c = np.full(circle_radius, circle_origin[2])
    proj_plt.scatter(
        X_c + circle_origin[0],
        Y_c + circle_origin[1],
        Z_c,
        marker="o",
        s=1,
        c=ref_color,
    )
    xy_plt.scatter(
        X_c + circle_origin[0],
        Y_c + circle_origin[1],
        marker="o",
        s=1,
        c=ref_color,
    )
if show_lemni_ref:
    # lemniscate reference
    phi = np.linspace(0, 2 * math.pi, num=a_lemni)
    X_l = (a_lemni * np.cos(phi)) / (np.full(a_lemni, 1) + np.sin(phi) * np.sin(phi))
    Y_l = (a_lemni * np.sin(phi) * np.cos(phi)) / (
        np.full(a_lemni, 1) + np.sin(phi) * np.sin(phi)
    )
    Z_l = np.full(a_lemni, lemni_origin[2])
    proj_plt.scatter(
        X_l + lemni_origin[0],
        Y_l + lemni_origin[1],
        Z_l,
        marker="o",
        s=1,
        c=ref_color,
    )
    xy_plt.scatter(
        X_l + lemni_origin[0],
        Y_l + lemni_origin[1],
        marker="o",
        s=1,
        c=ref_color,
    )



################################################# Plot X,Y,Z
x_plt.scatter(Time, POS[:, 0] - Offset[0], marker="o", s=1, c=curve_color)
x_plt.set_xlabel("time [s]")
x_plt.set_ylabel("X [mm]")
y_plt.scatter(Time, POS[:, 1] - Offset[1], marker="o", s=1, c=curve_color)
y_plt.set_xlabel("time [s]")
y_plt.set_ylabel("Y [mm]")
z_plt.scatter(Time, POS[:, 2] - Offset[2], marker="o", s=1, c=curve_color)
z_plt.set_xlabel("time [s]")
z_plt.set_ylabel("Z [mm]")

################################################# Plot Roll,Pitch, Yaw
#rol_plt.scatter(Time, RPY[:, 0], marker="o", s=1, c=curve_color)
#rol_plt.set_xlabel("time [s]")
#rol_plt.set_ylabel("roll [deg]")
#pit_plt.scatter(Time, RPY[:, 1], marker="o", s=1, c=curve_color)
#pit_plt.set_xlabel("time [s]")
#pit_plt.set_ylabel("pitch [deg]")
#yaw_plt.scatter(Time, RPY[:, 2], marker="o", s=1, c=curve_color)
#yaw_plt.set_xlabel("time [s]")
#yaw_plt.set_ylabel("yaw [deg]")

################################################# Plot Projection
if two_data_sets:
	proj_plt.scatter(POS[:, 0] - Offset[0],POS[:, 1] - Offset[1],POS[:, 2] - Offset[2],marker="o",s=1,c=curve_color,label=label1)
	proj_plt.scatter(POS2[:, 0] - Offset[0],POS2[:, 1] - Offset[1],POS2[:, 2] - Offset[2],marker="o",s=1,c=curve_color2,label=label2)
if not two_data_sets:
	proj_plt.scatter(POS[:, 0] - Offset[0],POS[:, 1] - Offset[1],POS[:, 2] - Offset[2],marker="o",s=1,c=curve_color)
	
proj_plt.set_xlabel("X [mm]")
proj_plt.set_ylabel("Y [mm]")
proj_plt.set_zlabel("Z [mm]")
d=np.amax([np.amax(POS[:, 0])-np.amin(POS[:, 0]),np.amax(POS[:, 1])-np.amin(POS[:, 1])])
h_avg=np.mean(POS[:,2])
proj_plt.set_xlim3d(np.amin(POS[:, 0]), np.amin(POS[:, 0])+d)
proj_plt.set_ylim3d(np.amin(POS[:, 1]), np.amin(POS[:, 1])+d)
#proj_plt.set_zlim3d(h_avg/2,d)

################################################# Plot 2D

if two_data_sets:
	xy_plt.scatter(POS[:, 0] - Offset[0],POS[:, 1] - Offset[1],marker="o",s=1,c=curve_color,label=label1,alpha=1)
	xy_plt.scatter(POS2[:, 0] - Offset[0],POS2[:, 1] - Offset[1],marker="o",s=1,c=curve_color2,label=label2,alpha=1)
if not two_data_sets:
	xy_plt.scatter(POS[:, 0] - Offset[0],POS[:, 1] - Offset[1],marker="o",s=1,c=curve_color)

xy_plt.legend()
xy_plt.set_aspect('equal', 'box')


################################################# Display Plots
plt.show()
