
# Here are stored all the constants used in the project
# The constants are stored in a separate file to make it easier to change them

SIMILAR_CHAR = {
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

NUMERAL = [
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

ALGO_NAME_LIST = [
    "omission", "repetition", "changeOrder", "replacement", "doubleReplacement", 
    "addition", "missingDot", "stripDash", "vowelSwap", "addDash", "homoglyph", 
    "commonMisspelling", "homophones", "wrongTld", "addTld", "subdomain", 
    "singularPluralize", "changeDotDash", "wrongSld", "numeralSwap", "addDynamicDns"
]

DNS_REQUEST_TYPE = ['A', 'AAAA', 'NS', 'MX']

EXCLUDED_TLD = ["gov.pl"] # why not ?


# Getters for constants
def const_get_similar_chars():
    """
    Return the dictionary of similar characters
    """
    return SIMILAR_CHAR

def const_get_numeral():
    """
    Return the list of numeral
    """
    return NUMERAL

def const_get_algo_name_list():
    """
    Return the list of algorithm names
    """
    return ALGO_NAME_LIST

def const_get_dns_request_type():
    """
    Return the list of DNS request type
    """
    return DNS_REQUEST_TYPE

def const_get_excluded_tld():
    """
    Return the list of excluded TLD
    """
    return EXCLUDED_TLD