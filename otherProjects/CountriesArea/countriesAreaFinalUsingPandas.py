import pandas as pd
comparisonCountry = input("Enter your country")
countriesList = []
n = int(input("Enter number of countries : "))
for i in range(0, n):
    country = str(input())
    countriesList.append(country)
print(countriesList)
df_two = pd.read_csv("countriesArea.csv", sep=";", usecols=['Ranking', 'Country', 'Area'])
df_two = df_two.set_index('Ranking')
print(df_two)
countries_area = [df_two[df_two["Country"] == i]["Area"].to_numpy()[0] for i in countriesList]
chosen_country = [df_two[df_two["Country"] == comparisonCountry]["Area"].to_numpy()[0]]
ranking_countries = {i:df_two[df_two["Country"] == i].index.to_numpy()[0] for i in countriesList}
print("The area of the chosen countries",countriesList, "represent:",(float(sum(countries_area)/chosen_country*100)),
      "% of",comparisonCountry)
print("Chosen Country ranking:",comparisonCountry,":",df_two[df_two["Country"] == comparisonCountry].
      index.to_numpy()[0])
print("Countries to compare ranking:",ranking_countries)