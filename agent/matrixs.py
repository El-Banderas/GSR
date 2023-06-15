
import numpy as np
import random
import functools

import re


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
    if str(value).isnumeric():
        return  (int(value).to_bytes(1, 'big'))[0]
    else:
        return ord(value)

def transpose_lists(matrix, size):
        result = [[0 for x in range(size)] for y in range(size)] 
        for i in range(size):
            # iterate through columns
            for j in range(size):
                result[j][i] = matrix[i][j]
        return result


def generate_xor_matrix(m1, m2, m3, m4, size):
    matrix = [[0 for x in range(size)] for y in range(size)] 
    for line in range(size):
        for col in range(size):
            n1 = convert_int_byte(m1[line][col])
            n2 = convert_int_byte(m2[line][col])
            n3 = convert_int_byte(m3[line][col])
            n4 = convert_int_byte(m4[line][col])
            matrix[line][col] = ((n1 ^ n2) ^ n3) ^ n4
    return matrix

def convert_byte_hexa(byte):
    byte = f"{bytes([byte])}"
    two_char = re.search(r"b\'\\x(.+)\'", byte)
    if two_char:
        return two_char.group(1)
    single_char = re.search(r"\'(.+)\'", byte)
    if single_char:
        return '0'+single_char.group(1)
    
    

def generate_key(array1, array2, size):
    key = [0 for x in range(size)]
    for position in range(size):
        n1 = convert_int_byte(array1[position])
        n2 = convert_int_byte(array2[position])
        key[position] = (n1 ^ n2) 
    bytes_in_string = list(map(lambda byte : convert_byte_hexa(byte), key))
    

    return ''.join(bytes_in_string)


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
        self.Z = np.empty((self.K, self.K))
        self.generate_matrixes()
        self.n_updates = 0

    def update_matrix(self):
        self.n_updates+=1
        print("Number of matrix updates: " , self.n_updates)
        # Como não é especificado o valor do i, eu rodo todas as linhas
        
        # Seja Zi* a linha i de Z, i.e., Zi*[j] = Z[i,j], atualizar a matriz Z de acordo com
        # Zi* = rotate(Zi*,random(Z[i,0],0,K-1));
        for i in range(self.size):
            random.seed(self.Z[i][0])
            self.Z[i] = rotate(self.Z[i], random.randint(0, self.size - 1))
        self.Z = transpose_lists(self.Z, self.size)
        

        for i in range(self.size):
            random.seed(self.Z[i][0])
            self.Z[i] = rotate(self.Z[i], random.randint(0, self.size - 1))
        
        self.Z = transpose_lists(self.Z, self.size)


    def get_key(self):
        self.update_matrix()
        random.seed(self.n_updates +self.Z[0][0])
        i = random.randint(0, self.size - 1)

        random.seed(self.Z[i][0])
        j = random.randint(0, self.size - 1)
        column_j = [row[j] for row in self.Z]
        key = generate_key(self.Z[i], column_j, self.size )
        return key

    def generate_matrixes(self):
        self.size = self.K
        self.ZA = generate_simple_matrix(self.M1, self.K)
        self.ZB = generate_simple_matrix(self.M2, self.K).transpose()
        

        self.ZC = generate_random_matrix(self.ZA, self.K)
        self.ZD = generate_random_matrix(self.ZB, self.K)


        self.Z = generate_xor_matrix(self.ZA, self.ZB, self.ZC, self.ZD, self.K)
        '''
        print("Z A")
        print_matrix(self.ZA, self.K)
        print("Z B")
        print_matrix(self.ZB, self.K)

        print("Z C")
        print_matrix(self.ZC, self.K)
        print("Z D")
        print_matrix(self.ZD, self.K)
        print("Z")
        print_matrix(self.Z, self.K)
        '''

        

    
