# Import all the utils
from .utils.generator_functions import *


from .conts.main import *

glyphs = const_get_similar_chars()

# Homoglyph
def homoglyph(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, all=False, combo=False):
    """One or more characters that look similar to another character but are different are called homogylphs"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Homoglyph")

        def mix(domain):
            for w in range(1, len(domain)):
                for i in range(len(domain)-w+1):
                    pre = domain[:i]
                    win = domain[i:i+w]
                    suf = domain[i+w:]
                    for c in win:
                        for g in glyphs.get(c, []):
                            yield pre + win.replace(c, g) + suf

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        s = '.'.join(domainList)

        result1 = set(mix(s))
        result2 = set()
        cp = 0
        loc_result_list = resultList.copy()

        if all:
            for r in result1:
                result2.update(set(mix(r)))
        
        for element in list(result1 | result2):
            element = prefix + element + '.' + tld
            if givevariations:
                flag = False
                for var in algo_list:
                    if [element, var] in resultList:
                        flag = True
                if not flag:
                    cp += 1
                    loc_result_list.append([element, "homoglyph"])

            elif element not in resultList:
                cp += 1
                loc_result_list.append(element)

        if verbose:
            print(f"{cp}\n")

        return final_treatment(domain, loc_result_list, limit, givevariations, keeporiginal, "homoglyph")

    return resultList
