import itertools as itrt
import pandas as pd
from mpmath import gamma, log

# r = nombre de valeurs différentes que peut prendre la variable x_i
# q = nombre d'instanciations possibles que les parents de x_i peuvent prendre (se référer au graphe)
    # Par exemple, pour passengerclass, q = r(fare)
        # Pour citricacid, on aura q = r(volatileacidity) * r(fixedacidity)
# m_ijk = nombre de fois dans les données où x_i = k et que les parents de x_i prennent la j_ème instanciation possible

D:pd.DataFrame = pd.read_csv('./small.csv')

G:list = [
    # "age","portembarked","fare","numparentschildren","passengerclass","sex","numsiblings","survived"
    [0, 0, 0, 1, 0, 0, 1, 0], # age
    [0, 0, 1, 0, 0, 0, 0, 0], # portembarked
    [0, 0, 0, 0, 1, 0, 0, 0], # fare
    [0, 0, 0, 0, 0, 0, 0, 1], # numparentschildren
    [0, 0, 0, 0, 0, 0, 0, 1], # passengerclass
    [0, 0, 0, 0, 0, 0, 0, 1], # sex
    [0, 0, 0, 0, 0, 0, 0, 1], # numsiblings
    [0, 0, 0, 0, 0, 0, 0, 0], # survived
]

G_map:list = list(D.columns)


# X_1 = age, X_2 = portembarked, ...

# Nombre de valeurs que x_i prend
def r(x_i:str)->int:
    return len(set(D[x_i]))


def get_parents(node:str)->list:
    try:
        index_of_node = G_map.index(node)
        adj_column = [i[index_of_node] for i in G]
        return [G_map[key] for key,val in enumerate(adj_column) if val == 1]
    except ValueError:
        print(f"The value {node} does not exist in the dataframe")


def q(x_i:str)->int:
    result = 1

    for i in get_parents(x_i):
        result *= r(i)
    
    return result


def get_possible_instances(x_i:str)->tuple:
    return tuple(set(D[x_i]))


# Par exemple, si les parents prennent les valeurs 0 ou 1, et 0 ou 1 ou 2, on aura [(0,1), (0,1,2)]
# j est un parent spécifique (numéroté)
def pi(x_i:str, j:int=None)->list|tuple:

    parents_instances = [get_possible_instances(parent) for parent in get_parents(x_i)]

    pairs = list(itrt.product(*parents_instances))

    if j:
        assert j < len(pairs)
    
    return pairs[j] if j else pairs


def m(x_i:str, j:int, k: int)->int:

    parents = get_parents(x_i)
    column = D[x_i]
    result = 0
    j_e_ins = pi(x_i, j)

    # assert len(parents) == len(j_e_ins)
    # assert k in get_possible_instances(x_i)

    for index, i in enumerate(column):
        if i == k:
            for index_p, p in enumerate(parents):

                parent_col_val = D[p][index]
                j_eme_ins_parent = j_e_ins[index_p]

                if parent_col_val == j_eme_ins_parent:
                    result += 1

    return result

# print(m("survived", 5, 2))

def score():
    result = 0

    for i in G_map:
        
        for j in range(1, q(i)):

            print("q(i)",q(i))
            print("r(i)",r(i))
            print("m(i,j,0)",m(i,j,0))
            print("r(i)+m(i, j, 0)", r(i)+m(i, j, 0))
            print("gamma(r(i)+m(i, j, 0))", gamma(r(i)+m(i, j, 0)))
            print("gamma(r(i)) / gamma(r(i)+m(i, j, 0)",gamma(r(i)) / gamma(r(i)+m(i, j, 0)))
            print("log(gamma(r(i)) / gamma(r(i)+m(i, j, 0)))", log(
                gamma(r(i)) / gamma(r(i)+m(i, j, 0))
            ))            
            print("seconde somme", sum([
                log(gamma(1+ m(i, j, k))) for k in range(1, r(i))]))
            print("".join(['-' for i in range(50)]))

            break


            temp_res = log(
                gamma(r(i)) / gamma(r(i)+m(i, j, 0))
            ) + sum([
                log(gamma(1+ m(i, j, k))) for k in range(1, r(i))
            ])

            result += temp_res

    return result

print(score())