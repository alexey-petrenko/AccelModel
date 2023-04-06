import numpy as np

class AccElement:
    def __init__(self, L=0, s=0, name=None):
        self.L = L # m
        self.s = s  # m -- location of the element center along the beamline
        self.name = name
        self.type_name = None
        
    def __lt__(self, other):
        # to sort elements according to their location
        return self.s < other.s
    
    def __str__(self):
        return f"{self.type_name}.{self.name}"

    def __repr__(self):
        return f"{self.type_name}.{self.name}"
    
    def M(self, l=None):
        # l is the distance to the element start (inside the element)
        if l is None: l = self.L

        return np.matrix([
            [1, l, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, l, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1]
        ])
      
class Quadrupole(AccElement):
    def __init__(self, *args, K1=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.K1        = K1 # 1/m^2 -- geometric strength of quadrupole
        self.type_name = "Quadrupole"

    def M(self, l=None):
        if l is None: l = self.L
        
        K1 = self.K1
        
        if K1 == 0:
            return np.matrix([
                [1, l, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0],
                [0, 0, 1, l, 0, 0],
                [0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 1]
            ])
        
        k = np.sqrt(np.abs(K1))
        
        sinkl  = np.sin(k*l)
        coskl  = np.cos(k*l)
        sinhkl = np.sinh(k*l)
        coshkl = np.cosh(k*l)

        if K1 > 0:
            return np.matrix([
                [   coskl, sinkl/k,  0,      0,     0, 0],
                [-k*sinkl, coskl,    0,      0,     0, 0],
                [    0,     0,    coshkl, sinhkl/k, 0, 0],
                [    0,     0,  k*sinhkl, coshkl,   0, 0],
                [    0,     0,       0,      0,     1, 0],
                [    0,     0,       0,      0,     0, 1]
            ])
        
        if K1 < 0:
            return np.matrix([
                [  coshkl, sinhkl/k,  0,     0,      0, 0],
                [k*sinhkl, coshkl,    0,     0,      0, 0],
                [    0,     0,      coskl, sinkl/k,  0, 0],
                [    0,     0,   -k*sinkl, coskl,    0, 0],
                [    0,     0,       0,      0,      1, 0],
                [    0,     0,       0,      0,      0, 1]
            ])
        
        return None

class Solenoid(AccElement):
    def __init__(self, *args, K=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.K         = K # 1/m geometrical strength of solenoid
        self.type_name = "Solenoid"

    def M(self, l=None):

        if l is None: l = self.L

        K = self.K

        if K == 0:
            return np.matrix([
                [1, l, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0],
                [0, 0, 1, l, 0, 0],
                [0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 1]
            ])


        S = np.sin(K*l)
        C = np.cos(K*l)

        return np.matrix([
            [ C**2,   (S*C)/K,  S*C,   (S**2)/K, 0, 0],
            [-K*S*C,   C**2,   -K*S**2, S*C,     0, 0],
            [-S*C,   -(S**2)/K, C**2,  (S*C)/K , 0, 0],
            [ K*S**2, -S*C,    -K*S*C,  C**2,    0, 0],
            [ 0,       0,       0,      0,       0, 0],
            [ 0,       0,       0,      0,       0, 0]
        ])

class SectorBend(AccElement):
    #Uniform sector bend
    def __init__(self, *args, alpha=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.alpha     = alpha #rad, the angle of bend of central orbit
        self.type_name = "Sector Bend"

    def M(self, l=None):
        if l is None: l = self.L

        alpha = self.alpha
        if alpha == 0: return np.matrix([
                       [1, l, 0, 0, 0, 0],
                       [0, 1, 0, 0, 0, 0],
                       [0, 0, 1, l, 0, 0],
                       [0, 0, 0, 1, 0, 0],
                       [0, 0, 0, 0, 1, 0],
                       [0, 0, 0, 0, 0, 1],
                    ])

        h = alpha/l
        C = np.cos(alpha)
        S = np.sin(alpha)

        return np.matrix([
            [ C,            alpha*S/l,       0, 0, 0,       alpha*(1-C)/l], 
            [-alpha*S/l,    C,               0, 0, 0,                   S], 
            [ 0,            0,               1, l, 0,                   0], 
            [ 0,            0,               0, 1, 0,                   0], 
            [ S,            alpha*(1 - C)/l, 0, 0, 1, (alpha - S)*alpha/l], 
            [ 0,            0,               0, 0, 0,                   1], 
        ])      

class Beamline(list):
    def __init__(self, *args, name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name # the name of the beamline
    
    def M(self, s1, s2):
        # returns the transport matrix from s1 to s2 (s2 can be less than s1)?
        # s2 could be also a list of values
        if type(s2) is not list: s2 = [s2]

 
        matrixes_dict = {}

        for start_s in s2:
            if s1 < start_s: print("s2 can be less than s1")

            beamline = self[start_s:s1+1]

            res_matrix = np.eye(6)

            for i in range(1, len(beamline)+1):
                res_matrix = np.matmul(res_matrix, beamline[-i].M())

            matrixes_dict[f"{beamline[0].name} ---> {beamline[-1].name}"] = res_matrix

        self.matrixes_dict = matrixes_dict
       
        return None
    
    def tracking(self, s1, s2, beam_starting_set):
        # returns set of parameters of the beam in point s2 (s1 -- begining, s2 -- endindg)
        # beam_starting_set 
        pass

class Beam(list):
    def __init__(self, *args, name=None, start_params=None, transfer_matrixes=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.start_params = start_params # name of the set of starting beam parameters 
