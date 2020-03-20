import pandas as pd

processed_files =['processed_data/excitement.csv', 'processed_data/happy.csv', 'processed_data/pleasant.csv', 'processed_data/surprise.csv', 'processed_data/fear.csv', 'processed_data/angry.csv']


sample=pd.DataFrame(columns= ['Tweet_ID', 'Created_At', 'Tweet_Text'])

for processed_file in processed_files:
    df=pd.read_csv(processed_file, sep='\t',index_col =0)

    sample_df=df.sample(n=20,axis=0)
    sample=sample.append(sample_df,ignore_index=True)
print(sample)
sample.to_csv('sample.csv', index=False)