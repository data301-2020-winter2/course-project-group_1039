from typing import Iterable, Type
import pandas as pd
import os

def load_and_process_one(path=None):
    if path is None:
        raise TypeError("Expecting 1 argument but 0 argument is passed.")
    elif not os.path.exists(path):
        raise FileExistsError("Path does not exist.")
    elif not os.path.isfile(path):
        raise FileNotFoundError("No file found.")

    df = pd.read_csv(path, delimiter=',')
    return df


def load_and_process_many(source=None):
    if source is None:
        raise TypeError("Expecting 1 argument but 0 argument is passed.")
    elif not os.path.exists(source):
        raise FileExistsError("Path does not exist.")
    elif not os.path.isdir(source):
        raise TypeError("Path is not a directory.")
    
    parts = list()
    for file in os.listdir(source):
        if file.endswith(".csv"):
            parts.append(
                pd.read_csv(os.path.join(source,file), 
                delimiter=","))
    df = pd.concat(parts,axis=0,ignore_index=True)
    return df