# Import all the modules

## The public libraries
import os, sys, math, yaml

## The local libraries
from generator.conts.main import *
from generator.utils.generator_functions import check_valid_domain

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

## The format function
from format.yara import formatYara
from format.regex import formatRegex, formatRegexRetrie
from format.yaml import formatYaml

## The dns resolving function
from dns_local.resolving import dnsResolving # named "dns_local" to avoid conflict with the dns library

## The utils
from utils.parser import getArguments
from generator.utils.get_pathetc import get_path_etc
sys.path.append(get_path_etc())


# Import all the constants of data from the file conts/main.py
# If you wanna add a new algorithm, you have to add it in the list algo_list
numerals = const_get_numeral()
algo_list = const_get_algo_name_list()


## [START] Final treatment

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

## [END] Final treatment

# Main file function
if __name__ == "__main__":

    # Step 1: Get the arguments
    parser = getArguments()
    args = parser.parse_args()

    resultList = list()

    # Step 2: Assign some variables
    verbose = args.v
    givevariations = args.givevariations
    dns_limited = args.dnslimited
    keeporiginal = args.keeporiginal

    limit = math.inf
    if args.limit: # If the user has specified a limit
        limit = int(args.limit)

    pathOutput = args.output

    if pathOutput and not pathOutput == "-":
        try:
            os.makedirs(pathOutput)
        except:
            pass # If the directory already exist

    # Step 3: Check the format output
    if args.formatoutput:
        if args.formatoutput == "text" or args.formatoutput == "yara" or args.formatoutput == "yaml" or args.formatoutput == "regex":
            formatoutput = args.formatoutput
        else:
            print("[-] Format type error")
            exit(-1)
    else:
        formatoutput = "text" # Default format

    # Verify that a domain name is receive
    if args.domainName:
        domainList = args.domainName
    elif args.filedomainName:
        with open(args.filedomainName, "r") as read_file:
            domainList = read_file.readlines()
    else:
        print("[-] No Entry")
        exit(-1)

    # Step 4: Check the domain name
    for domain in domainList:
        if domain[0] == '.':
            domain = domain[1:]
        if pathOutput:
            print(f"\n\t[*****] {domain} [*****]")

        # Go to the dedicated function
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

        # Step 5: Final treatment
        if verbose:
            print(f"Total: {len(resultList)}")

        formatOutput(formatoutput, resultList, domain, pathOutput, givevariations, args.betterregex)
        
        # Step 6: DNS resolving for each domain name
        if args.dnsresolving:
            dnsResolving(resultList, domain, pathOutput, verbose, givevariations, dns_limited, args.catchall)

        resultList = list()
