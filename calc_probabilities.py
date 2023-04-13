import pandas as pd
import numpy as np

titanic_df = pd.read_csv('./small.csv')

def get_bayes_probs_from_dataset(df:pd.DataFrame)->dict:
    results = {}

    for column in df.columns:
        values = df[column]
        uniques = set(values)

        result = {un: round(len([i for i in values if i == un])/len(df),3) for un in uniques}
        results[column] = result
    
    return results

probs = get_bayes_probs_from_dataset(titanic_df)

fare_values = titanic_df['fare']
portembarked_values = titanic_df['portembarked']

assert len(fare_values) == len(portembarked_values)

result = len([i for i in range(len(fare_values)) if fare_values[i] == 3 and portembarked_values[i] == 3])

print(round(result/len(titanic_df),3))