import os
import re
import sys
import math
import pathlib
pathProg = pathlib.Path(__file__).parent.absolute()

pathWork = ""
for i in re.split(r"/|\\", str(pathProg))[:-1]:
    pathWork += i + "/"
pathBin = pathWork + "bin"
pathTest = pathWork + "tests"
sys.path.append(pathBin)

from typo import *

Error = False

for file in os.listdir(pathTest):
    if file.split(".")[-1] == "txt":
        print(f"\n\t[*****] {domain} [*****]")
        domain = file.replace(".txt","")

        resultList = list()
        resultFile = list()
        resultList = runAll(domain=domain, limit=math.inf, verbose=False)

        with open(os.path.join(pathTest, file), "r", encoding="utf-8") as read_file:
            for line in read_file.readlines():
                resultFile.append(line.rstrip("\n"))
                
        result =  all(elem in resultList  for elem in resultFile)
        result2 = all(elem in resultFile  for elem in resultList)

        if result and result2:
            print("Two list are the same")
        else :
            if len(resultFile) == len(resultList):
                print("list not equal but have the same length")
            else:
                Error = True
                print("Not equal")

        resultList = list()
        resultFile = list()
if not Error:
    exit(0)
else:
    exit(1)