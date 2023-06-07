import pandas as pd
import csv
import os


columns = ['verb1','verb2','Antonym', 'DistinctFrom', 'EtymologicallyRelatedTo', 'LocatedNear', 'RelatedTo',
           'SimilarTo', 'Synonym', 'AtLocation', 'CapableOf', 'Causes', 'CausesDesire', 'CreatedBy',
           'DefinedAs', 'DerivedFrom', 'Desires', 'Entails', 'ExternalURL', 'FormOf', 'HasA',
           'HasContext', 'HasFirstSubevent', 'HasLastSubevent', 'HasPrerequisite', 'HasProperty',
           'InstanceOf', 'IsA', 'MadeOf', 'MannerOf', 'MotivatedByGoal', 'ObstructedBy', 'PartOf',
           'ReceivesAction', 'SenseOf', 'SymbolOf', 'UsedFor',"metaphor"]


df = pd.DataFrame(columns=columns)
df.columns = df.columns.str.lower()

literal_path="./conceptnet_paths/literal_pair_paths/"
metaphor_path="./conceptnet_paths/metaphoric_pair_paths/"

for filename in os.listdir(literal_path):
    file_path = os.path.join(literal_path, filename)
    if os.path.isfile(file_path):
        
        print(file_path)
        with open(file_path, 'r') as file:
            lines = file.readlines()

            X = []
            relation_count=dict()
            for line in lines:
                line = line.strip()
                if line:
                    segments = string.split(']')
		    extracted_words = []
		    for segment in segments:
   	                if '[' in segment:
        		    words = segment.split('[')[-1]
        		    extracted_words.extend([word.strip().strip("'") for word in words.split(',')])
                for word in extracted_words:
                    if word in relation_count: 
                        relation_count[word]+=1
                    else :
                        relation_count[word]=1
            new_row = {col: [relation_count.get(col, 0)] for col in df.columns}
            df.append(new_row,ignore_index=True)
print(df)
for filename in os.listdir(metaphor_path):
    file_path = os.path.join(metaphor_path, filename)
    if os.path.isfile(file_path):
        
        print(file_path)
 

