import openai 
import os 
import argparse
import csv
import time
import config
import pandas as pd
from tqdm import tqdm

os.environ['OPENAI_KEY'] = config.api_key
openai.api_key = os.getenv('OPENAI_KEY')

parser = argparse.ArgumentParser(description='Get phonetic transcription from gpt in IPA')

parser.add_argument('--gpt_version', choices=['text-davinci-003', 'gpt-3.5-turbo', 'gpt-4'], default='gpt-3.5-turbo')
parser.add_argument('--language', choices = ['english', 'hindi'], default = 'english')
parser.add_argument('--output', type = str, default = None)

args = parser.parse_args()

def get_input(language):
    if language == 'english':
        with open("most_frequent_words.txt", 'r') as file:
            titles = file.readlines()
    return titles

def main():
  
  freq_words = get_input(args.language)
  
  for i in tqdm(range(len(freq_words))):
    loop_time = time.time()
    prompt = f'Give the phonetic transcription of \'{freq_words[i]}\' in IPA'
    #print(prompt)


    try:
        completion = openai.ChatCompletion.create(
                    model=args.gpt_version, 
                    messages = [
                    {"role": "user", "content" : prompt}])
        
        poem = completion['choices'][0]['message']['content']
                
        with open(args.output, 'a') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow([prompt, poem])
    except:
        print('Sleeping...')
        time.sleep(40)
        
    if i % 50 == 0 and i != 0:
        print("Sleeping...")
        time.sleep(40)


if __name__ == '__main__':
    main()
