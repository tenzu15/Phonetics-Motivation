import csv 
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time

df = pd.read_csv('rare_words.txt', header=None)

for i in tqdm(range(len(df))):
    try :
        loop = time.time()
        word = df[0][i]
        header = {'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25'}
        url = "https://www.wordhippo.com/what-is/words-that-rhyme-with/" + word + ".html"
        page = requests.get(url, headers=header)
        soup = BeautifulSoup(page.content, 'html.parser')
        rhymes = [a.getText() for a in soup.select_one('div.relatedwords').find_all("a")]
        
        with open('gt_rhyme_rare.csv', 'a') as f:
                csvwriter = csv.writer(f)
                csvwriter.writerow([word, rhymes])
    except:
        pass
            
    if i%30 == 0 and i!=0:
        time.sleep(30)

