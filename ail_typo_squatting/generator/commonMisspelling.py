# Import all the utils
from .utils.generator_functions import *
from .utils.get_pathetc import get_path_etc

import json


pathEtc = get_path_etc()


def commonMisspelling(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Change a word by is misspellings"""
    # https://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/For_machines

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Common Misspelling")

        with open(pathEtc + "/common-misspellings.json", "r") as read_json:
            misspelling = json.load(read_json)
            keys = misspelling.keys()

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        resultLoc = list()
        loclist = list()

        for name in domainList:
            if name in keys:
                misspell = misspelling[name].split(",")
                for mis in misspell:
                    if prefix + mis.replace(" ","") not in resultLoc:
                        resultLoc.append(prefix + mis.replace(" ",""))
            elif name not in resultLoc:
                resultLoc.append(prefix + name)

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([tld])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        if combo:
            rLoc = checkResult(rLoc, resultList, givevariations, "commonMisspelling")
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "commonMisspelling")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, "commonMisspelling")
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "commonMisspelling")

    return resultList
