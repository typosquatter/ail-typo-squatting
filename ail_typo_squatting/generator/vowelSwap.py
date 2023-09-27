# Import all the utils
from .utils.generator_functions import *

# Vowel Swap
def vowelSwap(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Swap vowels within the domain name"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Vowel Swap")

        resultLoc = list()
        loclist = list()
        # vowels = 'aeiouy'
        vowels = ["a", "e", "i", "o", "u", "y"]

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        for name in domainList:
            for j in vowels:
                for k in vowels:
                    if j != k:
                        loc = prefix + name.replace(k, j)
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
            rLoc = checkResult(rLoc, resultList, givevariations, "vowelSwap")
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "vowelSwap")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, "vowelSwap")
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "vowelSwap")

    return resultList

