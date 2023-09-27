# Import all the modules

## The public libraries
import os, re, sys, json, math, yaml, string, inflect, argparse, random, requests, tldextract, pathlib 

## The local libraries
from conts.main import * # the constants

## The typo generator
from generator.addDash import addDash
from generator.addDynamicDns import addDynamicDns
from generator.addition import addition
from generator.addTld import addTld
from generator.changeDotDash import changeDotDash
from generator.changeOrder import changeOrder
from generator.commonMisspelling import commonMisspelling
from generator.doubleReplacement import doubleReplacement
from generator.homoglyph import homoglyph
from generator.homophones import homophones
from generator.missingDot import missingDot
from generator.numeralSwap import numeralSwap
from generator.omission import omission
from generator.repetition import repetition
from generator.replacement import replacement
from generator.singularPluralize import singularPluralize
from generator.stripDash import stripDash
from generator.subdomain import subdomain
from generator.vowelSwap import vowelSwap
from generator.wrongTld import wrongTld
from generator.wrongSld import wrongSld


## The utils
from generator.utils.get_pathetc import get_path_etc
sys.path.append(get_path_etc())

import pkgutil
from typing import cast

from retrie.trie import Trie



# Import all the constants of data from the file conts/main.py
# If you wanna add a new algorithm, you have to add it in the list algo_list
numerals = const_get_numeral()
algo_list = const_get_algo_name_list()
type_request = const_get_dns_request_type()
exclude_tld = const_get_excluded_tld()


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

### SEPARATOR 1 ###

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

### SEPARATOR 2 ###

def formatYara(resultList, domain, givevariations=False):
    """Output in yara format"""
    domainReplace = domain.replace(".", "_")

    rule = f"rule {domainReplace} {{\n\tmeta:\n\t\t"
    rule += f'domain = "{domain}"\n\t'
    rule += "strings: \n"

    cp = 0
    for result in resultList: 
        if givevariations:
            result = result[0]
        rule += f'\t\t$s{cp} = "{result}"\n'
        cp += 1
    
    rule += "\tcondition:\n\t\t any of ($s*)\n}" 

    return rule

def formatRegex(resultList, givevariations=False):
    """Output in regex format"""
    regex = ""
    for result in resultList:
        if givevariations:
            result = result[0]
        reg = ""
        for car in result:
            if car in string.ascii_letters or car in string.digits:
                reg += car
            elif car in string.punctuation:
                reg += "\\" + car
        regex += f"{reg}|"
    regex = regex[:-1]

    return regex

def formatRegexRetrie(resultList, givevariations=False):
    """Output in regex format"""

    trie = Trie()
    if not givevariations:
        trie.add(*resultList)
    else:
        loc_list = [element[0] for element in resultList]
        trie.add(*loc_list)

    return trie.pattern()

def formatYaml(resultList, domain, givevariations=False):
    """Output in yaml format"""
    yaml_file = {"title": domain}
    variations = list()

    for result in resultList:
        if givevariations:
            variations.append(result[0])
        else:
            variations.append(result)

    yaml_file["variations"] = variations

    return yaml_file

def formatOutput(format, resultList, domain, pathOutput, givevariations=False, betterRegex=False):
    """
    Call different function to create the right format file
    """

    if format == "text":
        if pathOutput and not pathOutput == "-":
            with open(f"{pathOutput}/{domain}.txt", "w", encoding='utf-8') as write_file:
                for element in resultList:
                    if givevariations:
                        write_file.write(f"{element[0]}, {element[1]}\n")
                    else:
                        write_file.write(element + "\n")
        elif pathOutput == "-":
            for element in resultList:
                if givevariations:
                    print(f"{element[0]}, {element[1]}")
                else:
                    print(element)

    elif format == "yara":
        yara = formatYara(resultList, domain, givevariations)
        if pathOutput and not pathOutput == "-":
            with open(f"{pathOutput}/{domain}.yar", "w", encoding='utf-8') as write_file:
                write_file.write(yara)
        elif pathOutput == "-":
            print(yara)

    elif format == "regex":
        if betterRegex:
            regex = formatRegexRetrie(resultList, givevariations)
        else:
            regex = formatRegex(resultList, givevariations)
        if pathOutput and not pathOutput == "-":
            with open(f"{pathOutput}/{domain}.regex", "w", encoding='utf-8') as write_file:
                write_file.write(regex)
        elif pathOutput == "-":
            print(regex)

    elif format == "yaml":
        yaml_file = formatYaml(resultList, domain, givevariations)
        if pathOutput and not pathOutput == "-":
            with open(f"{pathOutput}/{domain}.yml", "w", encoding='utf-8') as write_file:
                yaml.dump(yaml_file, write_file)
        elif pathOutput == "-":
            print(yaml_file)
    else:
        print(f"Unknown format: {format}. Will use text format instead")
        formatOutput("text", resultList, domain, pathOutput, givevariations)

### SEPARATOR 3 ###

def runAll(domain, limit, formatoutput, pathOutput, verbose=False, givevariations=False, keeporiginal=False, all_homoglyph=False):
    """Run all algo on each domain contain in domainList"""

    resultList = list()

    for algo in algo_list:
        func = globals()[algo]
        resultList = func(domain, resultList, verbose, limit, givevariations, keeporiginal)

    if verbose:
        print(f"Total: {len(resultList)}")

    formatOutput(formatoutput, resultList, domain, pathOutput, givevariations)

    return resultList


# Main file function
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", help="verbose, more display", action="store_true")

    parser.add_argument("-dn", "--domainName", nargs="+", help="list of domain name")
    parser.add_argument("-fdn", "--filedomainName", help="file containing list of domain name")

    parser.add_argument("-o", "--output", help="path to ouput location")
    parser.add_argument("-fo", "--formatoutput", help="format for the output file, yara - regex - yaml - text. Default: text")
    parser.add_argument("-br", "--betterregex", help="Use retrie for faster regex", action="store_true")

    parser.add_argument("-dnsr", "--dnsresolving", help="resolve all variation of domain name to see if it's up or not", action="store_true")
    parser.add_argument("-dnsl", "--dnslimited", help="resolve all variation of domain name but keep only up domain in final result json", action="store_true")

    parser.add_argument("-l", "--limit", help="limit of variations for a domain name")
    parser.add_argument("-var", "--givevariations", help="give the algo that generate variations", action="store_true")
    parser.add_argument("-ko", "--keeporiginal", help="Keep in the result list the original domain name", action="store_true")

    parser.add_argument("-a", "--all", help="Use all algo", action="store_true")
    parser.add_argument("-om", "--omission", help="Leave out a letter of the domain name", action="store_true")
    parser.add_argument("-repe", "--repetition", help="Character Repeat", action="store_true")
    parser.add_argument("-repl", "--replacement", help="Character replacement", action="store_true")
    parser.add_argument("-drepl", "--doublereplacement", help="Double Character Replacement", action="store_true")
    parser.add_argument("-cho", "--changeorder", help="Change the order of letters in word", action="store_true")
    parser.add_argument("-add", "--addition", help="Add a character in the domain name", action="store_true")
    parser.add_argument("-md", "--missingdot", help="Delete a dot from the domain name", action="store_true")
    parser.add_argument("-sd", "--stripdash", help="Delete of a dash from the domain name", action="store_true")
    parser.add_argument("-vs", "--vowelswap", help="Swap vowels within the domain name", action="store_true")
    parser.add_argument("-ada", "--adddash", help="Add a dash between the first and last character in a string", action="store_true")

    parser.add_argument("-hg", "--homoglyph", help="One or more characters that look similar to another character but are different are called homogylphs", action="store_true")
    parser.add_argument("-ahg", "--all_homoglyph", help="generate all possible homoglyph permutations. Ex: circl.lu, e1rc1.lu", action="store_true")

    parser.add_argument("-cm", "--commonmisspelling", help="Change a word by is misspellings", action="store_true")
    parser.add_argument("-hp", "--homophones", help="Change word by an other who sound the same when spoken", action="store_true")
    parser.add_argument("-wt", "--wrongtld", help="Change the original top level domain to another", action="store_true")
    parser.add_argument("-wsld", "--wrongsld", help="Change the original second level domain to another", action="store_true")
    parser.add_argument("-at", "--addtld", help="Adding a tld before the original tld", action="store_true")
    parser.add_argument("-sub", "--subdomain", help="Insert a dot at varying positions to create subdomain", action="store_true")
    parser.add_argument("-sp", "--singularpluralize", help="Create by making a singular domain plural and vice versa", action="store_true")
    parser.add_argument("-cdd", "--changedotdash", help="Change dot to dash", action="store_true")
    parser.add_argument("-addns", "--adddynamicdns", help="Add dynamic dns at the end of the domain", action="store_true")
    parser.add_argument("-ns", "--numeralswap", help="Change a numbers to words and vice versa. Ex: circlone.lu, circl1.lu", action="store_true")
    parser.add_argument("-combo", help="Combine multiple algo on a domain name", action="store_true")
    parser.add_argument("-ca", "--catchall", help="Combine with -dnsr. Generate a random string in front of the domain.", action="store_true")
    
    args = parser.parse_args()

    resultList = list()

    verbose = args.v
    givevariations = args.givevariations

    dns_limited = args.dnslimited

    keeporiginal = args.keeporiginal

    limit = math.inf
    if args.limit:
        limit = int(args.limit)

    pathOutput = args.output

    if pathOutput and not pathOutput == "-":
        try:
            os.makedirs(pathOutput)
        except:
            pass

    if args.formatoutput:
        if args.formatoutput == "text" or args.formatoutput == "yara" or args.formatoutput == "yaml" or args.formatoutput == "regex":
            formatoutput = args.formatoutput
        else:
            print("[-] Format type error")
            exit(-1)
    else:
        formatoutput = "text"

    # Verify that a domain name is receive
    if args.domainName:
        domainList = args.domainName
    elif args.filedomainName:
        with open(args.filedomainName, "r") as read_file:
            domainList = read_file.readlines()
    else:
        print("[-] No Entry")
        exit(-1)


    for domain in domainList:
        if domain[0] == '.':
            domain = domain[1:]
        if pathOutput:
            print(f"\n\t[*****] {domain} [*****]")

        
        if args.combo:
            base_result = list()
            for arg in vars(args):
                for algo in algo_list:
                    if algo.lower() == arg:
                        if getattr(args, arg):
                            if verbose:
                                print(f"[+] {algo}")

                            func = globals()[algo]
                            # First Iteration
                            if not base_result:
                                if algo == "homoglyph":
                                    base_result = func(domain, resultList, False, limit, givevariations, keeporiginal, all=args.all_homoglyph)
                                else:
                                    base_result = func(domain, resultList, False, limit, givevariations, keeporiginal)
                                resultList = base_result.copy()
                                
                                if verbose:
                                    print(f"{len(resultList)}\n")
                            else:
                                loc_result = list()
                                loc_result = base_result.copy()
                                for r in loc_result:
                                    if type(r) == list:
                                        r = r[0]

                                    if algo == "homoglyph":
                                        loc_result = func(r, loc_result, False, limit, givevariations, keeporiginal, all=args.all_homoglyph, combo=True)
                                    else:
                                        loc_result = func(r, loc_result, False, limit, givevariations, keeporiginal, True)
                                resultList = resultList + loc_result
                                base_result = loc_result

                                if verbose:
                                    print(f"{len(loc_result)}\n")                                 
        elif args.all:
            for algo in algo_list:
                func = globals()[algo]
                if algo == "homoglyph":
                    resultList = func(domain, resultList, verbose, limit, givevariations, keeporiginal, all=args.all_homoglyph)
                else:
                    resultList = func(domain, resultList, verbose, limit, givevariations, keeporiginal)
        else:
            for arg in vars(args):
                for algo in algo_list:
                    if algo.lower() == arg:
                        if getattr(args, arg):
                            func = globals()[algo]
                            if algo == "homoglyph":
                                resultList = func(domain, resultList, verbose, limit, givevariations, keeporiginal, all=args.all_homoglyph)
                            else:
                                resultList = func(domain, resultList, verbose, limit, givevariations, keeporiginal)


        if verbose:
            print(f"Total: {len(resultList)}")

        formatOutput(formatoutput, resultList, domain, pathOutput, givevariations, args.betterregex)


        if args.dnsresolving:
            dnsResolving(resultList, domain, pathOutput, verbose, givevariations, dns_limited, args.catchall)

        resultList = list()
