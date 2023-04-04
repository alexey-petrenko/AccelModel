import numpy as np

class AccElement:
    def __init__(self, L=0, s0=0, name=None):
        self.L  = L  # m
        self.s0 = s0  # m -- location of the element center along the beamline
        self.name = name
        self.type_name = None
        
    def M(self):
        L = self.L
        return np.matrix([
          [1, L, 0, 0, 0, 0],
          [0, 1, 0, 0, 0, 0],
          [0, 0, 1, L, 0, 0],
          [0, 0, 0, 1, 0, 0],
          [0, 0, 0, 0, 1, 0],
          [0, 0, 0, 0, 0, 1]
        ])

class UniformElement(AccElement):
    def M(self, L=None):
        if L is None: L = self.L

        return np.matrix([
          [1, L, 0, 0, 0, 0],
          [0, 1, 0, 0, 0, 0],
          [0, 0, 1, L, 0, 0],
          [0, 0, 0, 1, 0, 0],
          [0, 0, 0, 0, 1, 0],
          [0, 0, 0, 0, 0, 1]
        ])
      
class Quadrupole(UniformElement):
    def __init__(self, K1=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.K1 = K1 # 1/m^2 -- geometric strength of quadrupole
        self.type_name = "Quadrupole"
