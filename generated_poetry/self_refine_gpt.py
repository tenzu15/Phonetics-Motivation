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

parser = argparse.ArgumentParser(description='Generate poems using chatgpt')

parser.add_argument('--gpt_version', choices=['text-davinci-003', 'gpt-3.5-turbo', 'gpt-4'], default='gpt-3.5-turbo')
parser.add_argument('--language', choices = ['english', 'hindi'], default = 'english')
parser.add_argument('--output', type = str, default = None)

args = parser.parse_args()

def get_prompt(prompt, poem):
    prefix_1 = f'You are a helpful AI assistant with extensive knowledge of literature and creative writing. Poetry also called verse is a form of literature that uses aesthetic and often rhythmic qualities of language − such as phonaesthetics, sound symbolism, and metre − to evoke meanings in addition to, or in place of, a prosaic ostensible meaning. A poem is a literary composition, written by a poet, using this principle.\n'
    prefix_2 = f'In this case, you will be provided with a poem and you must refine it to satisfy the given instruction\n' 
   
    
    prompt = f'{prefix_1}\n{prefix_2}\n{prompt}\n\n{poem}'

    return prompt

def main():
  
  poems = pd.read_csv('english_poems_05_10_refined.csv',header=None)
  print(f'read {len(poems)} into file ....')
  
  
  for i in tqdm(range(len(poems))):
    loop_time = time.time()
    instruction = poems[0][i].split('\n')[4] + poems[0][i].split('\n')[5]
    prompt = get_prompt(instruction,poems[1][i])
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