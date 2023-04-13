from numpy import average
import pandas as pd

df = pd.read_csv('./small.csv')

df = df.to_dict('records')

# print(df)


def stats(variable:str, value:int)->dict:
    return {
        'age': {
            1: calc_prob_var_val("age", 1, variable, value),
            2: calc_prob_var_val("age", 2, variable, value),
            3: calc_prob_var_val("age", 3, variable, value)
        },
        'portembarked': {
            1: calc_prob_var_val("portembarked", 1, variable, value),
            2: calc_prob_var_val("portembarked", 2, variable, value),
            3: calc_prob_var_val("portembarked", 3, variable, value)
        },
        'fare': {
            1: calc_prob_var_val("fare", 1, variable, value),
            2: calc_prob_var_val("fare", 2, variable, value),
            3: calc_prob_var_val("fare", 3, variable, value)
        },
        'numparentschildren': {
            1: calc_prob_var_val("numparentschildren", 1, variable, value),
            2: calc_prob_var_val("numparentschildren", 2, variable, value),
            3: calc_prob_var_val("numparentschildren", 3, variable, value)
        },
        'passengerclass': {
            1: calc_prob_var_val("passengerclass", 1, variable, value),
            2: calc_prob_var_val("passengerclass", 2, variable, value),
            3: calc_prob_var_val("passengerclass", 3, variable, value)
        },
        'sex': {
            1: calc_prob_var_val("sex", 1, variable, value),
            2: calc_prob_var_val("sex", 2, variable, value)
        },
        'numsiblings': {
            1: calc_prob_var_val("numsiblings", 1, variable, value),
            2: calc_prob_var_val("numsiblings", 2, variable, value),
            3: calc_prob_var_val("numsiblings", 3, variable, value)
        },
        'survived': {
            1: calc_prob_var_val("survived", 1, variable, value),
            2: calc_prob_var_val("survived", 2, variable, value)
        }
    }

def calc_prob_var_val(var_dict:str, val_dict:int, var_in:str, val_in:int)->int:
    global df
    return round(len([i for i in df if i[var_in] == val_in and i[var_dict] == val_dict])/len(df),2)

print(stats("portembarked",3))