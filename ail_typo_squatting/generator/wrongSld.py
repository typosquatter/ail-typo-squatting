# Import all the utils
from .utils.generator_functions import *

import pkgutil
from typing import cast

# Wrong Sld
def wrongSld(domain, resultList, verbose, limit, givevariations=False, keeporiginal=False, combo=False):
    """Change the original second level domain to another"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Wrong Sld")
        
        originalTld = domain.split(".")[-1]

        prefix, domain_without_tld, possible_complete_tld = parse_domain(domain)

        domainLoc = ""
        cp = 0
        loc_result_list = resultList.copy()

        if possible_complete_tld != originalTld:
            if prefix:
                domainLoc = prefix

            for element in domain_without_tld.split("."):
                domainLoc += element + "."
        
        maybe_pkg_data = pkgutil.get_data("tldextract", ".tld_set_snapshot")
        pkg_data = cast(bytes, maybe_pkg_data)
        text = pkg_data.decode("utf-8")
        public, private = tldextract.suffix_list.extract_tlds_from_suffix_list(text)

        if possible_complete_tld != originalTld:
            split_tld = possible_complete_tld.split(".")
            for p in public:
                if p.endswith("." + split_tld[-1]):
                    loc = p.split(".")[-2] + "." + p.split(".")[-1]
                    if givevariations:
                        if not [domainLoc + loc, "wrongSld"] in resultList:
                            loc_result_list.append([domainLoc + loc, "wrongSld"])
                    else:
                        if not domainLoc + loc in resultList:
                            loc_result_list.append(domainLoc + loc)

            for p in private:
                if p.endswith("." + split_tld[-1]):
                    loc = p.split(".")[-2] + "." + p.split(".")[-1]
                    if givevariations:
                        if not [domainLoc + loc, "wrongSld"] in resultList:
                            cp += 1
                            loc_result_list.append([domainLoc + loc, "wrongSld"])
                    else:
                        if not domainLoc + loc in resultList:
                            cp += 1
                            loc_result_list.append(domainLoc + loc)

        if verbose:
            print(f"{cp}\n")
    
        return final_treatment(domain, loc_result_list, limit, givevariations, keeporiginal, "wrongSld")

    return resultList
