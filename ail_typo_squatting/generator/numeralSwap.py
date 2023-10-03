# Import all the utils
from .utils.generator_functions import *
from .const.main import *

numerals = const_get_numeral()

"""

   Original Domain        Typosquatted Domain
  +----------------+     +--------------------+
  |    circl.lu    |     |      c1rcl.lu      |
  +----------------+     +--------------------+

"""

# Numeral Swap
def numeralSwap(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Change a numbers to words and vice versa"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Numeral Swap")

        resultLoc = list()
        loclist = list()

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        for name in domainList:
            for numerals_list in numerals:
                for nume in numerals_list:
                    if nume in name:
                        for nume2 in numerals_list:
                            if not nume2 == nume:
                                loc = prefix + name.replace(nume, nume2)
                                if not loc in resultLoc:
                                    resultLoc.append(loc)
            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        if loclist:
            loclist.append([tld])
            rLoc = globalAppend(loclist)

            if verbose:
                print(f"{len(rLoc)}\n")

            if combo:
                rLoc = checkResult(rLoc, resultList, givevariations, "numeralSwap")
                rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "numeralSwap")
                return rLoc

            resultList = checkResult(rLoc, resultList, givevariations, "numeralSwap")
            resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "numeralSwap")
        elif verbose:
            print("0\n")


    return resultList
