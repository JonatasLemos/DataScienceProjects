import re
with open("logdata.txt", "r",encoding="utf-8") as file:
    logdata = file.read()
ip = list(re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", logdata))
# user_name = list(re.findall("\s\w*\d*\s*(?=\[)", logdata))
user_name = list(re.findall("(?<=-\s).*(?=\s\[)", logdata))
# time_access = list(re.findall("\d\d/.*/.*:.*:.*:.*\s-\d\d\d\d", logdata))
time_access = list(re.findall("(?<=\[).*(?=])", logdata))
# request = list(re.findall("[A-Z]*\s/.\s[A-Z]*/\d\.\d", logdata))
# request = list(re.findall("\w*\s/.*\s[A-Z]*/\d\.\d", logdata))
request = list(re.findall("(?<=\").*(?=\")", logdata))
logs = []
for item in re.finditer("(?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
                        ")(\ \-\ )(?P<user_name>(?<=-\s).*(?=\s\[))"
                        "(\ \[)(?P<time_access>(?<=\[).*(?=]))(\]\ )"
                        "(\")(?P<request>(?<=\").*(?=\"))(\")",logdata):
    logs.append(item.groupdict())
print(logs)
print(len(logs))
pattern="""
(?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})        
(?P<user_name>(?<=-\s).*(?=\s\[))                        
(?P<time>(?<=\[).*(?=]))       
(?P<request>(?<=\").*(?=\"))"""
print(len(ip))
# print(ip)
print(len(time_access))
# print(time_access)
print(len(user_name))
# print(user_name)
print(len(request))
# print(request)
