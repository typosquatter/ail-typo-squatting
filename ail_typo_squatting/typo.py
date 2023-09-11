import os
import re
import sys
import json
import math
import yaml
import string
import inflect
import argparse
import random

import requests

import tldextract

import pathlib
pathProg = pathlib.Path(__file__).parent.absolute()
pathWork = ""
for i in re.split(r"/|\\", str(pathProg))[:-1]:
    pathWork += i + "/"
pathEtc = pathWork + "etc"
sys.path.append(pathEtc)

import pkgutil
from typing import cast


glyphs = {
    '0': ['o'],
    '1': ['l', 'i', 'ı'],
    '2': ['ƻ'],
    '5': ['ƽ'],
    'a': ['à', 'á', 'à', 'â', 'ã', 'ä', 'å', 'ɑ', 'ạ', 'ǎ', 'ă', 'ȧ', 'ą', 'ə'],
    'b': ['d', 'ʙ', 'ɓ', 'ḃ', 'ḅ', 'ḇ', 'ƅ'],
    'c': ['e', 'ƈ', 'ċ', 'ć', 'ç', 'č', 'ĉ', 'ᴄ'],
    'd': ['b', 'cl', 'ɗ', 'đ', 'ď', 'ɖ', 'ḑ', 'ḋ', 'ḍ', 'ḏ', 'ḓ'],
    'e': ['c', 'é', 'è', 'ê', 'ë', 'ē', 'ĕ', 'ě', 'ė', 'ẹ', 'ę', 'ȩ', 'ɇ', 'ḛ'],
    'f': ['ƒ', 'ḟ'],
    'g': ['q', 'ɢ', 'ɡ', 'ġ', 'ğ', 'ǵ', 'ģ', 'ĝ', 'ǧ', 'ǥ'],
    'h': ['ĥ', 'ȟ', 'ħ', 'ɦ', 'ḧ', 'ḩ', 'ⱨ', 'ḣ', 'ḥ', 'ḫ', 'ẖ'],
    'i': ['1', 'l', 'í', 'ì', 'ï', 'ı', 'ɩ', 'ǐ', 'ĭ', 'ỉ', 'ị', 'ɨ', 'ȋ', 'ī', 'ɪ'],
    'j': ['ʝ', 'ǰ', 'ɉ', 'ĵ'],
    'k': ['lc', 'ḳ', 'ḵ', 'ⱪ', 'ķ', 'ᴋ'],
    'l': ['1', 'i', 'ɫ', 'ł', 'ı', 'ɩ'],
    'm': ['n', 'nn', 'rn', 'rr', 'ṁ', 'ṃ', 'ᴍ', 'ɱ', 'ḿ'],
    'n': ['m', 'r', 'ń', 'ṅ', 'ṇ', 'ṉ', 'ñ', 'ņ', 'ǹ', 'ň', 'ꞑ'],
    'o': ['0', 'ȯ', 'ọ', 'ỏ', 'ơ', 'ó', 'ö', 'ᴏ'],
    'p': ['ƿ', 'ƥ', 'ṕ', 'ṗ'],
    'q': ['g', 'ʠ'],
    'r': ['ʀ', 'ɼ', 'ɽ', 'ŕ', 'ŗ', 'ř', 'ɍ', 'ɾ', 'ȓ', 'ȑ', 'ṙ', 'ṛ', 'ṟ'],
    's': ['ʂ', 'ś', 'ṣ', 'ṡ', 'ș', 'ŝ', 'š', 'ꜱ'],
    't': ['ţ', 'ŧ', 'ṫ', 'ṭ', 'ț', 'ƫ'],
    'u': ['ᴜ', 'ǔ', 'ŭ', 'ü', 'ʉ', 'ù', 'ú', 'û', 'ũ', 'ū', 'ų', 'ư', 'ů', 'ű', 'ȕ', 'ȗ', 'ụ'],
    'v': ['ṿ', 'ⱱ', 'ᶌ', 'ṽ', 'ⱴ', 'ᴠ'],
    'w': ['vv', 'ŵ', 'ẁ', 'ẃ', 'ẅ', 'ⱳ', 'ẇ', 'ẉ', 'ẘ', 'ᴡ'],
    'x': ['ẋ', 'ẍ'],
    'y': ['ʏ', 'ý', 'ÿ', 'ŷ', 'ƴ', 'ȳ', 'ɏ', 'ỿ', 'ẏ', 'ỵ'],
    'z': ['ʐ', 'ż', 'ź', 'ᴢ', 'ƶ', 'ẓ', 'ẕ', 'ⱬ']
    }

numerals = [
    ["0", "zero"],
    ["1", "one", "first"],
    ["2", "two", "second"],
    ["3", "three", "third"],
    ["4", "four", "fourth", "for"],
    ["5", "five", "fifth"],
    ["6", "six", "sixth"],
    ["7", "seven", "seventh"],
    ["8", "eight", "eighth"],
    ["9", "nine", "ninth"]
]

algo_list = ["omission", "repetition", "changeOrder", "replacement", "doubleReplacement", "addition", "missingDot", "stripDash", "vowelSwap", "addDash", "homoglyph", "commonMisspelling", "homophones", "wrongTld", "addTld", "subdomain", "singularPluralize", "changeDotDash", "wrongSld", "numeralSwap", "addDynamicDns"]

type_request = ['A', 'AAAA', 'NS', 'MX']

exclude_tld = ["gov.pl"]


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


def omission(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Leave out a letter of the domain name"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Omission")

        resultLoc = list()
        loclist = list()

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        for name in domainList:
            for i in range(0,len(name)):
                resultLoc.append(prefix + name)
                loc = prefix + name[0:i]
                loc += name[i+1:len(name)]

                if loc not in resultLoc:
                    resultLoc.append(loc)

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([tld])

        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        if combo:
            rLoc = checkResult(rLoc, resultList, givevariations, "omission")
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "omission")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, "omission")
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "omission")

    return resultList

def repetition(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Characters Repetition"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Characters Repetition")

        resultLoc = list()
        loclist = list()

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        for name in domainList:
            resultLoc.append(prefix + name)
            for i, c in enumerate(name):
                if prefix + name[:i] + c + name[i:] not in resultLoc:
                    resultLoc.append(prefix + name[:i] + c + name[i:])

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([tld])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        if combo:
            rLoc = checkResult(rLoc, resultList, givevariations, 'repetition')
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "repetition")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, 'repetition')
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "repetition")

    return resultList

def changeOrder(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Change the order of letters in word"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Change Order")

        resultLoc = list()
        loclist = list()

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        for name in domainList:
            if len(name) == 1:
                resultLoc.append(prefix + name)
            else:
                for i in range(0, len(name)):
                    loc = name[0:i] + name[i+1:]
                    for j in range(0, len(loc)):
                        inter = prefix + loc[:j] + name[i] + loc[j:]
                        if not inter in resultLoc:
                            resultLoc.append(inter)

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([tld])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")
        
        if combo:
            rLoc = checkResult(rLoc, resultList, givevariations, 'changeOrder')
            # print("Hello")
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "changeOrder")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, 'changeOrder')
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "changeOrder")

    return resultList


def replacement(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Adjacent character replacement to the immediate left and right on the keyboard"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Replacement")

        resultLoc = list()
        loclist = list()

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        for name in domainList:
            for i in (*range(48, 58), *range(97, 123)):
                for j in range(0, len(name)):
                    pre = name[:j]
                    suf = name[j+1:]
                    variation = prefix + pre + chr(i) + suf
                    if variation not in resultLoc:
                        resultLoc.append(variation)

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([tld])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        if combo:
            rLoc = checkResult(rLoc, resultList, givevariations, 'replacement')
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "replacement")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, 'replacement')
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "replacement")

    return resultList


def doubleReplacement(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Double Character Replacement"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Double Character Replacement")

        resultLoc = list()
        loclist = list()

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        for name in domainList:
            for i in (*range(48, 58), *range(97, 123)):
                for j in range(0, len(name)):
                    pre = name[:j]
                    suf = name[j+2:]
                    variation = prefix + pre + chr(i) + chr(i) + suf
                    if variation not in resultLoc:
                        resultLoc.append(variation)

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([tld])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        if combo:
            rLoc = checkResult(rLoc, resultList, givevariations, 'doubleReplacement')
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "doubleReplacement")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, 'doubleReplacement')
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "doubleReplacement")

    return resultList



def addition(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Add a character in the domain name"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Addition")

        resultLoc = list()
        loclist = list()

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        for name in domainList:
            for i in (*range(48, 58), *range(97, 123)):
                # Adding 'i' in front of 'name'
                variation = prefix + chr(i) + name
                if variation not in resultLoc:
                    resultLoc.append(variation)

                # Adding 'i' at the end of 'name'
                variation = prefix + name + chr(i)
                if variation not in resultLoc:
                    resultLoc.append(variation)

                for j in range(0, len(name)):
                    variation = prefix + name[:j] + chr(i) + name[j:]
                    if variation not in resultLoc:
                        resultLoc.append(variation)

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([tld])

        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        if combo:
            rLoc = checkResult(rLoc, resultList, givevariations, 'addition')
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "addition")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, 'addition')
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "addition")

    return resultList


def utilMissingDot(resultLoc, loc):
    """Function for missingDot algorithm"""
    
    i = 0
    while "." in loc:
        loc2 = loc[::-1].replace(".", "", 1)[::-1]

        loc = loc.replace(".", "", 1)

        if loc not in resultLoc:
            resultLoc.append(loc)

        if loc2 not in resultLoc:
            resultLoc.append(loc2) 
        i += 1
        
    return resultLoc

def missingDot(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Delete a dot from the domain name"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Missing Dot")

        resultLoc = list()
        cp = 0

        domainList = domain.split(".")

        loc = domain
        utilMissingDot(resultLoc, loc)
        
        loc = f"www{domain}"
        utilMissingDot(resultLoc, loc)

        loc_result_list = resultList.copy()

        for i in range(0, len(resultLoc)):
            if domainList[-1] in resultLoc[i].split(".")[0]:
                resultLoc[i] = resultLoc[i] + ".com"

            if givevariations:
                flag = False
                for var in algo_list:
                    if [resultLoc[i], var] in resultList:
                        flag = True
                if not flag:
                    cp += 1
                    loc_result_list.append([resultLoc[i], "missingDot"])
            elif resultLoc[i] not in resultList:
                cp += 1
                loc_result_list.append(resultLoc[i])             

        if verbose:
            print(f"{cp}\n")

        # if combo:
        #     return final_treatment(domain, loc_result_list, limit, givevariations, keeporiginal, "missingDot")
        return final_treatment(domain, loc_result_list, limit, givevariations, keeporiginal, "missingDot")


    return resultList

def stripDash(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Delete a dash from the domain name"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Strip Dash")

        loc = domain
        cp = 0
        loc_result_list = resultList.copy()
        while "-" in loc:
            loc2 = loc[::-1].replace("-", "", 1)[::-1]
            loc = loc.replace("-", "", 1)

            if givevariations:
                flag = False
                for var in algo_list:
                    if [loc, var] in resultList:
                        flag = True
                if not flag:
                    cp += 1
                    loc_result_list.append([loc, "stripDash"])

                flag = False
                for var in algo_list:
                    if [loc2, var] in resultList:
                        flag = True
                if not flag:
                    cp += 1
                    loc_result_list.append([loc2, "stripDash"])
            else:
                if loc not in resultList:
                    cp += 1
                    loc_result_list.append(loc)

                if loc2 not in resultList:
                    cp += 1
                    loc_result_list.append(loc2)
        
        if verbose:
            print(f"{cp}\n")

        return final_treatment(domain, loc_result_list, limit, givevariations, keeporiginal, "stripDash")

    return resultList

def vowelSwap(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Swap vowels within the domain name"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Vowel Swap")

        resultLoc = list()
        loclist = list()
        # vowels = 'aeiouy'
        vowels = ["a", "e", "i", "o", "u", "y"]

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        for name in domainList:
            for j in vowels:
                for k in vowels:
                    if j != k:
                        loc = prefix + name.replace(k, j)
                        if loc not in resultLoc:
                            resultLoc.append(loc)

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([tld])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        if combo:
            rLoc = checkResult(rLoc, resultList, givevariations, "vowelSwap")
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "vowelSwap")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, "vowelSwap")
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "vowelSwap")

    return resultList


def addDash(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Add a dash between the first and last character in a string"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Add Dash")

        resultLoc = list()
        loclist = list()

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        for name in domainList:
            if len(name) == 1:
                resultLoc.append(prefix + name)
            else:
                resultLoc.append(prefix + name)
                for i in range(1, len(name)):
                    if prefix + name[:i] + '-' + name[i:] not in resultLoc:
                        resultLoc.append(prefix + name[:i] + '-' + name[i:])

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([tld])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        if combo:
            rLoc = checkResult(rLoc, resultList, givevariations, "addDash")
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "addDash")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, "addDash")
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "addDash")

    return resultList


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


def commonMisspelling(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Change a word by is misspellings"""
    # https://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/For_machines

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Common Misspelling")

        with open(pathEtc + "/common-misspellings.json", "r") as read_json:
            misspelling = json.load(read_json)
            keys = misspelling.keys()

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        resultLoc = list()
        loclist = list()

        for name in domainList:
            if name in keys:
                misspell = misspelling[name].split(",")
                for mis in misspell:
                    if prefix + mis.replace(" ","") not in resultLoc:
                        resultLoc.append(prefix + mis.replace(" ",""))
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
            rLoc = checkResult(rLoc, resultList, givevariations, "commonMisspelling")
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "commonMisspelling")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, "commonMisspelling")
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "commonMisspelling")

    return resultList


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


def addTld(domain, resultList, verbose, limit, givevariations=False, keeporiginal=False, combo=False):
    """Adding a tld before the original tld"""
    # https://data.iana.org/TLD/tlds-alpha-by-domain.txt
    # Version 2022012800

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Adding Tld")
        with open(pathEtc + "/tlds-alpha-by-domain.txt", "r") as read_file:
            tlds = read_file.readlines()
        
        cp = 0 
        loc_result_list = resultList.copy()
        for tld in tlds:
            cp += 1
            if givevariations:
                loc_result_list.append([domain + "." + tld.lower().rstrip("\n"), 'addTld'])
            else:
                loc_result_list.append(domain + "." + tld.lower().rstrip("\n"))

        if verbose:
            print(f"{cp}\n")

        # if combo:
        #     return final_treatment(domain, loc_result_list, limit, givevariations, keeporiginal, "addTld")

        # resultList = resultList + loc_result_list
        # resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "addTld")

        return final_treatment(domain, loc_result_list, limit, givevariations, keeporiginal, "addTld")

    return resultList


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


def singularPluralize(domain, resultList, verbose, limit, givevariations=False, keeporiginal=False, combo=False):
    """Create by making a singular domain plural and vice versa"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Singular Pluralize")
            
        resultLoc = list()
        loclist = list()
        inflector = inflect.engine()

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        for name in domainList:
            loc = inflector.plural(name)
            resultLoc.append(prefix + name)

            if loc and loc not in resultLoc:
                resultLoc.append(prefix+ loc)
            
            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([tld])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        if combo:
            rLoc = checkResult(rLoc, resultList, givevariations, "singularPluralize")
            rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "singularPluralize")
            return rLoc

        resultList = checkResult(rLoc, resultList, givevariations, "singularPluralize")
        resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "singularPluralize")

    return resultList

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


def numeralSwap(domain, resultList, verbose, limit, givevariations=False,  keeporiginal=False, combo=False):
    """Change a numbers to words and vice versa"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Numeral Swap")

        resultLoc = list()
        loclist = list()

        prefix, domain_without_tld, tld = parse_domain(domain)
        domainList = [domain_without_tld]

        for name in domainList:
            for numerals_list in numerals:
                for nume in numerals_list:
                    if nume in name:
                        for nume2 in numerals_list:
                            if not nume2 == nume:
                                loc = prefix + name.replace(nume, nume2)
                                if not loc in resultLoc:
                                    resultLoc.append(loc)
            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        if loclist:
            loclist.append([tld])
            rLoc = globalAppend(loclist)

            if verbose:
                print(f"{len(rLoc)}\n")

            if combo:
                rLoc = checkResult(rLoc, resultList, givevariations, "numeralSwap")
                rLoc = final_treatment(domain, rLoc, limit, givevariations, keeporiginal, "numeralSwap")
                return rLoc

            resultList = checkResult(rLoc, resultList, givevariations, "numeralSwap")
            resultList = final_treatment(domain, resultList, limit, givevariations, keeporiginal, "numeralSwap")
        elif verbose:
            print("0\n")


    return resultList


def dnsResolving(resultList, domain, pathOutput, verbose=False, givevariations=False, dns_limited=False):
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

        if pathOutput and not pathOutput == "-":
            with open(f"{pathOutput}/{domain}_resolve.json", "w", encoding='utf-8') as write_json:
                json.dump(domain_resolve, write_json, indent=4)
    if pathOutput == '-':
        print(json.dumps(domain_resolve), flush=True)

    return domain_resolve


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

def formatOutput(format, resultList, domain, pathOutput, givevariations=False):
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


def runAll(domain, limit, formatoutput, pathOutput, verbose=False, givevariations=False, keeporiginal=False, all_homoglyph=False):
    """Run all algo on each domain contain in domainList"""

    resultList = list()

    if args.all:
        for algo in algo_list:
            func = globals()[algo]
            resultList = func(domain, resultList, verbose, limit, givevariations, keeporiginal)

    if verbose:
        print(f"Total: {len(resultList)}")

    formatOutput(formatoutput, resultList, domain, pathOutput, givevariations)

    return resultList



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", help="verbose, more display", action="store_true")

    parser.add_argument("-dn", "--domainName", nargs="+", help="list of domain name")
    parser.add_argument("-fdn", "--filedomainName", help="file containing list of domain name")

    parser.add_argument("-o", "--output", help="path to ouput location")
    parser.add_argument("-fo", "--formatoutput", help="format for the output file, yara - regex - yaml - text. Default: text")

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

        formatOutput(formatoutput, resultList, domain, pathOutput, givevariations)


        if args.dnsresolving:
            dnsResolving(resultList, domain, pathOutput, verbose, givevariations, dns_limited)

        resultList = list()
