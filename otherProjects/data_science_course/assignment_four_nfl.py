import pandas as pd
import numpy as np
import scipy.stats as stats
import re
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
# QUESTION 1
nfl_df=pd.read_csv("nfl.csv")
cities=pd.read_html("wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
# Search pattern
patternDel = "([A-Z]FC.*)"
# filter using pattern
filter = nfl_df['W'].str.contains(patternDel)
nfl_df = nfl_df[~filter]
nfl_df = nfl_df[nfl_df["year"] == 2018]
print(nfl_df.loc[0:, ["team", "W", "L", "W-L%"]])
# print(cities.loc[0:, ["Metropolitan area", "NFL"]])
# Getting rid of -
pat = "(.*\w.*)"
cities["NFL"]=cities["NFL"].str.extract(pat)
cities = cities.dropna()
# print(cities.loc[0:, ["Metropolitan area", "NFL"]])
# #  Getting rid of [note \d]
pattern="([A-Z].*(?=\[note)|[A-Z].*)"
cities["NFL"]=cities["NFL"].str.extract(pattern)
cities = cities.dropna()
print(cities.loc[0:, ["Metropolitan area", "NFL"]])
print(len(cities))
# Concatenating city+team
cities["NFL_CITY_TEAM"]=cities["Metropolitan area"]+" "+cities["NFL"]
print(cities.loc[0:,["Metropolitan area","NFL","NFL_CITY_TEAM"]])
# # # print(nhl_df)
# # # Getting rid of *
pattern="([A-Z].*(?=\+)|[A-Z].*(?=\*)|[A-Z].*)"
nfl_df["team"]=nfl_df["team"].str.extract(pattern)
print(nfl_df.loc[:, ["team"]])
print(len(nfl_df))
# # # Regex with or |
pattern = "((.*(?=(?<=\w)[A-Z].*))|[A-Z].*)"
cities["NFL_CITY_TEAM"]=cities["NFL_CITY_TEAM"].str.extract(pattern)
print(cities.loc[:,["NFL_CITY_TEAM"]])
print(len(cities))
# # # Playing with some lists
list_of_matches = []
for i in cities["NFL_CITY_TEAM"]:
    for j in nfl_df["team"]:
        if i.split(" ")[-1] == j.split(" ")[-1]:
            # list_of_matches.append(i)
            list_of_matches.append(j)
        elif i.split(" ")[0] == j.split(" ")[0]:
            print(i,j)
print(list_of_matches)
print(len(list_of_matches))
cities["team"] = list_of_matches
# # CALCULATING MEAN
nfl_df["W-L%"]=nfl_df["W-L%"].astype(float)
new_york_mean = ((nfl_df[nfl_df["team"] == "New York Giants"]["W-L%"].to_numpy()[0] + \
                  nfl_df[nfl_df["team"] == "New York Jets"]["W-L%"].to_numpy()[0]) / 2)
la_mean = ((nfl_df[nfl_df["team"] == "Los Angeles Chargers"]["W-L%"].to_numpy()[0] + \
            nfl_df[nfl_df["team"] == "Los Angeles Rams"]["W-L%"].to_numpy()[0]) / 2)
sf_mean = ((nfl_df[nfl_df["team"] == "San Francisco 49ers"]["W-L%"].to_numpy()[0] + \
            nfl_df[nfl_df["team"] == "Oakland Raiders"]["W-L%"].to_numpy()[0]) / 2)
print(new_york_mean)
print(la_mean)
print(sf_mean)
final_nfl = pd.merge(cities, nfl_df,
                     on="team",
                     how='left')
# Setting new index
final_nfl = final_nfl.set_index("team")
print(final_nfl)
print(len(final_nfl))
# # # Setting new values to specif cells
final_nfl.at["New York Giants",'W-L%'] = new_york_mean
final_nfl.at["Los Angeles Rams","W-L%"] = la_mean
final_nfl.at["Oakland Raiders","W-L%"] = sf_mean
print(final_nfl)
population_by_region = final_nfl["Population (2016 est.)[8]"].astype(float)
win_loss_by_region = final_nfl["W-L%"].astype(float)
corr,pval=stats.pearsonr(population_by_region,win_loss_by_region)
print(corr)
print(pval)
