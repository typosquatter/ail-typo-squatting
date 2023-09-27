# Import all the utils
from .utils.generator_functions import *

import inflect

def singularPluralize(domain, resultList, verbose, limit, givevariations=False, keeporiginal=False, combo=False):
    """Create by making a singular domain plural and vice versa"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Singular Pluralize")
            
        resultLoc = list()
        loclist = list()
        inflector = inflect.engine()

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        for name in domainList:
            loc = inflector.plural(name)
            resultLoc.append(prefix + name)

            if loc and loc not in resultLoc:
                resultLoc.append(prefix+ loc)
            
            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([tld])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        if combo:
            rLoc = checkResult(rLoc, resultList, givevariations, "singularPluralize")
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "singularPluralize")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, "singularPluralize")
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "singularPluralize")

    return resultList
