# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 11:02:54 2024

@author: tomvi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
path = "D:\\dir\\Python\\NotoSansJP-VariableFont_wght.ttf"
fprop = fm.FontProperties(fname = path)

def hist(text):
    histogram = {}
    for char in text:
        if char in histogram:
            histogram[char] += 1
        else:
            histogram[char] = 1
    result = pd.DataFrame(list(histogram.items()), columns=['Character',\
            'Frequency'])
    return result.sort_values("Frequency", ascending= False)
    
def filter_string(input_string, chars_to_remove):
    return ''.join(char for char in input_string if char not in chars_to_remove)

def analyze_text(text, level=0.9):
    global histogram_data
    total = len(text)
    histo = hist(text)
    histogram_data = histo
    score = 0
    char_number = 0
    for count in histo["Frequency"]:
        score += count
        char_number += 1
        if score/total > level:
            return char_number
            break
        
        
def summary(text_data, level=0.9):
    total = len(text_data)
    unique = set(text_data)
    char_number = len(unique)
    per_man = int(100*char_number/np.sqrt(total))
    print(f'Out of {total} characters, {char_number} tokens.\
 Normalised value is {per_man}.')    
    print(f'Char number for {level*100} percent: \
 {analyze_text(text_data, level)}')
    print("")
        

hira = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんゝ"
hira_nigori = "がぎぐげござじずぜぞだづでどばびぶべぼぱぴぷぺぽ"
kata = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
kata_nigori = "ガギグゲゴザジズゼゾダヅデドバビブベボパピプペポ"
numbers = "一二三四五六七八九十百千万壱弐1234567890"
special = "()〇\n。、：，？〔〕︰；　・▲（）-ー△―「」『』！ .[]》《"
exclude = hira + hira_nigori + kata + kata_nigori + numbers + special

folder_path = "D:\\dir\\pydata\\idai\\"

texts = ["jingoki", \
         "warizansho", \
         "dokaisho", \
         "meibi", \
         "sanryoroku",\
         "hatsubi", \
         "kaisanki"
         ]

text_parts = ["jingoki_prepost", \
              "jingoki_rest", \
              "dokaisho_prepost", \
              "dokaisho_rest", \
              "hatsubi_prepost", \
              "hatsubi_rest"
              ]

texts_ref = ["kojiki", \
             "okunohosomichi", \
             "kyushu", \
             "rongo", \
             "rongo_alt"
            ]

level = 0.98


collection = ""
all_texts = ""
for text in texts:
    file_path = folder_path + text + ".txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        text_data = filter_string(file.read(), exclude)
        raw_data = file.read()
    print(text)
    summary(text_data, level)
    collection += text_data
    all_texts += text_data
    
    
for text in text_parts:
    file_path = folder_path + text + ".txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        text_data = filter_string(file.read(), exclude)
        raw_data = file.read()
    print(text)
    summary(text_data, level)
    all_texts += text_data
    
for text in texts_ref:
    file_path = folder_path + text + ".txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        text_data = filter_string(file.read(), exclude)
        raw_data = file.read()
    print(text)
    summary(text_data, level)
    all_texts += text_data    

print("all texts")
summary(all_texts, level)

print("collection")
summary(collection, level)

