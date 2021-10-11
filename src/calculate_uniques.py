import pandas as pd

def getUniqueEnteties(triples):
    enteties = []

    for triple in triples:

        if triple[0] not in enteties:
            enteties.append(triple[0])

        if triple[2] not in enteties:
            enteties.append(triple[2])

    return enteties

def getUniqueRelations(triples):
    relations = []

    for triple in triples:

        if triple[1] not in relations:
            relations.append(triple[1])

    return relations


df = pd.read_csv(r'all_triples_fake_2.csv')

triples = []

for index, row in df.iterrows():
    #print(triple)

    triples.append([row[0], row[1], row[2]])

print(len(getUniqueEnteties(triples)))
print(len(getUniqueRelations(triples)))
