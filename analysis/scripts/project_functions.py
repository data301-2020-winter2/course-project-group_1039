import pandas as pd
import os

def load_and_process_one(source=None):
    if source is None:
        raise TypeError("Expecting 1 argument but 0 argument is passed.")
    elif not os.path.exists(source):
        raise FileExistsError("Path does not exist.")
    elif os.path.isdir(source):
        raise FileNotFoundError("Expected file path but diretory path is given.")

    return process(pd.read_csv(source, delimiter=','))


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
    
    return process(pd.concat(parts, axis=0, ignore_index=True))
    


def process(dataframe=None):    
    if dataframe is None:
        raise ValueError("Expecting 1 argument but 0 is passed.")
    elif not isinstance(dataframe, pd.DataFrame):
        raise TypeError(f"An oject of type DataFrame is expected but {type(dataframe)} is passed.")
    
    return  (dataframe
                .drop(columns=['Id'])
                .loc[dataframe["Year"] >= 1910]
                .assign(Popular = (dataframe["Count"] > 1000))  
                .reset_index(drop=True)
            )

    

if __name__ == "__main__":
    df = load_and_process_one('data/raw/national/NationalNames.csv')
    print(df)