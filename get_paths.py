import pandas as pd
import csv
import os

import itertools

def generate_combinations(arr):
    combinations = list(itertools.product(*arr))
    output = ['-'.join(words) for words in combinations]
    return output

columns = [
    'verb1', 'verb2',  "metaphor"
]
for i in range(1,501):
    path_name="Path"+str(i)
    columns.append(path_name)

df = pd.DataFrame(columns=columns)
df.columns = df.columns.str.lower()

literal_path = "./conceptnet_paths/literal_pair_paths/"
metaphor_path = "./conceptnet_paths/metaphoric_pair_paths/"

def get_paths(path,metaphor):
    if metaphor:
        path="./conceptnet_paths/metaphoric_pair_paths/"
    else:
        path="./conceptnet_paths/literal_pair_paths/"
    print(type(path))
    for filename in os.listdir(path):
        print(type(filename))
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            print(file_path)
            with open(file_path, 'r') as file:
                lines = file.readlines()
                path_dict=dict()
                all_paths=[]
                count=1
                for line in lines:
                    curr_path=[]
                    word_strings=[]
                    for i in range(len(line)):
                        if line[i]=="[":
                            for j in range(i+2,len(line)):
                                if line[j]=="]":
                                    word=line[i+1:j]
                                    break
                            word_strings.append(word)
                    path=[]
                    for word in word_strings:
                        words=word.split(",")
                        new_words=[]
                        for new in words:
                            new=new.strip("'").strip('"').strip(" ")
                            new_words.append(new.strip("'"))
                        path.append(new_words)
                    output1 = generate_combinations(path)
                    for output in output1:
                        all_paths.append(output)
                        path_name="path"+str(count)
                        count+=1
                        path_dict[path_name]=output1
                    
                all_paths=list(set(all_paths))


                if metaphor:
                    path_dict["metaphor"]=1
                else:
                    path_dict[metaphor]=0
                file_name=filename.replace(".txt","")
                segments=file_name.split("_")
                word1 = segments[1].split("-")[0]
                word2 = segments[1].split("-")[1]
                path_dict["verb1"]=word1
                path_dict["verb2"]=word2
                new_row = {col: path_dict.get(col, 0) for col in df.columns}
                df.loc[len(df)]=new_row
                
"""
for filename in os.listdir(metaphor_path):
    file_path = os.path.join(metaphor_path, filename)
    if os.path.isfile(file_path):
        print(file_path)
        with open(file_path, 'r') as file:
            lines = file.readlines()
            path_dict=dict()
            count=1
            for line in lines:
                curr_path=[]
                word_strings=[]
                for i in range(len(line)):
                    if line[i]=="[":
                        for j in range(i+2,len(line)):
                            if line[j]=="]":
                                word=line[i+1:j]
                                break
                        word_strings.append(word)
                path=[]
                for word in word_strings:
                    words=word.split(",")
                    new_words=[]
                    for new in words:
                        new=new.strip("'").strip('"').strip(" ")
                        new_words.append(new.strip("'"))
                    path.append(new_words)
                output1 = generate_combinations(path)
                path_name="path"+str(count)
                count+=1
                path_dict[path_name]=output1



            path_dict["metaphor"]=1
            file_name=filename.replace(".txt","")
            segments=file_name.split("_")
            word1 = segments[1].split("-")[0]
            word2 = segments[1].split("-")[1]
            path_dict["verb1"]=word1
            path_dict["verb2"]=word2
            new_row = {col: path_dict.get(col, 0) for col in df.columns}
            df.loc[len(df)]=new_row
"""


get_paths("./conceptnet_paths/literal_pair_paths/",0)
get_paths("./conceptnet_paths/metaphoric_pair_paths/",1)
#print(path_dict)
print("The length of Data Frame is : ",len(df))
df.to_excel("Path_features.xlsx",index=False)
    