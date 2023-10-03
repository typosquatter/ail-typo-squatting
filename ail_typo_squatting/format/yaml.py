def formatYaml(resultList, domain, givevariations=False):
    """Output in yaml format"""
    yaml_file = {"title": domain}
    variations = list()

    for result in resultList:
        if givevariations:
            variations.append(result[0])
        else:
            variations.append(result)

    yaml_file["variations"] = variations

    return yaml_file
