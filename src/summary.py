import pandas as pd

data = pd.read_csv (r'Filtered_dataset/Filtered_dataset/ISOT-fake.csv')
#use Title, Article for true. title, text for fake
df = pd.DataFrame(data, columns= ["title", "text"])

def makeDefaultSummary(title, text):
	if len(text.split('. ')) >= 2:
		summary = title + '. ' + '. '.join(text.split('. ')[0:2]) + '.'
	else:
		summary = title + '. ' + text
	return summary

summaries = []

for index, row in df.iterrows():
    summaries.append((makeDefaultSummary(row['title'], row['text'])))

new_df = {'Text': summaries}

final_df = pd.DataFrame(new_df)

print('DataFrame:\n', final_df)

final_df.to_csv('fake_summarized_all.csv', index = False)
