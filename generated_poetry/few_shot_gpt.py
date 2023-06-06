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

def get_input(language):
    if language == 'english':
        with open("poem_titles.txt", 'r') as file:
            titles = file.readlines()
    return titles


def get_prompt(title, language, rhyme):
    title = title.replace('\n', '')
    prefix_1 = f'You are a helpful AI assistant with extensive knowledge of literature and creative writing. Poetry also called verse is a form of literature that uses aesthetic and often rhythmic qualities of language − such as phonaesthetics, sound symbolism, and metre − to evoke meanings in addition to, or in place of, a prosaic ostensible meaning. A poem is a literary composition, written by a poet, using this principle.\n'
    prefix_2 = f'A rhyme scheme is the pattern of sounds that repeats at the end of a line or stanza. Rhyme schemes can change line by line, stanza by stanza, or can continue throughout a poem. Poems with rhyme schemes are generally written in formal verse, which has a strict meter: a repeating pattern of stressed and unstressed syllables.\n'
    prefix_3 = f'Rhyme scheme patterns are formatted in different ways. The patterns are encoded by letters of the alphabet. Lines designated with the same letter rhyme with each other. For example, the rhyme scheme ABAB means the first and third lines of a stanza, or the “A”s, rhyme with each other, and the second line rhymes with the fourth line, or the “B”s rhyme together.\n'
    eg_1 = f'Example of rhyme scheme ABCB:\nThe night has been long, (A) \nThe wound has been deep, (B)\nThe pit has been dark, (C)\nAnd the walls have been steep (B)\nIn this example, \'scheme\'  and \'dark\' do not rhyme while \'deep\' and \'steep\' rhyme'
    eg_2 = f'Example of rhyme scheme ABBA: \nWhen primroses are out in Spring, (A)\nAnd small blue violets come between; (B)\nWhen merry birds sing on boughs green, (B)\nAnd rills, as soon as born, must sing. (A)\nIn this example, \'Spring\' rhymes with \'sing\' and \'between\' rhymes with \'green\''
    eg_3 =f'Example of rhyme scheme ABAB:\nBid me to weep, and I will weep (A)\nWhile I have eyes to see; (B)\nAnd having none, yet I will keep (A)\nA heart to weep for thee. (B)\nIn this example, \'weep\' rhymes with \'keep\' and \'see\' rhymes with \'thee\''
    prompt = f'{prefix_1}\n{prefix_2}\n{prefix_3}\n\n{eg_1}\n\n{eg_2}\n\n{eg_3}\n \nNow, write a short poem on {title} using rhyme scheme {rhyme}'

    return prompt

def main():
  
  poem_titles = get_input(args.language)
  rhyme_schemes = ['ABBA', 'ABCB', 'AAAA', 'ABAB', 'AABB']
  
  
  for i in tqdm(range(len(poem_titles))):
    for rhyme in rhyme_schemes:
      loop_time = time.time()
      prompt = get_prompt(poem_titles[i], args.language, rhyme)
      print(prompt)
    

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