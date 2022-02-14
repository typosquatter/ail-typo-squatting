# ail-typo-squatting
Generate list of domain name using Domain name permutation engine to feed AIL



# (main) Requirements

- [inflect](https://github.com/jaraco/inflect)



## Optionnal

- [dnspython](https://github.com/rthalley/dnspython)





# Installation

ail-typo-squatting can be install with poetry. If you don't have poetry installed, you can do the following `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python`.

~~~
$ poetry install
$ poetry shell
$ ail-typo-squatting -h
~~~





# Usage

```bash
dacru@dacru:~/git/ail-typo-squatting/bin$ python3 typo.py --help  
usage: typo.py [-h] [-d] [-v] [-dn DOMAINNAME [DOMAINNAME ...]] [-fdn FILEDOMAINNAME] -o OUTPUT [-dnsr] [-l LIMIT] [-a] [-co]
               [-repe] [-tra] [-repl] [-drepl] [-ins] [-add] [-md] [-sd] [-vs] [-hyp] [-bs] [-hg] [-cm] [-hp] [-wt]
               [-at] [-sub] [-sp]

optional arguments:
  -h, --help            show this help message and exit
  -v                    verbose, more display
  -dn DOMAINNAME [DOMAINNAME ...], --domainName DOMAINNAME [DOMAINNAME ...]
                        list of domain name
  -fdn FILEDOMAINNAME, --filedomainName FILEDOMAINNAME
                        file containing list of domain name
  -o OUTPUT, --output OUTPUT
                        path to ouput location
                        
  -dnsr, --dnsresolving
                        resolve all variation of domain name to see if it's up or not
  -l LIMIT, --limit LIMIT
                        limit of variations for a domain name
                        
  -a, --all             Use all algo
  -co, --characteromission
                        Leave out a letter of the domain name
  -repe, --repetition   Character Repeat
  -tra, --transposition
                        Swappe the order of adjacent letters in the domain name
  -repl, --replacement  Adjacent character replacement to the immediate left and right on the keyboard
  -drepl, --doublereplacement
                        Double Character Replacement
  -ins, --insertion     Adjacent character insertion of letters to the immediate left and right on the keyboard of
                        each letter
  -add, --addition      Add a character in the domain name
  -md, --missingdot     Omission of a dot from the domain name
  -sd, --stripdash      Omission of a dash from the domain name
  -vs, --vowelswap      Swap vowels within the domain name
  -hyp, --hyphenation   Addition of a hypen '-' between the first and last character in a string
  -bs, --bitsquatting   The character is substituted with the set of valid characters that can be made after a single
                        bit flip
  -hg, --homoglyph      One or more characters that look similar to another character but are different are called
                        homogylphs
  -cm, --commonmisspelling
                        Change a word by is misspellings
  -hp, --homophones     Change word by an other who sound the same when spoken
  -wt, --wrongtld       Change the original top level domain to another
  -at, --addtld         Adding a tld before the original tld
  -sub, --subdomain     Insert a dot at varying positions to create subdomain
  -sp, --singularpluralize
                        Create by making a singular domain plural and vice versa
```



# Example of use

1. Creation of variations for `ail-project.org` and `circl.lu` domain name, using all algorithm

```bash
dacru@dacru:~/git/ail-typo-squatting/bin$ python3 typo.py -dn ail-project.org circl.lu -a -o .
```



2. Creation of variations for a file who contains domain name, using character omission - subdomain - hyphenation

````bash
dacru@dacru:~/git/ail-typo-squatting/bin$ python3 typo.py -fdn domain.txt -co -sub -hyp -o .
````



3. Creation of variations for `ail-project.org` and `circl.lu` domain name, using all algorithm and using dns resolution

````bash
dacru@dacru:~/git/ail-typo-squatting/bin$ python3 typo.py -dn ail-project.org circl.lu -a -dnsr -o .
````





# Use as library

1. To run all algorithm

~~~~python
from typo import runAll
import math

resultList = list()
domainList = ["google.com"]
for domain in domainList:
    resultList = runAll(domain=domain, limit=math.inf, verbose=False)
    print(resultList)
    resultList = list()
~~~~



2. To run specific algorithm

````python
from typo import characterOmission, subdomain, hyphenation
import math

resultList = list()
domainList = ["google.com"]
limit = math.inf
for domain in domainList:
    resultList = characterOmission(domain=domain, resultList=resultList, verbose=False, limit=limit)
    
    resultList = subdomain(domain=domain, resultList=resultList, verbose=False, limit=limit)
    
    resultList = hyphenation(domain=domain, resultList=resultList, verbose=False, limit=limit)
    
    print(resultList)
    
    resultList = list()
````



# Output

The variations will be write into a text file, where each line is a variation.

````
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
````



## Dns output

In case dns resolve is selected, an additional file will be created in JSON format

each keys are variations and may have a field "ip" if the domain name have been resolved. The filed "NotExist" will be there each time with a Boolean value to determine if the domain is existing or not.

````json
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
````



# List of algorithm use



| Algo                           | Description                                                  |
| :----------------------------- | :----------------------------------------------------------- |
| Character omission             | These typos are created by leaving out a letter of the domain name, one letter at a time. |
| Character Repeat               | These typos are created by repeating a letter of the domain name. |
| Adjacent Character Swap        | These typos are created by swapping the order of adjacent letters in the domain name. |
| Adjacent Character Replacement | These typos are created by replacing each letter of the domain name with letters to the immediate left and right on the keyboard. (QWERTY, AZERTY, QWERTZ, DVORAK) |
| Add character                  | These typos are created by add a characters in the domain name |
| Double Character Replacement   | These typos are created by replacing identical, consecutive letters of the domain name with letters to the immediate left and right on the keyboard. |
| Adjacent Character Insertion   | These typos are created by inserting letters to the immediate left and right on the keyboard of each letter. |
| Missing Dot                    | These typos are created by omitting a dot from the domain name. |
| Strip Dashes                   | These typos are created by omitting a dash from the domain name. |
| Singular or Pluralise          | These typos are created by making a singular domain plural and vice versa. |
| Common Misspellings            | These typos are created by changing a word by is misspelling. Over 8000 common misspellings from Wikipedia. For example, www.youtube.com becomes www.youtub.com and www.abseil.com becomes www.absail.com |
| Vowel Swapping                 | These typos are created by swapping vowels within the domain name except for the first letter. For example, www.google.com becomes www.gaagle.com. |
| Bit Flipping                   | These typos are created by substituting a character with the set of valid characters that can be made after a single bit flip. For example, facebook.com becomes bacebook.com, dacebook.com, faaebook.com,fabebook.com,facabook.com, etc. |
| Homophones                     | These typos are created by changing word by an other who sound the same when spoken. Over 450 sets of words that sound the same when spoken. For example, www.base.com becomes www.bass.com. |
| Homoglyphs                     | These typos are created by replacing characters to another character that look similar but are different.  An example is that the lower case l looks similar to the numeral one, e.g. l vs 1. For example, google.com becomes goog1e.com. |
| Hyphenation                    | These typos are created by adding a hypen `-` between the first and last character in a string |
| Wrong Top Level Domain         | These typos are created by changing the original top level domain to another. For example, www.trademe.co.nz becomes www.trademe.co.mz and www.google.com becomes www.google.org Uses the 19 most common top level domains. |
| Add Top Level Domain           | These typos are created by adding a tld before the right tld. Example: google.com becomes google.com.it |
| Subdomain                      | These typos are created by placing a dot in the domain name in order to create subdomain. Example: google.com becomes goo.gle.com |

