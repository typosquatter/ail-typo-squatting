import os
import re
import sys
import json
import math
import yaml
import string
import inflect
import argparse

import pathlib
pathProg = pathlib.Path(__file__).parent.absolute()
pathWork = ""
for i in re.split(r"/|\\", str(pathProg))[:-1]:
    pathWork += i + "/"
pathEtc = pathWork + "etc"
sys.path.append(pathEtc)


qwerty = {
    '1': '2q', '2': '3wq1', '3': '4ew2', '4': '5re3', '5': '6tr4', '6': '7yt5', '7': '8uy6', '8': '9iu7', '9': '0oi8', '0': 'po9',
    'q': '12wa', 'w': '3esaq2', 'e': '4rdsw3', 'r': '5tfde4', 't': '6ygfr5', 'y': '7uhgt6', 'u': '8ijhy7', 'i': '9okju8', 'o': '0plki9', 'p': 'lo0',
    'a': 'qwsz', 's': 'edxzaw', 'd': 'rfcxse', 'f': 'tgvcdr', 'g': 'yhbvft', 'h': 'ujnbgy', 'j': 'ikmnhu', 'k': 'olmji', 'l': 'kop',
    'z': 'asx', 'x': 'zsdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhjm', 'm': 'njk'
    }
qwertz = {
    '1': '2q', '2': '3wq1', '3': '4ew2', '4': '5re3', '5': '6tr4', '6': '7zt5', '7': '8uz6', '8': '9iu7', '9': '0oi8', '0': 'po9',
    'q': '12wa', 'w': '3esaq2', 'e': '4rdsw3', 'r': '5tfde4', 't': '6zgfr5', 'z': '7uhgt6', 'u': '8ijhz7', 'i': '9okju8', 'o': '0plki9', 'p': 'lo0',
    'a': 'qwsy', 's': 'edxyaw', 'd': 'rfcxse', 'f': 'tgvcdr', 'g': 'zhbvft', 'h': 'ujnbgz', 'j': 'ikmnhu', 'k': 'olmji', 'l': 'kop',
    'y': 'asx', 'x': 'ysdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhjm', 'm': 'njk'
    }
azerty = {
    '1': '2a', '2': '3za1', '3': '4ez2', '4': '5re3', '5': '6tr4', '6': '7yt5', '7': '8uy6', '8': '9iu7', '9': '0oi8', '0': 'po9',
    'a': '2zq1', 'z': '3esqa2', 'e': '4rdsz3', 'r': '5tfde4', 't': '6ygfr5', 'y': '7uhgt6', 'u': '8ijhy7', 'i': '9okju8', 'o': '0plki9', 'p': 'lo0m',
    'q': 'zswa', 's': 'edxwqz', 'd': 'rfcxse', 'f': 'tgvcdr', 'g': 'yhbvft', 'h': 'ujnbgy', 'j': 'iknhu', 'k': 'olji', 'l': 'kopm', 'm': 'lp',
    'w': 'sxq', 'x': 'wsdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhj'
    }
keyboards = [qwerty, qwertz, azerty]

glyphs = {
    '0': ['o'],
    '1': ['l', 'i'],
    '2': ['ƻ'],
    '5': ['ƽ'],
    'a': ['à', 'á', 'à', 'â', 'ã', 'ä', 'å', 'ɑ', 'ạ', 'ǎ', 'ă', 'ȧ', 'ą', 'ə'],
    'b': ['d', 'lb', 'ʙ', 'ɓ', 'ḃ', 'ḅ', 'ḇ', 'ƅ'],
    'c': ['e', 'ƈ', 'ċ', 'ć', 'ç', 'č', 'ĉ', 'ᴄ'],
    'd': ['b', 'cl', 'dl', 'ɗ', 'đ', 'ď', 'ɖ', 'ḑ', 'ḋ', 'ḍ', 'ḏ', 'ḓ'],
    'e': ['c', 'é', 'è', 'ê', 'ë', 'ē', 'ĕ', 'ě', 'ė', 'ẹ', 'ę', 'ȩ', 'ɇ', 'ḛ'],
    'f': ['ƒ', 'ḟ'],
    'g': ['q', 'ɢ', 'ɡ', 'ġ', 'ğ', 'ǵ', 'ģ', 'ĝ', 'ǧ', 'ǥ'],
    'h': ['lh', 'ĥ', 'ȟ', 'ħ', 'ɦ', 'ḧ', 'ḩ', 'ⱨ', 'ḣ', 'ḥ', 'ḫ', 'ẖ'],
    'i': ['1', 'l', 'í', 'ì', 'ï', 'ı', 'ɩ', 'ǐ', 'ĭ', 'ỉ', 'ị', 'ɨ', 'ȋ', 'ī', 'ɪ'],
    'j': ['ʝ', 'ǰ', 'ɉ', 'ĵ'],
    'k': ['lk', 'ik', 'lc', 'ḳ', 'ḵ', 'ⱪ', 'ķ', 'ᴋ'],
    'l': ['1', 'i', 'ɫ', 'ł'],
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
    'z': ['ʐ', 'ż', 'ź', 'ᴢ', 'ƶ', 'ẓ', 'ẕ', 'ⱬ'],
    '-': ['➖', '–', '˗', '‑', '⁃', '−', 'Ⲻ', '‒', 'ⲻ', '‐', '۔', '﹘']
    }

type_request = ['A', 'AAAA', 'NS', 'MX']


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
        # concat other word with latest concatanation, ex: google.abuse.com -> concat goole.ause and com
        else:
            for element in r[-1]:
                for add in loclist[i]:
                    if f"{element}.{add}" not in rloc:
                        rloc.append(f"{element}.{add}")
            r.append(rloc)
            rloc = list()
        i += 1

    return r[-1]
    

def checkResult(resultLoc, resultList):
    """
    Verify if element in resultLoc not exist in resultList before adding them in resultList
    """

    for element in resultLoc:
        if element not in resultList:
            resultList.append(element)

    return resultList


def characterOmission(domain, resultList, verbose, limit):
    """Leave out a letter of the domain name"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Character Omission")

        resultLoc = list()
        loclist = list()

        domainList = domain.split(".")[:-1]

        for name in domainList:
            for i in range(0,len(name)):
                resultLoc.append(name)
                loc = name[0:i]
                loc += name[i+1:len(name)]

                if loc not in resultLoc:
                    resultLoc.append(loc)

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([domain.split(".")[-1]])

        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        resultList = checkResult(rLoc, resultList)
        try:
            resultList.remove(domain)
        except:
            pass

        while len(resultList) > limit:
            resultList.pop()

    return resultList

def repetition(domain, resultList, verbose, limit):
    """Character Repeat"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Character Repeat")

        resultLoc = list()
        loclist = list()

        domainList = domain.split(".")[:-1]

        for name in domainList:
            for i, c in enumerate(name):
                if name[:i] + c + name[i:] not in resultLoc:
                    resultLoc.append(name[:i] + c + name[i:])

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([domain.split(".")[-1]])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        resultList = checkResult(rLoc, resultList)
        try:
            resultList.remove(domain)
        except:
            pass

        while len(resultList) > limit:
            resultList.pop()

    return resultList

def changeOrder(domain, resultList, verbose, limit):
    """Change the order of letters in word"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Change Order")

        resultLoc = list()
        loclist = list()

        domainList = domain.split(".")[:-1]

        for name in domainList:
            for i in range(0, len(name)):
                loc = name[0:i] + name[i+1:]
                for j in range(0, len(loc)):
                    inter = loc[:j] + name[i] + loc[j:]
                    if not inter in resultLoc:
                        resultLoc.append(loc[:j] + name[i] + loc[j:])

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([domain.split(".")[-1]])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        resultList = checkResult(rLoc, resultList)
        try:
            resultList.remove(domain)
        except:
            pass

        while len(resultList) > limit:
            resultList.pop()

    return resultList

def transposition(domain, resultList, verbose, limit):
    """Swappe the order of adjacent letters in the domain name"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Transposition")

        resultLoc = list()
        loclist = list()

        domainList = domain.split(".")[:-1]

        for name in domainList:
            for i in range(len(name)-1):
                if name[:i] + name[i+1] + name[i] + name[i+2:] not in resultLoc:
                    resultLoc.append(name[:i] + name[i+1] + name[i] + name[i+2:])

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()
        
        loclist.append([domain.split(".")[-1]])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        resultList = checkResult(rLoc, resultList)
        try:
            resultList.remove(domain)
        except:
            pass

        while len(resultList) > limit:
            resultList.pop()

    return resultList


def replacement(domain, resultList, verbose, limit):
    """Adjacent character replacement to the immediate left and right on the keyboard"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Replacement")

        resultLoc = list()
        loclist = list()

        domainList = domain.split(".")[:-1]

        for name in domainList:
            for i, c in enumerate(name):
                pre = name[:i]
                suf = name[i+1:]
                for layout in keyboards:
                    for r in layout.get(c, ''):
                        if pre + r + suf not in resultLoc:
                            resultLoc.append(pre + r + suf)

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([domain.split(".")[-1]])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        resultList = checkResult(rLoc, resultList)
        try:
            resultList.remove(domain)
        except:
            pass

        while len(resultList) > limit:
            resultList.pop()

    return resultList


def doubleReplacement(domain, resultList, verbose, limit):
    """Double Character Replacement"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Double Character Replacement")

        resultLoc = list()
        loclist = list()

        domainList = domain.split(".")[:-1]

        for name in domainList:
            for i, c in enumerate(name):
                pre = name[:i]
                suf = name[i+2:]
                for layout in keyboards:
                    for r in layout.get(c, ''):
                        if pre + r + r + suf not in resultLoc:
                            resultLoc.append(pre + r + r + suf)

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([domain.split(".")[-1]])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        resultList = checkResult(rLoc, resultList)
        try:
            resultList.remove(domain)
        except:
            pass

        while len(resultList) > limit:
            resultList.pop()

    return resultList


def insertion(domain, resultList, verbose, limit):
    """Adjacent character insertion of letters to the immediate left and right on the keyboard of each letter"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Insertion")

        resultLoc = list()
        loclist = list()

        domainList = domain.split(".")[:-1]

        for name in domainList:
            for i in range(1, len(name)-1):
                prefix, orig_c, suffix = name[:i], name[i], name[i+1:]
                for c in (c for keys in keyboards for c in keys.get(orig_c, [])):
                    if prefix + c + orig_c + suffix not in resultLoc:
                        resultLoc.append(prefix + c + orig_c + suffix)
                    if prefix + orig_c + c + suffix not in resultLoc:
                        resultLoc.append(prefix + orig_c + c + suffix)

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([domain.split(".")[-1]])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        resultList = checkResult(rLoc, resultList)
        try:
            resultList.remove(domain)
        except:
            pass

        while len(resultList) > limit:
            resultList.pop()

    return resultList


def addition(domain, resultList, verbose, limit):
    """Add a character in the domain name"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Addition")

        resultLoc = list()
        loclist = list()

        domainList = domain.split(".")[:-1]

        for name in domainList:
            for i in (*range(48, 58), *range(97, 123)):
                if name + chr(i) not in resultLoc:
                    resultLoc.append(name + chr(i))

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([domain.split(".")[-1]])

        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        resultList = checkResult(rLoc, resultList)
        try:
            resultList.remove(domain)
        except:
            pass

        while len(resultList) > limit:
            resultList.pop()

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

def missingDot(domain, resultList, verbose, limit):
    """Omission of a dot from the domain name"""

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

        for i in range(0, len(resultLoc)):
            if domainList[-1] in resultLoc[i].split(".")[0]:
                resultLoc[i] = resultLoc[i] + ".com"
            
            if resultLoc[i] not in resultList:
                cp += 1
                resultList.append(resultLoc[i])

        if verbose:
            print(f"{cp}\n")

        try:
            resultList.remove(domain)
        except:
            pass
        
        while len(resultList) > limit:
            resultList.pop()

    return resultList

def stripDash(domain, resultList, verbose, limit):
    """Omission of a dash from the domain name"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Strip Dash")

        loc = domain
        cp = 0
        while "-" in loc:
            loc2 = loc[::-1].replace("-", "", 1)[::-1]
            loc = loc.replace("-", "", 1)

            if loc not in resultList:
                cp += 1
                resultList.append(loc)

            if loc2 not in resultList:
                cp += 1
                resultList.append(loc2)
        
        if verbose:
            print(f"{cp}\n")

        try:
            resultList.remove(domain)
        except:
            pass

        while len(resultList) > limit:
            resultList.pop()

    return resultList

def vowel_swap(domain, resultList, verbose, limit):
    """Swap vowels within the domain name"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Vowel Swap")

        resultLoc = list()
        loclist = list()
        # vowels = 'aeiouy'
        vowels = ["a", "e", "i", "o", "u", "y"]

        domainList = domain.split(".")[:-1]

        for name in domainList:
            for i in range(0, len(name)):
                for vowel in vowels:
                    if name[i] in vowels:
                        if name[:i] + vowel + name[i+1:] not in resultLoc:
                            resultLoc.append(name[:i] + vowel + name[i+1:])

            for j in vowels:
                for k in vowels:
                    if j != k:
                        loc = name.replace(k, j)
                        if loc not in resultLoc:
                            resultLoc.append(loc)

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([domain.split(".")[-1]])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        resultList = checkResult(rLoc, resultList)
        try:
            resultList.remove(domain)
        except:
            pass

        while len(resultList) > limit:
            resultList.pop()

    return resultList


def hyphenation(domain, resultList, verbose, limit):
    """Addition of a hypen '-' between the first and last character in a string"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Hyphenation")

        resultLoc = list()
        loclist = list()

        domainList = domain.split(".")[:-1]

        for name in domainList:
            for i in range(1, len(name)):
                if name[:i] + '-' + name[i:] not in resultLoc:
                    resultLoc.append(name[:i] + '-' + name[i:])

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([domain.split(".")[-1]])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        resultList = checkResult(rLoc, resultList)
        try:
            resultList.remove(domain)
        except:
            pass

        while len(resultList) > limit:
            resultList.pop()

    return resultList


def bitsquatting(domain, resultList, verbose, limit):
    """The character is substituted with the set of valid characters that can be made after a single bit flip"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Bitsquatting")

        resultLoc = list()
        loclist = list()

        masks = [1, 2, 4, 8, 16, 32, 64, 128]
        chars = set('abcdefghijklmnopqrstuvwxyz0123456789-')

        domainList = domain.split(".")[:-1]

        for name in domainList:
            for i, c in enumerate(name):
                for mask in masks:
                    b = chr(ord(c) ^ mask)
                    if b in chars:
                        if name[:i] + b +name[i+1:] not in resultLoc:
                            resultLoc.append(name[:i] + b +name[i+1:])

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([domain.split(".")[-1]])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        resultList = checkResult(rLoc, resultList)
        try:
            resultList.remove(domain)
        except:
            pass

        while len(resultList) > limit:
            resultList.pop()

    return resultList


def homoglyph(domain, resultList, verbose, limit):
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

        domainList = domain.split(".")[:-1]
        tld = domain.split(".")[-1]

        s = ""
        for d in domainList:
            s += d + "."
        s = s[:-1]

        result1 = set(mix(s))
        result2 = set()
        cp = 0

        for r in result1:
            result2.update(set(mix(r)))
        
        for element in list(result1 | result2):
            if element not in resultList:
                cp += 1
                resultList.append(element + "." + tld)

        if verbose:
            print(f"{cp}\n")

        try:
            resultList.remove(domain)
        except:
            pass

        while len(resultList) > limit:
            resultList.pop()

    return resultList


def commonMisspelling(domain, resultList, verbose, limit):
    """Change a word by is misspellings"""
    # https://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/For_machines

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Common Misspelling")

        with open(pathEtc + "/common-misspellings.json", "r") as read_json:
            misspelling = json.load(read_json)
            keys = misspelling.keys()

        domainList = domain.split(".")[:-1]
        resultLoc = list()
        loclist = list()

        for name in domainList:
            if name in keys:
                misspell = misspelling[name].split(",")
                for mis in misspell:
                    if mis.replace(" ","") not in resultLoc:
                        resultLoc.append(mis.replace(" ",""))
            elif name not in resultLoc:
                resultLoc.append(name)

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([domain.split(".")[-1]])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        resultList = checkResult(rLoc, resultList)
        try:
            resultList.remove(domain)
        except:
            pass

        while len(resultList) > limit:
            resultList.pop()

    return resultList


def homophones(domain, resultList, verbose, limit):
    """Change word by an other who sound the same when spoken"""
    # From http://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/Homophones
    # Last updated 04/2020
    # cat /tmp/h | sed 's/^[ ]*//g' | egrep -v "These pairs become homophones in certain dialects only|^Names" | sed -E 's/ (and|or) /,/g' | sed 's/\//,/g' | sed 's/,,/,/g' | tr '[:upper:]' '[:lower:]' | tr -d " '" | grep -v "^$"

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Homophones")

        with open(pathEtc + "/homophones.txt", "r") as read_file:
            homophones = read_file.readlines()
        
        domainList = domain.split(".")[:-1]
        resultLoc = list()
        loclist = list()

        for name in domainList:
            for lines in homophones:
                line = lines.split(",")
                for word in line:
                    if name == word.rstrip("\n"):
                        for otherword in line:
                            if otherword.rstrip("\n") not in resultLoc and otherword.rstrip("\n") != name:
                                resultLoc.append(otherword.rstrip("\n"))
                    elif name not in resultLoc:
                        resultLoc.append(name)

            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([domain.split(".")[-1]])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        resultList = checkResult(rLoc, resultList)
        try:
            resultList.remove(domain)
        except:
            pass

        while len(resultList) > limit:
            resultList.pop()

    return resultList
    

def wrongTld(domain, resultList, verbose, limit):
    """Change the original top level domain to another"""
    # https://data.iana.org/TLD/tlds-alpha-by-domain.txt
    # Version 2022012800

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Wrong Tld")

        with open(pathEtc + "/tlds-alpha-by-domain.txt", "r") as read_file:
            tlds = read_file.readlines()
        
        originalTld = domain.split(".")[-1]
        domainLoc = ""
        cp = 0 

        for element in domain.split(".")[:-1]:
            domainLoc += element + "."

        for tld in tlds:
            if tld.lower().rstrip("\n") != originalTld:
                cp += 1
                resultList.append(domainLoc + tld.lower().rstrip("\n"))
        
        if verbose:
            print(f"{cp}\n")

        try:
            resultList.remove(domain)
        except:
            pass

        while len(resultList) > limit:
            resultList.pop()

    return resultList


def addTld(domain, resultList, verbose, limit):
    """Adding a tld before the original tld"""
    # https://data.iana.org/TLD/tlds-alpha-by-domain.txt
    # Version 2022012800

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Adding Tld")
        with open(pathEtc + "/tlds-alpha-by-domain.txt", "r") as read_file:
            tlds = read_file.readlines()
        
        cp = 0 
        for tld in tlds:
            cp += 1
            resultList.append(domain + "." + tld.lower().rstrip("\n"))
        
        if verbose:
            print(f"{cp}\n")

        try:
            resultList.remove(domain)
        except:
            pass

        while len(resultList) > limit:
            resultList.pop()

    return resultList


def subdomain(domain, resultList, verbose, limit):
    """Insert a dot at varying positions to create subdomain"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Subdomain")

        cp = 0

        for i in range(1, len(domain)-1):
            if domain[i] not in ['-', '.'] and domain[i-1] not in ['-', '.']:
                cp += 1
                resultList.append(domain[:i] + '.' + domain[i:])

        if verbose:
            print(f"{cp}\n")

        try:
            resultList.remove(domain)
        except:
            pass

        while len(resultList) > limit:
            resultList.pop()

    return resultList


def singularPluralize(domain, resultList, verbose, limit):
    """Create by making a singular domain plural and vice versa"""

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Singular Pluralize")
            
        resultLoc = list()
        loclist = list()
        inflector = inflect.engine()

        domainList = domain.split(".")[:-1]

        for name in domainList:
            
            loc = inflector.plural(name)
            resultLoc.append(name)

            if loc and loc not in resultLoc:
                resultLoc.append(loc)
            
            if resultLoc:
                loclist.append(resultLoc)
                resultLoc = list()

        loclist.append([domain.split(".")[-1]])
        rLoc = globalAppend(loclist)

        if verbose:
            print(f"{len(rLoc)}\n")

        resultList = checkResult(rLoc, resultList)
        try:
            resultList.remove(domain)
        except:
            pass

        while len(resultList) > limit:
            resultList.pop()

    return resultList

def changeDotHyph(domain, resultList, verbose, limit):
    """Change dot to hyphenation '-' """

    if not len(resultList) >= limit:
        if verbose:
            print("[+] Change dot to hyphenation")

        loc = domain
        while "." in loc:
            resultLoc = list()
            resultLoc2 = list()
            loc2 = loc[::-1].replace(".", "-", 1)[::-1]
            loc = loc.replace(".", "-", 1)

            if "." not in loc:
                resultLoc = addTld(loc, resultLoc, verbose, limit)
                resultList = checkResult(resultLoc, resultList)
            
            elif loc not in resultList:
                resultList.append(loc)

            resultLoc2 = addTld(loc2, resultLoc2, verbose, limit)
            resultList = checkResult(resultLoc2, resultList)

            try:
                resultList.remove(domain)
            except:
                pass

        while len(resultList) > limit:
            resultList.pop()

    return resultList


def runAll(domain, limit, formatoutput, pathOutput, verbose=False):
    """Run all algo on each domain contain in domainList"""

    resultList = list()

    resultList = characterOmission(domain, resultList, verbose, limit)

    resultList = repetition(domain, resultList, verbose, limit)

    resultList = transposition(domain, resultList, verbose, limit)

    resultList = replacement(domain, resultList, verbose, limit)

    resultList = doubleReplacement(domain, resultList, verbose, limit)

    resultList = changeOrder(domain, resultList, verbose, limit)

    resultList = insertion(domain, resultList, verbose, limit)

    resultList = addition(domain, resultList, verbose, limit)

    resultList = missingDot(domain, resultList, verbose, limit)

    resultList = stripDash(domain, resultList, verbose, limit)

    resultList = vowel_swap(domain, resultList, verbose, limit)

    resultList = hyphenation(domain, resultList, verbose, limit)

    resultList = bitsquatting(domain, resultList, verbose, limit)

    resultList = homoglyph(domain, resultList, verbose, limit)

    resultList = commonMisspelling(domain, resultList, verbose, limit)

    resultList = homophones(domain, resultList, verbose, limit)

    resultList = wrongTld(domain, resultList, verbose, limit)

    resultList = addTld(domain, resultList, verbose, limit)

    resultList = subdomain(domain, resultList, verbose, limit)

    resultList = singularPluralize(domain, resultList, verbose, limit)

    resultList = changeDotHyph(domain, resultList, verbose, limit)


    if verbose:
        print(f"Total: {len(resultList)}")

    formatOutput(formatoutput, resultList, domain, pathOutput)

    return resultList


def dnsResolving(resultList, domain, pathOutput):
    """Do a dns resolving on each variations and then create a json"""

    import dns.name
    import dns.resolver
    print("[+] Dns Resolving...")
    domain_resolve = dict()

    for result in resultList:
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
            domain_resolve[result]['NotExist'] = True
        else:
            domain_resolve[result]['NotExist'] = False

    if not pathOutput == "-":
        with open(f"{pathOutput}/{domain}_resolve.json", "w", encoding='utf-8') as write_json:
            json.dump(domain_resolve, write_json, indent=4)
    else:
        sys.stdout.write(json.dumps(domain_resolve))

    return domain_resolve


def formatYara(resultList, domain):
    """Output in yara format"""
    domainReplace = domain.replace(".", "_")

    rule = f"rule {domainReplace} {{\n\tmeta:\n\t\t"
    rule += f'domain = "{domain}"\n\t'
    rule += "strings: \n"

    cp = 0
    for result in resultList: 
        rule += f'\t\t$s{cp} = "{result}"\n'
        cp += 1
    
    rule += "\tcondition:\n\t\t any of ($s*)\n}" 

    return rule

def formatRegex(resultList):
    """Output in regex format"""
    regex = ""
    for result in resultList:
        reg = ""
        for car in result:
            if car in string.ascii_letters or car in string.digits:
                reg += car
            elif car in string.punctuation:
                reg += "\\" + car
        regex += f"{reg}|"
    regex = regex[:-1]

    return regex

def formatYaml(resultList, domain):
    """Output in yaml format"""
    yaml_file = {"title": domain}
    variations = list()

    for result in resultList:
        variations.append(result)

    yaml_file["variations"] = variations

    return yaml_file

def formatOutput(format, resultList, domain, pathOutput):
    """
    Call different function to create the right format file
    """

    if format == "text":
        if not pathOutput == "-":
            with open(f"{pathOutput}/{domain}.txt", "w", encoding='utf-8') as write_file:
                for element in resultList:
                    write_file.write(element + "\n")
        else:
            for element in resultList:
                sys.stdout.write(element + "\n")
    elif format == "yara":
        yara = formatYara(resultList, domain)
        if not pathOutput == "-":
            with open(f"{pathOutput}/{domain}.yar", "w", encoding='utf-8') as write_file:
                write_file.write(yara)
        else:
            sys.stdout.write(yara)
    elif format == "regex":
        regex = formatRegex(resultList)
        if not pathOutput == "-":
            with open(f"{pathOutput}/{domain}.regex", "w", encoding='utf-8') as write_file:
                write_file.write(regex)
        else:
            sys.stdout.write(regex)
    elif format == "yaml":
        yaml_file = formatYaml(resultList, domain)
        if not pathOutput == "-":
            with open(f"{pathOutput}/{domain}.yml", "w", encoding='utf-8') as write_file:
                yaml.dump(yaml_file, write_file)
        else:
            sys.stdout.write(yaml)




if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", help="verbose, more display", action="store_true")

    parser.add_argument("-dn", "--domainName", nargs="+", help="list of domain name")
    parser.add_argument("-fdn", "--filedomainName", help="file containing list of domain name")

    parser.add_argument("-o", "--output", help="path to ouput location", required=True)
    parser.add_argument("-fo", "--formatoutput", help="format for the output file, yara - regex - yaml - text. Default: text")

    parser.add_argument("-dnsr", "--dnsresolving", help="resolve all variation of domain name to see if it's up or not", action="store_true")

    parser.add_argument("-l", "--limit", help="limit of variations for a domain name")

    parser.add_argument("-a", "--all", help="Use all algo", action="store_true")
    parser.add_argument("-co", "--characteromission", help="Leave out a letter of the domain name", action="store_true")
    parser.add_argument("-repe", "--repetition", help="Character Repeat", action="store_true")
    parser.add_argument("-tra", "--transposition", help="Swappe the order of adjacent letters in the domain name", action="store_true")
    parser.add_argument("-repl", "--replacement", help="Adjacent character replacement to the immediate left and right on the keyboard", action="store_true")
    parser.add_argument("-drepl", "--doublereplacement", help="Double Character Replacement", action="store_true")
    parser.add_argument("-cho", "--changeorder", help="Change the order of letters in word", action="store_true")
    parser.add_argument("-ins", "--insertion", help="Adjacent character insertion of letters to the immediate left and right on the keyboard of each letter", action="store_true")
    parser.add_argument("-add", "--addition", help="Add a character in the domain name", action="store_true")
    parser.add_argument("-md", "--missingdot", help="Omission of a dot from the domain name", action="store_true")
    parser.add_argument("-sd", "--stripdash", help="Omission of a dash from the domain name", action="store_true")
    parser.add_argument("-vs", "--vowelswap", help="Swap vowels within the domain name", action="store_true")
    parser.add_argument("-hyp", "--hyphenation", help="Addition of a hypen '-' between the first and last character in a string", action="store_true")
    parser.add_argument("-bs", "--bitsquatting", help="The character is substituted with the set of valid characters that can be made after a single bit flip", action="store_true")
    parser.add_argument("-hg", "--homoglyph", help="One or more characters that look similar to another character but are different are called homogylphs", action="store_true")
    parser.add_argument("-cm", "--commonmisspelling", help="Change a word by is misspellings", action="store_true")
    parser.add_argument("-hp", "--homophones", help="Change word by an other who sound the same when spoken", action="store_true")
    parser.add_argument("-wt", "--wrongtld", help="Change the original top level domain to another", action="store_true")
    parser.add_argument("-at", "--addtld", help="Adding a tld before the original tld", action="store_true")
    parser.add_argument("-sub", "--subdomain", help="Insert a dot at varying positions to create subdomain", action="store_true")
    parser.add_argument("-sp", "--singularpluralize", help="Create by making a singular domain plural and vice versa", action="store_true")
    parser.add_argument("-cdh", "--changedothyphenation", help="Change dot to hyphenation", action="store_true")
    
    args = parser.parse_args()

    resultList = list()

    verbose = args.v

    limit = math.inf
    if args.limit:
        limit = int(args.limit)
    reachLimit = False

    pathOutput = args.output

    if not pathOutput == "-":
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

    # the option for all algo to run is selected
    if args.all:
        for domain in domainList:
            print(f"\n\t[*****] {domain} [*****]")

            resultList = runAll(domain, limit, formatoutput, pathOutput, verbose)

            if args.dnsresolving:
                dnsResolving(resultList, domain, pathOutput)
                                
            resultList = list()

    # The user select sepcial algo but not all
    else:
        for domain in domainList:
            print(f"\n\t[*****] {domain} [*****]")

            if args.characteromission:
                resultList = characterOmission(domain, resultList, verbose, limit)

            if args.repetition:
                resultList = repetition(domain, resultList, verbose, limit)

            if args.transposition:
                resultList = transposition(domain, resultList, verbose, limit)

            if args.replacement:
                resultList = replacement(domain, resultList, verbose, limit)

            if args.doublereplacement:
                resultList = doubleReplacement(domain, resultList, verbose, limit)
            
            if args.changeorder:
                resultList = changeOrder(domain, resultList, verbose, limit)

            if args.insertion:
                resultList = insertion(domain, resultList, verbose, limit)

            if args.addition:
                resultList = addition(domain, resultList, verbose, limit)

            if args.missingdot:
                resultList = missingDot(domain, resultList, verbose, limit)

            if args.stripdash:
                resultList = stripDash(domain, resultList, verbose, limit)

            if args.vowelswap:
                resultList = vowel_swap(domain, resultList, verbose, limit)

            if args.hyphenation:
                resultList = hyphenation(domain, resultList, verbose, limit)

            if args.bitsquatting:
                resultList = bitsquatting(domain, resultList, verbose, limit)

            if args.homoglyph:
                resultList = homoglyph(domain, resultList, verbose, limit)

            if args.commonmisspelling:
                resultList = commonMisspelling(domain, resultList, verbose, limit)

            if args.homophones:
                resultList = homophones(domain, resultList, verbose, limit)

            if args.wrongtld:
                resultList = wrongTld(domain, resultList, verbose, limit)

            if args.addtld:
                resultList = addTld(domain, resultList, verbose, limit)

            if args.subdomain:
                resultList = subdomain(domain, resultList, verbose, limit)

            if args.singularpluralize:
                resultList = singularPluralize(domain, resultList, verbose, limit)
            
            if args.changedothyphenation:
                resultList = changeDotHyph(domain, resultList, verbose, limit)

            try:
                resultList.remove(domain)
            except:
                pass

            if verbose:
                print(f"Total: {len(resultList)}")
            
            formatOutput(formatoutput, resultList, domain, pathOutput)


            if args.dnsresolving:
                domain_resolve = dict()

                dnsResolving(resultList, domain, pathOutput)

            resultList = list()
