#open a .usda file
with open("template.usda") as usda_file:
    data = usda_file.read()

#split the file into lines

lines = data.splitlines()

for line in lines:
    print(line) #print the line
    print ("new line")
