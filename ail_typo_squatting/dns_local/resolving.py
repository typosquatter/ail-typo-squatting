import random, json


type_request = ['A', 'AAAA', 'NS', 'MX']

# This is a catch all function
def catchAll(current_domain):
    import dns.resolver

    is_catch_all = False

    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    ca_str = ''
    for _ in range(10):
        ca_str += random.choice(chars)

    domain_catch_all = f"{ca_str}.{current_domain}"
    try:
        answer = dns.resolver.resolve(domain_catch_all, 'A')
        if len(answer):
            is_catch_all = True
    except:
        pass
    if is_catch_all:
        return domain_catch_all
    return False

# This is a dns resolving function
def dnsResolving(resultList, domain, pathOutput, verbose=False, givevariations=False, dns_limited=False, catch_all=False):
    """Do a dns resolving on each variations and then create a json"""

    import dns.name
    import dns.resolver

    if verbose:
        print("[+] Dns Resolving...")

    domain_resolve = dict()

    for result in resultList:
        if givevariations:
            variation = result[1]
            result = result[0]

            if not variation in list(domain_resolve.keys()):
                domain_resolve[variation] = list()
            loc_dict = dict()
            loc_dict[result] = dict()
            try:
                n = dns.name.from_text(result)
            except Exception as e:
                print(e)
                print(result)
                try:
                    resultList.remove(result)
                except:
                    pass
                continue

            for t in type_request:
                try:
                    answer = dns.resolver.resolve(n, t)
                    loc = list()
                    for rdata in answer:
                        loc.append(rdata.to_text())
                    if len(loc) > 0:
                        loc_dict[result][t] = loc
                except:
                    pass
            
            if len(loc_dict[result]) == 0:
                if dns_limited:
                    loc_dict = dict()
                else:
                    loc_dict[result]['NotExist'] = True
            else:
                loc_dict[result]['NotExist'] = False
                if catch_all:
                    loc_dict[result]['CatchAll'] = catchAll(n)

            if loc_dict:
                domain_resolve[variation].append(loc_dict)

        else:
            domain_resolve[result] = dict()
            n = dns.name.from_text(result)

            for t in type_request:
                try:
                    answer = dns.resolver.resolve(n, t)
                    loc = list()
                    for rdata in answer:
                        loc.append(rdata.to_text())
                    if len(loc) > 0:
                        domain_resolve[result][t] = loc
                except:
                    pass
            
            if len(domain_resolve[result]) == 0:
                if dns_limited:
                    del domain_resolve[result]
                else:
                    domain_resolve[result]['NotExist'] = True
            else:
                domain_resolve[result]['NotExist'] = False
                if catch_all:
                    domain_resolve[result]['CatchAll'] = catchAll(n)

        if pathOutput and not pathOutput == "-":
            with open(f"{pathOutput}/{domain}_resolve.json", "w", encoding='utf-8') as write_json:
                json.dump(domain_resolve, write_json, indent=4)
    if pathOutput == '-':
        print(json.dumps(domain_resolve), flush=True)

    return domain_resolve
