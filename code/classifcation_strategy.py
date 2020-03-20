import csv
import pandas as pd
from pymongo import MongoClient

#We use the NRC classification strategy to regroup the tweet in 6 classes.

emotions1 = ['excitement_collection', 'happy_collection', 'pleasant_collection', 'surprise_collection', 'fear_collection', 'angry_collection']
emotions2 = ['excitement', 'happy', 'pleasant', 'surprise', 'fear', 'angry']
files= ['exc_nrc_score.csv', 'happ_nrc_score.csv', 'ple_nrc_score.csv', 'sur_nrc_score.csv', 'fear_nrc_score.csv', 'ang_nrc_score.csv']
for emotion1, emotion2, file in zip(emotions1, emotions2, files):
    client = MongoClient('localhost', 27017)

    db1 = client['twitter_db1']
    collection1 = db1[emotion1]
    db2 = client['twitter_db2']
    collection2 = db2[emotion2]

    df = pd.read_csv(file, sep='\t',index_col =0)
    tweets_iterator = collection1.find()

#We use the class with the highest score as the tweet's class
    #And then we create a new database for storing the cleaned data

    for i, tweet in zip(range(df.shape[0]), tweets_iterator):

        count=0
        x=df.iloc[i,:]
        x_argmax=x[x==x.max()].index
        for k in x_argmax:
            count+=1
        if count==1:
            if x_argmax[0]!=emotion2:
                collection2_switch = db2[x_argmax[0]]
                collection2_switch.insert(tweet)
            else:
                collection2.insert(tweet)
        else:
            collection2.insert(tweet)


#We export the cleaned data into CSV files for pre-processing

files =['data/excitement.csv', 'data/happy.csv', 'data/pleasant.csv', 'data/surprise.csv', 'data/fear.csv', 'data/angry.csv']

for emotion, file in zip(emotions2, files):
    client = MongoClient('localhost', 27017)
    db = client['twitter_db2']
    collection1 = db[emotion]

    tweets_iterator = collection1.find()

    for tweet in tweets_iterator:
        with open(file,'a', encoding='utf-8') as f:
            tsv_w = csv.writer(f, delimiter='\t')
            tsv_w.writerow([tweet['id'], tweet['created_at'], tweet['full_text']])





