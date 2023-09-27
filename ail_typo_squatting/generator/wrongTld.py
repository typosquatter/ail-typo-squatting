# Import all the utils
from .utils.generator_functions import *
from .utils.get_pathetc import get_path_etc

pathEtc = get_path_etc()

import pkgutil
from typing import cast

def wrongTld(domain, resultList, verbose, limit, givevariations=False, keeporiginal=False, combo=False):
    """Change the original top level domain to another"""
    # https://data.iana.org/TLD/tlds-alpha-by-domain.txt
    # Version 2022102502

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Wrong Tld")

        with open(pathEtc + "/tlds-alpha-by-domain.txt", "r") as read_file:
            tlds = read_file.readlines()
        
        originalTld = domain.split(".")[-1]

        prefix, domain_without_tld, possible_complete_tld = parse_domain(domain)

        domainLoc = ""
        domainLoc_orig = ''
        cp = 0
        loc_result_list = resultList.copy()

        if possible_complete_tld != originalTld:
            if prefix:
                domainLoc = prefix

            for element in domain_without_tld.split("."):
                domainLoc += element + "."
        for element in domain.split(".")[:-1]:
            domainLoc_orig += element + "."

        for tld in tlds:
            if tld.lower().rstrip("\n") != originalTld:
                cp += 1
                if givevariations:
                    if possible_complete_tld != originalTld:
                        cp += 1
                        loc_result_list.append([domainLoc + tld.lower().rstrip("\n"), 'wrongTld'])
                    loc_result_list.append([domainLoc_orig + tld.lower().rstrip("\n"), 'wrongTld'])
                else:
                    if possible_complete_tld != originalTld:
                        cp += 1
                        loc_result_list.append(domainLoc + tld.lower().rstrip("\n"))
                    loc_result_list.append(domainLoc_orig + tld.lower().rstrip("\n"))
        
        maybe_pkg_data = pkgutil.get_data("tldextract", ".tld_set_snapshot")
        pkg_data = cast(bytes, maybe_pkg_data)
        text = pkg_data.decode("utf-8")
        public, private = tldextract.suffix_list.extract_tlds_from_suffix_list(text)

        if possible_complete_tld == originalTld:
            split_tld = possible_complete_tld.split(".")
            for p in public:
                if p.endswith("." + split_tld[-1]):
                    loc = p.split(".")[-2] + "." + p.split(".")[-1]
                    if givevariations:
                        if not [domainLoc_orig + loc, "wrongTld"] in resultList:
                            loc_result_list.append([domainLoc_orig + loc, "wrongTld"])
                    else:
                        if not domainLoc_orig + loc in resultList:
                            loc_result_list.append(domainLoc_orig + loc)

            for p in private:
                if p.endswith("." + split_tld[-1]):
                    loc = p.split(".")[-2] + "." + p.split(".")[-1]
                    if givevariations:
                        if not [domainLoc_orig + loc, "wrongTld"] in resultList:
                            cp += 1
                            loc_result_list.append([domainLoc_orig + loc, "wrongTld"])
                    else:
                        if not domainLoc_orig + loc in resultList:
                            cp += 1
                            loc_result_list.append(domainLoc_orig + loc)

        if verbose:
            print(f"{cp}\n")

        return final_treatment(domain, loc_result_list, limit, givevariations, keeporiginal, "wrongTld")

    return resultList
