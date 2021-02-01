from fuzzywuzzy import fuzz
# cities = input("Enter your city file")
# citiesToCorrect = input("Enter the cities to correct name")
f = open("spCities.txt", "r")
allCities = [line.strip() for line in f]

g = open("spLembradas.txt", "r")
myCities = [line.strip() for line in g]

indexArray = []
indexArrayWrong = []
newMyCities = []
for i in myCities:
    if i in allCities:
        newMyCities.append(i)
    if i not in allCities:
        for j in allCities:
            if fuzz.ratio(i.lower(), j.lower()) > 75:
                newMyCities.append(j)
print("Your corrected cities: ",newMyCities)
booleanArray = []
for i in allCities:
    if i in newMyCities:
        remebered = "1"
        booleanArray.append(remebered)
    if i not in newMyCities:
        remebered = "0"
        booleanArray.append(remebered)
print("All Cities:", allCities)
print("Your boolean array: ",booleanArray)
with open('booleanCities.txt', 'w') as f:
    for item in booleanArray:
        f.write("%s\n" % item)

