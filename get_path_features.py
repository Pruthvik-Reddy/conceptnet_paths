import pandas as pd
import csv
import os

df=pd.read_excel("all_unique_paths.xlsx")
column_list = df[0].tolist()
column_list.extend(["metaphor","verb1","verb2"])
import itertools

def generate_combinations(arr):
    combinations = list(itertools.product(*arr))
    output = ['-'.join(words) for words in combinations]
    return output

literal_path = "./conceptnet_paths/literal_pair_paths/"
metaphor_path = "./conceptnet_paths/metaphoric_pair_paths/"

new_df=pd.DataFrame(columns=column_list)


def get_paths(path,metaphor):
    if metaphor:
        folder_path="./conceptnet_paths/metaphoric_pair_paths/"
    else:
        folder_path="./conceptnet_paths/literal_pair_paths/"
    #print(type(path))
    for filename in os.listdir(folder_path):
        #print(type(filename))
        #print(type(path))
        
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            print(file_path)
            with open(file_path, 'r') as file:
                lines = file.readlines()
                relation_dict=dict()
                all_paths=set()
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
                        relation_dict[output]=1
                        if output not in all_paths:
                            all_paths.add(output)
                            
                    
                all_paths=list(set(all_paths))


                if metaphor:
                    relation_dict["metaphor"]=1
                else:
                    relation_dict[metaphor]=0
                file_name=filename.replace(".txt","")
                segments=file_name.split("_")
                word1 = segments[1].split("-")[0]
                word2 = segments[1].split("-")[1]
                relation_dict["verb1"]=word1
                relation_dict["verb2"]=word2
                new_row = {col: relation_dict.get(col, 0) for col in new_df.columns}
                #print(new_row)
                new_df.loc[len(new_df)]=new_row
                
get_paths("./conceptnet_paths/literal_pair_paths/",0)
get_paths("./conceptnet_paths/metaphoric_pair_paths/",1)
#print(path_dict)
print("The length of Data Frame is : ",len(new_df))
new_df.to_excel("Relation_Features.xlsx",index=False)
