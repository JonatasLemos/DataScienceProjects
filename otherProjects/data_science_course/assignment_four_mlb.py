import pandas as pd
import numpy as np
import scipy.stats as stats
import re
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
# QUESTION 1
mlb_df=pd.read_csv("mlb.csv")
cities=pd.read_html("wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
print(mlb_df.loc[0:15, ["team", "W", "L", "W-L%"]])
# print(cities.loc[0:, ["Metropolitan area", "MLB"]])
# Getting rid of -
pat = "(.*\w.*)"
cities["MLB"]=cities["MLB"].str.extract(pat)
cities = cities.dropna()
print(cities.loc[0:, ["Metropolitan area", "MLB"]])
#  Getting rid of [note \d]
print(len(cities))
pattern="([A-Z].*(?=\[note)|[A-Z].*|^\d.*)"
cities["MLB"]=cities["MLB"].str.extract(pattern)
cities = cities.dropna()
print(cities.loc[0:, ["Metropolitan area", "MLB"]])
print(len(cities))
# Concatenating city+team
cities["MLB_CITY_TEAM"]=cities["Metropolitan area"]+" "+cities["MLB"]
print(cities.loc[0:,["Metropolitan area","MLB","MLB_CITY_TEAM"]])
mlb_df = mlb_df[mlb_df["year"] == 2018]
pattern = "((.*(?=(?<=\w)[A-Z].*))|[A-Z].*)"
cities["MLB_CITY_TEAM"]=cities["MLB_CITY_TEAM"].str.extract(pattern)
# cities["NHL_CITY_TEAM"]=cities["NHL_CITY_TEAM"].str.extract(pattern)
print(cities.loc[0:,["Metropolitan area","MLB","MLB_CITY_TEAM"]])
list_of_matches = []
for i in cities["MLB_CITY_TEAM"]:
    for j in mlb_df["team"]:
        if i.split(" ")[-1] == j.split(" ")[-1]:
            # list_of_matches.append(i)
            list_of_matches.append(j)
        # elif i.split(" ")[0] == j.split(" ")[0]:
        #     print(i,j)
list_of_matches.remove("Chicago White Sox")
print(list_of_matches)
print(len(list_of_matches))
cities["team"] = list_of_matches
# # CALCULATING MEAN
mlb_df["W-L%"]=mlb_df["W-L%"].astype(float)
new_york_mean = ((mlb_df[mlb_df["team"] == "New York Yankees"]["W-L%"].to_numpy()[0] + \
                  mlb_df[mlb_df["team"] == "New York Mets"]["W-L%"].to_numpy()[0]) / 2)
la_mean = ((mlb_df[mlb_df["team"] == "Los Angeles Dodgers"]["W-L%"].to_numpy()[0] + \
            mlb_df[mlb_df["team"] == "Los Angeles Angels"]["W-L%"].to_numpy()[0]) / 2)
sf_mean = ((mlb_df[mlb_df["team"] == "Oakland Athletics"]["W-L%"].to_numpy()[0] + \
            mlb_df[mlb_df["team"] == "San Francisco Giants"]["W-L%"].to_numpy()[0]) / 2)
chicago_mean = ((mlb_df[mlb_df["team"] == "Chicago Cubs"]["W-L%"].to_numpy()[0] + \
            mlb_df[mlb_df["team"] == "Chicago White Sox"]["W-L%"].to_numpy()[0]) / 2)
final_mlb = pd.merge(cities, mlb_df,
                     on="team",
                     how='left')
# # Setting new index
final_mlb = final_mlb.set_index("team")
print(final_mlb)
print(len(final_mlb))
# # # Setting new values to specif cells
final_mlb.at["New York Yankees", 'W-L%'] = new_york_mean
final_mlb.at["Los Angeles Dodgers", "W-L%"] = la_mean
final_mlb.at["San Francisco Giants", "W-L%"] = sf_mean
final_mlb.at["Chicago Cubs", "W-L%"] = chicago_mean
print(final_mlb)
population_by_region = final_mlb["Population (2016 est.)[8]"].astype(float)
win_loss_by_region = final_mlb["W-L%"].astype(float)
corr,pval=stats.pearsonr(population_by_region,win_loss_by_region)
print(corr)
print(pval)
