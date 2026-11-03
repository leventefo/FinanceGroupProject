import pandas as pd
import statsmodels.api as sm

def regress(df):
    
    outcome_variable = df[df.columns[0]]
    predictor_variables = sm.add_constant(df[df.columns[1:]])

    return sm.OLS(outcome_variable, predictor_variables).fit()

def save_regression_summary(regression_results, file_name):

    with open(f"regressions/{file_name}.txt", "w") as f:
        f.write(regression_results.summary().as_text())

def save_regression(regression_results):
    
    regression_results.save("regressions/regression_results.pickle")


def run_regressions():

    for data_set in ["2.formatted_data", "3.normalized_data"]:
        df_myData = pd.read_parquet(f"data/{data_set}.parquet")
        regression_results = regress(df_myData)
        print(regression_results.summary())
        save_regression_summary(regression_results, f"{'n_' if data_set == "3.normalized_data" else ''}" + "&".join(df_myData.columns))
        if data_set == "3.normalized_data":
            save_regression(regression_results)

def main():

    run_regressions()

main()