from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def getListOfEnteties():
    data = pd.read_csv (r'ISOT_sum_ner_3.csv')
    df = pd.DataFrame(data, columns= ["0", "2"])

    print(df)

    enteties = []

    for index, row in df.iterrows():
        enteties.append(row['0'])
        enteties.append(row['2'])

    return enteties

counts = Counter(getListOfEnteties()).most_common(15)

labels = []
values = []

for x in counts:
    labels.append(x[0])
    values.append(x[1])

# sort your values in descending order
#indSort = np.argsort(values)[::-1]

# rearrange your data
#labels = np.array(labels)[indSort]
#values = np.array(values)[indSort]

#indexes = np.arange(len(labels))

plt.barh(labels,values)

# add labels
#plt.xticks(indexes + bar_width, labels)
plt.show()
