import pandas as pd
from pythonProjects.fuzzyfunction import fuzzy
comparisonCountry = input("Enter your country")
countriesList = []
n = int(input("Enter number of countries : "))
for i in range(0, n):
    country = str(input())
    countriesList.append(country)
print(countriesList)
df_two = pd.read_csv("countriesArea.csv", sep=";", usecols=['Ranking', 'Country', 'Area'])
countries_dict = df_two.to_dict(orient='index')
newMyCountries = []
indexArrayWrong = []
for keys in countries_dict:
    for i in countriesList:
        if countries_dict[keys]["Country"] == i:
            newMyCountries.append(i)
        elif fuzzy(countries_dict[keys]["Country"], i, 89):
            newMyCountries.append(countries_dict[keys]["Country"])
area_array = []
print(countries_dict.values())
for country_id, country_info in countries_dict.items():
    for i in newMyCountries:
        if country_info["Country"] == i:
            area_array.append(country_info["Area"])
        elif country_info["Country"] == comparisonCountry:
            comaparisonCountryArea = country_info["Area"]
# To test with names are Ok
for i in countriesList:
    if i not in newMyCountries:
        print("not in NewMyCountries: ",i)
print("myCountries",len(countriesList),countriesList)
print("newMyCountries",len(newMyCountries),newMyCountries)
print("The countries areas are:",area_array)
print("The area of the base country is:",comaparisonCountryArea)
print("The total area is",sum(area_array), "square km")
print("The percentage of this country is",(sum(area_array)/comaparisonCountryArea)*100,"%")
