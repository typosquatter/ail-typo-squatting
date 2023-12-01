import argparse

def getArguments():
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
    parser.add_argument("-uddns", "--updatedynamicdns", help="Update dynamic dns warning list", action="store_true")
    parser.add_argument("-ns", "--numeralswap", help="Change a numbers to words and vice versa. Ex: circlone.lu, circl1.lu", action="store_true")
    parser.add_argument("-combo", help="Combine multiple algo on a domain name", action="store_true")
    parser.add_argument("-ca", "--catchall", help="Combine with -dnsr. Generate a random string in front of the domain.", action="store_true")

    return parser
    