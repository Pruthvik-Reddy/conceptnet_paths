import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

columns = [
     'Antonym', 'DistinctFrom', 'EtymologicallyRelatedTo', 'LocatedNear', 'RelatedTo',
    'SimilarTo', 'Synonym', 'AtLocation', 'CapableOf', 'Causes', 'CausesDesire', 'CreatedBy',
    'DefinedAs', 'DerivedFrom', 'Desires', 'Entails', 'ExternalURL', 'FormOf', 'HasA',
    'HasContext', 'HasFirstSubevent', 'HasLastSubevent', 'HasPrerequisite', 'HasProperty',
    'InstanceOf', 'IsA', 'MadeOf', 'MannerOf', 'MotivatedByGoal', 'ObstructedBy', 'PartOf',
    'ReceivesAction', 'SenseOf', 'SymbolOf', 'UsedFor'
]
lowercase_list = [item.lower() for item in columns]
columns=lowercase_list


data=pd.read_excel("features.xlsx")
data2=pd.read_excel("features.xlsx")
for col in columns:
    data[col]=data[col].str.replace('[', '').str.replace(']', '').astype(int)
    data2[col]=data2[col].str.replace('[', '').str.replace(']', '').astype(int)

data["metaphor"]=data["metaphor"].str.replace('[', '').str.replace(']', '').astype(int)
data2["metaphor"]=data2["metaphor"].str.replace('[', '').str.replace(']', '').astype(int)
for index, row in data2[columns].iterrows():
    for col in columns:
        if row[col] > 0:
            data2.at[index, col] = 1
        else:
            data2.at[index, col] = 0
X = data[columns]
y = data['metaphor']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = LogisticRegression(max_iter=10000,solver="sag")
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

X = data2[columns]
y = data2['metaphor']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = LogisticRegression(max_iter=10000,solver="sag")
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

