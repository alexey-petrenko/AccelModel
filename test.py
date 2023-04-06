#!/usr/bin/env python3

import accmodel as am
import numpy as np

Q1 = am.Quadrupole(L=0.2, K1=2.0, name="Q1")
Q2 = am.Quadrupole(L=0.2, K1=-2.0, name="Q2", s=1.0)

print(f"{Q1.type_name}: name={Q1.name}, K1={Q1.K1} 1/m^2, location={Q1.s} m")
print(f"Q1 matrix = \n{Q1.M()}\n")

Sol1 = am.Solenoid(L=0.5, K=1.4, name="Sol1", s=2.0)

print(f"{Sol1.type_name}: name={Sol1.name}, K={Sol1.K} 1/m, location={Sol1.s} m")
print(f"Sol1 matrix = \n{Sol1.M()}\n")

S_bend1 = am.SectorBend(L=0.6, alpha=0.31, name="S_bend1", s=2)
print(f"{S_bend1.type_name}: name={S_bend1.name}, alpha={S_bend1.alpha} rad, location={S_bend1.s} m")
print(f"S_bend1 matrix = \n{S_bend1.M()}\n")

# create beamline:

chan = am.Beamline([Q1,Q2], name="channel 1")

print(chan)

chan.append(Sol1)

print(chan)

#input("Press Enter to Exit.")

Q2.s = -1.0

chan.sort()

print(chan)

s2, s1 = [0,1], 2
tracking_matrixes_from_Beamline = chan.M(s1, s2)

tracking_matrix_handmade0 = np.matmul(chan[2].M(), chan[1].M())
tracking_matrix_handmade1 = np.matmul(tracking_matrix_handmade0, chan[0].M()) 

print(f"Beamline: {chan[s2[0]:s1+1]}")
print(tracking_matrixes_from_Beamline['Q2 ---> Sol1'] == tracking_matrix_handmade1) 
print(f"Beamline: {chan[s2[1]:s1+1]}")
print(tracking_matrixes_from_Beamline['Q1 ---> Sol1'] == tracking_matrix_handmade0) 
print(f"transport matrixes = \n{tracking_matrixes_from_Beamline}\n")
#print(trans_matrix_from_Beamline)
print(tracking_matrixes_from_Beamline.keys())
