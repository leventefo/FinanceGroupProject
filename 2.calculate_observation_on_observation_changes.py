import pandas as pd


def calculate_mom_changes(df):
    
    for col in df.columns:

        if "percent" in col.lower():
            df[col] = df[col].diff()
            df = df.rename(columns = {col: df[col].name.split("(")[0] + "(MoM (pp))"})
            
        elif "index" in col.lower():
            df[col] = df[col].diff()
            df = df.rename(columns = {col: df[col].name.split("(")[0] + "(MoM (index-point))"})

        else:
            df[col] = df[col].pct_change() * 100
            df = df.rename(columns = {col: df[col].name.split("(")[0] + "(MoM (%))"})

    try:
        return df.dropna()

    finally:
        print(df.dropna())


def save_df(df, name):

    df.to_csv(f"data/{name}.csv")
    df.to_parquet(f"data/{name}.parquet")
            

def main():
    
    df_raw_data = pd.read_parquet("data/1.raw_data.parquet")
    df_mom_change = calculate_mom_changes(df_raw_data)
    save_df(df_mom_change, "2.formatted_data")

main()