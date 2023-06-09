import requests
import json
import pandas as pd 
import config
import csv
import time
from tqdm import tqdm

app_id = config.oxford_app_id
app_key = config.oxford_app_key

language = 'en-us'
fields = 'pronunciations'
strictMatch = 'false'

df = pd.read_csv('freq_words_output_chatgpt.csv', header=None)

for i in tqdm(range( len(df))):
    loop_time = time.time()
    
    try :
        word_id = df[0][i]
        url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + '/' + word_id.lower() + '?fields=' + fields + '&strictMatch=' + strictMatch;
        url2 = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + 'en-gb' + '/' + word_id.lower() + '?fields=' + fields + '&strictMatch=' + strictMatch;
        
        r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
        r2 = requests.get(url2, headers = {'app_id': app_id, 'app_key': app_key})
        
        print(r)
        text = json.loads(r.text)
        text2 = json.loads(r2.text)
        #print(text)
        ans = []
        
        ipa = text['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations']
        ipa2 = text2['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations']
        print(ipa)
        print(ipa2)
        
        
        for j in range(len(ipa)):
            if ipa[j]['phoneticNotation'] == 'IPA':
                ans.append(ipa[j]['phoneticSpelling'])
                
        for k in range(len(ipa2)):
            if ipa2[k]['phoneticNotation'] == 'IPA':
                ans.append(ipa2[k]['phoneticSpelling'])
                
    
        ans = list(set(ans))
        print(ans)
        time.sleep(5)
    
        with open('ground_truth_most_freq.csv', 'a') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow([word_id, ans])
    except:
        ans = 'Not Found'
        with open('ground_truth_most_freq.csv', 'a') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow([word_id, ans])
    print(i)
    if i%15 == 0 and i!=0:
        print('Sleeping')
        time.sleep(30)
