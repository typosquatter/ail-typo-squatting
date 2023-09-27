# Import all the utils
from .utils.generator_functions import *



# Omission
def omission(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Leave out a letter of the domain name"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Omission")

        resultLoc = list()
        loclist = list()

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        for name in domainList:
            for i in range(0,len(name)):
                resultLoc.append(prefix + name)
                loc = prefix + name[0:i]
                loc += name[i+1:len(name)]

                if loc not in resultLoc:
                    resultLoc.append(loc)

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([tld])

        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        if combo:
            rLoc = checkResult(rLoc, resultList, givevariations, "omission")
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "omission")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, "omission")
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "omission")

    return resultList