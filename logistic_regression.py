import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
from sklearn.inspection import permutation_importance



column_df=pd.read_excel("all_unique_paths_2.xlsx")
column_list = column_df[0].tolist()

data=pd.read_excel("Relation_Features_2.xlsx")

X = data[column_list]
y = data['metaphor']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print('Accuracy:', accuracy)
print('Precision:', precision)
print('Recall:', recall)
print('F1 Score:', f1)


print();print()
print("Printing the Importance of Features :")
print(model.coef_)

# Those values, however, will show that the second parameter
# is more influential
print(np.std(X, 0)*model.coef_)

print()
print("Model Inspection :")
model_fi = permutation_importance(model, X, y)
print(model_fi['importances_mean'])