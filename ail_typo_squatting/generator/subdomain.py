# Import all the utils
from .utils.generator_functions import *


"""

   Original Domain        Typosquatted Domain
  +----------------+     +----------------------+
  |    circl.lu    |     |  c.ircl.lu           |
  +----------------+     +----------------------+

"""

# Subdomain
def subdomain(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Insert a dot at varying positions to create subdomain"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Subdomain")

        cp = 0
        loc_result_list = resultList.copy()

        prefix, domain_without_tld, domain_tld = parse_domain(domain)
        
        if prefix:
            domain_tmp = prefix + domain_without_tld
        else:
            domain_tmp = domain_without_tld

        for i in range(1, len(domain_tmp)):
            if domain_tmp[i] not in ['-', '.'] and domain_tmp[i-1] not in ['-', '.']:
                cp += 1
                if givevariations:
                    loc_result_list.append([domain_tmp[:i] + '.' + domain_tmp[i:] + '.' + domain_tld, 'subdomain'])
                else:
                    loc_result_list.append(domain_tmp[:i] + '.' + domain_tmp[i:] + '.' + domain_tld)

        if verbose:
            print(f"{cp}\n")

        return final_treatment(domain, loc_result_list, limit, givevariations, keeporiginal, "subdomain")

    return resultList
