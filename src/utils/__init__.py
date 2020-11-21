dataSet = {}
with open('src/utils/data/words_alpha.txt','rt') as file:
    data = file.read()
    dataSet = set(data.split('\n'))
    dataSet = set(filter(lambda x: len(x)>2,dataSet))

def generateBrandNameSuggestion(username):
    posibilities = []
    for i in range(1,len(username)):
        posibilities.append((username[:i],username[i:]))
    for pos in posibilities:
        if pos[0] in dataSet and pos[1] in dataSet:
            return ' '.join([i.capitalize() for i in pos])
    return username.capitalize()

def generateBrandNameSynonyms(brandName):
    synonyms = []
    synonyms.append(brandName.lower())
    synonyms.append(brandName.upper())
    synonyms.append(brandName.capitalize())
    synonyms.append(brandName.replace(' ',''))
    synonyms.append(brandName.replace(' ','_'))
    return synonyms


print(generateBrandNameSuggestion('facebook'))