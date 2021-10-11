import nltk
from stanza.server import CoreNLPClient
import spacy
from stop_words import get_stop_words
import re
nlp = spacy.load('en_core_web_sm')
import neuralcoref
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
import pandas as pd
import matplotlib.pyplot as plt
import json

stop_words = list(get_stop_words('english'))		 #About 900 stopwords

caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
coref = neuralcoref.NeuralCoref(nlp.vocab)
neuralcoref.add_to_pipe(nlp)

data = pd.read_csv (r'Filtered_dataset/filtered_fake.csv')
df = pd.DataFrame(data, columns= ["title"])

articles = []

for index, row in df.iterrows():
	articles.append(row['title'])

articles = [x.strip() for x in articles]

#testing
#print(articles)

#articles.append("London has been a major settlement for two millennia, and was originally called Londinium, which was founded by the Romans")
# articles.append("Hillary Clinton killed in monster truck mishap.")
# articles.append('Julia Roberts told Celine Dion, "If you hate Trump you can go in your country."')
# articles.append('"Trump welcomes Jamaica as a U.S. territory"')
# articles.append('Jennifer Aniston said, "Me and all the Trump supporter celebrities decide to make a company named ‘celebrities for Trump’')
# articles.append("Trump wins the award Obama never could.")
# articles.append('Lady Gaga was arrested after a confrontation with First Lady Melania Trump.')
# articles.append("Kim Jong Un killed in (President Donald) Trump’s overnight black op attack on North Korea.")
# articles.append("Trump fires deputy attorney general Rod Rosenstein, raising questions over Mueller’s fate.")
# articles.append("3 liberal celebrities arrested for conspiracy to assassinate President Trump.")
# articles.append("Hillary Clinton filed for divorce In New York courts.")
# articles.append("FBI issues Warrant For Obama’s Arrest After Confirming Illegal Trump Tower Wiretap.")
# articles.append('Queen Elizabeth said, "Muslim refugees are dividing nationality, I fully agree with Donald Trump we should deport them to avoid bloody terrorist attacks."')
#

def printGraph(triples):
	G = nx.Graph()
	for triple in triples:
		G.add_node(triple[0])
		G.add_node(triple[1])
		G.add_node(triple[2])
		G.add_edge(triple[0], triple[1])
		G.add_edge(triple[1], triple[2])

	pos = nx.spring_layout(G)
	plt.figure()
	nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
			node_size=500, node_color='seagreen', alpha=0.9,
			labels={node: node for node in G.nodes()})
	plt.axis('off')
	plt.show()

def makeDefaultSummary(title, text):
	if len(text.split('. ')) >= 2:
		summary = title + '. ' + '. '.join(text.split('. ')[0:2]) + '.'
	else:
		summary = title + '. ' + text
	return summary

def split_into_sentences(text):
	text = " " + text + "  "
	text = text.replace("\n"," ")
	text = re.sub(prefixes,"\\1<prd>",text)
	text = re.sub(websites,"<prd>\\1",text)
	if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
	text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
	text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
	text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
	text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
	text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
	text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
	text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
	if "”" in text: text = text.replace(".”","”.")
	if "\"" in text: text = text.replace(".\"","\".")
	if "!" in text: text = text.replace("!\"","\"!")
	if "?" in text: text = text.replace("?\"","\"?")
	text = text.replace(".",".<stop>")
	text = text.replace("?","?<stop>")
	text = text.replace("!","!<stop>")
	text = text.replace("<prd>",".")
	sentences = text.split("<stop>")
	sentences = sentences[:-1]
	sentences = [s.strip() for s in sentences]
	return sentences

def neuralcorefIt(text):
	print('before coref: ' + text)

	sentences = split_into_sentences(text)

	sentences[0] = sentences[0].capitalize()
	 for s in sentences:
	 	if s[-1] == '?':
	 		sentences.remove(s)
	
	 	newText =  ' '.join(sentences)

	#print('after split into sent ' + newText)
	doc = nlp(text)

	#print(doc._.coref_clusters)

	return doc._.coref_resolved


def getPresentTense(triples):
	lmtzr = WordNetLemmatizer()
	for t in range(0, len(triples)):
		for i in range(0,len(triples[t])):
			for word in triples[t][i].split(" "):
				triples[t][i] = triples[t][i].replace(word, lmtzr.lemmatize(word,'v'))
	return triples

def getTriples(text):

	triples = []

	for sentence in ann.sentence:
		for triple in sentence.openieTriple:

			newTriple = []

			# subject_tokens = word_tokenize(triple.subject)
			# remove_stop = [word for word in subject_tokens if not word in stop_words]
			# new_subject = ' '.join(remove_stop)
			#
			# object_tokens = word_tokenize(triple.object)
			# remove_stop = [word for word in object_tokens if not word in stop_words]
			# new_object = ' '.join(remove_stop)

			newTriple.append(triple.subject)
			newTriple.append(triple.relation)
			newTriple.append(triple.object)

			triples.append(newTriple)

	return triples

articles_with_triples = []

csv_triples = []

with CoreNLPClient(
		annotators='tokenize, ssplit, pos, lemma, depparse, natlog, openie, dcoref', output_format='json',
		 timeout=600000) as client:
	for article in articles:
		triples = []
		processedText = neuralcorefIt(article)

		#print('after coref: ' + processedText)
		output = client.annotate(processedText)

		result2 = []

		for item in output:
			print(item)

		result = [output["sentences"][0]["openie"] for item in output]
		for i in range(0,len(output["sentences"])):
			result2.append(output['sentences'][i]['openie'])

		for i in range(0,len(result2)):
			for rel in result2[i]:
				subj = rel['subject']
				obj = rel['object']
				for ref in output['corefs']:
					if len(output['corefs'][ref]) > 1 and output['corefs'][ref][1]['position'][0] == i + 1:
						if output['corefs'][ref][1]['text'] == subj:
							subj = output['corefs'][ref][0]['text']


				# subj_pos = processedText.find(subj)
				# obj_pos = processedText.find(obj)
				# opennre = model.infer({'text': processedText, 'h': {'pos': (subj_pos, subj_pos + len(subj))}, 't': {'pos': (obj_pos, obj_pos + len(obj))}})

				relationSent=[subj,rel['relation'], obj]
				triples.append(relationSent)
		triples = getPresentTense(triples)

		csv_triples.append(triples)

		json_with_triples = {
			"article": article,
			"triples": triples,
			"label": "false"
		}

		articles_with_triples.append(json_with_triples)

df = pd.DataFrame(articles_with_triples)

df.to_json("dataframe_test_fake_triples.json")

df = pd.DataFrame(csv_triples)

df.to_csv('fake_triples_only.csv', index = False)

with open('json_test_fake_triples.json', 'w') as json_file:
	json.dump(articles_with_triples, json_file)


print("----- Triple extraction done... -------")