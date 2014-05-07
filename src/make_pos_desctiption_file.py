
import os
import sys

if __name__ == "__main__":
    w = 24
    h = 24

    file = open("..\\pos.dat", "w")
    for root, _, files in os.walk("..\\pos\\"):
        for f in files:
            file.write("pos\\" + f +" 1 0 0 24 24\n")    
    file.close()
