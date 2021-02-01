import re
# PART A
simple_string = """Amy is 5 years old, and her sister Mary is 2 years old. 
    Ruth and Peter, their parents, have 3 kids."""
result = list(re.findall("[A-Z]\w*",simple_string))
print(result)
print(len(result))

# PART B
with open("grades.txt", "r",encoding="utf-8") as file:
    grades = file.read()
# grades = """A to B the man who are a B"""
# result = list(re.findall("\w.*(?=:\sB)",grades))
result = list(re.findall("\S.*(?=:\sB)",grades))
print(result)
print(len(result))


