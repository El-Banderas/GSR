
import numpy as np
import random

def print_matrix(matrix, size):
    for row in range(size):
        for column in range(size):
            print(matrix[row][column], end=" ")
        print()

def rotate(l, y=1):
   if len(l) == 0:
      return l
   y = -y % len(l)     # flip rotation direction
   return l[y:] + l[:y]

def generate_simple_matrix(input, size):
    matrix = []
    base_array = [] 
    for pos in range(size):
        base_array.append(input[pos])
    for line in range(size):
            matrix.append(rotate(base_array, line))
    return np.array(matrix)
    #print(matrix, size)

def generate_random_matrix(input, size):
    matrix = [[0 for x in range(size)] for y in range(size)] 
    for line in range(size):
        for col in range(size):
            # insert seed
            random.seed(input[line][col])
            matrix[line][col] = random.randint(0,255) 
    return matrix

def convert_int_byte(value):
    return  (int(value).to_bytes(1, 'big'))[0]

def generate_xor_matrix(m1, m2, m3, m4, size):
    print("AQUI")
    matrix = [[0 for x in range(size)] for y in range(size)] 
    for line in range(size):
        for col in range(size):
            n1 = convert_int_byte(m1[line][col])
            n2 = convert_int_byte(m2[line][col])
            n3 = convert_int_byte(m3[line][col])
            n4 = convert_int_byte(m4[line][col])
            print(n1)
            matrix[line][col] = ((n1 ^ n2) ^ n3) ^ n4
    return matrix

class Matrixs:
    def __init__(self, dictionary):
        self.K = dictionary["K"]
        
        self.M = dictionary["M"]
        M = np.array([*dictionary["M"]])
        # position 0 to K
        self.M1 = self.M[0:self.K]
        # position K to end
        self.M2 = self.M[self.K:]
        self.ZA = []
        self.ZB = []
        self.ZC = []
        self.ZD = []
        self.Z = []
        self.generate_matrixes()


    def generate_matrixes(self):
        self.ZA = generate_simple_matrix(self.M1, self.K)
        self.ZB = generate_simple_matrix(self.M2, self.K).transpose()
        

        self.ZC = generate_random_matrix(self.ZA, self.K)
        self.ZD = generate_random_matrix(self.ZB, self.K)


        print("Z A")
        print_matrix(self.ZA, self.K)
        print("Z B")
        print_matrix(self.ZB, self.K)

        print("Z C")
        print_matrix(self.ZC, self.K)
        print("Z D")
        print_matrix(self.ZD, self.K)
        self.Z = generate_xor_matrix(self.ZA, self.ZB, self.ZC, self.ZD, self.K)
        print("Z")
        print_matrix(self.Z, self.K)
        

    
