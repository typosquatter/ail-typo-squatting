# Import all the utils
from .utils.generator_functions import *

"""

   Original Domain        Typosquatted Domain
  +----------------+     +----------------------+
  |    circl.lu    |     |       circll.lu      |
  +----------------+     +----------------------+

"""

# Repetition
def repetition(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Characters Repetition"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Characters Repetition")

        resultLoc = list()
        loclist = list()

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        for name in domainList:
            resultLoc.append(prefix + name)
            for i, c in enumerate(name):
                if prefix + name[:i] + c + name[i:] not in resultLoc:
                    resultLoc.append(prefix + name[:i] + c + name[i:])

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([tld])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        if combo:
            rLoc = checkResult(rLoc, resultList, givevariations, 'repetition')
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "repetition")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, 'repetition')
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "repetition")

    return resultList
