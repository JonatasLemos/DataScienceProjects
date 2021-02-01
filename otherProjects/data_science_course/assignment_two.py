import pandas as pd
import numpy as np
import scipy.stats as stats
import numpy as np
# PART 1
pd.set_option('display.max_columns', None)
df=pd.read_csv("NISPUF17.csv")
list_of_EDUC1 = df['EDUC1'].unique()
list_of_EDUC1.sort()
print(list_of_EDUC1)
list_of_levels = ['less than high school','high school','more than high school but not college','college']
dict_of_proportions = {list_of_levels[i-1]: df[df['EDUC1'] == i]['EDUC1'].count()/df['EDUC1'].count()
     for i in list_of_EDUC1}
print(dict_of_proportions,"OK")
# PART 2
# CBF_01 P_NUMFLU
# Yes 1 # No 2 # Don’t know 99 # Missing 77
print(df['CBF_01'].unique())
print(df['P_NUMFLU'].unique())
new_df = df.groupby("CBF_01").agg({"P_NUMFLU":(np.nanmean)})
values_list = []
# CBF_01 as index, P_NUMFLU as column
for i in new_df.index:
    if i == 1:
        # Column and index of row
        values_list.append(new_df["P_NUMFLU"][i])
    if i == 2:
        values_list.append(new_df["P_NUMFLU"][i])
print(new_df)
print(tuple(values_list))
print(new_df.iloc[3])

# PART 3
print(len(df["HAD_CPOX"]))
new_df = df.dropna(subset=['P_NUMVRC'])
print(len(new_df["HAD_CPOX"]))
print("UNIQUE SEX", new_df['SEX'].unique())
print("UNIQUE CHICKEN", new_df['HAD_CPOX'].unique())
print("UNIQUE VACC", new_df['P_NUMVRC'].unique())
print(new_df[new_df['HAD_CPOX'] == 1]['P_NUMVRC'])
print("len??", len(new_df["HAD_CPOX"]))
print("YES CHICKEN", new_df[new_df['HAD_CPOX'] == 2]['HAD_CPOX'].count())
print("NO CHICKEN", new_df[new_df['HAD_CPOX'] == 1]['HAD_CPOX'].count())
print("FEMALE", new_df[new_df['SEX'] == 2]['HAD_CPOX'].count())
filtered_df = new_df[(new_df['HAD_CPOX'] == 1) & (new_df['P_NUMVRC'] == 2)]['P_NUMVRC'].count()
print(filtered_df,"NUM COUNT")
list_of_possibilites = ["male had CPOX were vac","female had CPOX were vac",
                        "female had CPOX were not vac", "male had CPOX were not vac"]
filtered_df = []
for i in range(1,3):
    for j in range(1,3):
        filtered_df.append(new_df[(new_df['HAD_CPOX'] == i) & (new_df['SEX'] == j) & (new_df['P_NUMVRC'] != 0)]
                           ['HAD_CPOX'].count())
dict_of_cases = {list_of_possibilites[i]:filtered_df[i] for i in range(len(filtered_df))}
print(dict_of_cases,"EM?")
# 'female had CPOX with VAC dose'/'female no CPOX with VAC dose'
list_of_values = list(dict_of_cases.values())
tuple_of_male = (list_of_values[0],list_of_values[2])
tuple_of_female = (list_of_values[1],list_of_values[3])
dict = {
    "male":tuple_of_male[0]/tuple_of_male[1],
    "female":tuple_of_female[0]/tuple_of_female[1]
}
print(dict)

# PART 4
df=pd.DataFrame({"had_chickenpox_column":np.random.randint(1,3,size=(100)),
                   "num_chickenpox_vaccine_column":np.random.randint(0,6,size=(100))})
corr,pval=stats.pearsonr(df["had_chickenpox_column"],df["num_chickenpox_vaccine_column"])
corr,pval=stats.pearsonr(new_df['HAD_CPOX'],new_df["P_NUMVRC"])
print(corr)
print(pval)
