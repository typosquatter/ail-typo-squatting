# Import all the utils
from .utils.generator_functions import *
from .addTld import addTld

"""
    Original Domain            Typosquatted Domain
   +--------------------+     +------------------------+
   |    sub.circl.lu    |     |    sub-circl-lu.com    |
   +--------------------+     +------------------------+
"""

def changeDotDash(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Change dot to dash"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Change dot to dash")

        domain_extract = tldextract.extract(domain)
        original_tld = domain_extract.suffix
        original_dwt = domain_extract.domain

        if not original_tld:
            print("[-] Domain not valid")
            exit(-1)

        domain_list = [original_dwt]

        loc = domain
        loc2 = domain
        loc_result_list = resultList.copy()
        while "." in loc:
            resultLoc = list()
            resultLoc2 = list()
            loc2 = loc2[::-1].replace(".", "-", 1)[::-1]
            loc = loc.replace(".", "-", 1)

            loc_domain_extract = tldextract.extract(loc)
            loc_dwt = loc_domain_extract.domain
            loc_tld = loc_domain_extract.suffix

            loc2_domain_extract = tldextract.extract(loc2)
            loc2_dwt = loc2_domain_extract.domain
            loc2_tld = loc2_domain_extract.suffix


            if "." not in loc and loc_dwt not in domain_list:
                resultLoc = addTld(loc, resultLoc, verbose, limit, givevariations)
                loc_result_list = checkResult(resultLoc, resultList, givevariations, "changeDotDash")
                domain_list.append(loc_dwt)
            elif loc_dwt not in domain_list:
                if loc_tld != original_tld:
                    resultLoc = addTld(loc, resultLoc, verbose, limit, givevariations)
                    loc_result_list = checkResult(resultLoc, resultList, givevariations, "changeDotDash")
                else:
                    if givevariations:
                        loc_result_list.append([loc, 'changeDotDash'])
                    else:
                        loc_result_list.append(loc)
                domain_list.append(loc_dwt)

            if "." not in loc2 and loc2_dwt not in domain_list:
                resultLoc2 = addTld(loc2, resultLoc2, verbose, limit, givevariations)
                loc_result_list = checkResult(resultLoc2, resultList, givevariations, "changeDotDash")
                domain_list.append(loc2_dwt)
            elif loc2_tld != original_tld:
                if loc2_dwt not in domain_list:
                    resultLoc2 = addTld(loc2, resultLoc2, verbose, limit, givevariations)
                    loc_result_list = checkResult(resultLoc2, resultList, givevariations, "changeDotDash")
                else:
                    if givevariations:
                        loc_result_list.append([loc2, 'changeDotDash'])
                    else:
                        loc_result_list.append(loc2)
                domain_list.append(loc2_dwt)

        return final_treatment(domain, loc_result_list, limit, givevariations, keeporiginal, "changeDotDash")

    return resultList
