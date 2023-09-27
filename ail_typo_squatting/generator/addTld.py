# Import all the utils
from .utils.generator_functions import *
from .utils.get_pathetc import get_path_etc

pathEtc = get_path_etc()

"""

   Original Domain        Typosquatted Domain
  +----------------+     +------------------------+
  |    circl.lu    |     |     circl.lu.com       |
  +----------------+     +------------------------+

"""

# Add Tld
def addTld(domain, resultList, verbose, limit, givevariations=False, keeporiginal=False, combo=False):
    """Adding a tld before the original tld"""
    # https://data.iana.org/TLD/tlds-alpha-by-domain.txt
    # Version 2022012800

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Adding Tld")
        with open(pathEtc + "/tlds-alpha-by-domain.txt", "r") as read_file:
            tlds = read_file.readlines()
        
        cp = 0 
        loc_result_list = resultList.copy()
        for tld in tlds:
            cp += 1
            if givevariations:
                loc_result_list.append([domain + "." + tld.lower().rstrip("\n"), 'addTld'])
            else:
                loc_result_list.append(domain + "." + tld.lower().rstrip("\n"))

        if verbose:
            print(f"{cp}\n")

        # if combo:
        #     return final_treatment(domain, loc_result_list, limit, givevariations, keeporiginal, "addTld")

        # resultList = resultList + loc_result_list
        # resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "addTld")

        return final_treatment(domain, loc_result_list, limit, givevariations, keeporiginal, "addTld")

    return resultList

