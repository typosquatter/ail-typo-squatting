# Import all the utils
from .utils.generator_functions import *

# Addition
def addition(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Add a character in the domain name"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Addition")

        resultLoc = list()
        loclist = list()

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        for name in domainList:
            for i in (*range(48, 58), *range(97, 123)):
                # Adding 'i' in front of 'name'
                variation = prefix + chr(i) + name
                if variation not in resultLoc:
                    resultLoc.append(variation)

                # Adding 'i' at the end of 'name'
                variation = prefix + name + chr(i)
                if variation not in resultLoc:
                    resultLoc.append(variation)

                for j in range(0, len(name)):
                    variation = prefix + name[:j] + chr(i) + name[j:]
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
            rLoc = checkResult(rLoc, resultList, givevariations, 'addition')
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "addition")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, 'addition')
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "addition")

    return resultList
