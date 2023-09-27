# Import all the utils
from .utils.generator_functions import *

# Add Dash
def addDash(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Add a dash between the first and last character in a string"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Add Dash")

        resultLoc = list()
        loclist = list()

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        for name in domainList:
            if len(name) == 1:
                resultLoc.append(prefix + name)
            else:
                resultLoc.append(prefix + name)
                for i in range(1, len(name)):
                    if prefix + name[:i] + '-' + name[i:] not in resultLoc:
                        resultLoc.append(prefix + name[:i] + '-' + name[i:])

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([tld])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        if combo:
            rLoc = checkResult(rLoc, resultList, givevariations, "addDash")
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "addDash")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, "addDash")
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "addDash")

    return resultList
