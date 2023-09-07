from argparser import get_args
from scraping import *
import pandas as pd
import pickle

args = get_args()

print(args)
dict, all_classes = scrape_models(args.version, args.architecture, True)

all_classes.sort()
all_classes.insert(0, 'BaseExtractor')
all_classes.insert(0, 'BaseModel')
all_classes.insert(0, 'URL')
all_classes.insert(0, 'Name')

df = pd.DataFrame(columns=all_classes)


#dict.pop('Auto')


print('Checking {} Models'.format(len(dict)))
for key, value in dict.items():
    base_model, base_extractor = get_base_model(value[1])
    model_list = [value[0], value[1], base_model, base_extractor]
    for c in range(len(value)):
        value[c] = value[c].replace(key, '')
    for impl_class in all_classes[4::]:
            if impl_class in value:
                model_list.append(True)
            else:
                model_list.append(False)

    df.loc[len(df)] = model_list

info_df = df[['Name','URL', 'BaseModel', 'BaseExtractor']]

FLAX = df.columns.str.contains('Flax')
TF = df.columns.str.contains('TF')
mask = FLAX+TF
PyTorch = df[df.columns[~mask]]

PyTorch = pd.concat([info_df, PyTorch], axis =1)


PyTorch.to_csv('Huggingface_transformer_Pytorch.csv', index = False)