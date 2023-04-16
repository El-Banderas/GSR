import re
from matrixs import Matrixs

default_file = "./input.txt"

params = {}

def read_file():
    pattern = re.compile("(\w)=(.+)$")
    for i, line in enumerate(open(default_file)):
        result = re.search(pattern, line)
        if result.group(1) == "M":
            params[result.group(1)] = result.group(2)
        else:
            params[result.group(1)] = int(result.group(2))

if __name__ == "__main__":
    print("Olá da main")
    read_file()
    print(params)
    matrixs = Matrixs(params)


