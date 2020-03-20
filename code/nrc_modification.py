import pandas as pd

#This is for some modification of the NRC dictionary

df = pd.read_csv('nrc.txt', sep='\t', header=None, keep_default_na=False, na_values=[''])

list = ['anticipation', 'fear', 'anger', 'trust', 'surprise', 'sadness', 'joy', 'disgust']

for i in range(df.shape[0]):
    if df.iloc[i,1].startswith("#"):
        continue
    else:
        df.iloc[i,1]="#"+df.iloc[i,1]

for i in range(df.shape[0]):
    if df.iloc[i,0] == list[0]:
        df.iloc[i,0]='excitement'
    elif df.iloc[i,0] == list[3]:
        df.iloc[i,0] = 'pleasant'
    elif df.iloc[i,0] == list[5]:
        df.iloc[i,0] = 'surprise'
    elif df.iloc[i,0] == list[6]:
        df.iloc[i,0] = 'happy'
    elif df.iloc[i,0] == list[7]:
        df.iloc[i, 0] = 'fear'
    elif df.iloc[i,0] == list[2]:
        df.iloc[i, 0] = 'angry'

df.to_csv('final_nrc.csv',sep='\t',index=None, header=None)





