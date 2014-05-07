
import os
import sys

if __name__ == "__main__":
    w = 24
    h = 24

    file = open("..\\neg.dat", "w")
    for root, _, files in os.walk("..\\neg\\"):
        for f in files:
            file.write("neg\\" + f + "\n")    
    file.close()
