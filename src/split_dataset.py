import json
import nltk
import re
import spacy
nlp = spacy.load("en_core_web_sm")
import pandas as pd

from nltk.corpus import stopwords
stopWords = set(stopwords.words('english'))

def fix_obj(text):
    #doc = nlp(text)

    new_text = text

    if 'Republican Donald Trump' in text:
        return text.replace('Republican Donald Trump','Donald Trump')
    if '#' in text:
        new_text = text.replace('#', '')
    if '" ' in text:
        new_text = text.replace('" ', '')
    if ' "' in text:
        new_text = text.replace(' "', '')
    if ' "' in text:
        new_text = text.replace(' "', '')
    if 'answer?' in text:
        new_text = text.replace('answer?', '')

    return new_text

with open('json_test_fake_triples.json') as json_file:
    data = json.loads(json_file.read())

    triple_list = []

    for i in data:
        for j in i['triples']:
            print(j)
            triple_list.append(j)

    train_triples = []

    # triples_id = []

    for i in triple_list:

        newSub = fix_obj(i[0]).lower()
        newRel = i[1].lower()
        newObj = fix_obj(i[2]).lower()

        if 'hillary hillary' in newSub:
            newSub = newSub.replace('hillary hillary', 'hillary')
        if 'donald donald' in newSub:
            newSub = newSub.replace('donald donald', 'donald')

        if 'hillary hillary' in newObj:
            newObj = newObj.replace('hillary hillary', 'hillary')
        if 'donald donald' in newObj:
            newObj = newObj.replace('donald donald', 'donald')

        if 'republican president elect donald trump' in newSub:
            newSub = newSub.replace('republican president elect donald trump', 'donald trump')
        elif 'president elect donald trump' in newSub:
            newSub = newSub.replace('president elect donald trump', 'donald trump')

        if 'republican president elect donald trump' in newObj:
            newObj = newObj.replace('republican president elect donald trump', 'donald trump')
        elif 'president elect donald trump' in newObj:
            newObj = newObj.replace('president elect donald trump', 'donald trump')

        if 'u.s. republican presidential candidate donald trump' in newSub:
            newSub = newSub.replace('u.s. republican presidential candidate donald trump', 'donald trump')
        elif 'republican presidential candidate donald trump' in newSub:
            newSub = newSub.replace('republican presidential candidate donald trump', 'donald trump')
        elif 'presidential candidate donald trump' in newSub:
            newSub = newSub.replace('presidential candidate donald trump', 'donald trump')
        elif 'candidate donald trump' in newSub:
            newSub = newSub.replace('candidate donald trump', 'donald trump')

        if 'u.s. republican presidential candidate donald trump' in newObj:
            newObj = newObj.replace('u.s. republican presidential candidate donald trump', 'donald trump')
        elif 'republican presidential candidate donald trump' in newObj:
            newObj = newObj.replace('republican presidential candidate donald trump', 'donald trump')
        elif 'presidential candidate donald trump' in newObj:
            newObj = newObj.replace('presidential candidate donald trump', 'donald trump')
        elif 'candidate donald trump' in newObj:
            newObj = newObj.replace('candidate donald trump', 'donald trump')

        if 'white house candidate hillary clinton' in newSub:
            newSub = newSub.replace('white house candidate hillary clinton', 'hillary clinton')
        elif 'u.s. republican presidential candidate hillary clinton' in newSub:
            newSub = newSub.replace('u.s. republican presidential candidate hillary clinton', 'hillary clinton')
        elif 'republican presidential candidate hillary clinton' in newSub:
            newSub = newSub.replace('republican presidential candidate hillary clinton', 'hillary clinton')
        elif 'presidential candidate hillary clinton' in newSub:
            newSub = newSub.replace('presidential candidate hillary clinton', 'hillary clinton')
        elif 'candidate hillary clinton' in newSub:
            newSub = newSub.replace('candidate hillary clinton', 'hillary clinton')

        if 'u.s. republican presidential candidate hillary clinton' in newObj:
            newObj = newObj.replace('u.s. republican presidential candidate hillary clinton', 'hillary clinton')
        elif 'republican presidential candidate hillary clinton' in newObj:
            newObj = newObj.replace('republican presidential candidate hillary clinton', 'hillary clinton')
        elif 'presidential candidate hillary clinton' in newObj:
            newObj = newObj.replace('presidential candidate hillary clinton', 'hillary clinton')
        elif 'candidate hillary clinton' in newObj:
            newObj = newObj.replace('candidate hillary clinton', 'hillary clinton')

        #doc = nlp(newSub)

        #new_text = newSub

        # for ent in doc.ents:
        #     #print(ent)
        #     if(ent.label_ == 'PERSON'):
        #         print(ent.text.lower())
        #         if(ent.text.lower() == 'republican Donald Trump'):
        #             new_text = 'donald trump'
        #         elif(ent.text.lower() == 'donald Trump ’s'):
        #             new_text = 'donald Trump'
        #         elif(ent.text.lower() == 'Trump'):
        #             new_text = 'donald Trump'
        #         elif(ent.text.lower() == 'clinton'):
        #             new_text = 'hillary Clinton'
        #         elif(ent.text.lower() == 'Hillary'):
        #             new_text = 'hillary clinton'
        #         else:
        #             new_text = ent.text

        if 'barack barack' in newSub:
            newSub = newSub.replace('barack barack', 'barack')

        if newSub == 'u.s. donald trump':
            newSub = 'donald trump'
        if newSub == 'trump':
            newSub = 'donald trump'
        if newSub == 'republican u.s. donald trump':
            newSub = 'donald trump'
        if newSub == "barack obama 's":
            newSub = 'barack obama'
        if newSub == "hillary clinton ’s":
            newSub = 'hillary clinton'
        if newSub == "u.s. president barack obama":
            newSub = 'barack obama'


        print(str(i))
        print(newSub)
        new_triple = []
        new_triple.append(newSub)
        new_triple.append(newRel)
        new_triple.append(newObj)

        train_triples.append(new_triple)

        # triple_with_id = {
        #     'id': i,
        #     'triple': new_triple,
        #     'label': 'true'
        # }

        # triples_id.append(triple_with_id)


    print(train_triples)

    df = pd.DataFrame(train_triples)

    df.to_csv("all_triples_fake.csv", index = False)

    # df = pd.DataFrame(triples_id)
    #
    # df.to_csv("id_triples_fake.csv", index = False)

    # train_size = len(triple_list) * 0.7
    # test_size = len(triple_list) * 0.15
    # combined = test_size + test_size
    #
    # training_set = triple_list[:train_size]
    # rest_set = triple_list[combined:]
    #
    # test_set = rest_set[:test_size]
    # val_set = rest_set[test_size:]
    #
    # print(len(training_set))
    # print(len(test_set))
    # print(len(val_set))


def fix_subs(text):
    if 'Trump' in text:
        if not 'Donald Trump' in text:
            text = 'Donald Trump'

    if 'Republican nominee Donald Trump' in text:
        text = 'Donald Trump'

    if 'nominee Donald Trump' in text:
        text = 'Donald Trump'

    if 'Obama' in text:
        text = 'Barack Obama'

    if 'Clinton' in text:
        text = 'Hillary Clinton'
    if 'TRUMP' in text:
        text = 'Donald Trump'
    if 'HILLARY' in text:
        text = 'Hillary Clinton'

def fix_obj(text):
    #doc = nlp(text)

    new_text = text

    if 'Republican Donald Trump' in text:
        return text.replace('Republican Donald Trump','Donald Trump')
    if '#' in text:
        new_text = text.replace('#', '')
    if '" ' in text:
        new_text = text.replace('" ', '')
    if ' "' in text:
        new_text = text.replace(' "', '')
    if ' "' in text:
        new_text = text.replace(' "', '')
    if 'answer?' in text:
        new_text = text.replace('answer?', '')
    elif 'Donald Trump ’s' in text:
        return text.replace('Donald Trump ’s', 'Donald Trump')
    elif 'Donald Trump’s' in text:
        return text.replace('Donald Trump’s','Donald Trump')
    elif 'Trump' in text:
        return text.replace('Trump','Donald Trump')
    elif 'Clinton' in text and not 'Bill' in text:
        return text.replace('Clinton','Hillary Clinton')
    elif 'Hillary' in text:
        return text.replace('Hillary','Hillary Clinton')
    elif 'TRUMP' in text:
        return text.replace('TRUMP', 'Donald Trump')
    elif 'Obama' in text:
        return text.replace('Obama', 'Barack Obama')
    elif 'PRESIDENT ELECT TRUMP' in text:
        return text.replace('PRESIDENT ELECT TRUMP', 'Donald Trump')



    return new_text

def extract_entities_spacy(text):
    proc = nlp(text)
    if len(proc.ents) == 0:
        return "unk"
    else:
        return " ".join([x.text for x in proc.ents])

def remove_stops(text):
    """Remove stopwords"""

    new_text = text

    for x in stopWords:
        if x in text:
            new_text = new_text.replace(x, '')
    return new_text

def process_entity(value):

    lemmatizer = nltk.WordNetLemmatizer()

    return re.sub("[^\s'_A-Za-z]", "",
                  remove_stops(fix_entities(extract_entities_spacy(value).lower().strip()))).lstrip().rstrip()
def process_relation(value):
    return re.sub("[^\s'_A-Za-z]", "", lemmatizer.lemmatize(value.lower().strip(), pos='v')).lstrip().rstrip()

def shorten_relations(relation, n):
    """Restrict relation length"""
    if len(nltk.tokenize.word_tokenize(relation)) > n:
        return ""
    else:
        return relation

df = pd.read_csv(r'all_triples_fake.csv')

#print(df)

enteties = []
relations = []

for index, row in df.iterrows():
    #print(triple)
    enteties.append(row['0'])
    enteties.append(row['2'])
    relations.append(row['1'])

print(relations)

df = pd.DataFrame(enteties)
df.to_csv("all_fake_enteties", index = False)

df = pd.DataFrame(relations)
df.to_csv("all_fake_relations", index = False)

exit()
test_triples =[]

for i in range(len(data)):
    triples = data[i]['triples']

    for triple in triples:
        newSub = fix_obj(triple[0]).lower()
        newRel = triple[1].lower()
        newObj = fix_obj(triple[2]).lower()

        if 'hillary hillary' in newSub:
            newSub = newSub.replace('hillary hillary', 'hillary')
        if 'donald donald' in newSub:
            newSub = newSub.replace('donald donald', 'donald')

        if 'hillary hillary' in newObj:
            newObj = newObj.replace('hillary hillary', 'hillary')
        if 'donald donald' in newObj:
            newObj = newObj.replace('donald donald', 'donald')

        new_triple = []
        new_triple.append(newSub)
        new_triple.append(newRel)
        new_triple.append(newObj)

        triple_with_id = {
            'id': i,
            'triple': new_triple,
            'label': 'false'
        }

        test_triples.append(triple_with_id)

print(test_triples)

df = pd.DataFrame(test_triples)
df.to_csv("id_triples_fake.csv", index = False)
