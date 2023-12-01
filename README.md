# ail-typo-squatting

ail-typo-squatting is a Python library to generate list of potential typo squatting domains with domain name permutation engine to feed AIL and other systems. 

The tool can be used as a stand-alone tool or to feed other systems.

# Requirements

- Python 3.6+
- [inflect](https://github.com/jaraco/inflect) library
- [pyyaml](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [tldextract](https://github.com/john-kurkowski/tldextract)

- [dnspython](https://github.com/rthalley/dnspython)

# Installation

## Source install

ail-typo-squatting can be install with poetry. If you don't have poetry installed, you can do the following `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python`.

```bash
$ poetry install
$ poetry shell
$ cd ail-typo-squatting
$ python typo.py -h
```

## pip installation

```bash
$ pip3 install ail-typo-squatting
```

# Usage

```bash
dacru@dacru:~/git/ail-typo-squatting/bin$ python3 typo.py --help  
usage: typo.py [-h] [-v] [-dn DOMAINNAME [DOMAINNAME ...]] [-fdn FILEDOMAINNAME] [-o OUTPUT] [-fo FORMATOUTPUT] [-br] [-dnsr] [-dnsl] [-l LIMIT] [-var] [-ko] [-a] [-om] [-repe] [-repl] [-drepl] [-cho]
               [-add] [-md] [-sd] [-vs] [-ada] [-hg] [-ahg] [-cm] [-hp] [-wt] [-wsld] [-at] [-sub] [-sp] [-cdd] [-addns] [-uddns] [-ns] [-combo] [-ca]

optional arguments:
  -h, --help            show this help message and exit
  -v                    verbose, more display
  -dn DOMAINNAME [DOMAINNAME ...], --domainName DOMAINNAME [DOMAINNAME ...]
                        list of domain name
  -fdn FILEDOMAINNAME, --filedomainName FILEDOMAINNAME
                        file containing list of domain name
  -o OUTPUT, --output OUTPUT
                        path to ouput location
  -fo FORMATOUTPUT, --formatoutput FORMATOUTPUT
                        format for the output file, yara - regex - yaml - text. Default: text
  -br, --betterregex    Use retrie for faster regex
  -dnsr, --dnsresolving
                        resolve all variation of domain name to see if it's up or not
  -dnsl, --dnslimited   resolve all variation of domain name but keep only up domain in final result json
  -l LIMIT, --limit LIMIT
                        limit of variations for a domain name
  -var, --givevariations
                        give the algo that generate variations
  -ko, --keeporiginal   Keep in the result list the original domain name
  -a, --all             Use all algo
  -om, --omission       Leave out a letter of the domain name
  -repe, --repetition   Character Repeat
  -repl, --replacement  Character replacement
  -drepl, --doublereplacement
                        Double Character Replacement
  -cho, --changeorder   Change the order of letters in word
  -add, --addition      Add a character in the domain name
  -md, --missingdot     Delete a dot from the domain name
  -sd, --stripdash      Delete of a dash from the domain name
  -vs, --vowelswap      Swap vowels within the domain name
  -ada, --adddash       Add a dash between the first and last character in a string
  -hg, --homoglyph      One or more characters that look similar to another character but are different are called homogylphs
  -ahg, --all_homoglyph
                        generate all possible homoglyph permutations. Ex: circl.lu, e1rc1.lu
  -cm, --commonmisspelling
                        Change a word by is misspellings
  -hp, --homophones     Change word by an other who sound the same when spoken
  -wt, --wrongtld       Change the original top level domain to another
  -wsld, --wrongsld     Change the original second level domain to another
  -at, --addtld         Adding a tld before the original tld
  -sub, --subdomain     Insert a dot at varying positions to create subdomain
  -sp, --singularpluralize
                        Create by making a singular domain plural and vice versa
  -cdd, --changedotdash
                        Change dot to dash
  -addns, --adddynamicdns
                        Add dynamic dns at the end of the domain
  -uddns, --updatedynamicdns
                        Update dynamic dns warning list
  -ns, --numeralswap    Change a numbers to words and vice versa. Ex: circlone.lu, circl1.lu
  -combo                Combine multiple algo on a domain name
  -ca, --catchall       Combine with -dnsr. Generate a random string in front of the domain.

```

# Usage example

1. Creation of variations for `ail-project.org` and `circl.lu`, using all algorithm.

```bash
dacru@dacru:~/git/ail-typo-squatting/bin$ python3 typo.py -dn ail-project.org circl.lu -a -o .
```

2. Creation of variations for a file who contains domain name, using character omission - subdomain - hyphenation.

```bash
dacru@dacru:~/git/ail-typo-squatting/bin$ python3 typo.py -fdn domain.txt -co -sub -hyp -o . -fo yara
```

3. Creation of variations for `ail-project.org` and `circl.lu`, using all algorithm and using dns resolution.

```bash
dacru@dacru:~/git/ail-typo-squatting/bin$ python3 typo.py -dn ail-project.org circl.lu -a -dnsr -o .
```

4. Creation of variations for `ail-project.org`  and give the algorithm that generate the variation (**only for text format**).

```bash
dacru@dacru:~/git/ail-typo-squatting/bin$ python3 typo.py -dn ail-project.org -a -o - -var
```

# Used as a library

## To run all algorithms

```python
from ail_typo_squatting import runAll
import math

resultList = list()
domainList = ["google.com"]
formatoutput = "yara"
pathOutput = "."
for domain in domainList:
    resultList = runAll(
        domain=domain, 
        limit=math.inf, 
        formatoutput=formatoutput, 
        pathOutput=pathOutput, 
        verbose=False, 
        givevariations=False,
        keeporiginal=False
    )

    print(resultList)
    resultList = list()
```

## To run specific algorithm

```python
from ail_typo_squatting import formatOutput, omission, subdomain, addDash
import math

resultList = list()
domainList = ["google.com"]
limit = math.inf
formatoutput = "yara"
pathOutput = "."
for domain in domainList:
    resultList = omission(domain=domain, resultList=resultList, verbose=False, limit=limit, givevariations=False,  keeporiginal=False)

    resultList = subdomain(domain=domain, resultList=resultList, verbose=False, limit=limit, givevariations=False,  keeporiginal=False)

    resultList = addDash(domain=domain, resultList=resultList, verbose=False, limit=limit, givevariations=False,  keeporiginal=False)

    print(resultList)
    formatOutput(format=formatoutput, resultList=resultList, domain=domain, pathOutput=pathOutput, givevariations=False)

    resultList = list()
```

# Sample output

There's **4 format** possible for the output file:

- text
- yara
- regex
- sigma

For **Text** file, each line is a variation.

```
ail-project.org
il-project.org
al-project.org
ai-project.org
ailproject.org
ail-roject.org
ail-poject.org
ail-prject.org
ail-proect.org
ail-projct.org
ail-projet.org
ail-projec.org
aail-project.org
aiil-project.org
...
```

For **Yara** file, each rule is a variation.

```
rule ail-project_org {
    meta:
        domain = "ail-project.org"
    strings: 
        $s0 = "ail-project.org"
        $s1 = "il-project.org"
        $s2 = "al-project.org"
        $s3 = "ai-project.org"
        $s4 = "ailproject.org"
        $s5 = "ail-roject.org"
        $s6 = "ail-poject.org"
        $s7 = "ail-prject.org"
        $s8 = "ail-proect.org"
        $s9 = "ail-projct.org"
        $s10 = "ail-projet.org"
        $s11 = "ail-projec.org"
    condition:
         any of ($s*)
}
```

For **Regex** file, each variations is transform into regex and concatenate with other to do only one big regex.

```
ail\-project\.org|il\-project\.org|al\-project\.org|ai\-project\.org|ailproject\.org|ail\-roject\.org|ail\-poject\.org|ail\-prject\.org|ail\-proect\.org|ail\-projct\.org|ail\-projet\.org|ail\-projec\.org
```

For **Sigma** file, each variations are list under `variations` key.

```
title: ail-project.org
variations:
- ail-project.org
- il-project.org
- al-project.org
- ai-project.org
- ailproject.org
- ail-roject.org
- ail-poject.org
- ail-prject.org
- ail-proect.org
- ail-projct.org
- ail-projet.org
- ail-projec.org
```

## DNS output

In case DNS resolve is selected, an additional file will be created in JSON format

each keys are variations and may have a field "ip" if the domain name have been resolved. The filed "NotExist" will be there each time with a Boolean value to determine if the domain is existing or not.

```json
{
    "circl.lu": {
        "NotExist": false,
        "ip": [
            "185.194.93.14"
        ]
    },
    "ircl.lu": {
        "NotExist": true
    },
    "crcl.lu": {
        "NotExist": true
    },
    "cicl.lu": {
        "NotExist": true
    },
    "cirl.lu": {
        "NotExist": true
    },
    "circ.lu": {
        "NotExist": true
    },
    "ccircl.lu": {
        "NotExist": true
    },
    "ciircl.lu": {
        "NotExist": true
    },
    ...
}
```

# List of algorithms used

| Algo               | Description                                                                                                                                                                                                                               |
|:------------------ |:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AddDash            | These typos are created by adding a dash between the first and last character in a string.                                                                                                                                                |
| Addition           | These typos are created by add a characters in the domain name.                                                                                                                                                                           |
| AddDynamicDns      | These typos are created by adding a dynamic dns at the end of the original domain.                                                                                                                                                        |
| AddTld             | These typos are created by adding a tld before the right tld. Example: google.com becomes google.com.it                                                                                                                                   |
| ChangeDotDash      | These typos are created by changing a dot to a dash.                                                                                                                                                                                      |
| ChangeOrder        | These typos are created by changing the order of letters in the each part of the domain.                                                                                                                                                  |
| Combo              | These typos are created by combining multiple algorithms. For example, circl.lu becomes cirl6.lu                                                                                                                                          |
| CommonMisspelling  | These typos are created by changing a word by is misspelling. Over 8000 common misspellings from Wikipedia. For example, www.youtube.com becomes www.youtub.com and www.abseil.com becomes www.absail.com.                                |
| Double Replacement | These typos are created by replacing identical, consecutive letters of the domain name.                                                                                                                                                   |
| Homoglyph          | These typos are created by replacing characters to another character that look similar but are different.  An example is that the lower case l looks similar to the numeral one, e.g. l vs 1. For example, google.com becomes goog1e.com. |
| Homophones         | These typos are created by changing word by an other who sound the same when spoken. Over 450 sets of words that sound the same when spoken. For example, www.base.com becomes www.bass.com.                                              |
| MissingDot         | These typos are created by deleting a dot from the domain name.                                                                                                                                                                           |
| NumeralSwap        | These typos are created by changing a number to words and vice versa. For example, circlone.lu becomes circl1.lu.                                                                                                                         |
| Omission           | These typos are created by leaving out a letter of the domain name, one letter at a time.                                                                                                                                                 |
| Repetition         | These typos are created by repeating a letter of the domain name.                                                                                                                                                                         |
| Replacement        | These typos are created by replacing each letter of the domain name.                                                                                                                                                                      |
| StripDash          | These typos are created by deleting a dash from the domain name.                                                                                                                                                                          |
| SingularPluralize  | These typos are created by making a singular domain plural and vice versa.                                                                                                                                                                |
| Subdomain          | These typos are created by placing a dot in the domain name in order to create subdomain. Example: google.com becomes goo.gle.com                                                                                                         |
| VowelSwap          | These typos are created by swapping vowels within the domain name except for the first letter. For example, www.google.com becomes www.gaagle.com.                                                                                        |
| WrongTld           | These typos are created by changing the original top level domain to another. For example, www.trademe.co.nz becomes www.trademe.co.mz and www.google.com becomes www.google.org Uses the 19 most common top level domains.               |
| WrongSld           | These typos are created by changing the original second level domain to another. For example, www.trademe.co.uk becomes www.trademe.ac.uk and www.google.com will still be www.google.com .                                               |

# Acknowledgment

![](./img/cef.png)

The project has been co-funded by CEF-TC-2020-2 - 2020-EU-IA-0260 - JTAN - Joint Threat Analysis Network.
