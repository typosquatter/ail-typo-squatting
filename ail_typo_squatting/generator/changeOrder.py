# Import all the utils
from .utils.generator_functions import *

"""

   Original Domain        Typosquatted Domain
  +----------------+     +-------------------+
  |    circl.lu    |     |     cicrl.com     |
  +----------------+     +-------------------+

"""

# Change Order
def changeOrder(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Change the order of letters in word"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Change Order")

        resultLoc = list()
        loclist = list()

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        for name in domainList:
            if len(name) == 1:
                resultLoc.append(prefix + name)
            else:
                for i in range(0, len(name)):
                    loc = name[0:i] + name[i+1:]
                    for j in range(0, len(loc)):
                        inter = prefix + loc[:j] + name[i] + loc[j:]
                        if not inter in resultLoc:
                            resultLoc.append(inter)

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([tld])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")
        
        if combo:
            rLoc = checkResult(rLoc, resultList, givevariations, 'changeOrder')
            # print("Hello")
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "changeOrder")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, 'changeOrder')
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "changeOrder")

    return resultList
