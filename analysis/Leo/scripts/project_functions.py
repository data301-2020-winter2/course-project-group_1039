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

def load_and_process_one_national(source=None):
    if source is None:
        raise TypeError("Expecting 1 argument but 0 argument is passed.")
    elif not os.path.exists(source):
        raise FileExistsError("Path does not exist.")
    elif os.path.isdir(source):
        raise FileNotFoundError("Expected file path but diretory path is given.")

    return process_national(pd.read_csv(source, delimiter=','))


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

def process_national(dataframe=None):    
    if dataframe is None:
        raise ValueError("Expecting 1 argument but 0 is passed.")
    elif not isinstance(dataframe, pd.DataFrame):
        raise TypeError(f"An oject of type DataFrame is expected but {type(dataframe)} is passed.")
    
    df =    ( dataframe
                .drop(columns=['Id'])
                .dropna()
                .drop_duplicates(keep='first')
                .loc[dataframe["Year"] >= 1880]
                .reset_index(drop=True)
            )
    # if "State" in dataframe.colummns.data:
    #     df= ( df.drop_duplicates(subset=["Name", "State"], keep="first")
    #             .pivot(index="",columns="",values="")
    #         )
    # else:
    #     df = df.pivot(index="Year", columns="Name", values="Count")
    return df


    # Method to get the top names based on decade and gender (move to project_functions)
def get_top_names_byDec_gender(dataframe,decade,gender,num_of_names):
    df_filtered = dataframe.loc[   (dataframe['Year'] >= decade) & 
                                    (dataframe['Year'] < decade+10) & 
                                    (dataframe['Gender'] == gender) 
                                ]
    df_cleaned = df_filtered.groupby(['Name','Gender'],as_index=False).agg(sum).sort_values(ascending=False, by=['Count']).head(num_of_names)
    return df_cleaned

def get_top_names_byDec(dataframe,decade,num_of_names):
    df_filtered = dataframe.loc[(dataframe['Year'] >= decade) & (dataframe['Year'] < decade+10)]
    df_cleaned = df_filtered.groupby(['Name','Gender'],as_index=False).agg(sum).sort_values(ascending=False, by=['Count']).head(num_of_names)
    return df_cleaned

def get_top_names_byYear(dataframe,year,num_of_names):
    df_filtered = dataframe.loc[(dataframe['Year'] == year)]
    df_cleaned = df_filtered.groupby(['Name','Gender'],as_index=False).agg(sum).sort_values(ascending=False, by=['Count']).head(num_of_names)
    return df_cleaned


# returns a dataframe with the top name for each decade filtered by gender
def get_top_name_foreachDec_gender(dataframe,gender):

    data = []
    for year in range(1880,2011,10):
        data.append([year,get_top_names_byDec_gender(dataframe,year,gender,1).iloc[0]['Name'],
                        get_top_names_byDec_gender(dataframe,year,gender,1).iloc[0]['Count']]
                    )


    df = pd.DataFrame(data, columns = ['Decade','Name', 'Count'])
    return df

# returns a dataframe with the top name for each decade
def get_top_name_foreachDec(dataframe):

    data = []
    for year in range(1880,2011,10):
        data.append([year,get_top_names_byDec(dataframe,year,1).iloc[0]['Name'],
                        get_top_names_byDec(dataframe,year,1).iloc[0]['Gender'],
                        get_top_names_byDec(dataframe,year,1).iloc[0]['Count']]
                    )


    df = pd.DataFrame(data, columns = ['Year','Name', 'Gender','Count'])
    return df

# returns the top name for each year for each gender
def get_top_name_foreachYear_male_female(dataframe):

    data = []
    for year in range(1879,2014):
        data.append([year,get_top_names_byDec_gender(dataframe,year,'F',1).iloc[0]['Name'],
                        get_top_names_byDec(dataframe,year,1).iloc[0]['Gender'],
                        get_top_names_byDec_gender(dataframe,year,'F',1).iloc[0]['Count']]
                    )


    df_m = pd.DataFrame(data, columns = ['Decade','Name','Gender','Count'])

    for year in range(1879,2014):
        data.append([year,get_top_names_byDec_gender(dataframe,year,'M',1).iloc[0]['Name'],
                        get_top_names_byDec(dataframe,year,1).iloc[0]['Gender'],
                        get_top_names_byDec_gender(dataframe,year,'M',1).iloc[0]['Count']]
                    )


    df_f = pd.DataFrame(data, columns = ['Year','Name','Gender', 'Count'])
    merged_df = df_f.merge(df_m,how='outer')

    return merged_df

# returns a dataframe with the top name for each year
def get_top_names_foreachYear(dataframe,num_of_names):

    data = []
    for year in range(1879,2015):
        data.append([year,get_top_names_byYear(dataframe,year,num_of_names).iloc[0]['Name'],
                        get_top_names_byYear(dataframe,year,num_of_names).iloc[0]['Count']]
                    )


    df = pd.DataFrame(data, columns = ['Year','Name', 'Count'])
    return df


if __name__ == "__main__":
    df = load_and_process_one('data/raw/national/NationalNames.csv')
    print(df)