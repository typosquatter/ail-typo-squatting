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

def characterOmission(domain):
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

    return globalAppend(loclist)


def repetition(domain):
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

    return globalAppend(loclist)


def transposition(domain):
    """Adjacent Character Swap"""
    resultLoc = list()
    loclist = list()

    domainList = domain.split(".")

    for name in domainList:
        for i in range(len(name)-1):
            if name[:i] + name[i+1] + name[i] + name[i+2:] not in resultLoc:
                resultLoc.append(name[:i] + name[i+1] + name[i] + name[i+2:])

        loclist.append(resultLoc)
        resultLoc = list()
    
    return globalAppend(loclist)


def replacement(domain):
    """Adjacent Character Replacement"""
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

    return globalAppend(loclist)


def doubleReplacement(domain):
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

    return globalAppend(loclist)


def insertion(domain):
    """Adjacent Character Insertion"""

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

    return globalAppend(loclist)

def addition(domain):
    resultLoc = list()
    loclist = list()

    domainList = domain.split(".")

    for name in domainList:
        for i in (*range(48, 58), *range(97, 123)):
            if name + chr(i) not in resultLoc:
                resultLoc.append(name + chr(i))

        loclist.append(resultLoc)
        resultLoc = list()

    return globalAppend(loclist)


def utilMissingDot(resultLoc, loc):
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

def missingDot(domain):
    resultLoc = list()

    domainList = domain.split(".")

    loc = domain
    utilMissingDot(resultLoc, loc)
    
    loc = f"www{domain}"
    utilMissingDot(resultLoc, loc)

    for i in range(0, len(resultLoc)):
        if domainList[-1] in resultLoc[i].split(".")[0]:
            resultLoc[i] = resultLoc[i] + ".com"
    
    return resultLoc

def stripDash(domain):
    resultLoc = list()
    loc = domain

    i = 0
    while "-" in loc:
        loc2 = loc[::-1].replace("-", "", 1)[::-1]
        loc = loc.replace("-", "", 1)

        if loc not in resultLoc:
            resultLoc.append(loc)

        if loc2 not in resultLoc:
            resultLoc.append(loc2) 
        i += 1

    return resultLoc

def vowel_swap(domain):
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

    return globalAppend(loclist)

def hyphenation(domain):
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
    return globalAppend(loclist)


def bitsquatting(domain):
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

    return globalAppend(loclist)


def homoglyph(domain):
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

    return result1 | result2


def commonMisspelling(domain):
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

    return globalAppend(loclist)


def homophones(domain):
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

    return globalAppend(loclist)
    

def wrongTld(domain):
    # https://data.iana.org/TLD/tlds-alpha-by-domain.txt
    # Version 2022012800

    with open(pathEtc + "/tlds-alpha-by-domain.txt", "r") as read_file:
        tlds = read_file.readlines()
    
    originalTld = domain.split(".")[-1]
    resultLoc = list()
    domainLoc = ""
    for element in domain.split(".")[:-1]:
        domainLoc += element + "."

    for tld in tlds:
        if tld.lower().rstrip("\n") != originalTld:
            resultLoc.append(domainLoc + tld.lower().rstrip("\n"))
    
    return resultLoc

def subdomain(domain):
    resultLoc = list()
    for i in range(1, len(domain)-1):
        if domain[i] not in ['-', '.'] and domain[i-1] not in ['-', '.']:
            resultLoc.append(domain[:i] + '.' + domain[i:])
    
    return resultLoc


def singularPluralize(domain, inflector):

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

    return globalAppend(loclist)


domain = "google.abuse.it"

inflector = inflect.engine()

# result = characterOmission(domain) # 144
# result = repetition(domain) # 75
# result = transposition(domain) # 40
# result = replacement(domain) # 18315
# result = doubleReplacement(domain) # 18315
# result = insertion(domain) # 16800
# result = addition(domain) # 46656
# result = missingDot(domain) # 6
# result = stripDash(domain)
# result = vowel_swap(domain) # 2016
# result = hyphenation(domain) # 20
# result = bitsquatting(domain) # 6210
# result = homoglyph(domain) # 12486
# result = commonMisspelling(domain)
# result = homophones(domain)
result = wrongTld(domain) # 1487
# result = subdomain(domain)
# result = singularPluralize(domain, inflector)

print(result)
print(len(result))

# print(set(result))
# print(len(set(result)))
