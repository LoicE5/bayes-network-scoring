import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
import numpy as np
from time import time as now

df = pd.read_csv('datasets/small.csv').sample(
    frac = 1,
    random_state=1
).reset_index()

y = df['survived']
X = df.drop('survived', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=0)

X_train = X_train.to_numpy()
X_test = X_test.to_numpy()
y_train = y_train.to_numpy()
y_test = y_test.to_numpy()

def calculate_classifier_accuracy(
    X_train:np.ndarray,
    X_test:np.ndarray,
    y_train:np.ndarray,
    y_test:np.ndarray,
    classifier:GaussianNB,
    return_confusion_matrix:bool=False,
    show_execution_time:bool=False,
    show_accuracy_with_train_data:bool=False
):
    start_time = now()
    classifier.fit(X_train,y_train)

    predicted = classifier.predict(X_test)

    accuracy = [True if predicted[i] == y_test[i] else False for i in range(len(predicted))]
    accuracy_stats = {
        "right": len([i for i in accuracy if i]),
        "wrong": len([i for i in accuracy if not i])
    }
    accuracy_stats["percentage"] = round((accuracy_stats["right"]/len(accuracy))*100,2)

    if return_confusion_matrix:
        accuracy_stats["confusion_matrix"] = {
        "true_positive": len([1 for i in range(len(predicted)) if (predicted[i] == y_test[i] and predicted[i] == 1)]),
        "true_negative": len([1 for i in range(len(predicted)) if (predicted[i] == y_test[i] and predicted[i] == 0)]),
        "false_positive":len([1 for i in range(len(predicted)) if (predicted[i] != y_test[i] and predicted[i] == 1)]),
        "false_negative":len([1 for i in range(len(predicted)) if (predicted[i] != y_test[i] and predicted[i] == 0)])
    }

    if show_execution_time:
        print("Execution time :",round(now()-start_time,5),"seconds")

    if show_accuracy_with_train_data:
        print("Accuracy with training data :",calculate_classifier_accuracy(X_train,X_train,y_train,y_train,classifier,False,False,False)["percentage"],"%")
    
    return accuracy_stats

print(calculate_classifier_accuracy(X_train, X_test, y_train, y_test, GaussianNB()))