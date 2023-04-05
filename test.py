#!/usr/bin/env python3

import elements as am

Q1 = am.Quadrupole(L=0.2, K1=2.0, name="Q1")

print(f"{Q1.type_name}: name={Q1.name}, K1={Q1.K1} 1/m^2, location={Q1.s} m")
print(f"Q1 matrix = {Q1.M()}")

Sol1 = am.Solenoid(L=0.5, K=1.4, name="Sol1", s=1.2)

print(f"{Sol1.type_name}: name={Sol1.name}, K={Sol1.K} 1/m, location={Sol1.s} m")
print(f"Sol1 matrix = \n{Sol1.M()}\n")

S_bend1 = am.Sector_bend(L=0.6, h=0.2, name="S_bend1", s=2)
print(f"{S_bend1.type_name}: name={S_bend1.name}, h={S_bend1.h} 1/m, location={S_bend1.s} m")
print(f"S_bend1 matrix = \n{S_bend1.M()}\n")


#input("Press Enter to Exit.")

