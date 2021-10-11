import pandas as pd
import spacy
nlp = spacy.load('en_core_web_sm')

nlp.add_pipe(nlp.create_pipe('sentencizer’))

data = pd.read_csv (r'Filtered_dataset/ISOT-fake.csv')
#use Title, Article for true. title, text for fake
df = pd.DataFrame(data, columns= ["title", "text"])

def makeDefaultSummary(title, text):
    doc = nlp(text)
    sentences = [sent.string.strip() for sent in doc.sents]

    if len(sentences) > 2:
        summary = title + ' ' + sentences[0] + ' ' + sentences[1]
    else:
        summary = title + ' ' + sentences[0]

    print(summary)
    return summary

summaries = []

for index, row in df.iterrows():
    summaries.append((makeDefaultSummary(row['title'], row['text'])))

new_df = {'Text': summaries}

final_df = pd.DataFrame(new_df)

print('DataFrame:\n', final_df)

final_df.to_csv('fake_summarized_all.csv', index = False)
