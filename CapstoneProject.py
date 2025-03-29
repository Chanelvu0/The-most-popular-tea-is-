#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 19:16:22 2025

@author: chanelvu
"""

import pandas as pd
df = pd.read_csv("/Users/chanelvu/Desktop/Food review.csv")

df['Summary'] = df['Summary'].astype(str).str.lower()
df['Text'] = df['Text'].astype(str).str.lower()

# Filter only tea products
tea_keywords = [
    'black tea', 'blacktea', 'green tea', 'greentea',
    'hot tea', 'hottea', 'earl grey', 'earlgrey',
    'chamomile', 'jasmine', 'herbal', 'herbaltea',
    'oolong', 'white tea', 'whitetea', 'chai',
    'matcha', 'english breakfast', 'loose leaf', 'tea']

pattern = r'\b(?:' + '|'.join(tea_keywords) + r')\b'

# Filter only tea-related reviews
df = df[
    df['Summary'].str.contains(pattern, na=False, regex=True) |
    df['Text'].str.contains(pattern, na=False, regex=True)
]
# Map tea-related keywords to TeaCategory
tea_keywords = {
    "green tea|greentea": "Green Tea",
    "matcha": "Matcha",
    "black tea|blacktea": "Black Tea",
    "english breakfast": "English Breakfast",
    "earl grey|earlgrey": "Earl Grey",
    "jasmine": "Jasmine",
    "chamomile": "Chamomile",
    "oolong": "Oolong",
    "white tea|whitetea": "White Tea",
    "chai": "Chai"
}

df["TeaCategory"] = None

for pattern, label in tea_keywords.items():
    df.loc[df["Text"].str.contains(pattern, na=False), "TeaCategory"] = label

# Fallback: if review mentions tea but no match → "Other"
df.loc[df["TeaCategory"].isna() & df["Text"].str.contains(r"\btea\b", na=False), "TeaCategory"] = "Other"

def assign_tea_group(cat):
    if cat in ["Green Tea", "Matcha"]:
        return "Green Tea"
    elif cat in ["Black Tea", "English Breakfast", "Earl Grey"]:
        return "Black Tea"
    elif cat in ["Chamomile", "Jasmine"]:
        return "Herbal Tea"
    elif cat == "White Tea":
        return "White Tea"
    elif cat == "Chai":
        return "Spiced Tea"
    elif cat == "Oolong":
        return "Oolong"
    elif cat == "Other":
        return "Other"
    else:
        return "General Tea"

df["TeaGroup"] = df["TeaCategory"].apply(assign_tea_group)
df = df[df["TeaCategory"] != "Other"]
df = df[df["TeaGroup"] != "General Tea"]



# Helpfulness Score Column
df['HelpfulnessScore'] = df.apply(
    lambda x: f"{round((x['HelpfulnessNumerator'] / x['HelpfulnessDenominator']) * 100)}%"
    if x['HelpfulnessDenominator'] > 0 else None,
    axis=1
)
# Change format of score
def format_helpfulness(x):
    num = x['HelpfulnessNumerator']
    den = x['HelpfulnessDenominator']
    
    if den == 0 and num == 0:
        return "no vote"
    elif den > 0:
        return f"{round((num / den) * 100)}%"
    else:
        return None  
df['HelpfulnessScore'] = df.apply(format_helpfulness, axis=1)

#Move HelpfulnessScore
cols = list(df.columns)
score_index = cols.index('Score')
cols.insert(score_index + 1, cols.pop(cols.index('HelpfulnessScore')))
df = df[cols]

# Convert Unix time to date
df['Time'] = pd.to_datetime(df['Time'], unit='s')

# Rename column to ReviewDate
df.rename(columns={'Time': 'ReviewDate'}, inplace=True)

# Drop original helpfulness columns
df.drop(columns=['HelpfulnessNumerator', 'HelpfulnessDenominator'], inplace=True)

# Drop rows with missing Summary, Text, or Score
df.dropna(subset=['Summary', 'Text', 'Score'], inplace=True)
#Drop duplicates 
df.drop_duplicates(subset=['ProductId', 'UserId', 'Text'], inplace=True)
# Sort by review date from newest to oldest
df.sort_values(by='ReviewDate', ascending=False, inplace=True)

df.reset_index(drop=True, inplace=True)
df['Id'] = range(1, len(df) + 1)
print("Preview of tea-related reviews:")
print(df[['Summary', 'Text']].head())
print("Number of reviews left:", df.shape[0])

# Export to CSV
df.to_csv("/Users/chanelvu/Desktop/cleaned_tea_reviews.csv", index=False)
