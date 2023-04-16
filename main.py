import re

default_file = "./input.txt"

def read_file():
    pattern = re.compile("\w=\d+")
    for i, line in enumerate(open(default_file)):
        for match in re.finditer(pattern, line):
            print(f'Found on line {i+1} : {match.group()}')
    

if __name__ == "__main__":
    print("Olá da main")
    read_file()

