import os
import re
import sys
import math
import shutil
import pathlib
pathProg = pathlib.Path(__file__).parent.absolute()

pathWork = ""
for i in re.split(r"/|\\", str(pathProg))[:-1]:
    pathWork += i + "/"
pathBin = os.path.join(pathWork, "ail_typo_squatting")
pathTest = os.path.join(pathWork, "tests")
sys.path.append(pathBin)

from typo import *


###### ALL UTILS FUNCTION ######

# This function is used to check where is the difference between two list
def whereIsTheDif(list1, list2):
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            print("The difference is at the index : " + str(i))
            print(f"list1[{i}] = {list1[i]} | list2[{i}] = {list2[i]}")

# simple function to order two list by size
def orderListBySize(list1, list2):
    if len(list1) < len(list2):
        return list1, list2
    else:
        return list2, list1

# simple function to find the missing element in a list
def findMissingElement(list1, list2):
    small, big = orderListBySize(list1, list2)
    # we need to find the missing element in the big list that is not in the small list
    for i in range(len(big)):
        if big[i] not in small:
            print(f"Missing element : {big[i]}")

# Purge format of a list
def purgeListFormat(mylist):
    if type(mylist[0]) == str and "," in mylist[0]:
        mylist = [inner_list.split(",")[0] for inner_list in mylist]

    if isinstance(mylist[0], list):
        mylist = [inner_list[0] for inner_list in mylist]
    
    return mylist

###### ALL MAIN FUNCTION ######

def giveVariations(domain):
    if ".var.txt" in file:
        print(f"\n\t[*****] givevariations {domain} [*****]")
        return True, file.replace(".var.txt","")
    
    print(f"\n\t[*****] {domain} [*****]")

    return False, file.replace(".txt","")

def createTrash(pathTrash):
    if not os.path.isdir(pathTrash):
        os.mkdir(pathTrash)


def main(file):
    givevariations, domain = giveVariations(file)

    pathTrash = os.path.join(pathWork, "trash")
    createTrash(pathTrash)

    resultList = list()
    resultFile = list()
    resultList = runAll(domain=domain, limit=math.inf, formatoutput="text", pathOutput=pathTrash, verbose=False, givevariations=givevariations, keeporiginal=False, all_homoglyph=False)

    shutil.rmtree(pathTrash)

    with open(os.path.join(pathTest, file), "r", encoding="utf-8") as read_file:
        for line in read_file.readlines():
            resultFile.append(line.rstrip("\n"))
                
    result =  all(elem in resultList  for elem in resultFile)
    result2 = all(elem in resultFile  for elem in resultList)

    if result and result2:
        print("[✅] Two list are the same")
    else :
        if len(resultFile) == len(resultList):
            print("[✅] list not equal but have the same length")
        else:
            print("[❌] list not equal and have not the same length")
            print(f"len(resultFile) = {len(resultFile)} and len(resultList) = {len(resultList)}")

            resultFile = purgeListFormat(resultFile)
            resultList = purgeListFormat(resultList)

            findMissingElement(resultList, resultFile)
            exit(1)


# Main execution here
for file in os.listdir(pathTest):
    if file.split(".")[-1] == "txt":
        main(file)