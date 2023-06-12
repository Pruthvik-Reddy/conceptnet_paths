import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
from sklearn.inspection import permutation_importance
from sklearn.feature_extraction.text import CountVectorizer


column_df=pd.read_excel("all_unique_paths_2.xlsx")
column_list = column_df[0].tolist()

data=pd.read_csv("MOH-X_formatted_svo_cleaned.csv")
data['sentence'] = data['sentence'].str.lower()

count_vectorizer = CountVectorizer(analyzer='word', token_pattern=r'\w+')
sentences=count_vectorizer.fit_transform(data["sentence"])
feature_names=count_vectorizer.get_feature_names_out()

df_features = pd.DataFrame(sentences.toarray(),columns=feature_names)
df_original = pd.DataFrame({'metaphor': data["label"],"verb1":data["verb"],"verb2":data["arg1"]})

# Concatenate the original DataFrame and the feature vectors DataFrame
df_combined = pd.concat([df_original, df_features], axis=1)
df_combined.to_excel("feature_vectors.xlsx", index=False)





df_relations=pd.read_excel("Relation_Features_2.xlsx")
df_merged = pd.merge(df_relations, df_combined, on=['verb1', 'verb2', 'metaphor'])

train_columns=column_list+feature_names.tolist()
X = df_merged[train_columns]
y = df_merged['metaphor']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
print("Performance on combining Relation_features with bag of words")
print('Accuracy:', accuracy)
print('Precision:', precision)
print('Recall:', recall)
print('F1 Score:', f1)
