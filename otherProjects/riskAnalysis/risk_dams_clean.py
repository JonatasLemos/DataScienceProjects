import numpy as np
from pythonProjects.risk_analysis_function.dataframes import *
from pythonProjects.risk_analysis_function.volumes import volume
from pythonProjects.risk_analysis_function.muncipalities_flow import df_filtered, df_filtered_special
from pythonProjects.risk_analysis_function.distances import straight_distance, municipal
from pythonProjects.risk_analysis_function.risk_pour import risk_pour_function, fid_function
pd.set_option('display.max_columns', None)
# FUNCTION to get the volume from each dam automatically
volumes = []
volume(df_dams_paraopeba,df_all_dams_volume,volumes)
df_dams_paraopeba['Volume'] = volumes
# FUNCTION STRAIGHT DISTANCE
dams_set = []
dams_min_dist = []
straight_distance(3,df_distances,dams_set,dams_min_dist)
df_distances['IsTheMinDistance'] = df_distances["DISTANCE"].isin(dams_min_dist)
# ADDING NEAR_FID AND distance_from_pour
dams_final_dist = []
dams_near_fid = []
for i in range(len(df_distances)):
    if df_distances.iloc[i][4] == True:
        dams_final_dist.append(df_distances.iloc[i][3])
        dams_near_fid.append(df_distances.iloc[i][2])
df_dams_paraopeba['distance_from_pour'] = dams_final_dist
df_dams_paraopeba['NEAR_FID'] = dams_near_fid
print("NEW DF_DAMS PARAOPEBA")
print(df_dams_paraopeba,"\n")
# MERGE DFs
result = pd.merge(df_dams_paraopeba,df_pour,
                 on="NEAR_FID",
                 how='left')
print("DF_DAMS_PARAOPEBA AND DF_POUR MERGE")
print(result)
# NORMALIZING VOLUMES WITH LIST COMPREHENSION
df_dams_paraopeba["Volume"].astype('float')
# volumes_normalized = [i/10000 for i in result["Volume"]]
result["Volume"] = result["Volume"]/10000
# DISTANCE POUR_DAM CALCULATIONS with zip (double loop)
flow_distance_pour_dam = [i - j for i, j in zip(result["flow_length_x"],result["flow_length_y"])]
# ADDING distances and volumes
result["flow_distance_pour_dam"] = flow_distance_pour_dam
# Find unique values in column
unique_fids = result['FID'].unique()
print("UNIQUE FIDS")
print(unique_fids,"\n")
# CALCULATING RISK from each dam
risk_from_dam = [(1/40000**(i))*j
                          for i,j in zip(result["flow_distance_pour_dam"],result["Volume"])]
result['risk_from_dam'] = risk_from_dam
print("RESULT WITH RISK FROM DAM")
print(result,"\n")
sum_risk = []
for i in unique_fids:
    for j in range(len(result)):
        if result.iloc[j][6] == i:
            sum_risk.append(i)
            sum_risk.append(result.iloc[j][3])
print("SUM RISK")
print(sum_risk,"\n")
res_dct = {sum_risk[i + 1]: sum_risk[i] for i in range(0, len(sum_risk), 2)}
list_tuples = list(res_dct.items())
print("DICTIONARY FROM SUM_RISK")
print(res_dct,"\n")
print("TUPLES LIST FROM DICTIONARY ")
print(list_tuples,"\n")
new_dict = {}
for value,key in list_tuples:
        total = new_dict.get(key, 0) + value
        new_dict[key] = total
list_of_risks = list(new_dict.items())
print("LIST OF RISKS")
print(list_of_risks,"\n")
# RENAME DF COLUMNS
df_new = result.rename(columns={'flow_length_x': 'dam_flow_length','flow_length_y': 'pour_flow_length'})
# PRINT RENAMED COLUMNS
risk_pour = []
risk_pour_function(df_filtered,list_of_risks,risk_pour)
print("DF Municipalities")
print(df_filtered,"\n")
df_filtered["FlowDifference"] = df_filtered["FlowDifference"].astype(float)
# risk_by_city = [(1/4**(i))*j for i,j in zip(df_filtered["FlowDifference"],df_filtered["risk_pour"])]
df_filtered["risk_by_city"] = (1/4**(df_filtered["FlowDifference"]))*df_filtered["risk_pour"]
cities_dict = dict(zip(df_filtered["risk_by_city"],df_filtered["Municipality"]))
list_of_cities = list(cities_dict.items())
new_dict_cities = {}
for value,key in list_of_cities:
        total = new_dict_cities.get(key, 0) + value
        new_dict_cities[key] = total
print("DF Municipalities with risk by city")
print(df_filtered,"\n")
print("Dictionary with columns risk_by_city and municipality")
print(cities_dict,"\n")
print("List with dictionary items")
print(list_of_cities,"\n")
print("Dictionary with repeated elements sum")
print(new_dict_cities,"\n")
# SPECIAL CITIES
print("Special cities DF")
print(df_filtered_special,"\n")
risk_pour_special = []
risk_pour_function(df_filtered_special,list_of_risks,risk_pour_special)
df_filtered_special["FlowDifference"] = df_filtered_special["FlowDifference"].astype(float)
risk_by_city_special = [(1/4**(i))*j for i,j in zip(df_filtered_special["FlowDifference"],df_filtered_special["risk_pour"])]
df_filtered_special["risk_by_city"] = risk_by_city_special
cities_dict_special = dict(zip(df_filtered_special["risk_by_city"],df_filtered_special["Municipality"]))
list_of_cities_special = list(cities_dict_special.items())
new_dict_cities_special = {}
for value,key in list_of_cities_special:
        total = new_dict_cities_special.get(key, 0) + value
        new_dict_cities_special[key] = total
print("Dictionary with repeated elements sum special")
print(new_dict_cities_special,"\n")
# SPECIAL CITIES END
# DICTIONARY WITH ALL THE CITIES TOGETHER NORMAL AND SPECIAL
new_dict_cities.update(new_dict_cities_special)
print("Complete dictionary")
print(new_dict_cities,"\n")
list_dict_new = list(new_dict_cities.items())
print("List dict items")
print(list_dict_new,"\n")
myDict = {}
myDict["Municipality"] = [i[0] for i in list_dict_new]
myDict["Risk"] = [i[1] for i in list_dict_new]
print("pre DF dictionary")
print(myDict,"\n")
df_final_risk = pd.DataFrame.from_dict(myDict)
print("Final Risk DF")
print(df_final_risk, "\n")
df_final_risk.to_excel(r'risk_dams_output.xlsx',index = False)


