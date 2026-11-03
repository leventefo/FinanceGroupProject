import pandas as pd



def mean_normalize(df):

    for col in df.columns[1:]:
        df[col] = (df[col]-df[col].mean()) / df[col].std()
        df = df.rename(columns = {col: df[col].name.split("(")[0] + "(Normalized)"})

    return df


def save_df(df, name):

    df.to_csv(f"data/{name}.csv")
    df.to_parquet(f"data/{name}.parquet")


def main():
    
    df_formatted_data = pd.read_parquet('data/2.formatted_data.parquet')
    df_normalized = mean_normalize(df_formatted_data.copy())
    save_df(df_normalized, "3.normalized_data")

main()