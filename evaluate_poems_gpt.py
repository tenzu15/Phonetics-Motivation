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
parser.add_argument('--output', type = str, default = None)

args = parser.parse_args()

def get_prompt(poem):
    prefix_1 = f'You are a helpful AI assistant with extensive knowledge of literature and creative writing. Poetry also called verse is a form of literature that uses aesthetic and often rhythmic qualities of language − such as phonaesthetics, sound symbolism, and metre − to evoke meanings in addition to, or in place of, a prosaic ostensible meaning. A poem is a literary composition, written by a poet, using this principle.\n'
    prefix_2 = f'In this case, you will be provided with a poem, and you must evaluate the quality of the poem across the following metrics. Even if you have seen this poem before, you must evaluate it impartially on the given metrics only. Please rate each metric out of 10.\n' 
    metric_1 = f'Fluency : whether the poem is well-organized, with the sentences smoothly connected and flowing together logically and aesthetically \n'
    metric_2 = f'Creativity : the use of original ideas and concepts in the poem with various figures of speech \n'
    metric_3 = f'Grammaticality : the correct usage of grammar in the language of the poem \n'
    metric_4 = f'Rhythm : the quality of the rhythm of the poem \n'
    metric_5 = f'Emotion Evocation : the poem evokes emotions in the reader by clever use of creative devices like imagery, metaphor etc.'
    
    prompt = f'{prefix_1}\n{prefix_2}\n{metric_1}{metric_2}{metric_3}{metric_4}{metric_5}\nThe poems starts below:\n\n{poem}'

    return prompt

def main():
  
  poems = pd.read_csv('english_poems_05_10.csv',header=None)
  print(f'read {len(poems)} into file ....')
  #rhyme_schemes = ['ABBA', 'ABCB', 'AAAA', 'ABAB', 'AABB']
  
  for i in tqdm(range(len(poems[269:]))):
    loop_time = time.time()
    prompt = get_prompt(poems[1][i])
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