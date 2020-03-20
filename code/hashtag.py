import re
from pymongo import MongoClient
import pandas as pd

#This is for computing the NRC score of each class's tweets for classification strategy, exporting them as 6 files
emotions = ['excitement_collection', 'happy_collection', 'pleasant_collection', 'surprise_collection', 'fear_collection', 'angry_collection']
files= ['exc_nrc_score.csv', 'happ_nrc_score.csv', 'ple_nrc_score.csv', 'sur_nrc_score.csv', 'fear_nrc_score.csv', 'ang_nrc_score.csv']
df = pd.read_csv('final_nrc.csv', sep='\t', header=None, keep_default_na=False, na_values=[''])
for emotion, file in zip(emotions,files):
    client = MongoClient('localhost', 27017)
    db = client['twitter_db1']
    collection = db[emotion]
    tweets_iterator = collection.find()

    score=pd.DataFrame(columns=['excitement','happy','pleasant','surprise','fear','angry'])

    for tweet in tweets_iterator:
        list = [ ]
        excitement=0
        happy=0
        pleasant=0
        surprise=0
        fear=0
        angry=0
        for i in re.split("[ ,\n]",tweet['full_text']):
            if i.startswith("#"):
                list.append(i)

    #If the tweet has the same hashtag word in the specific NRC class
        # we add the corresponding NRC score for each tweet's variable for potential class
        for x in list:
            for y in range(df.shape[0]):
                if x.lower()==df.iloc[y,1]:
                    if df.iloc[y,0]== 'excitement':
                        excitement +=float(df.iloc[y,2])
                    elif df.iloc[y,0]== 'happy':
                        happy += float(df.iloc[y, 2])
                    elif df.iloc[y,0]== 'pleasant':
                        pleasant += float(df.iloc[y, 2])
                    elif df.iloc[y,0]== 'surprise':
                        surprise += float(df.iloc[y, 2])
                    elif df.iloc[y,0]== 'fear':
                        fear += float(df.iloc[y, 2])
                    elif df.iloc[y,0]== 'angry':
                        angry += float(df.iloc[y, 2])
        score = score.append(pd.DataFrame({'excitement': [excitement], 'happy': [happy], 'pleasant': [pleasant], 'surprise': [surprise], 'fear': [fear], 'angry': [angry]}),ignore_index=True)
    # print(score)

    score.to_csv(file, sep='\t')
    print('one successful!')
#     print(list)
#     print('\n')


