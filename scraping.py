from bs4 import BeautifulSoup
import requests
from collections import OrderedDict
import pandas as pd
import numpy as np
import re
from datetime import datetime
def scrape_model_classes(name):

    url = 'https://huggingface.co/docs/transformers/v4.19.4/en/model_doc/{}'.format(name)

    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    final_name = soup.find('h1',{"class": 'relative group'}).find_all("span")[1].text.replace("\n\t", '')
    nav = soup.find_all('nav')[2]

    table = nav.find_all('a')

    implemented_classes = [final_name, url]

    for row in table:
        href = row['href'].split('.')
        if len(href) == 1:
            continue
        else:
            implemented_classes.append(href[-1])

    return implemented_classes, final_name


def get_name_in_classes(model_name, one_class):
    res_list = []
    res_list = re.findall('[A-Z][^A-Z]*', one_class)

    candidate = ""
    for i in range(len(res_list)):
        candidate = candidate + res_list[i]
        if model_name == candidate.lower():
            break

    print(candidate)

    return candidate


def scrape_models(version, architecture, class_dict):

    dict = {}
    all_classes= []
    url= "https://huggingface.co/docs/transformers/v4.27.2/en/model_doc/vit"

    url= "https://huggingface.co/docs/{}/{}/en/model_doc/van".format(architecture, version)

    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    flex = soup.find_all("a", {"class":"transform py-1 pr-2 pl-2 text-gray-500 transition-all first:mt-1 last:mb-4 hover:translate-x-px hover:text-black dark:hover:text-gray-300 ml-4" })

    print('Checking possible models... \n')
    i = 0
    for row in flex:

        if 'model_doc' in row['href']:
            model_name= row['href'].split('/')[6]


            model_classes, final_name = scrape_model_classes(model_name)



            if '_' in model_name:
                model_name = model_name.replace('_', '')
            elif '-' in model_name:
                model_name = model_name.replace('-', '')

            if len(model_classes)>2:
                one_class = model_classes[2]
                model_name = get_name_in_classes(model_name, one_class)
                dict[model_name] = model_classes

                for c in range(len(model_classes) - 2):
                    class_lower = model_classes[c + 2]
                    all_classes.append(class_lower.replace(model_name, ''))

                i+= 1


                print('{} model found'.format(i))

            else:
                continue



        else: continue


    return dict, list(set(all_classes))


def get_base_model(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    strings = soup.find_all("span", {"class":"hljs-string"})

    try:
        base_model= strings[0].contents[0]
    except:
        base_model = None
    try:
        base_extractor= strings[1].contents[0]
    except:
        base_extractor = None

    return base_model, base_extractor

