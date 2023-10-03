# Import all the utils
from .utils.generator_functions import *
from .utils.get_pathetc import get_path_etc

import requests, json

pathEtc = get_path_etc()

# Add Dynamic DNS
def addDynamicDns(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Add dynamic dns"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Dynamic DNS")
        
        try:
            r = requests.get("https://raw.githubusercontent.com/MISP/misp-warninglists/main/lists/dynamic-dns/list.json")
            dynamicdns = r.json()['list']
            with open(pathEtc + "/dynamic-dns.json", "w") as write_json:
                json.dump(r.json(), write_json, indent=4)
        except:
            with open(pathEtc + "/dynamic-dns.json", "r") as read_json:
                dynamicdns = json.load(read_json)["list"]


        resultLoc = list()

        domain_replace = [domain[::-1].replace(".", "-", 1)[::-1], domain.replace(".", "-"), domain.replace(".", "_")]

        for ddns in dynamicdns:
            for replace in domain_replace:
                d_loc = replace + ddns
                if d_loc not in resultLoc:
                    resultLoc.append(d_loc)

        if verbose:
            print(f"{len(resultLoc)}\n")

        if combo:
            resultLoc = checkResult(resultLoc, resultList, givevariations, "addDynamicDns")
            resultLoc = final_treatment(domain, resultLoc, limit, givevariations, keeporiginal, "addDynamicDns")
            return resultLoc

        resultList = checkResult(resultLoc, resultList, givevariations, "addDynamicDns")
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "addDynamicDns")

    return resultList

