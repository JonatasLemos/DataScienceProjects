import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import statistics
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
energy=pd.read_excel("Energy Indicators.xls",sheet_name="EnergyNew")
# QUESTION 1
energy=energy.rename(columns={'Unnamed: 0':'Country',
                   'Energy Supply per capita':'Energy Supply per Capita',
                   'Renewable Electricity Production': '% Renewable'})
energy["Energy Supply"]=energy["Energy Supply"]*1000000
energy = energy.replace(to_replace="\d", value="", regex=True)
countries_to_rename = ['Republic of Korea','United States of America','United Kingdom of Great Britain and Northern Ireland','China, Hong Kong Special Administrative Region']
renamed_countries = ['South Korea','United States','United Kingdom','Hong Kong']
energy = energy.replace(countries_to_rename,renamed_countries)
energy = energy.replace(to_replace="\s\(.*\)", value="", regex=True)
# print(energy)
GDP=pd.read_csv("world_bank.csv")
countries_to_rename = ['Korea, Rep.','Iran, Islamic Rep.','Hong Kong SAR, China']
renamed_countries = ['South Korea','Iran','Hong Kong']
GDP = GDP.replace(countries_to_rename, renamed_countries)
GDP=GDP.rename(columns={'Country Name':'Country'})
# Drop using rows
GDP.drop(GDP.iloc[:, 1:50], inplace = True, axis = 1)
ScimEn = pd.read_excel("scimagojr_3.xlsx")
before_15 = ScimEn["Documents"].count()
ScimEn = ScimEn[0:15]
# print(ScimEn)
inter_result = pd.merge(energy,GDP,
                 on="Country",
                 how='left')
# print(inter_result.head())
final_result = pd.merge(ScimEn,inter_result,
                 on="Country",
                 how='left')
# QUESTION 2
final_result = final_result.set_index("Country")
# print(final_result)
shape = tuple(final_result.shape)
# print(shape)
lost_entries = before_15*shape[1] - shape[0]*shape[1]
# print(lost_entries)
# QUESTION 3
only_gdp = final_result.iloc[:, 10:20]
list_gdps = []
for i in only_gdp.index:
        list_gdps.append(np.nanmean(only_gdp.loc[i]))
series_gdps = pd.Series(list_gdps).sort_values(ascending=False)
# QUESTION 4
only_gdp["mean_GDP"] = list_gdps
only_gdp = only_gdp.sort_values(by="mean_GDP",ascending=False)
country_6th = only_gdp.iloc[5]
# QUESTION 5
average_ener_supply_per_capta = final_result["Energy Supply per Capita"].mean()
print(average_ener_supply_per_capta)
# QUESTION 6
final_result = final_result.reset_index()
max_renewable = final_result["% Renewable"].max()
# x = final_result[final_result['% Renewable'] == max_renewable][['Country','% Renewable']]
x = final_result[final_result['% Renewable'] == max_renewable]['Country']
y = final_result[final_result['% Renewable'] == max_renewable]['% Renewable']
list_max_country = x.values.tolist()
list_max_renewable = y.values.tolist()
tuple_max_renew = tuple(list_max_country+list_max_renewable)
print(tuple_max_renew)
# QUESTION 7
final_result["Ratio"]=final_result["Self-citations"]/final_result["Citations"]
# print(final_result)
max_ratio = final_result["Ratio"].max()
x = final_result[final_result['Ratio'] == max_ratio]['Country']
y = final_result[final_result['Ratio'] == max_ratio]['Ratio']
list_max_country = x.values.tolist()
list_max_ratio = y.values.tolist()
tuple_max_ratio = tuple(list_max_country+list_max_ratio)
print(tuple_max_ratio)
# QUESTION 8
final_result["PopEst"] = final_result["Energy Supply"]/final_result["Energy Supply per Capita"]
print(final_result[["Energy Supply","Energy Supply per Capita","PopEst"]])
# QUESTION 9
final_result['Citable docs per Capita'] = final_result['Citable documents'] / final_result['PopEst']
x=final_result['Citable docs per Capita']
y=final_result['Energy Supply per Capita']
corr,pval=stats.pearsonr(final_result['Citable docs per Capita'],final_result["Energy Supply per Capita"])
print(corr,"CORR")
print(pval,"P-VAL")
# QUESTION 10
median_renew = statistics.median(final_result['% Renewable'])
print(median_renew)
list_0_1 = []
for i in final_result['% Renewable']:
    if i >= median_renew:
        list_0_1.append(1)
    else:
        list_0_1.append(0)
# print(list_0_1)
final_result["HighThanMedian"] = list_0_1
# list_country = final_result["Country"]
series_0_1 = pd.Series(list_0_1)
final_result = final_result.sort_values(by="Rank")
series_0_1.index = final_result["Country"]
print(series_0_1)
# QUESTION 11
ContinentDict  = {'China':'Asia',
                  'United States':'North America',
                  'Japan':'Asia',
                  'United Kingdom':'Europe',
                  'Russian Federation':'Europe',
                  'Canada':'North America',
                  'Germany':'Europe',
                  'India':'Asia',
                  'France':'Europe',
                  'South Korea':'Asia',
                  'Italy':'Europe',
                  'Spain':'Europe',
                  'Iran':'Asia',
                  'Australia':'Australia',
                  'Brazil':'South America'}
list_continents = [continent for country,continent in ContinentDict.items()]
print(list_continents)
final_result["Continent"] = list_continents
print(final_result[["Country","Continent","PopEst"]])
print(type(final_result["PopEst"]))
final_result["PopEst"]=final_result["PopEst"].astype(float)
# QUESTION 13
final_format = final_result['PopEst'].apply(lambda x : "{:,}".format(x))
final_series = pd.Series(final_format)
final_series.index = final_result["Country"]
print(final_series,"LAMBDA")
# END QUESTION 13
final = final_result.groupby("Continent").agg({"PopEst":[np.mean,np.sum,np.std,np.count_nonzero]})
print(final)
# QUESTION 12
final = final_result.groupby("Continent").agg("% Renewable")
print(final_result)
print(final_result["% Renewable"].max())
print(final_result["% Renewable"].min())
pace = 13.4737354
# pace_min = pace + final_result["% Renewable"].min()
list_of_bins = []
for i in range(0,5):
        list_of_bins.append((final_result["% Renewable"].min()+(pace*i)))
print(list_of_bins)
# 2.279353, 19.12152225, 35.9636915, 52.80586075000001, 69.64803
final_result['% Renewable'] = pd.cut(x=final_result['% Renewable'],
                              bins=[2.279352, 15.753088400000001, 29.226823800000002, 42.7005592, 56.1742946, 69.64803])
final_result = final_result.groupby(["Continent","% Renewable"]).count()
final_result = final_result.dropna()
print(final_result)
print(final_result["Country"])
series_final = pd.Series(final_result["Country"])
print(series_final)
