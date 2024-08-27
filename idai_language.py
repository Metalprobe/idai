# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 11:02:54 2024

@author: tomvi
"""

import pandas as pd
import numpy as np
import scipy.stats as stats

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
        if score/total >= level:
            return char_number
            break
        
        
def summary(text_data, level=0.9):
    total = len(text_data)
    unique = set(text_data)
    char_number = len(unique)
    per_man = int(100*char_number/np.sqrt(total))
    per_percent = analyze_text(text_data, level)
    print(f'Out of {total} characters, {char_number} tokens.\
 Normalised value is {per_man}.')    
    print(f'Char number for {level*100} percent: \
 {per_percent}')
    print("")
    return [total, char_number, level*100, per_percent]
        

hira = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんゝ"
hira_nigori = "がぎぐげござじずぜぞだづでどばびぶべぼぱぴぷぺぽゞ"
kata = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
kata_nigori = "ガギグゲゴザジズゼゾダヅデドバビブベボパピプペポ"
numbers = "一二三四五六七八九十廿廾丗百千万壱弐1234567890"
special = "()〇\n。、：，？〔〕︰；　・▲（）-ー△―「」『』！ .[]》《◦㊀㊁㊂…●Ｏ】【—．々"
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
              "hatsubi_rest", \
              "senyou_prepost", \
              "senyou_rest", \
              "shinkan_rest"
              ]

texts_ref = ["kojiki", \
             "okunohosomichi", \
             "rongo_alt", \
             "moshi"
             ]

math_ref = ["kyushu", \
            "shinkan", \
            "jugairoku", \
            "senyou"
            ]

table_data = []
levels = [0.75, 0.90, 0.95, 0.98, 1]

for level in levels:
    collection = ""
    all_texts = ""
    math_all = ""
    for text in texts:
        file_path = folder_path + text + ".txt"
        with open(file_path, 'r', encoding='utf-8') as file:
            text_data = filter_string(file.read(), exclude)
            raw_data = file.read()
        print(text)
        result = summary(text_data, level)
        result.append(text)
        table_data.append(result)
        collection += text_data
        all_texts += text_data
        math_all += text_data
        
        
    for text in text_parts:
        file_path = folder_path + text + ".txt"
        with open(file_path, 'r', encoding='utf-8') as file:
            text_data = filter_string(file.read(), exclude)
            raw_data = file.read()
        print(text)
        result = summary(text_data, level)
        result.append(text)
        table_data.append(result)
        summary(text_data, level)

        
    for text in texts_ref:
        file_path = folder_path + text + ".txt"
        with open(file_path, 'r', encoding='utf-8') as file:
            text_data = filter_string(file.read(), exclude)
            raw_data = file.read()
        print(text)
        result = summary(text_data, level)
        result.append(text)
        table_data.append(result)
        summary(text_data, level)
        all_texts += text_data    
        
        
    for text in math_ref:
        file_path = folder_path + text + ".txt"
        with open(file_path, 'r', encoding='utf-8') as file:
            text_data = filter_string(file.read(), exclude)
            raw_data = file.read()
        print(text)
        result = summary(text_data, level)
        result.append(text)
        table_data.append(result)
        summary(text_data, level)
        all_texts += text_data  
        math_all += text_data          
    
    print("all texts")
    result = summary(all_texts, level)
    result.append("all texts")
    table_data.append(result)
    
    print("collection")
    result = summary(collection, level)
    result.append("collection")
    table_data.append(result)
    
    print("math_all")
    result = summary(math_all, level)
    result.append("math_all")
    table_data.append(result)
    
    columns = ["Number of characters",
               "Unique characters",
               "Level",
               "Number of characters for the level",
               "Text"
            ]
    
result_table = pd.DataFrame(table_data, columns = columns)
    
result_pivot = result_table.pivot(index="Text",\
                        columns="Level", \
                        values = "Number of characters for the level")
result_pivot = result_pivot.reset_index()
to_merge = result_table[0:27][["Text", "Number of characters"]]
result_pivot = pd.merge(result_pivot, to_merge, on ="Text")
    






### TESTING
# Example data
test_results = []

is_idai = result_table["Text"].isin(texts)
is_ref = result_table["Text"].isin(texts_ref)
is_m_ref = result_table["Text"].isin(math_ref)
is_math = result_table["Text"].isin(texts + math_ref)

levels = [75, 90, 95, 98, 100]
for level in levels:
    is_level = result_table["Level"] == level
    level_results = result_table[is_level]
    idai = level_results[is_idai]["Number of characters for the level"]
    # Number of characters in each idai
    
    ref = level_results[is_ref]["Number of characters for the level"]
    # Number of characters in each ref text
    
    m_ref = level_results[is_m_ref]["Number of characters for the level"]
    # Number of characters in each math ref
    
    math = level_results[is_math]["Number of characters for the level"]
    # Number of characters in echa math text

    # Perform Mann-Whitney U Test
    result_ixr = stats.mannwhitneyu(ref, idai , alternative='greater')   
    result_mxr = stats.mannwhitneyu(ref, math , alternative='greater')   
    result_mrxi = stats.mannwhitneyu(m_ref, idai , alternative='greater')   
    
    t_stat, p_value = stats.ttest_ind(ref, idai)
    t_stat_m, p_value_m = stats.ttest_ind(ref, math)
    t_stat_mf, p_value_mf = stats.ttest_ind(m_ref, idai)
    
    ##results_
    
    
    # Output the results
    
    test_array = [level, \
                  result_ixr.statistic, \
                  result_ixr.pvalue, \
                  result_mxr.statistic, \
                  result_mxr.pvalue, \
                  result_mrxi.statistic, \
                  result_mrxi.pvalue, \
                  t_stat, p_value, \
                  t_stat_m, p_value_m, \
                  t_stat_mf, p_value_mf]
    
    test_results.append(test_array)
   
    
    
level = "total"
is_level = result_table["Level"] == 100
level_results = result_table[is_level]
idai = level_results[is_idai]["Number of characters"]
# Number of characters in each idai

ref = level_results[is_ref]["Number of characters"]
# Number of characters in each ref text

m_ref = level_results[is_m_ref]["Number of characters"]
# Number of characters in each math ref

math = level_results[is_math]["Number of characters"]
# Number of characters in echa math text
# Perform Mann-Whitney U Test
result_ixr = stats.mannwhitneyu(ref, idai , alternative='greater')   
result_mxr = stats.mannwhitneyu(ref, math , alternative='greater')   
result_mrxi = stats.mannwhitneyu(m_ref, idai , alternative='greater')   

t_stat, p_value = stats.ttest_ind(ref, idai)
t_stat_m, p_value_m = stats.ttest_ind(ref, math)
t_stat_mf, p_value_mf = stats.ttest_ind(m_ref, idai)

test_array = [level, \
              result_ixr.statistic, \
              result_ixr.pvalue, \
              result_mxr.statistic, \
              result_mxr.pvalue, \
              result_mrxi.statistic, \
              result_mrxi.pvalue, \
              t_stat, p_value, \
              t_stat_m, p_value_m, \
              t_stat_mf, p_value_mf]

test_results.append(test_array)    
   
    
columns = ["level", "stat_i", "p_i", \
           "stat_m", "p_m", "stat_mr", "p_mr", "t", "p", "tm", "pm", \
           "tmr", "pmr"]

results_frame = pd.DataFrame(test_results, columns = columns)
    
    

    
    
    
    
