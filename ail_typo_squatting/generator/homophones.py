# Import all the utils
from .utils.generator_functions import *
from .utils.get_pathetc import get_path_etc

pathEtc = get_path_etc()

"""

   Original Domain        Typosquatted Domain
  +----------------+     +-----------------+
  |    circl.lu    |     |     sircl.lu    |
  +----------------+     +-----------------+

"""

# Homophones
def homophones(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Change word by an other who sound the same when spoken"""
    # From http://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/Homophones
    # Last updated 04/2020
    # cat /tmp/h | sed 's/^[ ]*//g' | egrep -v "These pairs become homophones in certain dialects only|^Names" | sed -E 's/ (and|or) /,/g' | sed 's/\//,/g' | sed 's/,,/,/g' | tr '[:upper:]' '[:lower:]' | tr -d " '" | grep -v "^$"

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Homophones")

        with open(pathEtc + "/homophones.txt", "r") as read_file:
            homophones = read_file.readlines()
        
        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        resultLoc = list()
        loclist = list()

        for name in domainList:
            for lines in homophones:
                line = lines.split(",")
                for word in line:
                    if name == word.rstrip("\n"):
                        for otherword in line:
                            if prefix + otherword.rstrip("\n") not in resultLoc and otherword.rstrip("\n") != name:
                                resultLoc.append(prefix + otherword.rstrip("\n"))
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
            rLoc = checkResult(rLoc, resultList, givevariations, "homophones")
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "homophones")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, "homophones")
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "homophones")

    return resultList
 