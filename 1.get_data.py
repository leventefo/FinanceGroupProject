import pandas as pd
import requests
from datetime import datetime
import traceback
import sys
import time
import json


def read_FRED_api_key(file_name):

    with open(file_name, "r") as f:
        FRED_api_key = f.readline().strip()

    return FRED_api_key


def get_observations_and_metadata(series_id, api_key, observation_start, observation_end, frequency, aggregation_method):

    BASE_URL = "https://api.stlouisfed.org/fred/"
    FILE_TYPE = "json"
    
    series_observations_params = {

        "series_id" : series_id,
        "api_key" : api_key,
        "file_type" : FILE_TYPE,
        "observation_start" : observation_start,
        "observation_end" : observation_end,
        "frequency" : frequency,
        "aggregation_method" : aggregation_method

    }

    series_params = {
        
        "series_id" : series_id,
        "api_key" : api_key,
        "file_type" : FILE_TYPE,

    }

    series_observations_response = requests.get(url = BASE_URL + "series/observations", params = series_observations_params)
    series_response = requests.get(url = BASE_URL + "series", params = series_params)
    series_and_status_codes = {"observations" : series_observations_response.status_code, "metadata" : series_response.status_code}

    if series_observations_response.status_code == 200 and series_response.status_code == 200:

        series_observations, series = series_observations_response.json(), series_response.json()
        data = pd.DataFrame(series_observations["observations"])
        data["date"] = pd.to_datetime(data["date"])
        data = data.set_index("date")
        data.index.names = ['Date']
        data["value"] = pd.to_numeric(data["value"], errors = "coerce")
        data = data.drop(columns = ["realtime_start", "realtime_end"])
        data_units = series["seriess"][0]["units"]
        data = data.rename(columns = {"value":series_id + f" ({data_units})"})

        return check_for_NAN(data)

    else:

        for series_and_status_code in series_and_status_codes:
            if series_and_status_codes[series_and_status_code] != 200:
                print(f"Error in retrieving series {series_and_status_code}. Status code: f{series_and_status_codes[series_and_status_code]}")

        return {}

    
def check_for_NAN(df):

    try:
        return {"ID": df.columns[0], "dataframe": df.dropna()}

    finally:
        print(df)
        print("NAN(s): ", df.isnull().values.sum())


def get_series(series_ids, fred_api_key, start_date, end_date, frequency, aggregation_method):
    return [get_observations_and_metadata(series_id, fred_api_key, start_date, end_date, frequency, aggregation_method) for series_id in series_ids]


def save_series(df_list, file_name, series_ids):

    pd.concat(df_list, axis = 1).to_csv(f"data/{file_name}.csv")
    pd.concat(df_list, axis = 1).to_parquet(f"data/{file_name}.parquet")

    with open(f"series/{datetime.now().strftime("%Y-%m-%d--%H-%M-%S")}.txt", "w") as f:
        json.dump(series_ids, f)



def main():

    FRED_API_KEY = read_FRED_api_key("fred_api_key.txt")
    START_DATE = "1994-12-01"
    END_DATE = "2000-03-01"
    FREQUENCY = 'm'
    AGGREGATION_METHOD = 'eop'
    SERIES_IDs = ["NASDAQCOM", "PCE", "VIXCLS", "RMFSL", "H0MRPM", "CSCICP03USM665S"]

    myData = [list(element.values())[1] for element in get_series(SERIES_IDs, FRED_API_KEY, START_DATE, END_DATE, FREQUENCY, AGGREGATION_METHOD)]
    save_series(myData, "1.raw_data", SERIES_IDs)

main()