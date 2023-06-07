import pandas as pd
import csv
import os

columns = [
    'verb1', 'verb2', 'Antonym', 'DistinctFrom', 'EtymologicallyRelatedTo', 'LocatedNear', 'RelatedTo',
    'SimilarTo', 'Synonym', 'AtLocation', 'CapableOf', 'Causes', 'CausesDesire', 'CreatedBy',
    'DefinedAs', 'DerivedFrom', 'Desires', 'Entails', 'ExternalURL', 'FormOf', 'HasA',
    'HasContext', 'HasFirstSubevent', 'HasLastSubevent', 'HasPrerequisite', 'HasProperty',
    'InstanceOf', 'IsA', 'MadeOf', 'MannerOf', 'MotivatedByGoal', 'ObstructedBy', 'PartOf',
    'ReceivesAction', 'SenseOf', 'SymbolOf', 'UsedFor', "metaphor"
]

df = pd.DataFrame(columns=columns)
df.columns = df.columns.str.lower()

literal_path = "./conceptnet_paths/literal_pair_paths/"
metaphor_path = "./conceptnet_paths/metaphoric_pair_paths/"

for filename in os.listdir(literal_path):
    file_path = os.path.join(literal_path, filename)
    if os.path.isfile(file_path):
        print(file_path)
        with open(file_path, 'r') as file:
            lines = file.readlines()

            X = []
            relation_count = dict()
            for line in lines:
                line = line.strip()
                if line:
                    segments = line.split(']')
                    extracted_words = []
                    for segment in segments:
                        if '[' in segment:
                            words = segment.split('[')[-1]
                            extracted_words.extend([word.strip().strip("'") for word in words.split(',')])
                    for word in extracted_words:
                        if word in relation_count:
                            relation_count[word] += 1
                        else:
                            relation_count[word] = 1
            relation_count["metaphor"]=0
            file_name=filename.replace(".txt","")
            segments=file_name.split("_")
            word1 = segments[1].split("-")[0]
            word2 = segments[1].split("-")[1]
            relation_count["verb1"]=word1
            relation_count["verb2"]=word2
            new_row = {col: [relation_count.get(col, 0)] for col in df.columns}
            df.loc[len(df)]=new_row
            

for filename in os.listdir(metaphor_path):
    file_path = os.path.join(metaphor_path, filename)
    if os.path.isfile(file_path):
        print(file_path)
        with open(file_path, 'r') as file:
            lines = file.readlines()

            X = []
            relation_count = dict()
            for line in lines:
                line = line.strip()
                if line:
                    segments = line.split(']')
                    extracted_words = []
                    for segment in segments:
                        if '[' in segment:
                            words = segment.split('[')[-1]
                            extracted_words.extend([word.strip().strip("'") for word in words.split(',')])
                    for word in extracted_words:
                        if word in relation_count:
                            relation_count[word] += 1
                        else:
                            relation_count[word] = 1
            relation_count["metaphor"]=1
            file_name=filename.replace(".txt","")
            segments=file_name.split("_")
            word1 = segments[1].split("-")[0]
            word2 = segments[1].split("-")[1]
            relation_count["verb1"]=word1
            relation_count["verb2"]=word2
            new_row = {col: [relation_count.get(col, 0)] for col in df.columns}
            df.loc[len(df)]=new_row

print("The length of Data Frame is : ",len(df))
df.to_excel("features.xlsx",index=False)
    