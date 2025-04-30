import os
import pathlib

def get_path_etc():
    loc = pathlib.Path(__file__).resolve().parents[2]
    return os.path.join(loc, "etc")