import re

number = re.compile(r"[0-9]+")
suburb = ''
postcode = ''
address = ['PINE', 'HILL', '9010']
if len(address) >2:
    for i in address:
        if number.match(i) is None:
            suburb = suburb + ' ' + i
            suburb = suburb.strip()
        else:
            postcode = i

print(suburb)
print(postcode)