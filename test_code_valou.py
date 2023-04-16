# calcule la probabilité de x sachant les conditions
# exemple : p("fare", 1, {'portembarked':1}) = P(Fare=1 | portembarked=1 )

import pandas as pd

# data = pd.read_csv('datasets/small.csv')

# def p(x:str, valeurX:int, conditions:dict)->float:
    
#     listeColumns=[]
#     listeValues=[]
#     for node in conditions:
#         l=data[node].to_list()
#         listeValues.append(conditions[node])
#         listeColumns.append(l)
    
#     listeDesIndex = []
#     for i in range(len(listeColumns)):
#         valeurCheck = listeValues[i]
#         lIndex=[]
#         for index, j in enumerate(listeColumns[0]):
#             if j == valeurCheck:
#                 lIndex.append(index)
#         listeDesIndex.append(lIndex)

    
#     listeIndexConditions = listeDesIndex[0]
#     for l in range(len(listeDesIndex)):
#         listeIndexConditions = list(set(listeIndexConditions) & set(listeDesIndex[l]))
    
#     # On a recuperer dans listeIndexConditions les indices où les valeurs sont égales à celles attendues

#     cpt = len(listeIndexConditions)

#     col=data[x].to_list()
#     indices = []
#     for index, j in enumerate(col):
#         if valeurX == j:
#             indices.append(index)
#     listeIndexFinal = list(set(listeIndexConditions) & set(indices))

#     res = len(listeIndexFinal)/cpt

#     # return round(res, 3)
#     return res


# print(p('survived', 1, {'passengerclass':1, 'numparentschildren':1, 'numsiblings':1, 'sex':1}))

def p(dataframe:pd.DataFrame, x:str, valeurX:int, conditions:dict)->float:
    df_copy:pd.DataFrame = dataframe

    for key, value in conditions.items():
        df_copy = df_copy.loc[df_copy[key] == value]

    result = len([i for i in df_copy[x] if i == valeurX])/df_copy.__len__()

    return result

# print(p('fare', 1, {'portembarked':1}))