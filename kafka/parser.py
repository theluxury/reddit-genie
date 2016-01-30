
with open('stoplist.txt') as file:
    content = file.readlines()

finalResult = []
for line in content:
    if line != '\n':
        finalResult.append(line.split('\n')[0])

print finalResult
