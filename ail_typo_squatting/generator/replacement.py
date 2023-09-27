# Import all the utils
from .utils.generator_functions import *

def replacement(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Adjacent character replacement to the immediate left and right on the keyboard"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Replacement")

        resultLoc = list()
        loclist = list()

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        for name in domainList:
            for i in (*range(48, 58), *range(97, 123)):
                for j in range(0, len(name)):
                    pre = name[:j]
                    suf = name[j+1:]
                    variation = prefix + pre + chr(i) + suf
                    if variation not in resultLoc:
                        resultLoc.append(variation)

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([tld])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        if combo:
            rLoc = checkResult(rLoc, resultList, givevariations, 'replacement')
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "replacement")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, 'replacement')
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "replacement")

    return resultList
