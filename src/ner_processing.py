import spacy
nlp = spacy.load("en_core_web_sm")
import pandas as pd

data = pd.read_csv (r'all_triples_fake.csv')
df = pd.DataFrame(data, columns= ["0","1","2"])

ner_triples = []

for index, row in df.iterrows():
    new_triple = []

    new_sub = row['0']

    if 'Trump' in new_sub:
        if not 'Donald Trump' in new_sub:
            new_sub = 'Donald Trump'

    if 'Republican nominee Donald Trump' in new_sub:
        new_sub = 'Donald Trump'

    if 'nominee Donald Trump' in new_sub:
        new_sub = 'Donald Trump'

    if 'Obama' in new_sub:
        new_sub = 'Barack Obama'

    if 'Clinton' in new_sub:
        new_sub = 'Hillary Clinton'

    new_triple.append(new_sub)
    new_triple.append(row['1'])

    new_obj = row['2']

    if 'Trump' in new_obj:
        if not 'Donald Trump' in new_obj:
            new_obj = new_obj.replace('Trump', 'Donald Trump')

    if 'Republican nominee Donald Trump' in new_obj:
        new_obj = new_obj.replace('Republican nominee Donald Trump', 'Donald Trump')

    if 'nominee Donald Trump' in new_obj:
        new_obj = new_obj.replace('nominee Donald Trump', 'Donald Trump')

    if 'Obama' in new_obj:
        if not 'Barack Obama' in new_obj:
            new_obj = new_obj.replace('Obama', 'Barack Obama')

    if 'Clinton' in new_obj:
        if not 'Hillary Clinton' in new_obj:
            new_obj = new_obj.replace('Clinton', 'Hillary Clinton')

    new_triple.append(new_obj)

    print(new_triple)

    ner_triples.append(new_triple)

print(ner_triples)

df = pd.DataFrame(ner_triples)

df.to_csv("all_triples_fake_2.csv", index = False)

exit()

def ner_sub(text):
    doc = nlp(text)

    new_text = text

    for ent in doc.ents:
        if(ent.label_ == 'PERSON'):
            if(ent.text == 'Republican Donald Trump'):
                new_text = 'Donald Trump'
            elif(ent.text == 'Donald Trump ’s'):
                new_text = 'Donald Trump'
            elif(ent.text == 'Trump'):
                new_text = 'Donald Trump'
            elif(ent.text == 'Clinton'):
                new_text = 'Hillary Clinton'
            elif(ent.text == 'Hillary'):
                new_text = 'Hillary Clinton'
            else:
                new_text = ent.text

    return new_text

def ner_obj(text):
    doc = nlp(text)
    print('old: ' + text)
    new_text = text

    for ent in doc.ents:
        new_text = new_text[:ent.start_char] + ent.text + text[ent.end_char:]

    print('new: ' + new_text)
    return new_text

ner_triples = []

for index, row in df.iterrows():
    new_triple = []

    new_sub = ner_sub(row['0'])
    new_obj = row['2']

    new_triple.append(new_sub)
    new_triple.append(row['1'])
    new_triple.append(new_obj)

    print(new_triple)

    ner_triples.append(new_triple)

df = pd.DataFrame(ner_triples)

df.to_csv("ner_all_fake.csv", index = False)

exit()

def remove_stops(word):
    if word.lower() in set(set(stopwords.words('english'))):
        return ''
    else:
        return word

def extract_entities(text):
    res = []
    for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(text))):
        if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
            res.append((' '.join(c[0] for c in chunk.leaves())))
    if len(res) == 0:
        return text
    else:
        return res[0]

lemmatizer = WordNetLemmatizer()
df_triples["l1"] = (
    df_triples["e1"]
        .apply(lambda x: extract_entities(x))
        .apply(lemmatizer.lemmatize)
        .apply(lambda x: x.lower().strip())
        .apply(remove_stops)
        .apply(lambda x: re.sub("[^\s'_A-Za-z]", "", x))
        .apply(lambda x: x.lstrip().rstrip())
)
df_triples["l2"] = (
    df_triples["e2"]
        .apply(lambda x: extract_entities(x))
        .apply(lemmatizer.lemmatize)
        .apply(lambda x: x.lower().strip())
        .apply(remove_stops)
        .apply(lambda x: re.sub("[^\s'_A-Za-z]", "", x))
        .apply(lambda x: x.lstrip().rstrip())
)
df_triples["rel"] = (
    df_triples["r"]
        .apply(lemmatizer.lemmatize)
        .apply(lambda x: x.lower().strip())
        .apply(remove_stops)
        .apply(lambda x: re.sub("[^\s'_A-Za-z]", "", x))
        .apply(lambda x: x.lstrip().rstrip())
)

doc = nlp("U.S. President elect Donald Trump")
for ent in doc.ents:
    if(ent.label_ == 'PERSON'):
        print(ent.text)
    else:
        print(’Entity is not a person’)
