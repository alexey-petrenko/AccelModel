import elements as am

Q1 = am.Quadrupole(L=0.2, K1=2.0, name="Q1")

print(f"{Q1.type_name}: name={Q1.name}, K1={Q1.K1} m, location={Q1.s0} m")
