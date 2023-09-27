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