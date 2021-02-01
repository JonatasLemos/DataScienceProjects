import pandas as pd
import numpy as np
import scipy.stats as stats
import re
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
# QUESTION 1
nhl_df=pd.read_csv("nhl.csv")
cities=pd.read_html("wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
# Search pattern
patternDel = "(.*\sDivision)"
# filter using pattern
filter = nhl_df['W'].str.contains(patternDel)
# Using a boolean series to print a df
# ~ to get rows that don't match instead of rows that match
nhl_df = nhl_df[~filter]
nhl_df["W"] = nhl_df["W"].astype(float)
nhl_df["L"] = nhl_df["L"].astype(float)
nhl_df["W/L"] = nhl_df["W"]/nhl_df["L"]
print("NHL_DF WITH W/L","\n")
print(nhl_df.loc[0:,["team","W","L","W/L"]])
# Getting rid of -
pat = "(.*\w.*)"
cities["NHL"]=cities["NHL"].str.extract(pat)
cities = cities.dropna()
#  Getting rid of [note \d]
pattern="([A-Z].*(?=\[note)|[A-Z].*)"
cities["NHL"]=cities["NHL"].str.extract(pattern)
cities = cities.dropna()
print(cities)
# Concatenating city+team
cities["NHL_CITY_TEAM"]=cities["Metropolitan area"]+" "+cities["NHL"]
print(cities.loc[0:,["Metropolitan area","NHL","NHL_CITY_TEAM"]])
# print(nhl_df)
# Getting rid of *
pattern="(.*\w)"
nhl_df["team"]=nhl_df["team"].str.extract(pattern)
nhl_df = nhl_df[nhl_df["year"]==2018]
print(nhl_df.loc[:,["team","W/L"]])
print(len(nhl_df))
# Regex with or |
pattern = "((.*(?=(?<=\w)[A-Z].*))|[A-Z].*)"
cities["NHL_CITY_TEAM"]=cities["NHL_CITY_TEAM"].str.extract(pattern)
cities["NHL_CITY_TEAM"]=cities["NHL_CITY_TEAM"].str.extract(pattern)
print(cities.loc[:,["NHL_CITY_TEAM"]])
print(len(cities))
# Playing with some lists
list_nhl_city = cities["NHL_CITY_TEAM"]
list_teams = nhl_df["team"]
list_of_matches = []
for i in cities["NHL_CITY_TEAM"]:
    for j in nhl_df["team"]:
        if i.split(" ")[-1] == j.split(" ")[-1]:
            # list_of_matches.append(i)
            list_of_matches.append(j)
        # elif i.split(" ")[0] == j.split(" ")[0]:
        #     print(i,j)
print("QUE COMO??")
a = "matozinhos legal"
b = a.split(" ")[-1]
print(b)
print(list_of_matches)
print(len(list_of_matches))
cities["CorrectName"] = list_of_matches
print(cities)
# CALCULATING MEAN
new_york_mean = (nhl_df[nhl_df["team"]=="New Jersey Devils"]["W/L"].to_numpy()[0] +\
    nhl_df[nhl_df["team"]=="New York Islanders"]["W/L"].to_numpy()[0] +\
    nhl_df[nhl_df["team"]=="New York Rangers"]["W/L"].to_numpy()[0]) /3
print(new_york_mean,"EM??")
la_mean = (nhl_df[nhl_df["team"]=="Anaheim Ducks"]["W/L"].to_numpy()[0] +\
    nhl_df[nhl_df["team"]=="Los Angeles Kings"]["W/L"].to_numpy()[0])/2
print(la_mean)
cities=cities.rename(columns={'CorrectName':'team'})
final_nhl = pd.merge(cities,nhl_df,
                 on="team",
                 how='left')
print(final_nhl)
print(len(final_nhl))
# Setting new index
final_nhl = final_nhl.set_index("NHL_CITY_TEAM")
# Setting new values to specif cells
final_nhl.at["New York City Rangers",'W/L'] = new_york_mean
final_nhl.at["Los Angeles Kings","W/L"] = la_mean
print(final_nhl)
print(final_nhl)
population_by_region = final_nhl["Population (2016 est.)[8]"]
win_loss_by_region = final_nhl["W/L"]
final_nhl["W/L"]=final_nhl["W/L"].astype(float)
final_nhl['Population (2016 est.)[8]']=final_nhl['Population (2016 est.)[8]'].astype(float)
corr,pval=stats.pearsonr(final_nhl['Population (2016 est.)[8]'],final_nhl["W/L"])
print(corr)
print(pval)
