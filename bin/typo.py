import os
import re
import sys
import json
import inflect

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
    'z': ['ʐ', 'ż', 'ź', 'ᴢ', 'ƶ', 'ẓ', 'ẕ', 'ⱬ']
    }


def globalAppend(loclist):
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
    for element in resultLoc:
        if element not in resultList:
            resultList.append(element)

    return resultList


def characterOmission(domain, resultList):
    """Leave out a letter of the domain name"""

    resultLoc = list()
    loclist = list()

    domainList = domain.split(".")

    for name in domainList:
        for i in range(0,len(name)):
            resultLoc.append(name)
            loc = name[0:i]
            loc += name[i+1:len(name)]

            if loc not in resultLoc:
                resultLoc.append(loc)

        loclist.append(resultLoc)
        resultLoc = list()

    rLoc = globalAppend(loclist)

    return checkResult(rLoc, resultList)

def repetition(domain, resultList):
    """Character Repeat"""

    resultLoc = list()
    loclist = list()

    domainList = domain.split(".")

    for name in domainList:
        for i, c in enumerate(name):
            if name[:i] + c + name[i:] not in resultLoc:
                resultLoc.append(name[:i] + c + name[i:])

        loclist.append(resultLoc)
        resultLoc = list()

    rLoc = globalAppend(loclist)

    return checkResult(rLoc, resultList)


def transposition(domain, resultList):
    """Swappe the order of adjacent letters in the domain name"""

    resultLoc = list()
    loclist = list()

    domainList = domain.split(".")

    for name in domainList:
        for i in range(len(name)-1):
            if name[:i] + name[i+1] + name[i] + name[i+2:] not in resultLoc:
                resultLoc.append(name[:i] + name[i+1] + name[i] + name[i+2:])

        loclist.append(resultLoc)
        resultLoc = list()
    
    rLoc = globalAppend(loclist)

    return checkResult(rLoc, resultList)


def replacement(domain, resultList):
    """Adjacent character replacement to the immediate left and right on the keyboard"""

    resultLoc = list()
    loclist = list()

    domainList = domain.split(".")

    for name in domainList:
        for i, c in enumerate(name):
            pre = name[:i]
            suf = name[i+1:]
            for layout in keyboards:
                for r in layout.get(c, ''):
                    if pre + r + suf not in resultLoc:
                        resultLoc.append(pre + r + suf)

        loclist.append(resultLoc)
        resultLoc = list()

    rLoc = globalAppend(loclist)

    return checkResult(rLoc, resultList)


def doubleReplacement(domain, resultList):
    """Double Character Replacement"""

    resultLoc = list()
    loclist = list()

    domainList = domain.split(".")

    for name in domainList:
        for i, c in enumerate(name):
            pre = name[:i]
            suf = name[i+2:]
            for layout in keyboards:
                for r in layout.get(c, ''):
                    if pre + r + r + suf not in resultLoc:
                        resultLoc.append(pre + r + r + suf)

        loclist.append(resultLoc)
        resultLoc = list()

    rLoc = globalAppend(loclist)

    return checkResult(rLoc, resultList)


def insertion(domain, resultList):
    """Adjacent character insertion of letters to the immediate left and right on the keyboard of each letter"""

    resultLoc = list()
    loclist = list()

    domainList = domain.split(".")

    for name in domainList:
        for i in range(1, len(name)-1):
            prefix, orig_c, suffix = name[:i], name[i], name[i+1:]
            for c in (c for keys in keyboards for c in keys.get(orig_c, [])):
                if prefix + c + orig_c + suffix not in resultLoc:
                    resultLoc.append(prefix + c + orig_c + suffix)
                if prefix + orig_c + c + suffix not in resultLoc:
                    resultLoc.append(prefix + orig_c + c + suffix)

        loclist.append(resultLoc)
        resultLoc = list()

    rLoc = globalAppend(loclist)

    return checkResult(rLoc, resultList)


def addition(domain, resultList):
    """Add a character in the domain name"""

    resultLoc = list()
    loclist = list()

    domainList = domain.split(".")

    for name in domainList:
        for i in (*range(48, 58), *range(97, 123)):
            if name + chr(i) not in resultLoc:
                resultLoc.append(name + chr(i))

        loclist.append(resultLoc)
        resultLoc = list()

    rLoc = globalAppend(loclist)

    return checkResult(rLoc, resultList)


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

def missingDot(domain, resultList):
    """Omition of a dot from the domain name"""

    resultLoc = list()

    domainList = domain.split(".")

    loc = domain
    utilMissingDot(resultLoc, loc)
    
    loc = f"www{domain}"
    utilMissingDot(resultLoc, loc)

    for i in range(0, len(resultLoc)):
        if domainList[-1] in resultLoc[i].split(".")[0]:
            resultLoc[i] = resultLoc[i] + ".com"
        
        if resultLoc[i] not in resultList:
            resultList.append(resultLoc[i])
    
    return resultList

def stripDash(domain, resultList):
    """Omition of a dash from the domain name"""

    loc = domain

    i = 0
    while "-" in loc:
        loc2 = loc[::-1].replace("-", "", 1)[::-1]
        loc = loc.replace("-", "", 1)

        if loc not in resultList:
            resultList.append(loc)

        if loc2 not in resultList:
            resultList.append(loc2) 
        i += 1

    return resultList

def vowel_swap(domain, resultList):
    """Swap vowels within the domain name"""

    resultLoc = list()
    loclist = list()
    # vowels = 'aeiouy'
    vowels = ["a", "e", "i", "o", "u", "y"]

    domainList = domain.split(".")

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

        loclist.append(resultLoc)
        resultLoc = list()

    rLoc = globalAppend(loclist)

    return checkResult(rLoc, resultList)


def hyphenation(domain, resultList):
    """Addition of a hypen - between the first and last character in a string"""

    resultLoc = list()
    loclist = list()

    domainList = domain.split(".")[:-1]

    for name in domainList:
        for i in range(1, len(name)):
            if name[:i] + '-' + name[i:] not in resultLoc:
                resultLoc.append(name[:i] + '-' + name[i:])

        loclist.append(resultLoc)
        resultLoc = list()

    loclist.append([domain.split(".")[-1]])

    rLoc = globalAppend(loclist)

    return checkResult(rLoc, resultList)


def bitsquatting(domain, resultList):
    """The character is substituted with the set of valid characters that can be made after a single bit flip"""

    resultLoc = list()
    loclist = list()

    masks = [1, 2, 4, 8, 16, 32, 64, 128]
    chars = set('abcdefghijklmnopqrstuvwxyz0123456789-')

    domainList = domain.split(".")

    for name in domainList:
        for i, c in enumerate(name):
            for mask in masks:
                b = chr(ord(c) ^ mask)
                if b in chars:
                    if name[:i] + b +name[i+1:] not in resultLoc:
                        resultLoc.append(name[:i] + b +name[i+1:])

        loclist.append(resultLoc)
        resultLoc = list()

    rLoc = globalAppend(loclist)

    return checkResult(rLoc, resultList)


def homoglyph(domain, resultList):
    """One or more characters that look similar to another character but are different are called homogylphs"""

    def mix(domain):
        for w in range(1, len(domain)):
            for i in range(len(domain)-w+1):
                pre = domain[:i]
                win = domain[i:i+w]
                suf = domain[i+w:]
                for c in win:
                    for g in glyphs.get(c, []):
                        yield pre + win.replace(c, g) + suf

    result1 = set(mix(domain))
    result2 = set()

    for r in result1:
        result2.update(set(mix(r)))
    
    for element in list(result1 | result2):
        if element not in resultList:
            resultList.append(element)

    return resultList


def commonMisspelling(domain, resultList):
    """Over 8000 common misspellings from Wikipedia."""
    # https://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/For_machines

    with open(pathEtc + "/common-misspellings.json", "r") as read_json:
        misspelling = json.load(read_json)
        keys = misspelling.keys()

    domainList = domain.split(".")
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

    rLoc = globalAppend(loclist)

    return checkResult(rLoc, resultList)


def homophones(domain, resultList):
    """Over 450 sets of words that sound the same when spoken"""
    # From http://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/Homophones
    # Last updated 04/2020
    # cat /tmp/h | sed 's/^[ ]*//g' | egrep -v "These pairs become homophones in certain dialects only|^Names" | sed -E 's/ (and|or) /,/g' | sed 's/\//,/g' | sed 's/,,/,/g' | tr '[:upper:]' '[:lower:]' | tr -d " '" | grep -v "^$"

    with open(pathEtc + "/homophones.txt", "r") as read_file:
        homophones = read_file.readlines()
    
    domainList = domain.split(".")
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

    rLoc = globalAppend(loclist)

    return checkResult(rLoc, resultList)
    

def wrongTld(domain, resultList):
    """For example, www.trademe.co.nz becomes www.trademe.co.mz and www.google.com becomes www.google.org"""
    # https://data.iana.org/TLD/tlds-alpha-by-domain.txt
    # Version 2022012800

    with open(pathEtc + "/tlds-alpha-by-domain.txt", "r") as read_file:
        tlds = read_file.readlines()
    
    originalTld = domain.split(".")[-1]
    domainLoc = ""
    for element in domain.split(".")[:-1]:
        domainLoc += element + "."

    for tld in tlds:
        if tld.lower().rstrip("\n") != originalTld:
            resultList.append(domainLoc + tld.lower().rstrip("\n"))
    
    return resultList


def subdomain(domain, resultList):
    """Insert a dot at varying positions to create subdomain"""

    for i in range(1, len(domain)-1):
        if domain[i] not in ['-', '.'] and domain[i-1] not in ['-', '.']:
            resultList.append(domain[:i] + '.' + domain[i:])
    
    return resultList


def singularPluralize(domain, resultList, inflector):
    """Create by making a singular domain plural and vice versa."""

    resultLoc = list()
    loclist = list()

    domainList = domain.split(".")

    for name in domainList:
        
        loc = inflector.plural(name)
        resultLoc.append(name)

        if loc and loc not in resultLoc:
            resultLoc.append(loc)
        
        loclist.append(resultLoc)
        resultLoc = list()

    rLoc = globalAppend(loclist)

    return checkResult(rLoc, resultList)


domain = "google.abuse.it"

inflector = inflect.engine()
resultList = list()

# resultList = characterOmission(domain, resultList) # 144
# resultList = repetition(domain, resultList) # 75
# resultList = transposition(domain, resultList) # 40
# resultList = replacement(domain, resultList) # 18315
# resultList = doubleReplacement(domain, resultList) # 18315
# resultList = insertion(domain, resultList) # 16800
# resultList = addition(domain, resultList) # 46656
# resultList = missingDot(domain, resultList) # 6
# resultList = stripDash(domain, resultList)
# resultList = vowel_swap(domain, resultList) # 2016
# resultList = hyphenation(domain, resultList) # 20
# resultList = bitsquatting(domain, resultList) # 6210
resultList = homoglyph(domain, resultList) # 12486
# resultList = commonMisspelling(domain, resultList)
# resultList = homophones(domain, resultList)
# resultList = wrongTld(domain, resultList) # 1487
# resultList = subdomain(domain, resultList)
# resultList = singularPluralize(domain, resultList, inflector)

print(resultList)
print(len(resultList))
