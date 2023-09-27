# Import the modules
import tldextract

# Import the constants stored in "../const/main.py"
from ..conts.main import *

# The constants
algo_list = const_get_algo_name_list()
exclude_tld = const_get_excluded_tld()

# The functions 
def globalAppend(loclist):
    """
    Concate each element of each list of loclist to create all variations possible
    """

    r = list()
    rloc = list()
    result = list()
    cp = True
    i = 0
    while i < len(loclist):
        # First iteration, concat first words, ex: google.abuse.com -> concat variation for google and abuse
        if cp:
            for element in loclist[i]:
                for element2 in loclist[i+1]:
                    if f"{element}.{element2}" not in result:
                        result.append(f"{element}.{element2}")
            i += 1
            cp = False
            r.append(result)
        # concat other word with latest concatanation, ex: google.ause.com -> concat goole.ause and com
        else:
            for element in r[-1]:
                for add in loclist[i]:
                    if f"{element}.{add}" not in rloc:
                        rloc.append(f"{element}.{add}")
            r.append(rloc)
            rloc = list()
        i += 1

    return r[-1]
    
def checkResult(resultLoc, resultList, givevariations, algoName=''):
    """
    Verify if element in resultLoc not exist in resultList before adding them in resultList
    """
    loc_result_list = resultList.copy()
    if algoName == "changeDotDash" and givevariations:
        for element in resultLoc:
            flag = False
            for var in [algoName, "addTld"]:
                loc = element
                loc[1] = var
                if loc in resultList:
                    flag = True
                    continue
                    
            if not flag:
                element[1] = algoName
                loc_result_list.append(element)
    else:
        for element in resultLoc:
            if givevariations:
                flag = False
                for var in algo_list:
                    if [element, var] in resultList:
                        flag = True
                if not flag:
                    # if combo
                    loc_result_list.append([element, algoName])
            else:
                if element not in resultList:
                    loc_result_list.append(element)

    return loc_result_list

def check_valid_domain(domain_extract):
    if not domain_extract.suffix:
        return("[-] Domain not valid")

    if not domain_extract.suffix in exclude_tld:
        if not domain_extract.domain:
            return("[-] Only a TLD is identified. Try adding something like 'www.' before your domain.")
    return ""

def parse_domain(domain):
    domain_extract = tldextract.extract(domain)

    res = check_valid_domain(domain_extract)
    # If res is True then error
    if res:
        print(res)
        exit(-1)

    if not domain_extract.suffix in exclude_tld:
        if domain_extract.subdomain:
            prefix = domain_extract.subdomain
            prefix += '.'
        else:
            prefix = ''
    else:
        return '', domain_extract.suffix.split(".")[0], domain_extract.suffix.split(".")[1]

    return prefix, domain_extract.domain, domain_extract.suffix

def final_treatment(domain, resultList, limit, givevariations, keeporiginal, algo_name):
    """ Final treatment of a variation's function, keep original and name of variations' algorithm """
    if not keeporiginal:
        try:
            if givevariations:
                resultList.remove([domain, algo_name])
            else:
                resultList.remove(domain)
        except:
            pass
    elif givevariations:
        try:
            resultList.remove([domain, algo_name])
        except:
            pass
        if not [domain, 'original'] in resultList:
            resultList.insert(0, [domain, 'original'])

    while len(resultList) > limit:
        resultList.pop()

    return resultList
