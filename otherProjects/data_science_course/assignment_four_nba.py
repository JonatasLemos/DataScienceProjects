import pandas as pd
import numpy as np
import scipy.stats as stats
import re
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
# QUESTION 1
nba_df=pd.read_csv("nba.csv")
cities=pd.read_html("wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
# print(cities)
# print(nhl_df)
# Search pattern
patternDel = "(.*\sDivision)"
# filter using pattern
filter = nba_df['W'].str.contains(patternDel)
nba_df = nba_df[~filter]
print(nba_df.loc[0:, ["team", "W", "L", "W/L%"]])
print(cities.loc[0:, ["Metropolitan area", "NBA"]])
# Getting rid of -
pat = "(.*\w.*)"
cities["NBA"]=cities["NBA"].str.extract(pat)
cities = cities.dropna()
#  Getting rid of [note \d]
pattern="([A-Z].*(?=\[note)|[A-Z].*|^\d.*)"
cities["NBA"]=cities["NBA"].str.extract(pattern)
cities = cities.dropna()
print(cities.loc[0:, ["Metropolitan area", "NBA"]])
print(len(cities))
# Concatenating city+team
cities["NBA_CITY_TEAM"]=cities["Metropolitan area"]+" "+cities["NBA"]
print(cities.loc[0:,["Metropolitan area","NBA","NBA_CITY_TEAM"]])
# # print(nhl_df)
# # Getting rid of *
nba_df = nba_df[nba_df["year"] == 2018]
pattern="([A-Z].*(?=\*)|[A-Z].*(?=\s\W))"
nba_df["team"]=nba_df["team"].str.extract(pattern)
print(nba_df.loc[:, ["team"]])
print(len(nba_df))
# # Regex with or |
pattern = "((.*(?=(?<=\w)[A-Z].*))|[A-Z].*)"
cities["NBA_CITY_TEAM"]=cities["NBA_CITY_TEAM"].str.extract(pattern)
# cities["NHL_CITY_TEAM"]=cities["NHL_CITY_TEAM"].str.extract(pattern)
print(cities.loc[:,["NBA_CITY_TEAM"]])
list_of_matches = []
for i in cities["NBA_CITY_TEAM"]:
    for j in nba_df["team"]:
        if i.split(" ")[-1] == j.split(" ")[-1]:
            # list_of_matches.append(i)
            list_of_matches.append(j)
print(list_of_matches)
print(len(list_of_matches))
cities["team"] = list_of_matches
# print(cities)
# # CALCULATING MEAN
nba_df["W/L%"]=nba_df["W/L%"].astype(float)
new_york_mean = ((nba_df[nba_df["team"] == "New York Knicks"]["W/L%"].to_numpy()[0] + \
                 nba_df[nba_df["team"] == "Brooklyn Nets"]["W/L%"].to_numpy()[0])/2)
la_mean = ((nba_df[nba_df["team"] == "Los Angeles Clippers"]["W/L%"].to_numpy()[0] + \
                 nba_df[nba_df["team"] == "Los Angeles Lakers"]["W/L%"].to_numpy()[0])/2)
print(new_york_mean)
print(la_mean)
final_nba = pd.merge(cities, nba_df,
                     on="team",
                     how='left')
# Setting new index
final_nba = final_nba.set_index("team")
print(final_nba)
print(len(final_nba))
# # Setting new values to specif cells
final_nba.at["New York Knicks",'W/L%'] = new_york_mean
final_nba.at["Los Angeles Lakers","W/L%"] = la_mean
print(final_nba)
population_by_region = final_nba["Population (2016 est.)[8]"].astype(float)
win_loss_by_region = final_nba["W/L%"].astype(float)
corr,pval=stats.pearsonr(population_by_region,win_loss_by_region)
print(corr)
print(pval)
