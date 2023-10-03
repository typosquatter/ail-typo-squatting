import string
from retrie.trie import Trie

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
