import pathlib, re

def get_path_etc():
    pathProg = pathlib.Path(__file__).parent.absolute()
    pathWork = ""
    for i in re.split(r"/|\\", str(pathProg))[:-1]:
        if(i == "ail_typo_squatting"):
            break
        pathWork += i + "/"
    pathEtc = pathWork + "etc"
    return pathEtc