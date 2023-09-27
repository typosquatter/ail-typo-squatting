# Import all the utils
from .utils.generator_functions import *

# Missing Dot
def utilMissingDot(resultLoc, loc):
    """Function for missingDot algorithm"""
    
    i = 0
    while "." in loc:
        loc2 = loc[::-1].replace(".", "", 1)[::-1]

        loc = loc.replace(".", "", 1)

        if loc not in resultLoc:
            resultLoc.append(loc)

        if loc2 not in resultLoc:
            resultLoc.append(loc2) 
        i += 1
        
    return resultLoc

# Missing Dot
def missingDot(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Delete a dot from the domain name"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Missing Dot")

        resultLoc = list()
        cp = 0

        domainList = domain.split(".")

        loc = domain
        utilMissingDot(resultLoc, loc)
        
        loc = f"www{domain}"
        utilMissingDot(resultLoc, loc)

        loc_result_list = resultList.copy()

        for i in range(0, len(resultLoc)):
            if domainList[-1] in resultLoc[i].split(".")[0]:
                resultLoc[i] = resultLoc[i] + ".com"

            if givevariations:
                flag = False
                for var in algo_list:
                    if [resultLoc[i], var] in resultList:
                        flag = True
                if not flag:
                    cp += 1
                    loc_result_list.append([resultLoc[i], "missingDot"])
            elif resultLoc[i] not in resultList:
                cp += 1
                loc_result_list.append(resultLoc[i])             

        if verbose:
            print(f"{cp}\n")

        # if combo:
        #     return final_treatment(domain, loc_result_list, limit, givevariations, keeporiginal, "missingDot")
        return final_treatment(domain, loc_result_list, limit, givevariations, keeporiginal, "missingDot")


    return resultList
