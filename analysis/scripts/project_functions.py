import pandas as pd
import os

# CONSTANT FOR US REGION
NORTH_EAST = ['CT', 'DE', 'MA', 'MD', 'ME', 'NH', 'NJ', 'NY', 'PA', 'RI', 'VT']  
MID_WEST = ['IA', 'IL', 'IN', 'KS', 'MI', 'MN', 'MO', 'ND', 'NE', 'OH', 'SD', 'WI'] 
WEST = ['AK', 'AZ', 'CA', 'CO', 'HI', 'ID', 'MT', 'NM', 'NV', 'OR', 'UT', 'WA', 'WY'] 
SOUTH = ['AL', 'AR', 'DC', 'DE', 'FL', 'GA', 'KY', 'LA', 'MD', 'MS', 'NC', 'OK', 'SC', 'TN', 'TX', 'VA', 'WV']
POPULAR = 2000

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
    
    df =    ( dataframe
                .drop(columns=['Id'])
                .dropna()
                .drop_duplicates(keep='first')
                .loc[dataframe["Year"] >= 1910]
                .reset_index(drop=True)
            )
    # if "State" in dataframe.colummns.data:
    #     df= ( df.drop_duplicates(subset=["Name", "State"], keep="first")
    #             .pivot(index="",columns="",values="")
    #         )
    # else:
    #     df = df.pivot(index="Year", columns="Name", values="Count")
    return df

    

if __name__ == "__main__":
    df = load_and_process_one('data/raw/national/NationalNames.csv')
    print(df)